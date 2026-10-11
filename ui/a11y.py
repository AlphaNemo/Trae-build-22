"""
无障碍组件库 —— 毛玻璃暖色调 · 大字大按钮
设计基调：
  - 背景：米白渐变 + 3 个模糊 blob 光斑
  - 卡片：半透明白 + backdrop-filter blur(22px) saturate(1.8) + 1px 白边
  - 主色 #2E7D6B 青绿 · 警示红 #D93025
  - 核心行字号 52px 起，全程高对比，焦点可见
  - 手机壳 390×844 居中
"""

from nicegui import ui


# ── CSS 变量：暖色调 token（毛玻璃卡片从这些派生） ────────────
THEME_CSS = """
:root {
    /* 米白渐变背景色 */
    --bg-gradient-1: #FFF8F0;
    --bg-gradient-2: #F4EBE0;
    --bg-gradient-3: #EADDC8;
    /* 毛玻璃卡片 —— 半透明白 */
    --glass-bg: rgba(255, 255, 255, 0.55);
    --glass-bg-strong: rgba(255, 255, 255, 0.72);
    --glass-bg-alt: rgba(250, 243, 231, 0.65);
    --glass-border: rgba(255, 255, 255, 0.6);
    --glass-blur: 22px;
    /* 文字：深字，高对比 */
    --text-primary: #1A1A1A;
    --text-secondary: #4A4A4A;
    --text-muted: #7A7A7A;
    /* 主题色 */
    --accent: #2E7D6B;
    --accent-hover: #236656;
    --accent-glow: rgba(46, 125, 107, 0.35);
    /* 警示红 */
    --danger: #D93025;
    --danger-bg: rgba(217, 48, 37, 0.08);
    /* 边框 / 分隔 */
    --border: rgba(46, 125, 107, 0.15);
    /* 阴影 */
    --shadow-card: 0 8px 32px rgba(26, 26, 26, 0.08);
    --shadow-strong: 0 12px 48px rgba(26, 26, 26, 0.14);
    --shadow-btn: 0 2px 8px rgba(26, 26, 26, 0.1);
    /* 焦点 */
    --focus-ring: #2E7D6B;
    /* blob 光斑颜色 */
    --blob-1: rgba(46, 125, 107, 0.35);
    --blob-2: rgba(139, 92, 246, 0.25);
    --blob-3: rgba(236, 72, 153, 0.18);
}
"""


