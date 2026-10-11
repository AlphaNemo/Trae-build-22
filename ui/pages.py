"""
药品说明书 · 三行大字卡 —— 5 屏页面组件
屏幕：home(首页) → scan(拍照上传) → result(结果) → box(药盒) / share(分享弹层)
"""

import base64
import random
from nicegui import ui

from logic import scan_service
from ui.a11y import a11y_card, a11y_button, a11y_label
from ui.drug_data import DRUGS, get_drug
from ui.tts import speak, stop_speaking


# ── 全局状态（Python 全局变量就够，本次会话内有效） ────────

class AppState:
    def __init__(self):
        self.current_screen = 'home'       # home / scan / result / box
        self.selected_drug = None          # dict | None
        self.medbox: list[str] = []        # 药盒里的药 id 列表
        self.font_big = False              # 字号切换

    def add_to_box(self, drug_id: str):
        if drug_id not in self.medbox:
            self.medbox.append(drug_id)

    def remove_from_box(self, drug_id: str):
        if drug_id in self.medbox:
            self.medbox.remove(drug_id)


# 模块级单例 —— 所有页面共享
state = AppState()


# ── 页面切换（带 refresh） ──────────────────────────────

def go_to(screen: str, refresh_fn, drug=None):
    """切换屏幕并刷新"""
    state.current_screen = screen
    if drug is not None:
        state.selected_drug = drug
    refresh_fn.refresh()


# ── 首页（SCREEN: home） ────────────────────────────────

def build_home(refresh_fn):
    """屏 1 · 首页 —— 三个大按钮"""
    with ui.column().classes('w-full items-center gap-5'):
        # 顶部小标语
        a11y_label('拍一下，就知道这药怎么吃',
                   aria_label='首页标语',
                   color='#4A4A4A').classes('text-lg mt-4')

        # 首页标题大字
        ui.label('药品说明书\n三行大字卡').classes('text-4xl font-bold text-center') \
            .style('color: var(--text-primary); line-height: 1.3') \
            .props('aria-label="药品说明书三行大字卡应用标题" role="heading" aria-level="1"')

        ui.label('把 500 字说明书，压缩成三行大字').classes('text-base') \
            .style('color: var(--text-secondary)')

        # ── 三个大按钮（全宽） ──
        with ui.column().classes('w-full gap-4 mt-4'):
            a11y_button('📷  拍说明书',
                        variant='primary',
                        aria_label='拍说明书按钮，进入假拍照扫描') \
                .on('click', lambda: go_to('scan', refresh_fn))

            a11y_button('📋  从常用药里选',
                        variant='secondary',
                        aria_label='从常用药里选择按钮，进入药品列表') \
                .on('click', lambda: show_drug_picker(refresh_fn))

            # 我的药盒 —— 有药时显示数量
            box_text = f'💊  我的药盒 ({len(state.medbox)})' if state.medbox else '💊  我的药盒'
            a11y_button(box_text,
                        variant='secondary',
                        aria_label='打开我的药盒') \
                .on('click', lambda: go_to('box', refresh_fn))

        # 底部说明
        ui.label('不用登录 · 离线可用 · 专为老人设计') \
            .classes('text-sm mt-6').style('color: var(--text-muted)')


# ── 常用药选择弹层 ──────────────────────────────────────

def show_drug_picker(refresh_fn):
    """弹出药品选择菜单（8 种药，大卡片网格）"""
    with ui.dialog() as dialog, ui.card().classes('a11y-card'):
        ui.label('选择药品').classes('text-2xl font-bold mb-4') \
            .props('role="heading" aria-level="2"')

        with ui.column().classes('w-full gap-3'):
            for drug in DRUGS:
                did = drug['id']
                dname = drug['name']
                dl = drug['lines']
                summary = f"{dl['dose']} · {dl['freq']} · {dl['timing'][:8]}"

                def _make_pick(d=drug):
                    def _pick():
                        state.add_to_box(d['id'])
                        dialog.close()
                        go_to('result', refresh_fn, drug=d)
                    return _pick

                with ui.row().classes('w-full items-center justify-between q-py-sm px-3') \
                        .style('background: var(--bg-card-alt); border-radius: 12px; cursor: pointer') \
                        .on('click', _make_pick()):
                    with ui.column():
                        ui.label(dname).classes('text-lg font-semibold') \
                            .props(f'aria-label="选择 {dname}"')
                        ui.label(summary).classes('text-sm') \
                            .style('color: var(--text-muted)')

        ui.button('关闭', on_click=dialog.close) \
            .props('aria-label="关闭药品选择" outline').classes('mt-3')

    dialog.open()


