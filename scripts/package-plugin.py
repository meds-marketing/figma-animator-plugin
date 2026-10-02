#!/usr/bin/env python3
"""Package desktop wiring or a verified ChatGPT registered-app binding."""

import argparse
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "plugins" / "figma-animator"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app-id", help="Current, verified asdk_app_... ID for ChatGPT web; URL plugin_ prefix also accepted")
    parser.add_argument("--org-auth", action="store_true", help="Skills, bridge and configuration examples for a managed organization connection; no OAuth dependency")
    args = parser.parse_args()
    if args.org_auth and args.app_id:
        parser.error("Organization connection examples cannot change a registered ChatGPT app's authentication")
    if args.app_id:
        args.app_id = args.app_id.removeprefix("plugin_")
    if args.app_id and not re.fullmatch(r"asdk_app_[a-f0-9]{32}", args.app_id):
        parser.error("Use the registered app's technical ID, not a plugin package ID or URL.")

    # Only package declared source files; never include hidden OS metadata or credentials.
    paths = ["plugin.json", ".codex-plugin/plugin.json", "README.md", "ORG-AUTH.md",
             "assets/icon.svg", "assets/icon.png", "skills/animate-frame/SKILL.md"]
    if not args.app_id:
        paths += [".claude-plugin/plugin.json", "bridge/mcp-stdio.cjs",
                  "examples/org-auth/codex.toml", "examples/org-auth/claude.mcp.json", "examples/org-auth/stdio.mcp.json"]
        if not args.org_auth:
            paths += ["mcp.json", ".mcp.json"]
    contents = {path: (SOURCE / path).read_bytes() for path in paths}
    manifest = json.loads(contents["plugin.json"])
    interface = manifest["extensions"]["com.openai"]["interface"]
    for name in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        overlay = json.loads((SOURCE / name).read_text())
        for field in ("name", "version", "description", "repository"):
            if overlay.get(field) != manifest.get(field):
                parser.error(f"{name}: {field} must match plugin.json")
        if "interface" in overlay and overlay["interface"] != interface:
            parser.error(f"{name}: interface must match plugin.json")
    for field in ("logo", "composerIcon"):
        asset = interface[field].removeprefix("./")
        if asset not in contents:
            parser.error(f"{field}: asset must be in the package allowlist")
    if len(interface["shortDescription"]) > 30:
        parser.error("shortDescription must be at most 30 characters")
    if args.org_auth:
        overlay = json.loads(contents[".codex-plugin/plugin.json"])
        overlay.pop("mcpServers", None)
        contents[".codex-plugin/plugin.json"] = encode_json(overlay)
        contents["README.md"] = (
            "# Figma Animator — organization connection package\n\n"
            "Install this workflow skill alongside your administrator-managed MCP connection. "
            "This archive contains no OAuth dependency or usable key. Configure the shared "
            "connection using the client examples before using the skill. Local-server clients "
            "can launch bridge/mcp-stdio.cjs with a privately provisioned organization key.\n\n"
            "See ORG-AUTH.md for endpoint, identity, rotation and client availability details. "
            "Installing this package alone does not provision a server connection.\n"
        ).encode()
    if args.app_id:
        manifest = json.loads(contents["plugin.json"])
        manifest["extensions"]["com.openai"]["apps"] = "./.app.json"
        overlay = json.loads(contents[".codex-plugin/plugin.json"])
        overlay.pop("mcpServers", None)
        overlay["apps"] = "./.app.json"
        contents["plugin.json"] = encode_json(manifest)
        contents[".codex-plugin/plugin.json"] = encode_json(overlay)
        contents[".app.json"] = encode_json({"apps": {"figma-animator": {
            "id": args.app_id, "required": True}}})
        contents["README.md"] = (
            "# Figma Animator — ChatGPT web package\n\n"
            "This package includes the animate-frame skill and a required registered-app "
            f"binding to `{args.app_id}`. It contains no bundled MCP server declarations.\n\n"
            "Import into the account/workspace that can access that registered Figma Animator app. "
            "The mapping does not create an app or grant access. Use an administrator-provided "
            "workspace connection where the intended surface supports it; otherwise sign in "
            "through the existing Google OAuth flow. This ZIP cannot change authentication. "
            "See ORG-AUTH.md for availability and shared-credential setup. Previews and approval "
            "stay in the single inline animation workspace.\n\n"
            "For Codex or Claude Code direct MCP wiring, use figma-animator-desktop.zip. "
            "Client approval policies still apply; the skill cannot bypass them.\n"
        ).encode()

    name = "figma-animator.zip" if args.app_id else "figma-animator-org.zip" if args.org_auth else "figma-animator-desktop.zip"
    target = ROOT / "dist" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".zip.tmp")
    with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, data in sorted(contents.items()):
            archive.writestr(path, data)
    temporary.replace(target)
    print(f"Created {target} ({len(contents)} files)")


def encode_json(value):
    return (json.dumps(value, indent=2) + "\n").encode()


if __name__ == "__main__":
    main()
