# TECH_STACK.md — 前后端技术栈规范

> **项目**：Trae-build-22 ｜ TRAE on Campus @南方科技大学 · AI Accessibility Hackathon
> **活动**：2026-10-11（周日）13:00–18:30 ｜ 南科大智华楼 108
> **文档定位**：本项目技术选型的**唯一真相来源（Single Source of Truth）**，供人类与 AI 编码助手共同遵循
> **约束**：2.5 小时闪电开发，现场路演 Demo ｜ 更新：2026-10-10

---

## 0. 给 AI 编码助手的读取说明（Machine Instructions）

- 本文件是技术选型的**唯一依据**。生成代码前必须先读本文件。
- **禁止引入本文件未列出的框架或依赖**；需要新增时先说明理由。
- 生成代码**必须遵守第 6 节的目录结构**与第 9 节的编码规范。
- 接口字段**必须与 `shared/contract.md` 完全一致**（大小写敏感）。
- 一次只改一个模块，输出**完整文件**，可运行优先。
- **禁止生成伪代码、禁止省略 import、禁止使用未声明的变量**。

---

## 1. 技术栈声明（Machine-Readable）

```yaml
project:
  name: Trae-build-22
  repo: https://github.com/AlphaNemo/Trae-build-22
  type: web-app                 # 交付形态：浏览器网页
  runtime: python               # 3.10+
  os_target: windows
  deadline: 2026-10-11T13:00

stack:
  frontend:
    primary: nicegui            # 团队当前使用（见 main.py）；沙箱实测 3.18.0
    alternative: streamlit      # 更快，但 UI 定制弱
    heavy: nextjs               # 仅在有前端人力时
  backend:
    framework: fastapi          # >=0.110（沙箱实测 0.143.0）
    server: uvicorn             # 沙箱实测 0.54.0
    validation: pydantic
  ai_layer:
    llm: openai-compatible-api  # Claude / GPT / 通义 / 豆包 / DeepSeek
    vision: vlm                 # 图像描述
    speech_to_text: asr         # 语音识别
    text_to_speech: tts         # 优先浏览器内置 Web Speech API
  deploy:
    local: true
    option: vercel | streamlit-cloud | docker
  vcs: git

forbidden:                      # 2.5 小时内禁止使用
  - langchain
  - langgraph
  - 数据库 / ORM                 # 内存即可
  - 微服务 / 消息队列
  - 需要训练模型的方案
  - 硬件 / 传感器
```

---

## 2. 路线选择

| 路线 | 前端 | 后端 | 适合 | 风险 |
|---|---|---|---|---|
| **A+（当前默认）** | **NiceGUI** | 内嵌 FastAPI | 要现代 UI 又不想写 JS | 冷门库幻觉风险 ↑（务必锁版本） |
| A | Streamlit | 内嵌 / FastAPI | 最快出活 | UI 定制受限 |
| B | Next.js + Tailwind + shadcn/ui | Next API / FastAPI | 有前端人力、要精致 UI | 依赖/build 弱网翻车 |

**决策规则（AI 可直接套用）**：

```
默认 → A+（NiceGUI，与 main.py 现状一致）
需要极速保底 → A（Streamlit）
有熟练 React 人力且网络稳定 → B
无 API key 或时间 < 1h → 降级为 A + shared/mock.md 假数据
```

---

## 3. 前端技术栈

| 项 | 选型 | 说明 |
|---|---|---|
| 主框架 | **NiceGUI 3.x** | `ui.` 组件 + 事件驱动，UI 现代，纯 Python |
| 备选框架 | Streamlit | `st.` API，50 行起步 |
| 重装框架 | Next.js + Tailwind + shadcn/ui | 仅在有前端人力时 |
| 常用组件 | `ui.label` / `ui.button` / `ui.upload` / `ui.card` | 见 `main.py` |
| 布局 | `with ui.column()/row()/card():` | 缩进即结构 |
| 浏览器能力 | `ui.run_javascript()` + Web Speech API | TTS 朗读零依赖 |
| 样式 | `.classes()` / `.props()`（Tailwind / Quasar） | 精细调整 |

---

## 4. 后端技术栈

| 项 | 选型 | 说明 |
|---|---|---|
| 框架 | **FastAPI** | 原生 async，适合 AI IO |
| 服务器 | **Uvicorn** | `uvicorn app:app --reload` |
| 数据校验 | **Pydantic** | 定义接口契约模型 |
| 流式 | `StreamingResponse` + async generator | 打字机效果 |
| 上传 | `UploadFile`（需 `python-multipart`） | 图片/音频接收 |
| 跨域 | `CORSMiddleware` | 前后端分离必配 |

> 说明：NiceGUI 内置 FastAPI，简单场景逻辑可直接写在 `main.py`；需要独立接口时再拆出 FastAPI 服务。

