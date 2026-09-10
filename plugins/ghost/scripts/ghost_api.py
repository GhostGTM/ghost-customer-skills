#!/usr/bin/env python3
"""Ghost API requests with credentials kept out of command-line arguments.

Python 3.11+, standard library only. No automatic retries or redirect following.
Input files contain request data, never credentials. Identity is checked before
each customer-data request; it is not proof of a human's approval to mutate.
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

ORIGIN = "https://app.ghostgtm.ai"
PREFIX = "/api/v1"
MAX_INPUT = 1_000_000
MAX_RESPONSE = 8_000_000
UUID = r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}"
READ_PATH = re.compile(
    r"/(?:me|capabilities|data/[a-z][a-z0-9_-]{0,63}(?:/" + UUID + r")?"
    r"|operations(?:/" + UUID + r")?|sources/" + UUID + r"/content|labels/" + UUID + r"/assignments)\Z"
)


class ApiError(Exception):
    def __init__(self, code, message, status=None, receipt_id=None):
        self.detail = {"code": code, "message": message}
        if status is not None:
            self.detail["httpStatus"] = status
        if receipt_id:
            self.detail["idempotencyKey"] = receipt_id
        super().__init__(message)


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def parse_json(raw):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError("Non-finite JSON number")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)


class GhostApi:
    def __init__(self):
        if sys.version_info < (3, 11):
            raise ApiError("UNSUPPORTED_PYTHON", "Use Python 3.11 or newer with current security patches.")
        self.key = os.environ.get("GHOST_API_KEY", "")
        if not re.fullmatch(r"ghost_[A-Za-z0-9_-]{16,256}", self.key):
            raise ApiError("KEY_MISSING_OR_INVALID", "Set GHOST_API_KEY in the launching environment; do not paste it into chat or arguments.")
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPSHandler(context=ssl.create_default_context()),
            NoRedirects(),
        )

    def redact(self, value):
        text = json.dumps(value, ensure_ascii=False)
        return text.replace(self.key, "[REDACTED]")

    def send(self, method, path, body=None, idempotency_key=None):
        # All callers, including the identity preflight, use this same policy.
        if not isinstance(path, str) or not path.startswith("/"):
            raise ApiError("INVALID_PATH", "Use an allowed path relative to /api/v1.")
        parsed = urllib.parse.urlsplit(path)
        if parsed.scheme or parsed.netloc or parsed.fragment or "\\" in path or any(ord(c) < 32 for c in path):
            raise ApiError("INVALID_PATH", "Absolute URLs, fragments, and redirects are not supported.")
        if self.key in urllib.parse.unquote(path) or self.key in (json.dumps(body) if body is not None else ""):
            raise ApiError("KEY_IN_PAYLOAD", "Credentials must not appear in URLs or request data.")
        if method == "GET":
            allowed = READ_PATH.fullmatch(parsed.path) and body is None
        else:
            allowed = method == "POST" and path in ("/query", "/operations") and isinstance(body, dict)
        if not allowed:
            raise ApiError("INVALID_REQUEST", "Only catalog/data/receipt reads, POST /query, and POST /operations are supported.")
        if idempotency_key is not None and not re.fullmatch(UUID, idempotency_key):
            raise ApiError("INVALID_IDEMPOTENCY_KEY", "Use one UUID per intended operation and retain it for reconciliation.")
        if path == "/operations" and method == "POST" and not idempotency_key:
            raise ApiError("IDEMPOTENCY_KEY_REQUIRED", "A write requires its own idempotencyKey UUID in the request file.")
        headers = {"Accept": "application/json", "Authorization": "Bearer " + self.key}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        payload = None
        if body is not None:
            payload = json.dumps(body, ensure_ascii=False, allow_nan=False).encode("utf-8")
            if len(payload) > MAX_INPUT:
                raise ApiError("INPUT_TOO_LARGE", "Request data exceeds 1 MB; narrow the operation without silently truncating it.")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(ORIGIN + PREFIX + path, data=payload, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=45) as response:
                raw = response.read(MAX_RESPONSE + 1)
                if len(raw) > MAX_RESPONSE:
                    raise ApiError("RESPONSE_TOO_LARGE", "Response exceeds 8 MB; request a smaller page.")
                try:
                    return parse_json(raw)
                except (ValueError, UnicodeError, RecursionError):
                    raise ApiError("INVALID_RESPONSE", "Ghost returned a non-JSON response; no retry was made.") from None
        except urllib.error.HTTPError as error:
            validation = None
            if error.code == 400:
                try:
                    raw_error = error.read(16_001)
                    if len(raw_error) <= 16_000:
                        validation = self.validation_detail(parse_json(raw_error))
                except (OSError, ValueError, UnicodeError, RecursionError):
                    pass
            error.close()
            if 300 <= error.code < 400:
                message = "Redirect refused; credentials were not forwarded. Check the Ghost service connection."
            elif error.code in (401, 403):
                message = "Ghost denied access. Stop; do not switch credentials or transports to work around the denial."
            elif error.code == 429:
                message = "Rate limited. Wait and inspect existing receipts before any further operation."
            elif error.code >= 500:
                message = "Ghost did not confirm the outcome. Inspect operation receipts and the target before retrying; no retry was made."
            elif error.code == 400:
                message = "Check the operation's exact inputSchema at /capabilities. Use /query only for readOnly operations and /operations for writes or paid work; no retry was made."
            elif error.code == 404:
                message = "Use /capabilities to discover operations and /data/{resource} for collections (for example /data/icps); do not guess routes."
            else:
                message = "Ghost rejected the request. Inspect its catalog and target state; no retry was made."
            # Do not emit arbitrary server error bodies or exception reprs.
            safe_error = ApiError("HTTP_ERROR", message, error.code, idempotency_key)
            if validation:
                safe_error.detail["validation"] = validation
            raise safe_error from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise ApiError("TRANSPORT_ERROR", "Request outcome is unconfirmed. Inspect the operation receipts and target before retrying; no retry was made.", receipt_id=idempotency_key) from None

    def identity(self):
        result = self.send("GET", "/me")
        if not isinstance(result, dict) or not all(isinstance(result.get(k), str) and result[k] for k in ("workspaceId", "userId")):
            raise ApiError("INVALID_IDENTITY", "Ghost did not return a usable workspace and user identity.")
        return result

    def validation_detail(self, value):
        """Return bounded field diagnostics only from recognized validation errors."""
        if not isinstance(value, dict) or value.get("message") not in ("Input validation failed", "Invalid operation arguments"):
            return None
        data = value.get("data")
        if not isinstance(data, dict):
            return None
        def clean(text):
            return re.sub(r"ghost_[A-Za-z0-9_-]{16,256}", "[REDACTED]", text.replace(self.key, "[REDACTED]"))[:300]
        result = {}
        fields = data.get("fieldErrors")
        if isinstance(fields, dict):
            for name, messages in list(fields.items())[:20]:
                if isinstance(name, str) and not name.startswith("ghost_") and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]{0,119}", name) and isinstance(messages, list):
                    result[name] = [clean(message) for message in messages[:3] if isinstance(message, str)]
        issues = data.get("issues")
        if isinstance(issues, list):
            for issue in issues[:20]:
                if not isinstance(issue, dict) or not isinstance(issue.get("path"), list):
                    continue
                path = issue["path"]
                if not path or any(str(part).startswith("ghost_") for part in path) or any(not isinstance(part, (str, int)) or not re.fullmatch(r"[A-Za-z0-9_]{1,80}", str(part)) for part in path):
                    continue
                if isinstance(issue.get("message"), str):
                    result[".".join(map(str, path))[:120]] = [clean(issue["message"])]
        form_errors = data.get("formErrors")
        if isinstance(form_errors, list):
            result["request"] = [clean(message) for message in form_errors[:3] if isinstance(message, str)]
        return result or None

    def request(self, spec, workspace_id, user_id):
        if not workspace_id or not user_id:
            raise ApiError("IDENTITY_REQUIRED", "Resolve the intended workspace and user before accessing customer data.")
        if not isinstance(spec, dict) or set(spec) - {"method", "path", "body", "idempotencyKey"}:
            raise ApiError("INVALID_REQUEST", "Request file accepts only method, path, body, and idempotencyKey.")
        identity = self.identity()
        if identity["workspaceId"] != workspace_id or identity["userId"] != user_id:
            raise ApiError("IDENTITY_MISMATCH", "The API key does not match the intended workspace/user. No customer-data request was sent.")
        return self.send(spec.get("method", "GET"), spec.get("path"), spec.get("body"), spec.get("idempotencyKey"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("identity", help="Read only the key's workspace, user, and grants.")
    request_parser = sub.add_parser("request", help="Send one request after an identity check.")
    request_parser.add_argument("--workspace", required=True)
    request_parser.add_argument("--user", required=True)
    request_parser.add_argument("--input", required=True, help="UTF-8 JSON request file, or - for stdin. Never contains credentials.")
    args = parser.parse_args()
    api = None
    try:
        api = GhostApi()
        if args.command == "identity":
            result = api.identity()
        else:
            if args.input == "-":
                raw = sys.stdin.buffer.read(MAX_INPUT + 1)
            else:
                with open(args.input, "rb") as source:
                    raw = source.read(MAX_INPUT + 1)
            if len(raw) > MAX_INPUT:
                raise ApiError("INPUT_TOO_LARGE", "Request file exceeds 1 MB.")
            spec = parse_json(raw)
            result = api.request(spec, args.workspace, args.user)
        print(api.redact(result))
        return 0
    except ApiError as error:
        detail = {"error": error.detail}
    except (OSError, ValueError, TypeError, RecursionError):
        detail = {"error": {"code": "INVALID_INPUT", "message": "Could not read a valid UTF-8 JSON request; no automatic retry was made."}}
    print(api.redact(detail) if api else json.dumps(detail), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
