# shared/contract.md — 接口契约

> **作用**：定义模块之间的接口与数据形状，**冻结后各模块并行开发**。
> **状态**：**启用**。当前架构为 **NiceGUI 单进程装配**：`main.py` 挂载 `ui/` 页面与 `logic/` 路由（`from logic import api_router`），前后端同进程。
> **原则**：**先冻结，再开发**；任何人改动都要**在群里广播**。

---

## 1. 统一药品形状（全项目唯一药品数据格式）

后端返回、前端渲染、预置数据、AI 识别结果，**一律用下面这个形状**（与 `ui/drug_data.py`、`logic/mock_data.py` 同构，权威数值以 `shared/mock.md` 为准）：

```jsonc
{
  "id": "amoxi",                  // 药品 ID，对应素材图 assets/images/box_<id>.jpg
  "name": "阿莫西林胶囊",          // 药品名
  "lines": {                      // 三行大字
    "dose": "一次 2 粒",           //   第 1 行：一次几片
    "freq": "一天 3 次",           //   第 2 行：一天几次
    "timing": "饭后吃"             //   第 3 行：饭前还是饭后
  },
  "note": "空腹吃伤胃",            // 生活提示，可为 null
  "warning": "青霉素过敏者禁用"     // 高危警示（结果页警示条），可为 null
}
```

- 朗读文本 / 分享文本**不在数据里冗余存储**，由前端按 `lines + warning` 自行拼接（拼接规范见 `shared/mock.md` 第 3 节）。
- 数据三源对齐：`shared/mock.md`（权威）＝ `logic/mock_data.py`（后端）＝ `ui/drug_data.py`（前端离线副本）。改数据先改 mock.md 再同步两份代码；`py test_ai.py --data` 一键自检。

## 2. 通用约定

| 项 | 约定 |
|---|---|
| 命名风格 | **snake_case**（如 `drug_id`、`elapsed_ms`） |
| 编码 | UTF-8 |
| ID | 字符串 |
| 空值 | `null` |
| 错误结构 | `{ "error": { "code": "string", "message": "string" } }` |
| AI 结果包装 | `{ "result": <统一药品卡>, "meta": { "source": "ai"\|"preset"\|"mock", "model": "...", "elapsed_ms": 123 } }` |

**前端本地能力**（不走 HTTP，无后端依赖）：

| 能力 | 实现方式 |
|---|---|
| 「念给我听」 | 浏览器 Web Speech API 朗读（前端自拼文本） |
| 「发给子女」 | 前端复制 / 系统分享（前端自拼文本） |

## 3. 进程内直调约定（NiceGUI ↔ logic 无缝衔接）

前后端同进程，`ui/pages.py` 允许直接 import `logic/` 的服务函数，**与 HTTP 接口同形状**：

```python
from logic import scan_service, mock_data

drug = await scan_service.scan_drug(image_bytes, filename)   # AI 拍照识别 → 统一药品卡 | None
card = mock_data.get_med_card("amoxi")                        # 预置卡查询 → 统一药品卡 | None
meds = mock_data.list_medications()                           # 目录 → [{id, name}]
```

- `scan_drug` 返回 `None` = 未配 key / 超时 / 拍不清 / 非预置药，**前端必须回退** `ui/drug_data.py` 预置流程（静默降级，不许报错打断演示）。
- 进程内函数与 HTTP 接口的数据形状由本契约保证一致；改任何一侧都要对照第 1 节。

## 4. 接口目录与定义

| 接口 | 方法 | 路径 | 负责模块 | 状态 |
|---|---|---|---|---|
| 健康检查 | GET | `/health` | — | ✅ 固定 |
| 常用药目录 | GET | `/medications` | `logic/` | ✅ 必做 |
| 查用药卡 | POST | `/med-card` | `logic/` | ✅ 必做 |
| 拍照识药 | POST | `/scan` | `ai/`+`logic/` | ✅ 必做（必带 mock 降级） |
| 追问对话 | POST | `/chat` | `ai/` | ⬜ 加分（已实现） |
| 语音转文字 | POST | `/transcribe` | `ai/` | ⬜ 加分（已实现） |

### GET /health

```jsonc
// Response
{ "status": "ok" }
```

### GET /medications

```jsonc
// Response
{ "medications": [ { "id": "amoxi", "name": "阿莫西林胶囊" } ] }
```

### POST /med-card（选常用药 → 结果页）

```jsonc
// Request
{ "drug_id": "amoxi" }
// Response —— result 即第 1 节统一药品卡
{
  "result": {
    "id": "amoxi", "name": "阿莫西林胶囊",
    "lines": { "dose": "一次 2 粒", "freq": "一天 3 次", "timing": "饭前饭后都可以，间隔 8 小时" },
    "note": null, "warning": "青霉素过敏者禁用"
  },
  "meta": { "source": "preset" }
}
```

- **错误**：`drug_id` 不存在 → `404 { "error": { "code": "not_found", "message": "..." } }`

### POST /scan（拍说明书 → 结果页）

- **输入**：`multipart/form-data`，字段 `file`（图片文件）
- **Response**：同 `/med-card`；`meta.source` 取值 `ai`（VLM 现场识别，三行来自 AI、`id/name/note/warning` 来自预置卡）或 `mock`（降级，随机预置卡）
- **降级链**（`logic/scan_service.py`）：AI 失败 / JSON 解析失败 / 三行含「看不清」/ 药名匹配不到预置药 → 返回 `None` → 接口侧随机预置卡兜底，**接口永不失败**

### POST /chat（追问，加分项）

```jsonc
// Request          // Response
{ "message": "..." } { "reply": "..." }
```

### POST /transcribe（语音提问，加分项）

- **输入**：`multipart/form-data`，字段 `file`（音频）
- **Response**：`{ "text": "这个药饭前吃还是饭后吃？" }`

---

## 变更记录

- 2026-10-10 建立模板（赛题未知，待定题后填充）
- 2026-10-11 定题「药品说明书三行大字卡」，B 起草定稿草案：新增 `/medications`、`/med-card`、`/scan`，保留 `/chat`、`/transcribe` 为加分项；明确 TTS/分享走前端本地（角色B，待广播冻结）
- 2026-10-11 全队定稿纯前端 index.html 方案，本契约改为「未启用 · 备选存档」，接口定义保留不删，备胎演示用（角色B）
- 2026-10-11 下午 示例 id 与用药卡数据对齐权威数据源 shared/mock.md（amoxi 等短 id），与 logic/mock_data.py、素材药盒图一致（角色 D，请在群里广播）
- 2026-10-11 晚 **架构回切 NiceGUI + 后端同进程**，契约重新启用并改为「统一药品形状」：废止 drug_name/per_dose/... 旧卡形状与 speak_text/share_text 冗余字段，全部数据（预置/AI/HTTP/进程内）统一为 `{id,name,lines{dose,freq,timing},note,warning}`；新增进程内直调约定（scan_service/mock_data）；移除 bridge 适配层（角色B，需广播）
