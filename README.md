# 药品说明书「三行大字卡」 · Trae-build-22

> **让老人拍一下药盒/说明书，就知道这药怎么吃。**
> 我们不是药品管理 App——老人不是忘了吃药，是**看不清、看不懂**说明书。
> 我们只回答三个问题：**一次吃几片？一天吃几次？饭前还是饭后？**

<p>
  <img alt="hackathon" src="https://img.shields.io/badge/TRAE_on_Campus-南方科技大学·AI无障碍黑客松-blue">
  <img alt="date" src="https://img.shields.io/badge/Date-2026--10--11-green">
  <img alt="python" src="https://img.shields.io/badge/Python-3.10%2B-yellow">
  <img alt="NiceGUI" src="https://img.shields.io/badge/UI-NiceGUI%203.x-orange">
  <img alt="FastAPI" src="https://img.shields.io/badge/API-FastAPI-teal">
</p>

---

## 它解决什么问题

阿莫西林说明书有 4000 字，老年人要的只有三行。本项目面向**老年人、低视力、认知障碍、术后患者**：

1. **拍一下**——拍药盒或说明书照片，VLM 识别药品并提取用法用量
2. **只看三行**——结果页只显示「一次几片 / 一天几次 / 饭前饭后」三行大字 + 高危警示条
3. **念给我听**——浏览器语音朗读，不识字也能用
4. **发给子女**——一键生成用药卡文本转发家人

**准确性优先**：照片上看不清的绝不编造，识别不出就回退到 8 种常用药的权威预置数据，演示永不中断。

## 快速开始

```bash
git clone https://github.com/AlphaNemo/Trae-build-22.git
cd Trae-build-22
pip install -r requirements.txt        # 弱网可加 -i https://pypi.tuna.tsinghua.edu.cn/simple
copy .env.example .env                  # 填入 API key（.env 不入库）
py main.py                              # Windows；macOS/Linux 用 python main.py
```

打开 **http://localhost:8080**：首页「拍说明书 / 选常用药 / 给家人看」→ 拍照上传 → 三行大字卡。

- **演示素材**：`assets/images/drug_*.jpg`（说明书图，出真 AI 三行）、`box_*.jpg`（盒面图，识别药名+权威用法）、`fruit_bowl.jpg` 等干扰图（自动回退预置）
- **未配置 key 也能跑**：全流程预置数据兜底，离线可演示

## 技术架构

| 层 | 选型 |
|---|---|
| 前端 | **NiceGUI 3.x**（5 屏状态机：首页 → 拍照 → 结果 → 药盒 / 分享） |
| 后端 | **FastAPI** + Uvicorn + Pydantic（与 NiceGUI 同进程装配，见 `main.py`） |
| AI | OpenAI 兼容 VLM（拍照识药）+ LLM（追问）+ DashScope ASR（语音，加分项） |
| 语音播报 | 浏览器 Web Speech API（前端本地，零后端依赖） |

**统一药品形状**（前后端同构，契约见 [`shared/contract.md`](./shared/contract.md)）：

```jsonc
{ "id": "amoxi", "name": "阿莫西林胶囊",
  "lines": { "dose": "一次 2 粒", "freq": "一天 3 次", "timing": "饭后吃" },
  "note": null, "warning": "青霉素过敏者禁用" }
```

**识别降级链**（`logic/scan_service.py`）：AI 调用失败 / JSON 解析失败 / 药名匹配不到预置药 → 返回 `None` → 前端静默回退预置演示数据；三行含「看不清」→ 逐行用预置权威值补全。**接口永不失败**。

## 目录结构

```
Trae-build-22/
├─ main.py              # 入口（角色 A 独占：NiceGUI 装配 + logic 路由挂载）
├─ ui/                  # 5 屏界面、无障碍样式、TTS、本地药品数据副本（A）
├─ logic/               # 接口/契约实现、预置数据、scan_service 识别降级（B）
├─ ai/                  # VLM/LLM/ASR 封装、.env 配置、prompt 文本（B；prompt 归 C）
├─ assets/images/       # 演示素材：药盒图 / 说明书图 / 干扰图（D）
├─ docs/                # 需求文档（C，requirements.md 为唯一真相源）
├─ shared/
│  ├─ contract.md       # 接口契约：统一药品形状 + 进程内直调约定（B 主笔）
│  └─ mock.md           # 8 种常用药权威数据（D 维护）
├─ test_ai.py           # AI 冒烟（py test_ai.py）+ 数据一致性自检（py test_ai.py --data）
├─ requirements.txt     # 依赖版本锁定
└─ .env.example         # 密钥环境变量占位（真实 .env 禁止入库）
```

## 数据与测试

- **数据权威源**：[`shared/mock.md`](./shared/mock.md)（8 种常用药：阿莫西林、头孢克肟、二甲双胍、布洛芬、硝苯地平、感冒灵、他汀、氨氯地平）＝ `logic/mock_data.py` ＝ `ui/drug_data.py` 三副本逐字一致
- **改数据先改 mock.md**，再同步两份代码；`py test_ai.py --data` 秒级自检，不一致即退出码 1
- **AI 冒烟**：`py test_ai.py` 验证 chat/scan/transcribe 配置与连通性
- 已完成 17 张素材图全量回归：8 盒面 + 3 说明书全识别正确，6 张干扰图零误报

## 项目文档

| 文档 | 说明 |
|---|---|
| [`shared/contract.md`](./shared/contract.md) | 接口契约（统一药品形状、降级链、进程内直调） |
| [`shared/mock.md`](./shared/mock.md) | 药品权威数据与 TTS/分享文本拼接规范 |
| [`TECH_STACK.md`](./TECH_STACK.md) | 技术栈规范 |
| [`AGENT.md`](./AGENT.md) / `AGENT_A~D.md` | AI 编码助手全局规则 + 四角色规则 |
| [`AI_DOCS.md`](./AI_DOCS.md) | 官方文档索引 |
| [4人分工优化方案.md](./.trae/documents/4人分工优化方案.md) | 分工与三阶段时间轴 |

## 团队（2.5 小时闪电开发）

| 角色 | 负责范围 |
|---|---|
| A · 界面与装配（编码） | `main.py` 独占、`ui/` 五屏与无障碍交互、合并装配 |
| B · 接口与 AI（编码） | `logic/` 契约与降级链、`ai/` VLM/LLM/ASR、契约主笔 |
| C · 需求与路演（非技术） | 需求文档、prompt 文案、路演稿与答辩 |
| D · 测试与素材（非技术） | `shared/mock.md` 权威数据、素材图、测试走查、报时 |

协作规则：一个文件只有一个 owner；定题后契约先行冻结；小步提交（`<模块>: <改动>`）；AI 异常走 mock 降级，演示异常播兜底录屏。

---

## 许可

本项目为黑客松参赛作品，仅用于学习与公益演示。
