#!/usr/bin/env python3
"""Validate and package only the OpenAI source, excluding other host manifests."""

import argparse
import json
import re
import struct
import zipfile
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openai" / "posterly"


def validate(files):
    manifest = json.loads(files["plugin.json"])
    mcp = json.loads(files["mcp.json"])
    assert manifest["name"] == "posterly"
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert mcp["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
    assert set(mcp["mcpServers"]) == {"posterly"}
    assert mcp["mcpServers"]["posterly"] == {
        "type": "streamable-http", "url": "https://www.poster.ly/api/mcp"
    }
    extension = manifest["extensions"]["com.openai"]
    assert "apps" not in manifest and "apps" not in extension
    assert "hooks" not in manifest and "hooks" not in extension
    interface = extension["interface"]
    for field, limit in [("displayName", 30), ("shortDescription", 30),
                         ("longDescription", 4000), ("developerName", 80)]:
        assert isinstance(interface[field], str) and interface[field].strip()
        assert len(interface[field]) <= limit, field
    prompts = interface["defaultPrompt"]
    assert 1 <= len(prompts) <= 3
    assert len({" ".join(p.split()) for p in prompts}) == len(prompts)
    assert all(p.strip() and len(p) <= 128 and "\n" not in p for p in prompts)
    for field in ["websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"]:
        url = urlparse(interface[field])
        assert url.scheme == "https" and url.hostname == "www.poster.ly"
        assert not url.username and not url.password
    for field, minimum in [("logo", 256), ("composerIcon", 48)]:
        value = interface[field]
        assert value.startswith("./") and ".." not in Path(value).parts
        asset = files[value[2:]]
        assert asset[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", asset[16:24])
        assert minimum <= width <= 4096 and width == height
        assert len(asset) <= 5 * 1024 * 1024
    assert extension["onboardingSkill"][2:] in files
    skills = [name for name in files if name.endswith("/SKILL.md")]
    assert skills
    for name in skills:
        text = files[name].decode()
        assert text.startswith("---\n")
        header = text.split("---\n", 2)[1]
        assert re.search(r"^name: " + re.escape(Path(name).parent.name) + r"$", header, re.M)
        assert re.search(r"^description: \S", header, re.M)
    cases = extension["review"]["test_cases"]
    assert len(cases["positive"]) == 5 and len(cases["negative"]) == 3
    for case in cases["positive"]:
        for field in ["description", "prompt", "tools_triggered", "expected_behavior"]:
            assert isinstance(case[field], str) and case[field].strip()
    for case in cases["negative"]:
        assert case["description"].strip() and case["prompt"].strip()
    assert extension["publication"]["countries"] == []
    assert extension["publication"]["release_notes"].strip()
    for name, content in files.items():
        assert name in {"plugin.json", "mcp.json", "assets/icon.png",
                        "skills/posterly/SKILL.md", "skills/setup/SKILL.md"}, name
        if not name.endswith(".png"):
            text = content.decode()
            assert not re.search(r"pst_live_[a-zA-Z0-9]{8,}|sk-[a-zA-Z0-9]{16,}", text)
            assert "\u2014" not in text and "\u2013" not in text
    return manifest


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=ROOT / "dist")
parser.add_argument("--ready", action="store_true", help="Require a demo URL before packaging.")
args = parser.parse_args()
files = {}
for path in sorted(SOURCE.rglob("*")):
    assert not path.is_symlink(), path
    if path.is_file():
        files[path.relative_to(SOURCE).as_posix()] = path.read_bytes()
manifest = validate(files)
review = manifest["extensions"]["com.openai"]["review"]
if args.ready and not review.get("demo_recording_url"):
    parser.error("Missing verified demo_recording_url. This package is a draft.")
assert not args.output.resolve().is_relative_to(SOURCE.resolve())
args.output.mkdir(parents=True, exist_ok=True)
archive = args.output / ("posterly-openai-" + manifest["version"] + ".zip")
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
    for name, content in files.items():
        output.writestr("posterly/" + name, content)
with zipfile.ZipFile(archive) as output:
    packaged = {name.removeprefix("posterly/"): output.read(name) for name in output.namelist()}
    validate(packaged)
    assert packaged == files
print(archive)
print("Package validated and inspected: " + str(len(files)) + " files.")
if not review.get("demo_recording_url"):
    print("DRAFT: demo recording, reviewer access, and review case execution remain pending.")
else:
    print("Check reviewer access, saved-version cases, domain verification, and portal scans before submitting.")
