#!/usr/bin/env python3
"""
从 apps.yml 生成:
  1. public/apps.json — 备用数据源(只含 visible 的 app,不暴露未上线包名)
  2. docs/download.md 下载页 hero + 分类卡片区 — 与首页同一套文案与数据,主点击直达下载,SSR 直出不依赖客户端 JS
  3. docs/README.md 首页的 .app-grid 卡片区 — 与下载页同源,显隐由 visible 控制
  4. config.js 的导航栏「作品集合」下拉 — nav 字段控制(不写则跟随 visible)

维护 apps.yml 后运行:python3 generate_apps_json.py
"""
import html
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
OUT_CONFIG = BASE / "config.js"
OUT_SCSS = BASE / "styles" / "index.scss"


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
    """apps.json 只输出 visible 的 app,未上线包名不落到公开静态文件。"""
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    visible = [a for a in apps if a.get("visible")]
    OUT_JSON.write_text(json.dumps(visible, ensure_ascii=False, indent=2), encoding="utf-8")


# 首页/下载页共用 hero 文案, 两页不各说一套
GH_HERO_SUB = (
    "先为自己做，再交给你。这里的每一款应用，我都在每天使用："
    "没有广告、没有后台，你的数据只留在你的设备上——需要同步时，用的也是你自己的网盘。"
)

# 首页/下载页分类分区: key 与 apps.yml 的 category 字段对应, 按此顺序输出
HOME_CATEGORIES = [
    ("write", "写与读", "#2563eb"),
    ("image", "图片与影像", "#d97706"),
    ("audio", "声音", "#059669"),
    ("life", "家庭与健康", "#e11d48"),
    ("tools", "效率与安全", "#7c3aed"),
    ("web", "开源 · 网页工具", "#0d9488"),
]

MORE_CATEGORY = ("更多工具", "#78716c")  # 未登记 category 的兜底分区


def visible_sorted(apps):
    return sorted(
        [a for a in apps if a.get("visible")],
        key=lambda a: a.get("sort", 999),
    )


def build_hero(count, title, with_cta):
    """hero 头部: 首页与下载页同一套文案与结构, stats 数量自动统计 visible。

    with_cta: 首页带公众号/博客 CTA; 下载页不带(页尾已有交流群入口)。
    """
    cta = ""
    if with_cta:
        cta = (
            f'<div class="gh-cta">\n'
            f'<span class="gh-btn gh-btn-primary gh-wechat-btn" tabindex="0" title="关注公众号">\n'
            f'<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">'
            f'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>'
            f'<rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3z"/><path d="M20 14v.01"/><path d="M14 20v.01"/><path d="M20 20v.01"/></svg>\n'
            f"关注公众号 · 咕咚同学\n"
            f'<span class="gh-qr-pop">\n'
            f'<img src="https://gudong.s3.bitiful.net/asset/gongzhonghao.jpg" alt="咕咚同学公众号二维码">\n'
            f"<span>微信扫码关注，获取更新与上新通知</span>\n"
            f"</span>\n"
            f"</span>\n"
            f'<a class="gh-btn" href="https://blog.gudong.site/" target="_blank" rel="noopener" title="我的博客">\n'
            f'<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'<path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg>\n'
            f"我的博客</a>\n"
            f"</div>\n"
        )
    return (
        f'<header class="gh-hero">\n'
        f'<div class="gh-mark"><img src="https://gudong.s3.bitiful.net/asset/avatar.jpg" alt="咕咚"></div>\n'
        f'<div class="gh-eyebrow">独立开发 · MY LITTLE UNIVERSE</div>\n'
        f"<h1>{title}</h1>\n"
        f'<p class="gh-sub">{GH_HERO_SUB}</p>\n'
        f'<div class="gh-stats">\n'
        f'<span class="gh-stat"><b>{count}</b> 款应用</span>\n'
        f'<span class="gh-stat"><b>0</b> 广告</span>\n'
        f'<span class="gh-stat"><b>0</b> 后台</span>\n'
        f'<span class="gh-stat"><b>100%</b> 本地优先</span>\n'
        f"</div>\n"
        f"{cta}"
        f"</header>"
    )


def grouped_sections(visible):
    """按 HOME_CATEGORIES 分组; 未登记 category 的进「更多工具」兜底分区。"""
    sections = []
    grouped = set()
    for key, label, color in HOME_CATEGORIES:
        members = [a for a in visible if a.get("category") == key]
        if not members:
            continue
        grouped.update(a.get("name") for a in members)
        sections.append((label, color, members))
    others = [a for a in visible if a.get("name") not in grouped]
    if others:
        sections.append((MORE_CATEGORY[0], MORE_CATEGORY[1], others))
    return sections


