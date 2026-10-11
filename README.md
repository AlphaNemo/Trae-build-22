# Trae-build-22 · AI 无障碍助手

> 一支 4 人小队，在 **2.5 小时**内用 AI 与代码，为无障碍（Accessibility）做一点真正有用的东西。

<p>
  <img alt="hackathon" src="https://img.shields.io/badge/Hackathon-TRAE%20on%20Campus-blue">
  <img alt="date" src="https://img.shields.io/badge/Date-2026--10--11-green">
  <img alt="python" src="https://img.shields.io/badge/Python-3.10%2B-yellow">
  <img alt="NiceGUI" src="https://img.shields.io/badge/UI-NiceGUI-orange">
  <img alt="FastAPI" src="https://img.shields.io/badge/API-FastAPI-teal">
</p>

---

## 项目简介

本项目参加 **TRAE on Campus @南方科技大学 · AI Accessibility Hackathon**，
方向为 **AI × 无障碍**：借助 AI（多模态理解、语音交互等），帮助视障 / 听障 / 运动障碍等人群
更独立地完成日常中的一件事。

- **交付形态**：浏览器网页（现场投屏演示）
- **核心约束**：2.5 小时闪电开发，**能跑通 > 功能多**
- **赛题**：活动当天 14:00 **现场发布**，项目将据此最终定题

> 🚧 赛题与最终选题确定后，请在此补充一句话产品描述。

---

## 技术栈

| 层 | 选型 |
|---|---|
| 前端 | **NiceGUI 3.x**（纯 Python Web UI） |
| 后端 | **FastAPI** + Uvicorn + Pydantic |
| AI | LLM（OpenAI 兼容）+ VLM（图像描述）+ ASR（语音识别）|
| 语音播报 | 浏览器内置 Web Speech API |
| 部署 | 本地运行（可选 Vercel / Docker） |

> 完整规范见 [`TECH_STACK.md`](./TECH_STACK.md)。

---

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/AlphaNemo/Trae-build-22.git
cd Trae-build-22

# 2. 安装依赖（建议虚拟环境）
pip install nicegui fastapi "uvicorn[standard]" python-multipart

# 3. 运行
python main.py
```

打开浏览器访问 **http://localhost:8080** 即可。

---

## 目录结构

```
Trae-build-22/
├─ main.py              # 入口（NiceGUI 应用装配）
├─ ui/                  # 前端界面
├─ logic/               # 业务逻辑
├─ ai/                  # AI 调用 / prompt
└─ shared/
   ├─ contract.md       # 接口契约（前后端约定）
   └─ mock.md           # 演示用假数据
```

---

## 项目文档

| 文档 | 说明 |
|---|---|
| [`TECH_STACK.md`](./TECH_STACK.md) | 前后端技术栈规范（唯一真相来源）|
| [`AGENT.md`](./AGENT.md) | 给 AI 编码助手的项目规则 |
| [`shared/contract.md`](./shared/contract.md) | 接口契约 |
| [`shared/mock.md`](./shared/mock.md) | 假数据 |

---

## 团队协作

- **并行开发**：一人一块（`ui` / `logic` / `ai`），一个文件只有一个 owner；合并由装配者（角色 A）顺手完成，不设全职协调岗。
- **接口先行**：定题后 15 分钟内冻结 `shared/contract.md`（B 主笔），再各写各的。
- **非技术成员在关键路径上**：prompt 文案（C）与假数据（D）直接驱动开发，测试走查（D）与路演（C）决定演示质量。
- **结对沟通线**：C↔B 对齐 prompt 与 AI 输出，D↔A 对齐界面走查与 bug 复现；卡住 10 分钟即广播。
- **小步提交**：改动可运行后再提交，格式 `<模块>: <改动>`。
- **降级预案**：AI 接口异常 → 用 `shared/mock.md` 假数据顶；现场演示异常 → 播兜底录屏。

---

## 团队成员

> 分工原则：2 名编码成员负责全部代码；2 名非技术成员承担关键路径上的纯文本/素材工作（prompt 文案、假数据、测试、路演），四人全程满载。详见 `.trae/documents/4人分工优化方案.md`。

| 角色 | 负责范围 | 成员 |
|---|---|---|
| A · 界面与装配（编码） | `main.py` 独占、`ui/` 页面与交互、无障碍属性、浏览器 TTS、代码合并 | _待填_ |
| B · 接口与 AI（编码） | `logic/` 端点与契约实现、`ai/` LLM/VLM/ASR 封装、契约主笔 | _待填_ |
| C · 需求与路演（非技术） | 用户故事与需求文档、prompt 文案设计与迭代、路演稿与彩排主讲、答辩 Q&A | _待填_ |
| D · 测试与素材协调（非技术） | `shared/mock.md` 假数据、全流程测试与无障碍走查、bug 清单、演示素材与兜底录屏、报时 | _待填_ |

---

## 许可

本项目为黑客松参赛作品，仅用于学习与公益演示。