def setup_theme():
    """
    毛玻璃暖色调主题。必须在创建任何组件前调用。
    加 backdrop-filter + -webkit- 前缀，留纯色 fallback。
    """
    ui.colors(primary='#2E7D6B')

    ui.add_head_html(f'''
    <style>
      {THEME_CSS}

      /* ── 全局基础样式 ── */
      html, body {{
          margin: 0; padding: 0; min-height: 100vh;
          font-family: system-ui, -apple-system, "PingFang SC",
                       "Microsoft YaHei", "Noto Sans CJK SC", sans-serif !important;
          background: linear-gradient(135deg, var(--bg-gradient-1) 0%,
                                                var(--bg-gradient-2) 50%,
                                                var(--bg-gradient-3) 100%) !important;
          color: var(--text-primary) !important;
          line-height: 1.6;
          -webkit-font-smoothing: antialiased;
          background-attachment: fixed;
          overflow-x: hidden;
      }}
      body.q-body--dark {{
          background: linear-gradient(135deg, var(--bg-gradient-1) 0%,
                                              var(--bg-gradient-2) 50%,
                                              var(--bg-gradient-3) 100%) !important;
      }}

      /* ── blob 光斑（body 伪元素 + 3 个额外 div） ── */
      body::before {{
          content: "";
          position: fixed;
          top: -120px; left: -120px;
          width: 420px; height: 420px;
          border-radius: 50%;
          background: var(--blob-1);
          filter: blur(100px);
          z-index: 0;
          pointer-events: none;
      }}
      body::after {{
          content: "";
          position: fixed;
          bottom: -100px; right: -100px;
          width: 380px; height: 380px;
          border-radius: 50%;
          background: var(--blob-2);
          filter: blur(100px);
          z-index: 0;
          pointer-events: none;
      }}
      .bg-blob-3 {{
          position: fixed;
          top: 40%; left: 60%;
          width: 300px; height: 300px;
          border-radius: 50%;
          background: var(--blob-3);
          filter: blur(90px);
          z-index: 0;
          pointer-events: none;
      }}

      /* ── 手机壳容器（自适应宽度，移动端全屏，桌面 480px 上限） ── */
      .phone-shell {{
          width: 100%;
          max-width: 480px;
          margin: 0 auto;
          min-height: 100vh;
          background: var(--glass-bg);
          -webkit-backdrop-filter: blur(28px) saturate(1.8);
          backdrop-filter: blur(28px) saturate(1.8);
          border: none;
          border-radius: 0;
          box-shadow: none;
          overflow: hidden;
          position: relative;
          z-index: 1;
      }}
      /* 桌面端给手机壳加圆角 + 阴影（恢复"手机"观感） */
      @media (min-width: 520px) {{
          .phone-shell {{
              border: 1px solid var(--glass-border);
              border-radius: 32px;
              box-shadow: var(--shadow-strong);
              margin: 24px auto;
              min-height: 844px;
          }}
      }}

      /* ── 毛玻璃卡片 ── */
      .a11y-card {{
          background: var(--glass-bg);
          -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.8);
          backdrop-filter: blur(var(--glass-blur)) saturate(1.8);
          border-radius: 20px;
          border: 1px solid var(--glass-border);
          box-shadow: var(--shadow-card);
          padding: 20px;
      }}
      .a11y-card-warm {{
          background: var(--glass-bg-alt);
          -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.8);
          backdrop-filter: blur(var(--glass-blur)) saturate(1.8);
          border-radius: 20px;
          border: 1px solid var(--glass-border);
          padding: 20px;
      }}

      /* ── 大按钮（96px+ 高，手机全宽） ── */
      .a11y-btn {{
          background: var(--accent) !important;
          color: #FFFFFF !important;
          border: none !important;
          border-radius: 18px !important;
          min-height: 96px !important;
          font-size: 20px !important;
          font-weight: 600 !important;
          padding: 0 28px !important;
          box-shadow: 0 4px 20px var(--accent-glow) !important;
          transition: transform 0.15s ease, background 0.2s ease !important;
          width: 100%;
      }}
      .a11y-btn:hover {{
          background: var(--accent-hover) !important;
          transform: scale(0.98);
      }}
      .a11y-btn-secondary {{
          background: var(--glass-bg-strong) !important;
          -webkit-backdrop-filter: blur(12px) saturate(1.8);
          backdrop-filter: blur(12px) saturate(1.8);
          color: var(--text-primary) !important;
          border: 1px solid var(--glass-border) !important;
          box-shadow: var(--shadow-btn) !important;
      }}
      .a11y-btn-secondary:hover {{
          background: var(--glass-bg) !important;
          color: var(--accent) !important;
      }}
      .a11y-btn-danger {{
          background: var(--danger) !important;
          color: #FFFFFF !important;
          border: none !important;
      }}
      .a11y-btn-danger:hover {{
          filter: brightness(0.95);
      }}
      .a11y-btn-tiny {{
          min-height: 56px !important;
          font-size: 18px !important;
          width: auto;
          padding: 0 20px !important;
          background: var(--glass-bg-strong) !important;
          -webkit-backdrop-filter: blur(12px);
          backdrop-filter: blur(12px);
          color: var(--text-primary) !important;
          border: 1px solid var(--glass-border) !important;
          border-radius: 14px !important;
      }}
      .a11y-btn-tiny:hover {{
          background: var(--glass-bg) !important;
          color: var(--accent) !important;
      }}

      /* ── 三行大字卡（结果页核心） ── */
      .drug-name {{
          font-size: 36px !important;
          font-weight: 700 !important;
          color: var(--text-primary) !important;
          text-align: center;
          margin-bottom: 16px;
      }}
      .drug-line {{
          font-size: 52px !important;
          font-weight: 700 !important;
          color: var(--text-primary) !important;
          line-height: 1.3;
          text-align: left;
          padding: 8px 0;
      }}
      .drug-line-label {{
          font-size: 24px !important;
          font-weight: 500 !important;
          color: var(--text-muted) !important;
          display: block;
          margin-bottom: 4px;
      }}
      .drug-note {{
          font-size: 18px !important;
          color: var(--text-secondary) !important;
          text-align: center;
          padding: 8px 16px;
          background: var(--glass-bg-alt);
          -webkit-backdrop-filter: blur(12px);
          backdrop-filter: blur(12px);
          border-radius: 12px;
          border: 1px solid var(--glass-border);
      }}
      .drug-warning {{
          background: var(--danger-bg) !important;
          -webkit-backdrop-filter: blur(12px);
          backdrop-filter: blur(12px);
          border-left: 6px solid var(--danger) !important;
          border-radius: 12px !important;
          padding: 16px 20px !important;
          margin-top: 16px !important;
          font-size: 22px !important;
          font-weight: 600 !important;
          color: var(--danger) !important;
      }}

      /* ── 警示条 ── */
      .warning-bar {{
          background: var(--danger-bg);
          -webkit-backdrop-filter: blur(12px);
          backdrop-filter: blur(12px);
          border: 2px solid var(--danger);
          border-radius: 14px;
          padding: 14px 20px;
          margin-top: 16px;
          font-size: 20px;
          font-weight: 600;
          color: var(--danger);
          text-align: center;
      }}

      /* ── 扫描动画 ── */
      .scan-frame {{
          width: 100%;
          aspect-ratio: 3/4;
          background: var(--glass-bg);
          -webkit-backdrop-filter: blur(16px);
          backdrop-filter: blur(16px);
          border: 2px solid var(--glass-border);
          border-radius: 20px;
          position: relative;
          overflow: hidden;
      }}
      .scan-frame img {{
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
      }}
      .scan-line {{
          position: absolute;
          left: 0; right: 0;
          height: 4px;
          background: linear-gradient(90deg, transparent, #2E7D6B, transparent);
          animation: scanMove 1.2s ease-in-out infinite;
          box-shadow: 0 0 12px rgba(46, 125, 107, 0.7);
          z-index: 2;
      }}
      @keyframes scanMove {{
          0% {{ top: 10%; }}
          50% {{ top: 90%; }}
          100% {{ top: 10%; }}
      }}

      /* ── 药盒列表 ── */
      .box-item {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 16px 20px;
          background: var(--glass-bg);
          -webkit-backdrop-filter: blur(16px) saturate(1.8);
          backdrop-filter: blur(16px) saturate(1.8);
          border: 1px solid var(--glass-border);
          border-radius: 14px;
          margin-bottom: 12px;
          cursor: pointer;
          transition: transform 0.12s ease, background 0.2s ease;
      }}
      .box-item:hover {{
          background: var(--glass-bg-strong);
          transform: scale(0.99);
      }}

      /* ── 通用 ── */
      .q-btn {{
          color: var(--text-primary) !important;
      }}
      .nicegui-content {{ z-index: 1; position: relative; }}

      /* ── 焦点可见（无障碍核心） ── */
      .q-btn:focus-visible, .q-field:focus-visible {{
          outline: 4px solid var(--focus-ring) !important;
          outline-offset: 2px !important;
      }}
      .q-switch:focus-visible {{
          outline: 3px solid var(--focus-ring) !important;
          outline-offset: 2px !important;
          border-radius: 20px;
      }}

      /* ── 滚动条 ── */
      ::-webkit-scrollbar {{ width: 8px; }}
      ::-webkit-scrollbar-track {{ background: transparent; }}
      ::-webkit-scrollbar-thumb {{
          background: var(--border);
          border-radius: 4px;
      }}
      ::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}

      /* ── 大字号模式 ── */
      body.large-font {{
          font-size: 110% !important;
      }}
      body.large-font .drug-line {{ font-size: clamp(2.5rem, 9vw, 4rem) !important; }}
      body.large-font .drug-name {{ font-size: clamp(1.75rem, 6vw, 3rem) !important; }}
      body.large-font .a11y-btn {{ font-size: clamp(1.25rem, 5vw, 2rem) !important; }}
      body.large-font .drug-warning {{ font-size: clamp(1.25rem, 4vw, 1.75rem) !important; }}
      body.large-font .drug-note {{ font-size: clamp(1rem, 3vw, 1.375rem) !important; }}
      body.large-font .q-btn:focus-visible,
      body.large-font .q-field:focus-visible {{
          outline: 4px solid #2E7D6B !important;
          outline-offset: 3px !important;
      }}

      /* ── 返回按钮 ── */
      .back-btn {{
          font-size: 18px !important;
          color: var(--text-secondary) !important;
          background: var(--glass-bg-strong) !important;
          -webkit-backdrop-filter: blur(12px);
          backdrop-filter: blur(12px);
          border: 1px solid var(--glass-border) !important;
          min-height: 44px !important;
          border-radius: 12px !important;
          padding: 0 14px !important;
      }}
      .back-btn:hover {{ color: var(--accent) !important; }}

      /* ── 上传组件（毛玻璃） ── */
      .q-uploader {{
          background: var(--glass-bg-alt) !important;
          -webkit-backdrop-filter: blur(16px);
          backdrop-filter: blur(16px);
          border-radius: 16px !important;
          border: 2px dashed var(--border) !important;
      }}
    </style>
    ''')

    # 第 3 个 blob（因为 ::before/::after 被占了）
    ui.add_head_html('''
    <div class="bg-blob-3" aria-hidden="true"></div>
    ''')