# ── 拍照上传扫描（SCREEN: scan） ──────────────────────

def build_scan(refresh_fn):
    """屏 2 · 拍照上传 + 扫描动画
    用户可以选图片上传（药盒/说明书），显示预览 + 扫描线动画
    1.2s 后自动跳结果页（从常用药里随机选一个做演示）"""
    state.selected_drug = state.selected_drug or random.choice(DRUGS)

    # 扫描框容器（后面会被填入 img + scan-line）
    scan_frame = ui.element('div').classes('scan-frame self-center') \
        .style('width: 80%; max-width: 320px') \
        .props('aria-label="扫描取景框" role="img"')

    # 状态文字（动态更新）
    status = ui.label('请先选择一张药盒或说明书照片…') \
        .classes('text-base mt-2') \
        .style('color: var(--text-muted)') \
        .props('aria-live="polite" role="status"')

    async def _on_upload(e):
        """上传回调：读图片 → 显示预览 → 真 AI 识别（失败静默回退预置）→ 跳结果页"""
        status.set_text('正在识别…')

        data = await e.file.read()
        ctype = getattr(e.file, 'content_type', None) or 'image/jpeg'
        b64 = base64.b64encode(data).decode()
        img_src = f'data:{ctype};base64,{b64}'

        # 清空扫描框，填入图片 + 扫描线（动画在识别期间持续播放）
        scan_frame.clear()
        with scan_frame:
            ui.html(f'<img src="{img_src}" alt="上传的药品图片">')
            ui.element('div').classes('scan-line')

        # 真 AI 识别：配置了 key 且识别成功 → 用 AI 读到的三行；
        # 未配置 / 超时 / 拍不清 / 非预置药 → scan_service 返回 None，静默走预置演示流程
        drug = await scan_service.scan_drug(data, getattr(e.file, 'name', '') or 'photo.jpg')
        if drug is not None:
            state.selected_drug = drug
            status.set_text('✅ AI 识别：' + drug['name'] + '，正在生成三行卡…')
        else:
            status.set_text('✅ 已识别：' + state.selected_drug['name'] + '，正在生成三行卡…')
        ui.timer(0.8, lambda: go_to('result', refresh_fn), once=True)

    with ui.column().classes('w-full items-center gap-3'):
        # 返回按钮
        ui.button('← 返回',
                  on_click=lambda: go_to('home', refresh_fn)) \
            .props('aria-label="返回首页"').classes('back-btn self-start')

        ui.label('拍一下，就知道这药怎么吃').classes('text-lg mt-1') \
            .style('color: var(--text-secondary)')

        # 扫描框（先占位置，上传后填入图片）
        scan_frame

        # 上传按钮
        with ui.column().classes('w-full items-center gap-2 mt-1'):
            ui.upload(
                label='📷 选择图片（药盒 / 说明书）',
                multiple=False,
                max_files=1,
                on_upload=_on_upload,
            ).props('aria-label="选择药品图片上传" size=lg rounded accept="image/*"') \
                .classes('w-full')

        # 兜底链接：直接选药（PDF 方案原文）
        ui.button('📋 拍不清楚？从常用药里选',
                  on_click=lambda: show_drug_picker(refresh_fn)) \
            .props('aria-label="跳过扫描，从常用药里选择" outline') \
            .classes('mt-1')

        status


# ── 结果页（SCREEN: result）—— 核心三行大字卡 ─────────────

