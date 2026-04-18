"""任务 3 图②：GDP 十年累计增长率 vs 第三产业占比变动 的散点 + 回归线。

A 叙事的核心数据支撑图：结构升级是否与增长伴随？
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scripts._common import (
    DATA_DIR, SUPPORT, HIGHLIGHT, INDUSTRY, MUTED,
    editorial_title, source_footer, save_fig,
)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    gdp = df[df["年份"].isin([2015, 2024])].pivot(
        index="省份", columns="年份", values="GDP总量")
    ter = df[df["年份"].isin([2015, 2024])].pivot(
        index="省份", columns="年份", values="第三产业占比")
    gdp24 = df[df["年份"] == 2024].set_index("省份")["GDP总量"] / 1e4

    both = pd.DataFrame({
        "GDP增长率": (gdp[2024] / gdp[2015] - 1) * 100,
        "三产占比变化": (ter[2024] - ter[2015]) * 100,
        "gdp24": gdp24,
    }).dropna()
    corr = both["GDP增长率"].corr(both["三产占比变化"])

    fig, ax = plt.subplots(figsize=(12, 8.2))
    sizes = (both["gdp24"] / both["gdp24"].max()) * 700 + 40
    ax.scatter(both["三产占比变化"], both["GDP增长率"], s=sizes,
               color=INDUSTRY["第三产业"], alpha=0.72,
               edgecolor="white", linewidth=1.4, zorder=3)

    # 回归线
    z = np.polyfit(both["三产占比变化"], both["GDP增长率"], 1)
    xs = np.linspace(both["三产占比变化"].min() - 0.5,
                     both["三产占比变化"].max() + 0.5, 60)
    ax.plot(xs, np.poly1d(z)(xs), color=HIGHLIGHT, linestyle="--", linewidth=2,
            label=f"线性拟合  r = {corr:+.2f}", zorder=2)

    ax.axhline(both["GDP增长率"].median(), color=MUTED, linewidth=0.7,
               linestyle=":", alpha=0.8)
    ax.axvline(both["三产占比变化"].median(), color=MUTED, linewidth=0.7,
               linestyle=":", alpha=0.8)

    # 标注极端省份
    labeled = {"西藏自治区", "福建省", "黑龙江省", "四川省", "安徽省", "海南省",
               "重庆市", "河南省", "甘肃省", "广东省", "北京市", "上海市",
               "新疆维吾尔自治区", "山西省"}
    for prov in labeled:
        if prov not in both.index: continue
        row = both.loc[prov]
        short = prov.replace("省", "").replace("市", "").replace("自治区", "")\
            .replace("壮族", "").replace("回族", "").replace("维吾尔", "")
        ax.annotate(short, (row["三产占比变化"], row["GDP增长率"]),
                    xytext=(6, 4), textcoords="offset points",
                    fontsize=9.5, color="#222", fontweight="bold")

    ax.set_xlabel("2015 → 2024 第三产业占比变化（百分点）")
    ax.set_ylabel("2015 → 2024 GDP 累计增长率（%）")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend(loc="lower right", frameon=False, fontsize=11)

    fig.subplots_adjust(top=0.86, bottom=0.10, left=0.08, right=0.96)
    if corr > 0.3:
        hint = f"正相关 (r = {corr:+.2f})：结构升级更显著的省份，累计增速也更高。"
    elif corr < -0.3:
        hint = f"负相关 (r = {corr:+.2f})：结构升级与高增长呈相反走向。"
    else:
        hint = f"弱相关 (r = {corr:+.2f})：结构升级对增速的解释力有限，存在其他驱动因素。"
    editorial_title(fig,
                    "结构升级 vs 经济增速：两者有关联吗？",
                    hint + "  点大小 ∝ 2024 年 GDP 体量。")
    source_footer(fig)
    save_fig(fig, "task3_corr_structure")
    print(f"✓ outputs/task3_corr_structure.png  (r = {corr:+.3f})")


if __name__ == "__main__":
    main()
