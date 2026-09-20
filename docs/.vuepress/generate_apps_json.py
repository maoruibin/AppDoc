#!/usr/bin/env python3
"""
从 apps.yml 生成:
  1. public/apps.json — 备用数据源
  2. docs/download.md 的卡片网格区域 — HTML 卡片,SSR 直出,不依赖客户端 JS
  3. docs/README.md 首页的 .app-grid 卡片区 — 与下载页同源,显隐由 visible 控制

维护 apps.yml 后运行:python3 generate_apps_json.py
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
DOCS = BASE.parent  # docs/
YML = BASE / "apps.yml"
OUT_JSON = BASE / "public" / "apps.json"
OUT_DOWNLOAD = DOCS / "download.md"
OUT_HOME = DOCS / "README.md"


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


def gen_apps_json(apps):
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(apps, ensure_ascii=False, indent=2), encoding="utf-8")


def gen_download_table(apps):
    """生成 download.md 的卡片网格区域并替换到 <!-- APPS_TABLE_START/END --> 标记之间。"""
    import html

    visible = sorted(
        [a for a in apps if a.get("visible")],
        key=lambda a: a.get("sort", 999),
    )

    lines = ["<!-- 此卡片网格由 generate_apps_json.py 自动生成，请勿手动编辑 -->", '<div class="app-dl-grid">']
    for a in visible:
        icon = a.get("icon", "")
        name = a.get("name", "")
        desc = a.get("desc", "")
        doc = a.get("doc", "")
        download = a.get("download", "")
        safe_name = html.escape(str(name))
        safe_desc = html.escape(str(desc))
        lines.append(
            f'<a class="app-dl-card" href="{download}">'
            f'<img class="app-dl-icon" src="{icon}" alt="{safe_name}">'
            f'<div class="app-dl-info">'
            f'<div class="app-dl-name">{safe_name}</div>'
            f'<div class="app-dl-desc">{safe_desc}</div>'
            f"</div>"
            f'<span class="app-dl-btn">下载主页</span>'
            f"</a>"
        )
    lines.append("</div>")

    table_block = "\n".join(lines)

    content = OUT_DOWNLOAD.read_text(encoding="utf-8")
    pattern = r"<!-- APPS_TABLE_START -->.*?<!-- APPS_TABLE_END -->"
    replacement = f"<!-- APPS_TABLE_START -->\n{table_block}\n<!-- APPS_TABLE_END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("⚠️  download.md 表格区域未变化(检查标记是否存在)", file=sys.stderr)
    else:
        OUT_DOWNLOAD.write_text(new_content, encoding="utf-8")


def gen_home_grid(apps):
    """生成 README.md 首页 .app-grid 卡片区并替换到 <!-- APPS_GRID_START/END --> 标记之间。"""
    import html

    visible = sorted(
        [a for a in apps if a.get("visible")],
        key=lambda a: a.get("sort", 999),
    )

    lines = ['<div class="app-grid">']
    for a in visible:
        safe_name = html.escape(str(a.get("name", "")))
        safe_desc = html.escape(str(a.get("desc", "")))
        lines.append(
            f' <a class="app-card" href="{a.get("doc", "")}">'
            f'<img src="{a.get("icon", "")}" alt="{safe_name}">'
            f'<div class="app-name">{safe_name}</div>'
            f'<div class="app-desc">{safe_desc}</div>'
            f"</a>"
        )
    lines.append("</div>")

    grid_block = "\n".join(lines)

    content = OUT_HOME.read_text(encoding="utf-8")
    pattern = r"<!-- APPS_GRID_START -->.*?<!-- APPS_GRID_END -->"
    replacement = f"<!-- APPS_GRID_START -->\n{grid_block}\n<!-- APPS_GRID_END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("⚠️  README.md 卡片区域未变化(检查标记是否存在)", file=sys.stderr)
    else:
        OUT_HOME.write_text(new_content, encoding="utf-8")


def main():
    if not YML.exists():
        print(f"❌ 找不到 {YML}", file=sys.stderr)
        sys.exit(1)

    apps = parse_yml_simple(YML.read_text(encoding="utf-8"))

    gen_apps_json(apps)
    visible = [a for a in apps if a.get("visible")]
    print(f"✓ 生成 {OUT_JSON} ({len(apps)} 个 app,可见 {len(visible)} 个)")

    gen_download_table(apps)
    print(f"✓ 更新 {OUT_DOWNLOAD} 表格 ({len(visible)} 行)")

    gen_home_grid(apps)
    print(f"✓ 更新 {OUT_HOME} 首页卡片 ({len(visible)} 张)")


if __name__ == "__main__":
    main()
