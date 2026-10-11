# main.py —— 药品说明书 · 三行大字卡
# 后端路由挂载（角色 B 地盘，保留不动）
from nicegui import app, ui
from logic import api_router

app.include_router(api_router)

# 前端装配（角色 A 独占）
from ui.a11y import setup_theme, init_a11y_state
from ui.pages import (
    state, build_home, build_scan, build_result, build_box,
)

# ── 主题初始化（米白底 + 深字 + 警示红） ──────────────────
setup_theme()
init_a11y_state()


# ── 主渲染函数：按 state.current_screen 分发 ───────────────
@ui.refreshable
def render_screen():
    """5 屏状态机 —— @ui.refreshable 原地刷新"""
    screen = state.current_screen

    with ui.element('div').classes('phone-shell').props('role="main"'):
        if screen == 'home':
            build_home(render_screen)
        elif screen == 'scan':
            build_scan(render_screen)
        elif screen == 'result':
            build_result(render_screen)
        elif screen == 'box':
            build_box(render_screen)
        # share 是 dialog，不需要独立 screen
        # 未知状态兜底：回首页
        elif screen not in ('home', 'scan', 'result', 'box'):
            state.current_screen = 'home'
            build_home(render_screen)


# ── 入口：先渲染首页 ──────────────────────────────────────
render_screen()


# ── 启动 ──────────────────────────────────────────────────
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(host='127.0.0.1', port=8080, show=True, reload=False)
