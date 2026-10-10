# AI_DOCS.md

> 给 AI 编码助手的文档索引。写代码前按优先级查阅官方文档，
> **优先照文档写，不要凭记忆猜 API**。

---

## P0 · NiceGUI（前端主选）

- 本地（版本匹配，首选）：`site-packages/nicegui/llms.md`
- 在线：https://nicegui.io/llms.txt
- 任意页面加请求头 `Accept: text/markdown` → 返回 Markdown
- **铁律**：
  1. 一切皆 Python：优先 `ui.*`，别写 CSS / Quasar / JS。
  2. 无虚拟 DOM：勿删除重建元素（丢状态），用 `.set_text()` / `bind_*` 原地更新；整块刷新用 `@ui.refreshable`。
  3. 模块级变量全局共享：多用户状态用 `@ui.page` / `app.storage`。

---

## P1 · FastAPI（后端）

- 文档：https://fastapi.tiangolo.com/
- 机器入口：运行时 `/openapi.json`、交互文档 `/docs`
- 约束：`async def`；入出参用 Pydantic 模型；流式用 `StreamingResponse`。

## P1 · Pydantic（数据校验）

- 文档：https://docs.pydantic.dev/llms.txt

---

## P2 · Uvicorn（服务器）

- 文档：https://www.uvicorn.org/
- 运行：`uvicorn module:app --reload`

---

## P3 · 备选路线（仅在切换时查）

| 框架 | 文档 |
|---|---|
| Streamlit | https://docs.streamlit.io/llms.txt |
| Reflex | https://reflex.dev/llms.txt |
| Next.js | https://nextjs.org/docs/llms.txt |
| shadcn/ui | https://ui.shadcn.com/llms.txt |
| Tailwind CSS | https://tailwindcss.com/docs |
| Vercel AI SDK | https://ai-sdk.dev/docs |

---

## 使用规则

1. 按当前模块选对应文档，**只读相关页面**；超上下文就分段喂。
2. 不确定的 API **先查文档再写**，禁止臆造。
3. 本地已有 `llms.md` 时优先用它（版本一致）。
