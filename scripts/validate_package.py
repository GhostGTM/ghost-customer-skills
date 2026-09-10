#!/usr/bin/env python3
"""Validate the distributable package without accessing credentials or services."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "ghost"


def require(condition, message):
    if not condition:
        raise SystemExit(message)


manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
require(manifest["name"] == "ghost", "Plugin name must be ghost")
require(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), "Use a release version")
require("Version " + manifest["version"] in (ROOT / "README.md").read_text(), "README version is stale")
marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
require(marketplace["name"] == "ghost-customer-skills", "Unexpected marketplace name")
require(len(marketplace["plugins"]) == 1, "Review additional plugin distribution explicitly")
require(marketplace["plugins"][0]["source"] == "./plugins/ghost", "Plugin must use a local source")
mcp = json.loads((PLUGIN / ".mcp.json").read_text())
require(mcp == {"mcpServers": {"ghost": {"type": "http", "url": "https://mcp.ghostgtm.ai/mcp"}}}, "Unexpected server, credentials, or executable in MCP configuration")

skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
require(len(skills) == 24, "Review the advertised skill inventory when changing it")
for skill in skills:
    content = skill.read_text()
    require(content.startswith("---\n"), f"Missing frontmatter: {skill.name}")
    require(f"\nname: {skill.parent.name}\n" in content, f"Skill name mismatch: {skill.parent.name}")
    require("\ndescription: " in content, f"Missing discovery description: {skill.parent.name}")
    require("${CLAUDE_PLUGIN_ROOT}/references/working-with-ghost.md" in content, f"Missing shared safety contract: {skill.parent.name}")

for path in PLUGIN.rglob("*"):
    require(not path.is_symlink(), "Symlinks must not escape the distributable package")
    if not path.is_file() or "__pycache__" in path.parts:
        continue
    rel = path.relative_to(PLUGIN).as_posix()
    require(path.suffix in (".md", ".json", ".py"), f"Unexpected runtime file: {rel}")
    require("hooks" not in path.parts, "Automatic hooks require explicit security review")
    if path.suffix == ".md":
        text = path.read_text()
        for ref in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([a-zA-Z0-9_./-]+)", text):
            target = (PLUGIN / ref).resolve()
            require(PLUGIN.resolve() in target.parents and target.exists(), f"Broken or external runtime reference: {ref}")
        require(not re.search(r"(?:Bearer\s+\$|curl[^\n]*GHOST_API_KEY)", text), f"Unsafe credential example: {rel}")
        require("/Users/" not in text and ".claude/worktrees" not in text, f"Private path in {rel}")

cases = re.findall(r"^### (\d+)\.", (ROOT / "evals/acceptance.md").read_text(), re.M)
require([int(case) for case in cases] == list(range(1, len(cases) + 1)), "Acceptance cases must be consecutive")
require(len(cases) >= 44, "Missing security acceptance cases")
print(f"Validated Ghost {manifest['version']}: {len(skills)} skills, {len(cases)} acceptance cases, fixed MCP origin, local runtime references.")
