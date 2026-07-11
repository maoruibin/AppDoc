#!/usr/bin/env python3
"""
从 apps.yml 生成 public/apps.json,供下载页前端 fetch。
维护 apps.yml 后运行:python3 generate_apps_json.py
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
YML = BASE / "apps.yml"
OUT = BASE / "public" / "apps.json"


def parse_yml_simple(text):
    """简易 YAML 解析(只支持本文件的 - key: value 结构,避免依赖 PyYAML)。"""
    apps = []
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current:
                apps.append(current)
            current = {}
            stripped = stripped[2:].strip()
            if stripped:
                k, _, v = stripped.partition(":")
                current[k.strip()] = _cast(v.strip())
        elif ":" in stripped and current is not None:
            k, _, v = stripped.partition(":")
            current[k.strip()] = _cast(v.strip())
    if current:
        apps.append(current)
    return apps


def _cast(v):
    """转 bool/int,其余去引号保持 string。"""
    if v in ("true", "false"):
        return v == "true"
    try:
        return int(v)
    except ValueError:
        pass
    if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
        return v[1:-1]
    return v


def main():
    if not YML.exists():
        print(f"❌ 找不到 {YML}", file=sys.stderr)
        sys.exit(1)
    apps = parse_yml_simple(YML.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(apps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ 生成 {OUT} ({len(apps)} 个 app)")
    visible = [a for a in apps if a.get("visible")]
    print(f"  可见: {len(visible)} 个")


if __name__ == "__main__":
    main()
