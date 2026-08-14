# cost-reduction-platform-demo

公开降本项目管理 Demo，采用中文主界面 + 英文专业标签，展示一个适合公开作品集的降本项目台账、Batch Import、Deduplication 与数据治理演示项目。

Public portfolio demo for a cost reduction tracking workflow, built with a Chinese-first UI and selective English professional labels for clarity.

> This repository is a public reimplementation using synthetic data.
> It contains no proprietary code, internal data, confidential materials, or company-specific assets.

## 项目定位 | Project Positioning

这个项目聚焦“纸面 / Excel 台账 -> 可运行系统”的最小闭环，主要展示：

- 项目台账管理
- 工厂维度的数据隔离演示
- CSV / Excel / XLSX 批量导入
- 导入预览、字段校验、Deduplication 与确认导入

It is intentionally simple and easy to run locally, so recruiters, interviewers, or reviewers can understand the workflow quickly.

## V1 范围 | V1 Scope

- 概览 Dashboard
- 降本项目台账
- 新增、编辑、搜索、筛选
- CSV / Excel / XLSX 批量导入
- 字段校验
- 重复检测
- Preview 后 Confirm Import
- 简单多工厂数据隔离演示
- 项目详情页
- Synthetic seed data

## 不包含内容 | Not Included

- 真实公司名称、真实工厂、真实项目、真实账号、真实截图、真实 URL、真实生产数据
- 专有代码或内部业务资产
- 复杂认证、完整 RBAC
- 微服务、Docker、Kubernetes、复杂 CI/CD

## 技术栈 | Tech Stack

- Python 3.11
- FastAPI
- SQLite
- Jinja2 templates
- Tailwind via CDN

说明：

- 这个公开 Demo 使用 SQLite，便于本地运行和展示。
- 如果后续扩展为企业内项目，可继续延伸到 MySQL、Data Migration 与 Data Governance 场景，但当前仓库不包含真实企业迁移数据。

## 快速启动 | Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

启动后打开 [http://127.0.0.1:8000](http://127.0.0.1:8000)。

## 导入格式 | Import Format

导入字段如下：

```text
project_code, title, factory_name, category, status, owner, estimated_savings, currency, start_date, target_date, description
```

当前 Demo 支持的工厂：

- 阿尔法工厂
- 贝塔工厂
- 伽马工厂

仓库中提供了一个示例文件：

- `sample_data/projects_import_template.csv`

## Synthetic Data 示例 | Synthetic Data Used

当前种子数据仅包含虚构示例，例如：

- 阿尔法工厂、贝塔工厂、伽马工厂
- 压缩空气漏点巡检整治
- 包装膜宽度标准化优化
- 叉车动线重排优化
- 冷却水设定值复核
- 可循环托盘覆盖扩展

所有金额、负责人、时间计划和说明均为 Synthetic Data，仅用于公开展示。

## Repository Safety Statement

This repository is a public reimplementation using synthetic data.
It contains no proprietary code, internal data, confidential materials, or company-specific assets.
