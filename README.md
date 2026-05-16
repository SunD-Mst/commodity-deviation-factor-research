# 商品期货日内偏离因子研究（公开演示版）

本公开版本展示了商品期货日内偏离因子的完整研究流程。  
该项目面向作品集展示与面试评审：代码可直接运行，研究结构完整，但有意简化了敏感的交易细节。

## 项目目标

构建一个可复现的研究框架，用于分析：

> 开盘区间偏离结构，是否能够描述后续日内波动状态与路径特征。

该公共仓库聚焦于研究过程，而非可直接部署的交易规则。

主要内容包括：

- 数据加载与时间戳标准化
- 开盘区间基准构建
- ATR 标准化偏离因子计算
- 历史同期百分位计算
- 事件研究式验证
- Multi 曲线可视化
- 简化版策略研究接口

## 研究问题

开盘区间形成后，价格相对开盘区间中点的阶段性偏离，  
能否为后续日内偏离延续、波动扩张或均值回归提供可分析的信息？

本公开演示使用模拟数据与中性示例参数，  
不应被解读为交易建议，也不构成私人研究规则的披露。

## 因子定义

- `OR_mid`：开盘区间高点与低点的中点。
- `abs_deviation`：价格在当前观察阶段内相对 `OR_mid` 的最远偏离距离，并使用前序 ATR 标准化。
- `deviation_pct`：当前 `abs_deviation` 在历史同期样本中的百分位数，仅使用先前日期计算。

## 研究流程

1. 加载样本日内 OHLCV 数据。
2. 构建开盘区间高点、低点及中点。
3. 计算前序 ATR 与标准化偏离指标。
4. 重建不含未来数据泄露的历史同期百分位。
5. 使用演示阈值运行小型事件研究。
6. 生成示例曲线与统计摘要。
7. 运行带有占位逻辑的简化策略研究接口。

## 项目结构

```text
public_commodity_deviation_factor_research/
  README.md
  requirements.txt
  sample_data/
    sample_intraday_15m.csv
    sample_intraday_1m.csv
  src/
    quant_data_public.py
    factor_research_public.py
    event_study_public.py
    demo_strategy_public.py
  notebooks/
    public_factor_research_demo.ipynb
  outputs/
    .gitkeep