def render_section(label, color, members, card_fn):
    cards = "\n".join(card_fn(a) for a in members)
    return (
        f'<section class="gh-section">\n'
        f'<div class="gh-cat-head"><span class="gh-cat-dot" style="--gh-cat:{color}"></span>'
        f"<h2>{label}</h2><span class=\"gh-cat-count\">{len(members)} 款</span></div>\n"
        f'<div class="gh-grid">\n{cards}\n</div>\n'
        f"</section>"
    )


def render_card(a, main_link, main_blank, btn_html):
    """gh-* 卡片骨架。首页主链接=doc(站内跳转)+hover 下载; 下载页主链接=download(新窗口)+文档次入口。"""
    safe_name = html.escape(str(a.get("name", "")))
    safe_desc = html.escape(str(a.get("desc", "")))
    badge = f'<span class="gh-badge">{html.escape(str(a["badge"]))}</span>' if a.get("badge") else ""
    target = ' target="_blank" rel="noopener"' if main_blank else ""
    return (
        f'<div class="gh-item">'
        f' <a class="gh-card" href="{main_link}"{target}>'
        f'<span class="gh-icon-well"><img src="{a.get("icon", "")}" alt="{safe_name}"></span>'
        f'<span class="gh-card-main">'
        f'<span class="gh-card-name">{safe_name}{badge}</span>'
        f'<span class="gh-card-desc">{safe_desc}</span>'
        f"</span>"
        f"</a>{btn_html}"
        f"</div>"
    )


def home_dl_btn(a):
    """首页卡片下载快捷入口: 紧凑模式由 CSS 显示; a 内不可嵌 a, 作为兄弟节点放在 .gh-item 包裹层里"""
    if not a.get("download"):
        return ""
    safe_dl = html.escape(str(a.get("name", "")), quote=True)
    return (
        f'<a class="gh-dl" href="{a.get("download")}" target="_blank" rel="noopener" '
        f'aria-label="下载 {safe_dl}" title="下载 {safe_dl}">'
        f'<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg></a>'
    )


def dl_page_doc_btn(a):
    """下载页卡片「文档」次入口: 主点击已是下载, 角上反向放文档; 链接与下载相同时(网页工具)不重复放。"""
    doc = a.get("doc", "")
    if not doc or doc == a.get("download", ""):
        return ""
    safe_name = html.escape(str(a.get("name", "")), quote=True)
    safe_doc = html.escape(str(doc), quote=True)
    return (
        f'<a class="gh-doc" href="{safe_doc}" target="_blank" rel="noopener" '
        f'aria-label="查看 {safe_name} 文档" title="查看 {safe_name} 文档">'
        f'<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'<path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2z"/>'
        f'<path d="M22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z"/></svg></a>'
    )


def gen_download_page(apps):
    """生成 download.md 下载页 hero + 分类分区并替换到 APPS_DL 标记之间。

    与首页同一套文案与分类; 差异: 卡片主点击直达下载(下载页定位), badge 同样输出。
    """
    visible = visible_sorted(apps)
    sections = "\n".join(
        render_section(
            label,
            color,
            members,
            lambda a: render_card(a, a.get("download", ""), True, dl_page_doc_btn(a)),
        )
        for label, color, members in grouped_sections(visible)
    )
    page_block = (
        f"{build_hero(len(visible), '下载地址', with_cta=False)}\n"
        # 下载页定位是"快速找到 App", 静态套用首页的紧凑双列形态(无切换)
        f'<div id="gh-sections" class="gh-compact">\n{sections}\n</div>'
    )

    content = OUT_DOWNLOAD.read_text(encoding="utf-8")
    pattern = r"<!-- APPS_DL_START -->.*?<!-- APPS_DL_END -->"
    replacement = f"<!-- APPS_DL_START -->\n{page_block}\n<!-- APPS_DL_END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("⚠️  download.md 下载页区域未变化(检查标记是否存在)", file=sys.stderr)
    else:
        OUT_DOWNLOAD.write_text(new_content, encoding="utf-8")


