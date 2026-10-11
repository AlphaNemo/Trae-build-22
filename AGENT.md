# AGENT.md

> **给 AI 编码助手（TRAE / Cursor / Claude Code 等）的项目全局规则。**
> 本文件是**全局规则**；四个角色另有专属规则文件（`AGENT_A.md` ~ `AGENT_D.md`，见第 3 节）。
> 优先级：**角色文件 ≈ 本文件 > 通用习惯**；冲突时以更具体的约束为准。每次开始工作前**先读自己的角色文件**，再读本文件与 `TECH_STACK.md`。

---

## 1. 项目速览

- **项目**：Trae-build-22 ｜ AI 无障碍（Accessibility）Web 应用
- **背景**：TRAE on Campus @南方科技大学 · AI Accessibility Hackathon（2026-10-11）
- **交付形态**：**浏览器网页**（`localhost` 投屏演示）
- **硬约束**：**2.5 小时**内做出**能现场演示**的 MVP
- **第一原则**：**能跑通 > 功能多**；**演示效果 > 代码复杂度**

---

## 2. 技术栈（锁定，详见 TECH_STACK.md）

| 层 | 选型 |
|---|---|
| 前端 | **NiceGUI 3.x**（备选 Streamlit） |
| 后端 | **FastAPI** + Uvicorn + Pydantic |
| AI | OpenAI 兼容接口（LLM）+ VLM + ASR；TTS 优先浏览器内置 |
| 版本控制 | Git |

**禁止引入**：LangChain、LangGraph、数据库/ORM、微服务/消息队列、需训练模型的方案、硬件/传感器。
> 若确需新增依赖，**先说明理由并等待确认**，不得擅自引入。

---

## 3. 目录结构、所有权与角色路由

**四角色分工**：A 界面与装配（编码）、B 接口与 AI（编码）、C 需求与路演（非技术）、D 测试与素材（非技术）。完整分工见 `.trae/documents/4人分工优化方案.md`。

| 角色 | 规则文件 | 独占范围 |
|---|---|---|
| A · 界面与装配（编码） | `AGENT_A.md` | `main.py`、`ui/`、代码合并 |
| B · 接口与 AI（编码） | `AGENT_B.md` | `logic/`、`ai/`；`shared/contract.md` 主笔 |
| C · 需求与路演（非技术） | `AGENT_C.md` | 需求文档、prompt 文本、路演稿（不入库） |
| D · 测试与素材（非技术） | `AGENT_D.md` | `shared/mock.md`、测试清单、演示素材 |

```
main.py           # 入口装配（角色 A 独占，其他人不改）
ui/               # 前端界面（角色 A）
logic/            # 业务逻辑与接口（角色 B）
ai/               # AI 调用（角色 B；prompt 文本由角色 C 提供）
docs/             # 需求文档（角色 C，requirements.md 为唯一真相源）
shared/
  contract.md     # 接口契约（角色 B 主笔，冻结后只读）
  mock.md         # 假数据（角色 D 维护）
```

- **一个文件只有一个 owner**。
- **只改我指定的模块**，不得顺手改其他目录。
- 不得修改 `shared/contract.md`（除非主笔人 B 明确要求）。
- C / D 为非技术角色：**在他们的会话中禁止输出代码**，只产出纯文本 / Markdown / JSON 数据。

---

## 4. 工作方式（最重要）

1. **一次只改一个模块**，不要一次性实现多个功能。
2. **输出完整文件**，不要只给片段或 diff 省略。
3. 改动优先**最小补丁**，**禁止重写整个文件**来修一个小问题。
4. **禁止生成伪代码、禁止省略 import、禁止使用未声明的变量**。
5. 代码必须**可直接运行**；涉及 AI/IO 一律用 `async def`。
6. 修改前**先读相关文件和 `shared/contract.md`**。
7. 若我的报错信息不全，**先问我补充完整堆栈**，不要瞎猜。
8. 卡住 **10 分钟**即提醒我广播求助，不要死磕。

---

## 5. 代码规范

**NiceGUI（前端）**
- 用 `ui.xxx` 组件；布局用 `with ui.column()/row()/card():`。
- 浏览器能力用 `ui.run_javascript()`；TTS 用 Web Speech API。
- 事件用 `on_click` / `on_change` / `on_upload`；上传参数为 `e.file`（`await e.file.read()`）。
- 样式用 `.classes()` / `.props()`。

**FastAPI（后端）**
- 入出参用 **Pydantic 模型**定义（即契约）。
- 流式用 `StreamingResponse` + async generator。
- 文件上传需 `python-multipart`。
- 跨域用 `CORSMiddleware`。
- **不在 `async def` 里使用同步 `requests`**。

**通用**
- 面向无障碍：交互要可键盘操作、元素加 `aria-label`、图片给替代文字。
- **API key 只放后端环境变量**，绝不写进前端代码。

---

## 6. 接口契约

- `shared/contract.md` 是**唯一依据**。
- 字段名**大小写敏感**，任何变更必须**同步更新契约并广播**。
- 不要凭空造字段，以契约为准。

---

## 7. Git 提交与合并规范

- 格式：`<模块>: <改动>`，如 `ui: 增加图片上传`、`ai: 接入 VLM 描述`。
- **小步提交**：每次改动可运行后再提交。
- **合并由角色 A（装配者）执行**：每完成一个可运行切片立即合入 main；同文件冲突由 owner 裁决，跨模块冲突由 A **5 分钟内**限时裁决。
- commit 作者邮箱使用 GitHub **noreply** 地址（避免 push 被拒）。

---

## 8. 常用命令

```bash
# 安装（版本锁定，一键完成）
pip install -r requirements.txt

# 运行前端（NiceGUI）
python main.py

# 运行后端（如需独立服务；模块路径以 B 实际文件为准，如 logic/server.py）
uvicorn logic.server:app --reload --port 8000
```

---

## 9. 禁止清单（Do NOT）

- ❌ 引入第 2 节的禁用依赖
- ❌ 一次性实现多个模块 / 大范围重构
- ❌ 为消除报错而删校验、改安全逻辑、注释掉报错代码
- ❌ 写伪代码、省略 import、用未声明变量
- ❌ 把 API key 暴露在前端
- ❌ 改别人负责的目录

---

## 10. 交互约定

- 我给任务时通常带：**目标模块 + 契约 + 报错（如有）**，请据此最小改动。
- 你改完后请**说明「改了哪些文件、为什么」**，方便我核对 diff。
- 遇到需求歧义，**先问再写**，别自行发挥。

---

*本项目规则。与 `TECH_STACK.md` 配套使用；冲突时以两者中更具体的约束为准。*