def build_result(refresh_fn):
    """屏 3 · 结果页 —— 三行大字 + 警示条 + 操作按钮"""
    drug = state.selected_drug or DRUGS[0]

    def _back_to_home():
        stop_speaking()
        go_to('home', refresh_fn)

    def _back_to_home_pick_again():
        stop_speaking()
        show_drug_picker(refresh_fn)

    with ui.column().classes('w-full gap-3'):
        # 返回按钮
        ui.button('← 返回', on_click=_back_to_home) \
            .props('aria-label="返回首页"').classes('back-btn self-start')

        # 药名（36px）
        ui.label(drug['name']).classes('drug-name self-center') \
            .props(f'aria-label="{drug["name"]} 用药信息" role="heading" aria-level="1"')

        # ── 三行大字（52px） ──
        lines = drug['lines']

        with ui.column().classes('w-full gap-0 a11y-card').style('padding: 24px 20px'):
            # 第一行：一次几粒
            with ui.row().classes('w-full items-end gap-2'):
                ui.label('💊').classes('text-4xl')
                with ui.column():
                    ui.label('一次').classes('drug-line-label')
                    ui.label(lines['dose']).classes('drug-line') \
                        .props(f'aria-label="服药剂量：{lines["dose"]}"')

            ui.element('div').style('height: 1px; background: var(--border); margin: 8px 0')

            # 第二行：一天几次
            with ui.row().classes('w-full items-end gap-2'):
                ui.label('🕐').classes('text-4xl')
                with ui.column():
                    ui.label('一天').classes('drug-line-label')
                    ui.label(lines['freq']).classes('drug-line') \
                        .props(f'aria-label="服药频率：{lines["freq"]}"')

            ui.element('div').style('height: 1px; background: var(--border); margin: 8px 0')

            # 第三行：饭前/饭后
            with ui.row().classes('w-full items-end gap-2'):
                ui.label('🍽️').classes('text-4xl')
                with ui.column():
                    ui.label('吃饭').classes('drug-line-label')
                    ui.label(lines['timing']).classes('drug-line') \
                        .props(f'aria-label="服药时间：{lines["timing"]}"')

        # ── 灰色小注释（有 note 才显示） ──
        if drug.get('note'):
            ui.label(f'💡 {drug["note"]}').classes('drug-note self-center w-full') \
                .props(f'aria-label="温馨提示：{drug["note"]}"')

        # ── 红色警示条（有 warning 才显示） ──
        if drug.get('warning'):
            with ui.row().classes('w-full items-center gap-3 warning-bar'):
                ui.label('⚠️').classes('text-3xl')
                ui.label(drug['warning']).classes('flex-1') \
                    .props(f'role="alert" aria-label="红色警示：{drug["warning"]}"')

        # ── 操作按钮组：念给我听 / 放进药盒 / 发给子女 ──
        with ui.row().classes('w-full gap-2 mt-2'):
            a11y_button('🔊 念给我听',
                        variant='primary',
                        full_width=True,
                        aria_label='朗读这个药的用法') \
                .on('click', lambda: _speak_drug(drug))

        with ui.row().classes('w-full gap-2'):
            a11y_button('➕ 放进我的药盒',
                        variant='secondary',
                        full_width=True,
                        aria_label='把这个药加入我的药盒') \
                .on('click', lambda: _add_and_notify(drug, refresh_fn))

            a11y_button('📤 发给子女',
                        variant='secondary',
                        full_width=True,
                        aria_label='分享这个药的用法给子女') \
                .on('click', lambda: show_share_dialog(drug))

        # ── 字号调节 ──
        with ui.row().classes('w-full items-center justify-center gap-4 mt-2'):
            ui.label('字号') \
                .style('color: var(--text-muted)').props('aria-label="字号调节"')
            ui.button('A-',
                      on_click=lambda: _set_font_big(False)) \
                .props('aria-label="调小字号"').classes('back-btn q-px-sm')
            ui.button('A+',
                      on_click=lambda: _set_font_big(True)) \
                .props('aria-label="调大字号"').classes('back-btn q-px-sm')
            ui.button('换个药',
                      on_click=_back_to_home_pick_again) \
                .props('aria-label="换另一种药"').classes('back-btn')


def _speak_drug(drug: dict):
    """朗读完整用药信息（慢速 0.85，老人友好）"""
    lines = drug['lines']
    text = (f"{drug['name']}。"
            f"{lines['dose']}。{lines['freq']}。{lines['timing']}。")
    if drug.get('warning'):
        text += f"注意！{drug['warning']}。"
    if drug.get('note'):
        text += f"温馨提示，{drug['note']}。"
    speak(text, rate=0.85)


def _set_font_big(big: bool):
    from ui.a11y import toggle_large_font
    state.font_big = big
    toggle_large_font(big)


def _add_and_notify(drug: dict, refresh_fn):
    state.add_to_box(drug['id'])
    ui.notify(f'✅ {drug["name"]} 已放进药盒', type='positive')
    # 刷新首页药盒计数
    refresh_fn.refresh()


# ── 我的药盒（SCREEN: box） ──────────────────────────────