def gen_home_grid(apps):
    """生成 README.md 首页 hero + 分类分区并替换到 <!-- APPS_GRID_START/END --> 标记之间。"""
    visible = visible_sorted(apps)
    sections = "\n".join(
        render_section(
            label,
            color,
            members,
            lambda a: render_card(a, a.get("doc", ""), False, home_dl_btn(a)),
        )
        for label, color, members in grouped_sections(visible)
    )
    grid_block = (
        f"{build_hero(len(visible), '我的产品小宇宙', with_cta=True)}\n"
        f'<div class="gh-viewbar">\n'
        f'<div class="gh-seg" id="gh-density-seg">\n'
        f'<button type="button" data-gh-d="cozy" class="gh-on" aria-label="宽松视图">'
        f'<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" stroke="none" aria-hidden="true">'
        f'<rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/>'
        f'<rect x="3" y="13" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/></svg>'
        f"宽松</button>\n"
        f'<button type="button" data-gh-d="compact" aria-label="紧凑视图">'
        f'<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" stroke="none" aria-hidden="true">'
        f'<rect x="3" y="4" width="18" height="3.5" rx="1.75"/><rect x="3" y="10.25" width="18" height="3.5" rx="1.75"/>'
        f'<rect x="3" y="16.5" width="18" height="3.5" rx="1.75"/></svg>'
        f"紧凑</button>\n"
        f"</div>\n"
        f"</div>\n"
        f'<div id="gh-sections">\n{sections}\n</div>'
    )

    content = OUT_HOME.read_text(encoding="utf-8")
    pattern = r"<!-- APPS_GRID_START -->.*?<!-- APPS_GRID_END -->"
    replacement = f"<!-- APPS_GRID_START -->\n{grid_block}\n<!-- APPS_GRID_END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("⚠️  README.md 卡片区域未变化(检查标记是否存在)", file=sys.stderr)
    else:
        OUT_HOME.write_text(new_content, encoding="utf-8")


def nav_entries(apps):
    """导航栏展示条目:(sort, name, link, icon),展示规则见 gen_navbar docstring。"""
    entries = []
    for a in apps:
        in_nav = a.get("nav") if a.get("nav") is not None else a.get("visible")
        if not in_nav:
            continue
        link = a.get("nav_link") or a.get("doc") or ""
        if not link:
            print(f"⚠️  {a.get('name')} 在导航栏展示但没有 doc/nav_link,已跳过", file=sys.stderr)
            continue
        entries.append((a.get("sort", 999), a.get("name", ""), link, a.get("icon", "")))
    entries.sort(key=lambda e: e[0])
    return entries


def gen_navbar(apps):
    """生成 config.js 导航栏「作品集合」下拉并替换到 APPS_NAV 标记之间。

    展示条件:nav 字段不写则跟随 visible;显式 nav: true 可让未上下载页的 App 只进导航栏,
    nav: false 则只在导航栏隐藏。链接优先用 nav_link(覆盖 doc),sort 升序排列。
    """
    lines = [
        "// 此下拉由 generate_apps_json.py 从 apps.yml 生成，请勿手动编辑",
        *[f"      {{ text: '{name}', link: '{link}' }}," for _, name, link, _ in nav_entries(apps)],
    ]
    nav_block = "\n".join(lines)

    content = OUT_CONFIG.read_text(encoding="utf-8")
    pattern = r"// <!-- APPS_NAV_START -->.*?// <!-- APPS_NAV_END -->"
    replacement = f"// <!-- APPS_NAV_START -->\n{nav_block}\n// <!-- APPS_NAV_END -->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("⚠️  config.js 导航栏区域未变化(检查标记是否存在)", file=sys.stderr)
    else:
        OUT_CONFIG.write_text(new_content, encoding="utf-8")


def gen_nav_icons(apps):
    """生成 index.scss 中导航下拉每一项的 icon 规则(NAV_ICONS 标记区)。

    按链接精确匹配 .navbar-dropdown-item > a[href],给 ::before 注入背景图。
    """
    rules = [
        f'.navbar-dropdown .navbar-dropdown-item > a[href="{link}"]::before '
        f'{{ background-image: url("{icon}"); }}'
        for _, _, link, icon in nav_entries(apps)
        if icon
    ]
    icons_block = "\n".join(rules)

    content = OUT_SCSS.read_text(encoding="utf-8")
    pattern = r"// NAV_ICONS_START.*?// NAV_ICONS_END"
    replacement = f"// NAV_ICONS_START\n{icons_block}\n// NAV_ICONS_END"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("⚠️  index.scss icon 区域未变化(检查标记是否存在)", file=sys.stderr)
    else:
        OUT_SCSS.write_text(new_content, encoding="utf-8")


def main():
    if not YML.exists():
        print(f"❌ 找不到 {YML}", file=sys.stderr)
        sys.exit(1)

    apps = parse_yml_simple(YML.read_text(encoding="utf-8"))

    gen_apps_json(apps)
    visible = [a for a in apps if a.get("visible")]
    print(f"✓ 生成 {OUT_JSON} ({len(apps)} 个 app,可见 {len(visible)} 个)")

    gen_download_page(apps)
    print(f"✓ 更新 {OUT_DOWNLOAD} 下载页 ({len(visible)} 张)")

    gen_home_grid(apps)
    print(f"✓ 更新 {OUT_HOME} 首页卡片 ({len(visible)} 张)")

    gen_navbar(apps)
    nav_count = len(nav_entries(apps))
    print(f"✓ 更新 {OUT_CONFIG} 导航栏 ({nav_count} 项)")

    gen_nav_icons(apps)
    print(f"✓ 更新 {OUT_SCSS} 导航 icon ({nav_count} 条)")


if __name__ == "__main__":
    main()
