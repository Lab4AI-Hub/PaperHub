# ReproCode-Lab 社区贡献指南

首先，我们由衷地感谢您愿意为 ReproCode-Lab 社区贡献自己的时间和精力！❤️

我们是一个开放、友好、协作的社区。每一位贡献者，无论贡献大小，都将被尊重和鸣谢。本指南将帮助您顺利地完成您的第一次贡献。

## 贡献之前

在开始之前，请确保您已经：
1.  加入了我们的社区交流群（[点击加入]([你的社区交流群链接])）。
2.  仔细阅读了我们的 [行为准则 (CODE_OF_CONDUCT.md)](./CODE_OF_CONDUCT.md)。
3.  了解了我们项目的 [标准目录结构](#项目标准结构)。

## 贡献流程

我们采用标准的 GitHub Fork & Pull Request 协作流程。

### 第一步：认领任务

1.  前往我们的 [**Issue 列表**](https://github.com/ReproCode-Lab/ReproHub/issues)。
2.  您可以选择一个带有 `help wanted` 或 `good first issue` (适合新手) 标签的任务。
3.  在 Issue下方留言，例如“I would like to work on this issue.”，并 **@** 一位维护者。维护者会将该 Issue 分配给您。

如果您想复现一篇新的论文，请先 [**提交一个提案**](https://github.com/ReproCode-Lab/ReproHub/issues/new/choose)，待社区讨论通过后，再开始工作。

### 第二步：环境准备

1.  **Fork** `ReproHub` 仓库到您自己的 GitHub 账号下。
2.  **Clone** 您 Fork 后的仓库到本地：
    ```bash
    git clone [https://github.com/YOUR_USERNAME/ReproHub.git](https://github.com/YOUR_USERNAME/ReproHub.git)
    ```
3.  **创建新分支**：为您的任务创建一个描述性的分支，分支名建议为 `feat/paper-title-short` 或 `fix/issue-number`。
    ```bash
    git checkout -b feat/reproduce-mobilenet
    ```

### 第三步：代码实现与验证

1.  **创建目录**: 在 `papers/` 目录下，为您的论文创建一个符合命名规范的新目录。
2.  **编写代码**: 按照我们的 [项目标准结构](#项目标准结构) 添加您的代码、配置文件等。
3.  **【核心】算力验证**: 在 [**大模型实验室**]([你的“大模型实验室”平台链接]) 平台上，运行您的代码，确保能够成功训练并复现论文的关键指标。
4.  **保存验证报告**: 将平台生成的验证日志和结果对比报告，保存在您项目目录下的 `lab_validation/` 文件夹中。这是我们社区最有价值的部分！
5.  **编写项目 README**: 为您的项目目录创建一个 `README.md`，详细说明如何运行、环境配置、以及与原论文的结果对比。

### 第四步：提交 Pull Request

1.  **提交代码**: 将您的代码提交到您的分支。
    ```bash
    git add .
    git commit -m "feat: Add reproduction for MobileNet"
    git push origin feat/reproduce-mobilenet
    ```
2.  **创建 Pull Request**: 回到您 Fork 的 GitHub 仓库页面，点击 "New pull request"。
3.  **填写 PR 信息**:
    * 确保基准分支是 `ReproCode-Lab/ReproHub` 的 `main` 分支。
    * PR 的标题应清晰地描述您的工作，例如 `feat: Add reproduction for MobileNetV2`。
    * 在描述中，请关联您正在处理的 Issue (例如，`Closes #123`)。
    * 仔细填写 PR 模板中的检查清单。
4.  **代码审查**: 维护者和其他社区成员会对您的代码进行审查。请积极参与讨论，并根据反馈进行修改。
5.  **合并**: 一旦您的 PR 被批准，维护者会将其合并到主分支。恭喜您，您已经成功地为社区做出了贡献！

---

### 项目标准结构

所有复现项目都必须遵循以下目录结构：
papers/<br>
└── [author-year-title_short]/,<br>
    ├── src/              # 核心源代码<br>
    ├── configs/          # 配置文件<br>
    ├── lab_validation/   # 【核心】平台验证报告<br>
    ├── README.md         # 【核心】项目说明<br>
    └── requirements.txt  # Python依赖<br>