**标准接口形态**：

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/health` | 存活检查 |
| POST | `/chat` | 一次性返回 |
| POST | `/chat/stream` | 流式返回 |
| POST | `/describe` | 上传图片→AI 描述 |

---

## 5. AI 能力层

### 5.1 LLM（文本）
- 统一走 **OpenAI 兼容接口**（换 `base_url` + `api_key` 即可切换厂商）。
- key 只放**后端环境变量**，绝不进前端。

### 5.2 VLM（图像描述）
- 输入图片 → 输出自然语言描述 → 服务视障用户。

### 5.3 ASR（语音识别）
- 浏览器录音 → 上传 → ASR 接口 → 文本。

### 5.4 TTS（语音合成）——优先级
1. **浏览器内置 Web Speech API**（零依赖、免费）← 首选
2. 云厂商 TTS（音质更好时）

### 5.5 无障碍映射
| 人群 | 组合 |
|---|---|
| 视障 | VLM 图像描述 + OCR + TTS + 语义化标签 |
| 听障 | ASR + TTS + 声音事件识别 |
| 肢体障碍 | 语音交互 + 大按钮 + 焦点管理 |
| 老年 | 大字/高对比 UI + 语音播报 |

---

## 6. 目录结构（与仓库现状对齐）

```
Trae-build-22/
├─ main.py              # 入口装配（角色 A 独占）
├─ ui/                  # 前端界面（角色 A）
├─ logic/               # 业务逻辑（角色 B）
├─ ai/                  # AI 调用（角色 B；prompt 文本由角色 C 提供）
├─ docs/                # 需求文档（角色 C，requirements.md 为唯一真相源）
└─ shared/
   ├─ contract.md       # 接口契约（模板已建，定题后 15 分钟内冻结）
   └─ mock.md           # 假数据（模板已建，定题后由 D 填充）
```

- **一个文件只有一个 owner**；改公共文件前先广播。
- 接口契约**先冻结再开发**。
- 现状（2026-10-11 赛前）：`AGENT.md` + `AGENT_A~D.md` 已完备；`contract.md` / `mock.md` 均为**带填写指引的模板**，待现场定题后分别由 B、D 填充；`ui/`、`logic/`、`ai/`、`docs/` 已预建占位目录。

---

## 7. 接口契约（前后端约定）

写入 `shared/contract.md`：

```jsonc
// POST /chat
// Request
{ "message": "string" }
// Response
{ "reply": "string" }

// POST /chat/stream  →  text/plain（逐字）
// POST /describe
// Request: multipart/form-data, field = file
// Response
{ "filename": "string", "size": 0, "description": "string" }
```

> 字段名**大小写敏感**，任何变更必须同步更新本文件并广播全队。

---

## 8. 依赖与安装

```bash
# 一键安装（版本锁定，弱网加清华镜像）
pip install -r requirements.txt
#   弱网兜底：pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 运行
python main.py                 # NiceGUI（默认 8080 端口；Windows 无 python 命令时用 py main.py）
```

沙箱已验证版本：`nicegui 3.18.0`、`fastapi 0.143.0`、`uvicorn 0.54.0`、`Python 3.12`（赛前本机 Python 3.13 同样实测通过）。
完整版本锁定见根目录 [`requirements.txt`](./requirements.txt)；密钥环境变量见 [`.env.example`](./.env.example)。

---

## 9. 编码规范

**Do**
- ✅ `async def` 处理所有 AI/IO 调用
- ✅ 用 Pydantic 模型定义接口入出参
- ✅ 提交前贴出**完整报错 + 相关文件**
- ✅ 每次改动立即 `git commit`（小步提交）

**Don't**
- ❌ 不写伪代码、不省略 import、不用未声明变量
- ❌ 不为「最小补丁」而重写整个文件
- ❌ 不在 `async def` 里用同步 `requests`
- ❌ 不把 API key 写进前端
- ❌ 不引入 `forbidden` 清单里的依赖

**Git 提交格式**：`<模块>: <改动>`，如 `ui: 增加图片上传`

---

## 10. 开赛前环境 Checklist

- [x] 确认路线 A+（NiceGUI），全员统一
- [x] 本地跑通 `python main.py`（赛前已冒烟：8080 可访问）
- [x] 全部依赖已锁定 `requirements.txt` 并在本机安装验证（弱网用清华镜像）
- [ ] 至少 1 个 LLM API key 可用（含备用），按 `.env.example` 配置环境变量
- [ ] ASR / TTS / VLM 各验证一个（TTS 用浏览器 Web Speech，零成本先验）
- [ ] 其他队员的机器也跑一遍 `pip install -r requirements.txt`（弱网也能装）
- [x] Git 配置完成（`user.email` 用 GitHub noreply，避免 push 被拒）
- [ ] 现场定题后 15 分钟内：B 冻结 `shared/contract.md`，D 同步填 `shared/mock.md`

---

## 附：配套文件

| 文件 | 用途 |
|---|---|
| `main.py` | NiceGUI 入口（可运行 Hello World） |
| `requirements.txt` | 锁定依赖版本，一键安装 |
| `.env.example` | 密钥环境变量占位（复制为 `.env` 使用，禁止入库真实 key） |
| `shared/contract.md` | 接口契约模板（定题后 B 冻结） |
| `shared/mock.md` | 假数据模板（定题后 D 填充） |
| `AI_DOCS.md` | 官方文档索引（NiceGUI / FastAPI 等，防 API 幻觉） |
| `AGENT.md` / `AGENT_A~D.md` | AI 编码助手全局与四角色规则 |

*本文件为技术选型唯一真相来源，代码实现须与此保持一致。*
