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

- **并行开发**：一人一块（`ui` / `logic` / `ai`），一个文件只有一个 owner。
- **接口先行**：先冻结 `shared/contract.md`，再各写各的。
- **小步提交**：改动可运行后再提交，格式 `<模块>: <改动>`。

---

## 团队成员

| 角色 | 成员 |
|---|---|
| 产品 / 队长 | _待填_ |
| 前端（UI） | _待填_ |
| 后端 / 业务 | _待填_ |
| AI / 演示 | _待填_ |

---

## 许可

本项目为黑客松参赛作品，仅用于学习与公益演示。
