# 技术栈速查 · AI 无障碍黑客松

> 适用场景：**TRAE on Campus @南方科技大学 · AI Accessibility Hackathon**
> 目标：2.5 小时闪电开发，现场路演 Demo
> 维护方式：开赛前定稿，现场不再讨论选型

---

## 0. 一句话原则

> **闪电赛里，"最快跑通" > "最先进"。技术栈必须在开赛前定好。**

---

## 1. 结论先行：只有两条路值得走

| 路线 | 技术栈 | 适合谁 | 出活速度 |
|---|---|---|---|
| **A. Python 快原型（首选）** | `Streamlit` / `Gradio` + Python | 队里有人会 Python | ⚡⚡⚡ 50 行代码即可起步 |
| **B. JS 好看版** | `Next.js` + `Tailwind` + `shadcn/ui` + `Vercel AI SDK` | 队里有人会前端 | ⚡⚡ 15 分钟起模板，UI 更精致 |
| C. 移动端（慎用） | `Flutter` / `React Native` | 必须真机演示时 | ⚡ 2.5 小时风险高 |

- A 路线：**最快出 AI demo**，一个带文件上传的聊天界面不到 50 行 Python。
- B 路线：2026 黑客松 Web App 默认栈，UI 精致、Vercel 一键部署。
- C 路线：除非必须真机演示，否则不碰。

---

## 2. 通用技术栈分层

| 层 | 常见选项 | 黑客松建议 |
|---|---|---|
| 前端 / UI | Next.js、React、Vue、**Streamlit**、**Gradio** | 快原型用后两者；要好看用 Next.js |
| 后端 / API | **FastAPI**、Flask、Node、Next API Routes | AI 类首选 FastAPI（异步 + 自动文档） |
| 数据库 | Supabase、SQLite、Postgres | 闪电赛**能不用就不用** |
| AI 编排 | LangChain / LlamaIndex / 直接调 API | 短赛**直接调 API**，别上框架 |
| 部署 | **Vercel**、Streamlit Cloud、本地跑 | Vercel 一键部署最省事 |
| 版本控制 | Git | 按目录切分 + 接口契约冻结 |

---

## 3. AI + 无障碍「弹药清单」

### 3.1 通用 AI 能力

- **大模型 LLM API**：Claude / GPT / 国内（通义千问、豆包、DeepSeek、智谱）——看谁的 key 现成
- **多模态视觉 VLM**：图像描述、场景理解 —— 视障辅助的核心
- **语音识别 ASR**：Whisper / 讯飞 / 各云厂商 —— 听障、语音交互的核心
- **语音合成 TTS**：文本转语音播报
- **OCR**：文字识别 ——「拍一下读出来」

### 3.2 无障碍专属技术（可参考的现成产品）

- **读屏**：iOS `VoiceOver` / 安卓 `TalkBack`（系统自带）
- **视觉辅助**：微软 `Seeing AI`、谷歌 `Lookout`、`Be My Eyes`（GPT-4 驱动，发张图即描述）
- **听觉辅助**：`ASR + TTS`、声音事件识别（音频标记）、手语识别/合成

> ⚠️ **手语识别/合成、眼动追踪**虽然酷炫，但 2.5 小时**绝对做不出来**——直接跳过。

---

## 4. 无障碍场景 → 技术映射

| 目标人群 | 典型需求 | 用到的技术 |
|---|---|---|
| **视障** | 识别物体、读文字、听界面 | OCR + VLM 图像描述 + TTS + 语义化标签 |
| **听障** | 实时字幕、声音提醒、交流 | ASR + TTS + 声音事件识别 + 振动反馈 |
| **肢体/运动障碍** | 免手操作 | 语音交互 + 大按钮 + 焦点管理 |
| **老年群体** | 看不清、听不清 | 大字/高对比 UI + 语音播报 |

---

## 5. 默认推荐（直接抄）

```
前端：Streamlit（快） 或 Next.js + Tailwind + shadcn/ui（好看）
AI  ：直接调 LLM API（文本）+ VLM（图像描述）+ ASR（语音）
部署：本地跑 或 Vercel 一键上线
协作：Git（按目录切分 + 契约冻结）
```

- 赛题偏「拍照 → 理解 → 播报」：`Streamlit + VLM + TTS` 是最短路径。
- 赛题偏「实时语音 → 文字」：`网页录音 + ASR API`。

---

## 6. 避坑清单

- ❌ 别现场再选栈 —— **赛前就把环境装好、模板跑通**。
- ❌ 别上 LangChain / 数据库 / 微服务 —— 直接调 API、内存存数据。
- ❌ 别碰训练模型、硬件、传感器。
- ✅ 提前把各家 API 的 **key 和免费额度**备好（账号全登录）。
- ✅ 用 TRAE 生成代码时，**把技术栈写进提示词**（如「用 Python + Streamlit」），否则可能给出一套跑不起来的东西。

---

## 7. 开赛前环境 Checklist

- [ ] 选定路线 A 或 B，并让全员统一
- [ ] 本地跑通一个「Hello World」脚手架（能启动、能预览）
- [ ] 至少 1 个 LLM API key 可用（并有备用）
- [ ] ASR / TTS / VLM 能力至少各验证一个（哪怕用免费额度）
- [ ] Git 配置完成（`user.email` 用 GitHub noreply 邮箱，避免 push 被拒）
- [ ] 统一目录结构：`/ui` `/logic` `/ai` `/shared` + `main`
- [ ] 确定接口契约文件位置与字段规范
