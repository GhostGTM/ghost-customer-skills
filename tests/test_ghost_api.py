"""Credential, identity, request-data, redirect, and retry regression checks."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import threading
import unittest
from unittest.mock import patch
import urllib.error
import http.server

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ghost_api", ROOT / "plugins/ghost/scripts/ghost_api.py")
api_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(api_module)
KEY = "ghost_" + "1a" * 32
IDENTITY = {"workspaceId": "workspace-a", "userId": "user-a", "scopes": ["graph:read"]}


class Response(io.BytesIO):
    def __init__(self, value):
        super().__init__(json.dumps(value).encode())


class HelperTests(unittest.TestCase):
    def test_unsupported_python_fails_before_credentials_or_network(self):
        with patch.object(api_module.sys, "version_info", (3, 10, 20)), patch.object(api_module.os.environ, "get") as env_get, patch.object(api_module.urllib.request, "build_opener") as opener:
            with self.assertRaises(api_module.ApiError) as error:
                api_module.GhostApi()
            self.assertEqual(error.exception.detail["code"], "UNSUPPORTED_PYTHON")
            env_get.assert_not_called()
            opener.assert_not_called()

    def test_ambiguous_or_non_json_input_is_rejected(self):
        for raw in (b'{"path":"/query","path":"/operations"}', b'{"value":NaN}', b'{"value":Infinity}', b'\xff'):
            with self.subTest(raw=raw), self.assertRaises((ValueError, UnicodeError)):
                api_module.parse_json(raw)

    def setUp(self):
        self.env = patch.dict(os.environ, {"GHOST_API_KEY": KEY})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.api = api_module.GhostApi()

    def test_complete_record_and_source_reads_use_fixed_origin(self):
        record_id = "11111111-1111-4111-8111-111111111111"
        for path in ("/data/accounts/" + record_id, "/data/people/" + record_id, "/data/firmographics?accountId=" + record_id, "/sources/" + record_id + "/content?offset=7", "/labels/" + record_id + "/assignments"):
            with patch.object(self.api.opener, "open", return_value=Response({})) as send:
                self.api.send("GET", path)
                self.assertEqual(send.call_args.args[0].full_url, api_module.ORIGIN + api_module.PREFIX + path)

    def test_validation_errors_preserve_actionable_paths_but_not_secrets_or_arbitrary_bodies(self):
        other_key = "ghost_" + "ab" * 32
        body = {"message": "Input validation failed", "data": {"issues": [{"path": ["arguments", "fields", 0, "op"], "message": "Invalid option: expected select or eq"}, {"path": ["arguments"], "message": KEY + " " + other_key}], "input": {"secret": "must not echo"}}}
        error = urllib.error.HTTPError(api_module.ORIGIN, 400, "bad request", {}, Response(body))
        with patch.object(self.api.opener, "open", side_effect=error) as send:
            with self.assertRaises(api_module.ApiError) as caught:
                self.api.send("POST", "/query", {"operation": "graph.query_connected_api"})
        detail = caught.exception.detail
        self.assertIn("arguments.fields.0.op", detail["validation"])
        serialized = json.dumps(detail)
        for secret in (KEY, other_key, "must not echo"):
            self.assertNotIn(secret, serialized)
        self.assertEqual(send.call_count, 1)
        self.assertTrue(error.fp.closed)
        self.assertIsNone(self.api.validation_detail({"message": "SQL failed", "data": {"fieldErrors": {"sql": ["private"]}}}))

    def test_validation_details_are_bounded_and_cover_root_schema_errors(self):
        detail = self.api.validation_detail({"message": "Invalid operation arguments", "data": {"formErrors": ["Unrecognized key: workspaceId"], "fieldErrors": {"fields": ["x" * 1000] * 10}}})
        self.assertEqual(detail["request"], ["Unrecognized key: workspaceId"])
        self.assertEqual(len(detail["fields"]), 3)
        self.assertEqual(len(detail["fields"][0]), 300)


    def test_missing_or_header_injecting_key_fails_without_network(self):
        for key in ("", "ordinary-value", KEY + "\r\nX-Injected: yes"):
            with patch.dict(os.environ, {"GHOST_API_KEY": key}), self.assertRaises(api_module.ApiError):
                api_module.GhostApi()

    def test_wrong_workspace_or_user_never_reads_or_mutates_target(self):
        for expected in (("workspace-b", "user-a"), ("workspace-a", "user-b")):
            with patch.object(self.api.opener, "open", return_value=Response(IDENTITY)) as send:
                with self.assertRaises(api_module.ApiError) as error:
                    self.api.request({"method": "POST", "path": "/operations", "body": {}}, *expected)
                self.assertEqual(error.exception.detail["code"], "IDENTITY_MISMATCH")
                self.assertEqual(send.call_count, 1)
                self.assertEqual(send.call_args.args[0].full_url, api_module.ORIGIN + "/api/v1/me")

    def test_identity_is_checked_again_for_each_request(self):
        with patch.object(self.api.opener, "open", side_effect=[Response(IDENTITY), Response({"result": []}), Response({**IDENTITY, "workspaceId": "workspace-b"})]) as send:
            spec = {"method": "POST", "path": "/query", "body": {"operation": "graph.filter_accounts", "arguments": {}}}
            self.api.request(spec, "workspace-a", "user-a")
            with self.assertRaises(api_module.ApiError):
                self.api.request(spec, "workspace-a", "user-a")
            self.assertEqual(send.call_count, 3)

    def test_apostrophes_newlines_and_shell_syntax_remain_data(self):
        material = "Acme's notes\n$(touch /tmp/NEVER_EXECUTE) `echo not-a-command` ; ' \" \\"
        body = {"operation": "context.apply_entity", "arguments": {"overview": material}, "reason": "Yes, save Acme's notes"}
        spec = {"method": "POST", "path": "/operations", "body": body, "idempotencyKey": "12345678-1234-4123-8123-123456789abc"}
        with patch.object(self.api.opener, "open", side_effect=[Response(IDENTITY), Response({"id": "receipt"})]) as send:
            self.api.request(spec, "workspace-a", "user-a")
            request = send.call_args.args[0]
            self.assertEqual(json.loads(request.data), body)
            self.assertEqual(request.get_header("Authorization"), "Bearer " + KEY)
            self.assertNotIn(KEY, request.full_url)
            self.assertNotIn(KEY.encode(), request.data)

    def test_rejects_origin_escape_and_unsupported_endpoints_before_network(self):
        paths = ["https://attacker.example/query", "//attacker.example/query", "/../query", "/%2e%2e/query", "/data/../accounts", "/query#fragment", "/query\n", "/data/accounts\\evil", "/oauth/token"]
        with patch.object(self.api.opener, "open") as send:
            for path in paths:
                with self.subTest(path=path), self.assertRaises(api_module.ApiError):
                    self.api.send("GET", path)
            send.assert_not_called()

    def test_cannot_put_credential_in_query_or_body(self):
        with patch.object(self.api.opener, "open") as send:
            for method, path, body in (("GET", "/data/accounts?key=" + KEY, None), ("POST", "/query", {"token": KEY})):
                with self.assertRaises(api_module.ApiError):
                    self.api.send(method, path, body)
            send.assert_not_called()

    def test_write_requires_valid_idempotency_key(self):
        for value in (None, "not-a-uuid", "header\r\ninjection"):
            with patch.object(self.api.opener, "open") as send, self.assertRaises(api_module.ApiError):
                self.api.send("POST", "/operations", {}, value)
            send.assert_not_called()

    def test_denials_and_network_errors_never_retry_or_echo_server_secrets(self):
        errors = [urllib.error.HTTPError("https://app.ghostgtm.ai/api/v1/query", status, KEY, {}, io.BytesIO(KEY.encode())) for status in (401, 403, 429, 500)]
        errors.append(urllib.error.URLError(KEY))
        for cause in errors:
            with patch.object(self.api.opener, "open", side_effect=cause) as send, self.assertRaises(api_module.ApiError) as result:
                self.api.send("POST", "/query", {})
            self.assertEqual(send.call_count, 1)
            self.assertNotIn(KEY, json.dumps(result.exception.detail))
            if isinstance(cause, urllib.error.HTTPError):
                self.assertTrue(cause.closed)

    def test_result_and_error_redaction(self):
        self.assertNotIn(KEY, self.api.redact({"result": {"unexpectedEcho": KEY}}))
        self.assertIn("[REDACTED]", self.api.redact({"result": KEY}))

    def test_bounded_input_and_output(self):
        with patch.object(api_module, "MAX_INPUT", 10), self.assertRaises(api_module.ApiError):
            self.api.send("POST", "/query", {"value": "too much input"})
        with patch.object(api_module, "MAX_RESPONSE", 10), patch.object(self.api.opener, "open", return_value=Response({"result": "too much output"})), self.assertRaises(api_module.ApiError):
            self.api.send("GET", "/capabilities")

    def test_real_http_redirect_never_reaches_destination(self):
        reached = []
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                reached.append(self.path)
                self.send_response(307)
                self.send_header("Location", "/stolen")
                self.end_headers()
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.object(api_module, "ORIGIN", "http://127.0.0.1:" + str(server.server_port)), self.assertRaises(api_module.ApiError) as error:
                self.api.send("GET", "/me")
            self.assertEqual(error.exception.detail["httpStatus"], 307)
            self.assertEqual(reached, ["/api/v1/me"])
        finally:
            server.shutdown()
            server.server_close()

    def test_cli_reads_request_from_stdin_without_key_argument_or_output(self):
        request = {"path": "/capabilities"}
        output = io.StringIO()
        fake_stdin = io.TextIOWrapper(io.BytesIO(json.dumps(request).encode()))
        argv = ["ghost_api.py", "request", "--workspace", "workspace-a", "--user", "user-a", "--input", "-"]
        with patch.object(api_module.sys, "argv", argv), patch.object(api_module.sys, "stdin", fake_stdin), patch.object(api_module.GhostApi, "send", side_effect=[IDENTITY, {"unexpectedEcho": KEY}]), contextlib.redirect_stdout(output):
            self.assertEqual(api_module.main(), 0)
        self.assertNotIn(KEY, " ".join(argv))
        self.assertNotIn(KEY, output.getvalue())


if __name__ == "__main__":
    unittest.main()