# ── 无障碍辅助：大字号切换 ─────────────────────────────────

def toggle_large_font(enable: bool):
    """大字号模式 —— body class 切换 + localStorage 持久化"""
    action = "add" if enable else "remove"
    js = f'''
    (function(){{
        document.body.classList.{action}("large-font");
        localStorage.setItem("app-large-font", {"true" if enable else "false"});
    }})();
    '''
    ui.run_javascript(js)


def init_a11y_state():
    """初始化时恢复 localStorage 中的大字号偏好（必须在 setup_theme 之后、组件创建前调用）"""
    ui.add_head_html('''
    <script>
    (function(){
        var bigFont = localStorage.getItem("app-large-font");
        if (bigFont === "true") document.body.classList.add("large-font");
    })();
    </script>
    ''')


# ── 组件库（保持旧函数签名，内部换暖色调样式类） ──────────

def a11y_card(title: str = None, aria_label: str = None,
              warm: bool = False, **kwargs):
    """无障碍卡片 —— 暖色调白底"""
    label = aria_label or title or ''
    classes = 'a11y-card-warm' if warm else 'a11y-card'
    c = ui.card(**kwargs).classes(classes)
    if label:
        c.props(f'aria-label="{label}" role=region')
    return c


def a11y_button(text: str, on_click=None, icon: str = None,
                variant: str = 'primary', aria_label: str = None,
                full_width: bool = True, **kwargs):
    """无障碍大按钮
    variant: primary / secondary / danger / tiny
    """
    label = aria_label or text
    vclass = {
        'primary': 'a11y-btn',
        'secondary': 'a11y-btn a11y-btn-secondary',
        'danger': 'a11y-btn a11y-btn-danger',
        'tiny': 'a11y-btn-tiny',
    }.get(variant, 'a11y-btn')

    btn = ui.button(text, on_click=on_click, icon=icon, **kwargs)
    btn.props(f'aria-label="{label}" rounded')
    btn.classes(vclass)
    if full_width and variant != 'tiny':
        btn.style('width: 100%')
    return btn


