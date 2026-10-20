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


# 首页分类分区: key 与 apps.yml 的 category 字段对应, 按此顺序输出
HOME_CATEGORIES = [
    ("write", "写与读", "#2563eb"),
    ("image", "图片与影像", "#d97706"),
    ("audio", "声音", "#059669"),
    ("life", "家庭与健康", "#e11d48"),
    ("tools", "效率与安全", "#7c3aed"),
]


def gen_home_grid(apps):
    """生成 README.md 首页 hero + 分类分区并替换到 <!-- APPS_GRID_START/END --> 标记之间。"""
    import html

    visible = sorted(
        [a for a in apps if a.get("visible")],
        key=lambda a: a.get("sort", 999),
    )

    def card(a):
        safe_name = html.escape(str(a.get("name", "")))
        safe_desc = html.escape(str(a.get("desc", "")))
        badge = f'<span class="gh-badge">{html.escape(str(a["badge"]))}</span>' if a.get("badge") else ""
        # 下载快捷入口: 紧凑模式由 CSS 显示; a 内不可嵌 a, 作为兄弟节点放在 .gh-item 包裹层里
        dl_btn = ""
        if a.get("download"):
            safe_dl = html.escape(str(a.get("name", "")), quote=True)
            dl_btn = (
                f'<a class="gh-dl" href="{a.get("download")}" target="_blank" rel="noopener" '
                f'aria-label="下载 {safe_dl}" title="下载 {safe_dl}">'
                f'<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
                f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg></a>'
            )
        return (
            f'<div class="gh-item">'
            f' <a class="gh-card" href="{a.get("doc", "")}">'
            f'<span class="gh-icon-well"><img src="{a.get("icon", "")}" alt="{safe_name}"></span>'
            f'<span class="gh-card-main">'
            f'<span class="gh-card-name">{safe_name}{badge}</span>'
            f'<span class="gh-card-desc">{safe_desc}</span>'
            f"</span>"
            f"</a>{dl_btn}"
            f"</div>"
        )

    sections = []
    grouped = set()
    for key, label, color in HOME_CATEGORIES:
        members = [a for a in visible if a.get("category") == key]
        if not members:
            continue
        grouped.update(a.get("name") for a in members)
        cards = "\n".join(card(a) for a in members)
        sections.append(
            f'<section class="gh-section">\n'
            f'<div class="gh-cat-head"><span class="gh-cat-dot" style="--gh-cat:{color}"></span>'
            f"<h2>{label}</h2><span class=\"gh-cat-count\">{len(members)} 款</span></div>\n"
            f'<div class="gh-grid">\n{cards}\n</div>\n'
            f"</section>"
        )
    others = [a for a in visible if a.get("name") not in grouped]
    if others:
        cards = "\n".join(card(a) for a in others)
        sections.append(
            f'<section class="gh-section">\n'
            f'<div class="gh-cat-head"><span class="gh-cat-dot" style="--gh-cat:#78716c"></span>'
            f"<h2>更多工具</h2><span class=\"gh-cat-count\">{len(others)} 款</span></div>\n"
            f'<div class="gh-grid">\n{cards}\n</div>\n'
            f"</section>"
        )

    count = len(visible)
    block = "\n".join(sections)
    grid_block = (
        f'<header class="gh-hero">\n'
        f'<div class="gh-mark">咕</div>\n'
        f'<div class="gh-eyebrow">独立开发 · MY LITTLE UNIVERSE</div>\n'
        f"<h1>咕咚的小宇宙</h1>\n"
        f'<p class="gh-sub">先为自己做，再交给你。这里的每一款应用，我都在每天使用：没有广告、没有后台，你的数据只留在你的设备上——需要同步时，用的也是你自己的网盘。</p>\n'
        f'<div class="gh-stats">\n'
        f'<span class="gh-stat"><b>{count}</b> 款应用</span>\n'
        f'<span class="gh-stat"><b>0</b> 广告</span>\n'
        f'<span class="gh-stat"><b>0</b> 后台</span>\n'
        f'<span class="gh-stat"><b>100%</b> 本地优先</span>\n'
        f"</div>\n"
        f'<div class="gh-cta">\n'
        f'<a class="gh-btn gh-btn-primary" href="#gh-sections">浏览全部应用</a>\n'
        f"</div>\n"
        f"</header>\n"
        f'<div class="gh-viewbar">\n'
        f'<span class="gh-viewbar-label">视图</span>\n'
        f'<div class="gh-seg" id="gh-density-seg">\n'
        f'<button type="button" data-gh-d="cozy" class="gh-on">宽松</button>\n'
        f'<button type="button" data-gh-d="compact">紧凑</button>\n'
        f"</div>\n"
        f"</div>\n"
        f'<div id="gh-sections">\n{block}\n</div>'
    )

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
