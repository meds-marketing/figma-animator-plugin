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
    args = parser.parse_args()
    if args.app_id:
        args.app_id = args.app_id.removeprefix("plugin_")
    if args.app_id and not re.fullmatch(r"asdk_app_[a-f0-9]{32}", args.app_id):
        parser.error("Use the registered app's technical ID, not a plugin package ID or URL.")

    # Only package declared source files; never include hidden OS metadata or credentials.
    paths = ["plugin.json", ".codex-plugin/plugin.json", "README.md",
             "assets/icon.svg", "assets/icon.png", "skills/animate-frame/SKILL.md"]
    if not args.app_id:
        paths += ["mcp.json", ".mcp.json", ".claude-plugin/plugin.json"]
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
            "The mapping does not create an app or grant access. Sign in through its Google OAuth "
            "flow. Previews and approval stay in the single inline animation workspace.\n\n"
            "For Codex or Claude Code direct MCP wiring, use figma-animator-desktop.zip. "
            "Client approval policies still apply; the skill cannot bypass them.\n"
        ).encode()

    name = "figma-animator.zip" if args.app_id else "figma-animator-desktop.zip"
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
