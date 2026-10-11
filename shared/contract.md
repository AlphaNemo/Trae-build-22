# shared/contract.md — 接口契约

> **作用**：定义模块之间的接口，**冻结后各模块并行开发**。
> **状态**：**未启用 · 备选存档**。本题最终按《「药品说明书 · 三行大字卡」完整执行方案》以**纯前端单文件 `index.html`** 交付（零后端、零 AI、零网络，数据源见 `shared/mock.md`）。本契约保留为**可选后端增强**的存档（`uvicorn logic.server:app` 可运行、已测通），前端开发与现场演示**均不依赖**本契约，任何人不得照此给前端接后端。
> **原则**：**先冻结，再开发**；任何人改动都要**在群里广播**。

---

## 1. 使用方式

1. 定题已定：老人拍一下药盒/说明书，页面只显示三行大字——**一次几片、一天几次、饭前还是饭后**。
2. 字段名**大小写敏感**，前后端必须完全一致。
3. 冻结后本文件**只读**；`ui/`、`logic/`、`ai/` 各自照此实现，不互相等待。
4. 接口未实现时，先用 `shared/mock.md` 的假数据顶着。

---

## 2. 通用约定（统一，别各写各的）

| 项 | 约定 |
|---|---|
| 命名风格 | **snake_case**（如 `drug_id`、`speak_text`） |
| 编码 | UTF-8 |
| 时间 | ISO 8601 字符串，如 `2026-10-11T13:00:00+08:00` |
| ID | 字符串 |
| 空值 | `null` |
| 布尔 | `true` / `false` |
| 错误结构 | `{ "error": { "code": "string", "message": "string" } }` |

**AI 相关接口统一形状**（`/scan`、`/med-card` 采用）：

```
输出：{ "result": <结构化用药卡>, "meta": { "source": "ai"|"preset"|"mock", "model": "...", "elapsed_ms": 123 } }
// source=ai 现场VLM生成；source=preset 预置常用药库（离线权威）；source=mock 降级假数据
```

**无后端接口的能力**（前端本地完成，不走 HTTP）：

| 能力 | 实现方式 |
|---|---|
| 「念给我听」 | 浏览器 Web Speech API 朗读 `speak_text` |
| 「发给子女」 | 前端复制/系统分享 `share_text` |

---

## 3. 接口目录

| 接口 | 方法 | 路径 | 负责模块 | 状态 |
|---|---|---|---|---|
| 健康检查 | GET | `/health` | — | ✅ 固定 |
| 常用药目录 | GET | `/medications` | `logic/` | ✅ 必做 |
| 查用药卡 | POST | `/med-card` | `logic/` | ✅ 必做 |
| 拍照识药 | POST | `/scan` | `ai/` | ✅ 必做（必带 mock 降级） |
| 追问对话 | POST | `/chat` | `ai/` | ⬜ 加分（已顺手实现） |
| 语音转文字 | POST | `/transcribe` | `ai/` | ⬜ 加分（已顺手实现） |

---

## 4. 接口定义

### 健康检查

- **方法 / 路径**：`GET /health`
- **输出**

  | 字段 | 类型 | 说明 |
  |---|---|---|
  | `status` | string | 固定 `"ok"` |

### 常用药目录（「选常用药」按钮的数据源）

- **方法 / 路径**：`GET /medications`
- **输出**

  | 字段 | 类型 | 说明 |
  |---|---|---|
  | `medications` | array | 预置常用药列表 |
  | `medications[].id` | string | 药品 ID，供 `/med-card` 查询 |
  | `medications[].name` | string | 大字按钮显示名 |

- **示例**

  ```jsonc
  // Response
  { "medications": [ { "id": "amoxicillin", "name": "阿莫西林" } ] }
  ```

### 查用药卡（选常用药 → 结果页三行大字）

- **方法 / 路径**：`POST /med-card`
- **输入（Request）**

  | 字段 | 类型 | 必填 | 说明 |
  |---|---|---|---|
  | `drug_id` | string | 是 | 来自 `/medications` 的 `id` |

- **输出（Response，AI 统一形状）**：`result` 为用药卡 `MedicationCard`：

  | 字段 | 类型 | 说明 |
  |---|---|---|
  | `drug_name` | string | 药品名 |
  | `per_dose` | string | 大字第 1 行：一次几片，如 `"一次 1 片"` |
  | `daily_times` | string | 大字第 2 行：一天几次，如 `"一天 3 次"` |
  | `meal_timing` | string | 大字第 3 行：饭前还是饭后，如 `"饭后吃"` |
  | `speak_text` | string | 「念给我听」完整朗读文本（含遵医嘱提醒） |
  | `share_text` | string | 「发给子女」分享文本（简短用药卡） |

- **示例**

  ```jsonc
  // Request
  { "drug_id": "amoxicillin" }
  // Response
  {
    "result": {
      "drug_name": "阿莫西林",
      "per_dose": "一次 1 片",
      "daily_times": "一天 3 次",
      "meal_timing": "饭后吃",
      "speak_text": "阿莫西林：一次吃 1 片，一天吃 3 次，饭后吃。请按医生交代吃完疗程。",
      "share_text": "【用药卡】阿莫西林：一次 1 片，一天 3 次，饭后吃。"
    },
    "meta": { "source": "preset" }
  }
  ```

- **错误**：`drug_id` 不存在 → `404 { "error": { "code": "not_found", "message": "..." } }`

### 拍照识药（「拍说明书」→ 结果页三行大字）

- **方法 / 路径**：`POST /scan`
- **输入**：`multipart/form-data`，字段 `file`（药盒/说明书照片）
- **输出**：与 `/med-card` 相同（`result` = `MedicationCard` + `meta`）
- **降级**：AI 失败/未配置/超时 → 返回预置用药卡，`meta.source = "mock"`，**接口永不失败**
- **错误**：未上传文件 → `422 { "error": { "code": "validation_error", ... } }`

### 追问对话（加分：结果页「问一句」）

- **方法 / 路径**：`POST /chat`
- **输入**

  | 字段 | 类型 | 必填 | 说明 |
  |---|---|---|---|
  | `message` | string | 是 | 用户追问文本 |

- **输出**

  | 字段 | 类型 | 说明 |
  |---|---|---|
  | `reply` | string | AI 回复，口语化、适合朗读 |

- **示例**

  ```jsonc
  // Request
  { "message": "饭前忘了吃怎么办？" }
  // Response
  { "reply": "想起来就马上补吃，下一顿照常，千万不要一次吃两片。" }
  ```

### 语音转文字（加分：语音提问前置步骤）

- **方法 / 路径**：`POST /transcribe`
- **输入**：`multipart/form-data`，字段 `file`（录音，webm/wav 等）
- **输出**

  | 字段 | 类型 | 说明 |
  |---|---|---|
  | `text` | string | 转写文本，转发给 `/chat` |

---

## 5. 变更流程

- 谁改契约，谁**立刻在群里广播**，并在此更新。
- 每次修改在文末记一行：`- YYYY-MM-DD 改动说明（谁）`。

---

## 变更记录

- 2026-10-10 建立模板（赛题未知，待定题后填充）
- 2026-10-11 定题「药品说明书三行大字卡」，B 起草定稿草案：新增 `/medications`、`/med-card`、`/scan`，保留 `/chat`、`/transcribe` 为加分项；明确 TTS/分享走前端本地（角色B，待广播冻结）
- 2026-10-11 全队定稿纯前端 index.html 方案，本契约改为「未启用 · 备选存档」，接口定义保留不删，备胎演示用（角色B）
