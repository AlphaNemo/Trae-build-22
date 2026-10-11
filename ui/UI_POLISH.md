# UI_POLISH.md — UI 美化速查（NiceGUI）

> 目标：2.5 小时内把界面做**干净好看**。原则：**美化 ≤ 15 分钟**，够用就好，别本末倒置。

---

## 1. 起手式（直接抄，30 秒）

```python
from nicegui import ui

ui.colors(primary='#4F46E5')     # ① 换主色，观感立刻不一样
ui.dark_mode()                   # ② 暗色模式（可选）

# ③ 字体 + 全局留白
ui.add_head_html('''
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>body{font-family:Inter,"Noto Sans SC",sans-serif}</style>
''')
ui.add_css(':root{--nicegui-default-padding:1.25rem;--nicegui-default-gap:1.25rem}')

with ui.card().classes('w-96 p-6 rounded-2xl shadow-lg'):        # ④ 圆角 + 阴影
    ui.label('无障碍助手').classes('text-2xl font-semibold')
    ui.button('开始', icon='mic').props('rounded').classes('w-full')  # ⑤ 图标 + 圆角
```

---

## 2. NiceGUI 的 5 个美化开关

| 手段 | 写法 | 用途 |
|---|---|---|
| 换色 | `ui.colors(primary='#4F46E5')` | 一键换主题色 |
| Tailwind 类 | `.classes('p-4 rounded-xl shadow-md')` | 间距 / 圆角 / 阴影 / 字号 |
| Quasar 属性 | `.props('outline round dense')` | 按钮 / 输入框形态 |
| 自定义 CSS | `.style('...')`、`ui.add_css(...)` | 精细调整 |
| 图标 | `icon='mic'`（Material 内置） | 加图标显精致 |

---

## 3. 设计速成（改这 5 点，颜值翻倍）

1. **配色 ≤ 3 色**：1 主色 + 灰阶，别花花绿绿。
2. **留白**：多用 `p-*` / `gap-*`，宁松勿挤。
3. **圆角 + 轻阴影**：卡片 `rounded-2xl shadow-lg`。
4. **字号层级**：标题 `text-2xl font-semibold`，正文 14–16px。
5. **加图标**：每个按钮 / 标题配一个 `icon`。

**资源**：配色 [Coolors](https://coolors.co) / Tailwind 色板；图标用内置 Material Icons；中文字体 `Noto Sans SC`。

---

## 4. 给 AI 的美化提示词（直接粘）

```
参考 NiceGUI 官方样式文档，美化这个页面：
- 主色 #4F46E5，卡片 rounded-2xl + shadow-lg，整体圆角统一
- 每个按钮/标题加合适 icon，间距用 Tailwind 类
- 保持无障碍：文字对比度达 WCAG AA、可键盘操作、关键元素加 aria-label
只改样式，不改功能逻辑。
```

---

## 5. 时间性价比排序

| 优先级 | 做什么 | 耗时 |
|---|---|---|
| 1 | 换主色 + 圆角 / 阴影 | 1 min |
| 2 | 加图标 + 留白 | 3 min |
| 3 | 统一字体 / 字号层级 | 3 min |
| 4 | 微动效 / 暗色模式 | 有余力再做 |

> ⚠️ **美化总时长别超过 15 分钟**。比赛看的是「能用 + 痛点真」，UI 干净即可。

---

## 6. 顺手切题（无障碍 = 加分）

美化时一并做到，**既好看又得分**：

- 高对比配色（正文对比度 ≥ 4.5:1）
- 支持放大字号
- 全部功能可键盘操作
- 关键元素加 `aria-label`
- 图片配替代文字

---

*配套：`AI_DOCS.md`（文档索引）、`TECH_STACK.md`（选型）。*
