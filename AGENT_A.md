# AGENT_A.md — 角色 A · 界面与装配

> **本文件写给 AI 编码助手。** 与你结对的人类是黑客松团队的**角色 A**，负责全部前端页面与最终装配。
> 先读本文件，再读根目录 `AGENT.md`（全局规则）与 `shared/contract.md`（接口契约）。

---

## 1. 项目背景

- **项目**：AI 无障碍 Web 应用，黑客松现场 **2.5 小时**交付，浏览器 localhost 投屏演示
- **技术栈**：NiceGUI 3.x + FastAPI（内嵌）+ OpenAI 兼容 LLM/VLM/ASR + 浏览器 Web Speech API（TTS）
- **第一原则**：能跑通 > 功能多；演示效果 > 代码复杂度

## 2. 你的人类伙伴

- 有 Python 基础，但 **NiceGUI 经验有限**
- 写 NiceGUI 时以本地文档 `site-packages/nicegui/llms.md` 或 https://nicegui.io/llms.txt 为准，**禁止凭记忆猜 API**

## 3. 权限边界

| 范围 | 权限 |
|---|---|
| `main.py`、`ui/` | **独占**，只改这两个范围；你也只许输出这两个范围的代码 |
| `shared/contract.md` | 冻结后只读，不得修改 |
| `logic/`、`ai/` | 角色 B 的地盘，**禁止触碰** |

- 接口字段以 `shared/contract.md` 为准；接口未通时先用 `shared/mock.md` 的假数据渲染页面

## 4. 硬性规则

1. **一切皆 Python**：优先 `ui.*` 组件，禁止写 CSS / Quasar / JS（Web Speech 朗读除外，用 `ui.run_javascript` 实现）
2. **无虚拟 DOM**：禁止删除重建元素，用 `.set_text()` / `bind_*` 原地更新；整块刷新用 `@ui.refreshable`
3. **无障碍是评分点**：交互元素加 `aria-label`、全流程键盘可操作、焦点顺序合理、大按钮高对比
4. 涉及 AI/IO 一律 `async def`；输出**完整文件**，不写伪代码、不省略 import、不用未声明变量
5. 一次只改一个功能；最小补丁，禁止为修小问题重写整个文件
6. API key 绝不写进前端

## 5. 协作接口

- 结对伙伴是**角色 D（测试）**：他提交带复现步骤的 bug 报告给你的人类，修完由他复测
- 卡住 **10 分钟**就提醒他广播求助；改 `main.py` 前先提醒他口头通知全队

## 6. 工作方式

- 他每次提问会告诉你当前阶段（P0 定题 / P1 开发 / P2 收尾）与具体目标，你据此给**最小可运行实现**
- 改完后说明「改了哪些文件、为什么」，方便他核对 diff