def a11y_label(text: str, aria_label: str = None, big: bool = False,
               color: str = None, **kwargs):
    """无障碍文字标签"""
    label = aria_label or text
    l = ui.label(text, **kwargs)
    l.props(f'aria-label="{label}" role=text')
    style = ''
    if color:
        style += f'color: {color} !important; '
    if big:
        l.classes('text-xl font-semibold')
    if style:
        l.style(style)
    return l


def a11y_switch(label: str, on_change=None, aria_label: str = None, **kwargs):
    """无障碍开关"""
    a_label = aria_label or label
    sw = ui.switch(label, on_change=on_change, **kwargs)
    sw.props(f'aria-label="{a_label}" color="primary"')
    return sw


# ── 兼容旧 API 别名 ──────────────────────────────────────

def setup_glass_theme(primary: str = '#2E7D6B'):
    """兼容旧 main.py 调用的别名 —— 实际调用 setup_theme"""
    setup_theme()


def toggle_theme():
    """兼容旧代码：本项目只有一个暖色调主题，空实现"""
    pass


def apply_theme(theme: str):
    """兼容旧代码：本项目只有一个暖色调主题，空实现"""
    pass


def a11y_glass_card(title=None, aria_label=None, strong=False, **kwargs):
    return a11y_card(title=title, aria_label=aria_label,
                     warm=not strong, **kwargs)


def a11y_glass_button(text, on_click=None, icon=None, large=True, **kwargs):
    return a11y_button(text, on_click=on_click, icon=icon, **kwargs)


def a11y_glass_upload(label, accept='image/*', on_upload=None, **kwargs):
    """上传组件（本项目不常用，提供兼容）"""
    u = ui.upload(label=label, on_upload=on_upload,
                  multiple=False, **kwargs)
    u.props(f'aria-label="{label}" size=lg rounded accept="{accept}"')
    u.classes('a11y-card p-4')
    return u
