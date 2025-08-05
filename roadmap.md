---
layout: default
title: 社区复现路线图
---

## Lab4AI 社区论文复现路线图 (Roadmap)

本文档列出了我们社区计划复现的前沿AI论文。我们欢迎任何形式的贡献，如果您对列表中的某个项目感兴趣，或者有新的论文推荐，请在我们的 [**Issue 列表**](https://github.com/Lab4AI/ReproHub/issues) 中发起讨论！

---

{% for conference in site.data.roadmap %}
### {{ conference[0] }}

| 论文标题 (Paper) | 核心技术 (Core Tech) | 状态 | 认领/讨论 |
| :--- | :--- | :--- | :--- |
{% for paper in conference[1] %}
| **{{ paper.title }}** | `{{ paper.core_tech }}` | 💡 **待认领** | [发起讨论](https://github.com/Lab4AI/ReproHub/issues/new?template=paper_proposal.md) |
{% endfor %}

{% endfor %}