def build_box(refresh_fn):
    """屏 4 · 我的药盒 —— Python 全局变量存 id 列表"""
    with ui.column().classes('w-full gap-3'):
        ui.button('← 返回', on_click=lambda: go_to('home', refresh_fn)) \
            .props('aria-label="返回首页"').classes('back-btn self-start')

        ui.label('我的药盒').classes('text-3xl font-bold self-center mt-2') \
            .props('role="heading" aria-level="1"')

        # 空状态
        if not state.medbox:
            with ui.column().classes('w-full items-center gap-4 q-py-xl'):
                ui.label('💊').classes('text-6xl')
                ui.label('药盒还空着') \
                    .classes('text-xl font-semibold')
                ui.label('拍一次说明书，就能把药放进来') \
                    .classes('text-base') \
                    .style('color: var(--text-muted)')
                a11y_button('📋 从常用药里选',
                            variant='primary',
                            aria_label='选择药品加入药盒') \
                    .on('click', lambda: show_drug_picker(refresh_fn))
        else:
            # 有药列表
            with ui.column().classes('w-full'):
                for did in state.medbox:
                    drug = get_drug(did)
                    if not drug:
                        continue
                    dl = drug['lines']
                    summary = f"{dl['dose']} · {dl['freq']} · {dl['timing'][:12]}"

                    def _make_open(d=drug):
                        def _open():
                            go_to('result', refresh_fn, drug=d)
                        return _open

                    def _make_remove(did2=did):
                        def _remove():
                            state.remove_from_box(did2)
                            ui.notify('已从药盒移除', type='info')
                            refresh_fn.refresh()
                        return _remove

                    with ui.row().classes('w-full box-item'):
                        with ui.column().classes('flex-1').on('click', _make_open()):
                            ui.label(f'💊 {drug["name"]}').classes('text-lg font-semibold') \
                                .props(f'aria-label="打开 {drug["name"]}"')
                            ui.label(summary).classes('text-sm') \
                                .style('color: var(--text-muted)')

                        ui.button('🗑', on_click=_make_remove()) \
                            .props(f'aria-label="从药盒移除 {drug["name"]}"') \
                            .classes('back-btn')


# ── 分享弹层（屏 5 · 发给子女） ───────────────────────────

def show_share_dialog(drug: dict):
    """屏 5 · 发给子女 —— 弹出分享卡 + 复制文字按钮"""
    lines = drug['lines']
    text = f"""📋 {drug['name']} 用法三行卡
━━━━━━━━━━━━━━━━━━
💊 {lines['dose']}
🕐 {lines['freq']}
🍽️ {lines['timing']}"""
    if drug.get('warning'):
        text += f"\n\n⚠️ 警示：{drug['warning']}"
    text += f"\n\n📅 {_today()}"

    with ui.dialog() as dialog, ui.card().classes('a11y-card'):
        ui.label('发给子女').classes('text-2xl font-bold mb-3') \
            .props('role="heading" aria-level="2"')

        # 分享卡预览
        with ui.column().classes('a11y-card-warm w-full'):
            ui.label(drug['name']).classes('text-2xl font-bold self-center')
            ui.element('hr').style('border-color: var(--border); margin: 12px 0')
            ui.label('💊 一次').classes('drug-line-label')
            ui.label(lines['dose']).classes('text-xl')
            ui.label('🕐 一天').classes('drug-line-label mt-2')
            ui.label(lines['freq']).classes('text-xl')
            ui.label('🍽️ 吃饭').classes('drug-line-label mt-2')
            ui.label(lines['timing']).classes('text-xl')
            if drug.get('warning'):
                ui.label(f'⚠️ {drug["warning"]}').classes('drug-warning')

        with ui.row().classes('w-full gap-3 mt-4'):
            a11y_button('📋 复制文字', variant='primary',
                        full_width=True,
                        aria_label='复制分享文字到剪贴板') \
                .on('click', lambda: _copy_to_clipboard(text))

            a11y_button('关闭', variant='secondary',
                        full_width=True,
                        aria_label='关闭分享弹层') \
                .on('click', dialog.close)

    dialog.open()


def _today() -> str:
    from datetime import date
    d = date.today()
    return f'{d.year}年{d.month}月{d.day}日'


def _copy_to_clipboard(text: str):
    """用 Clipboard API 复制文字"""
    escaped = text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    js = f'''
    (function(){{
        navigator.clipboard.writeText(`{escaped}`).then(
            () => {{ showCopyToast('✅ 已复制，粘贴到家庭群即可'); }},
            () => {{ showCopyToast('❌ 复制失败，请手动选择文本'); }}
        );
    }})();
    function showCopyToast(msg) {{
        var el = document.createElement('div');
        el.textContent = msg;
        el.style.cssText = 'position:fixed;top:20px;left:50%;transform:translateX(-50%);background:var(--accent);color:#fff;padding:12px 24px;border-radius:12px;z-index:9999;font-size:16px;box-shadow:0 4px 20px rgba(0,0,0,0.2);';
        document.body.appendChild(el);
        setTimeout(()=>el.remove(), 2500);
    }}
    '''
    ui.run_javascript(js)
