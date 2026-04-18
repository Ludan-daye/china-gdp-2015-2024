"""任务 2 H2 英雄图：省份"结构时钟" —— 2015 vs 2024 第三产业占比散点图。

- 横轴 2015 第三产业占比；纵轴 2024 第三产业占比
- 45° 对角线 = 零转型基准
- 点大小 ∝ 2024 GDP 总量
- 偏离对角线的垂直距离 = 十年间结构升级幅度
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scripts._common import (
    DATA_DIR, INDUSTRY, HIGHLIGHT, SUPPORT, MUTED,
    editorial_title, source_footer, save_fig,
)


HIGHLIGHT_PROVINCES = {
    "北京市", "上海市", "天津市", "广东省", "江苏省", "浙江省", "山东省",
    "四川省", "河南省", "湖北省", "福建省", "西藏自治区", "海南省",
    "黑龙江省", "贵州省", "新疆维吾尔自治区",
}


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    piv = df[df["年份"].isin([2015, 2024])].pivot(
        index="省份", columns="年份", values="第三产业占比") * 100
    gdp24 = df[df["年份"] == 2024].set_index("省份")["GDP总量"] / 1e4
    both = piv.join(gdp24.rename("gdp24"))
    both["转型幅度"] = both[2024] - both[2015]

    fig, ax = plt.subplots(figsize=(11.5, 10.5))
    # 45° 对角线
    lo, hi = 40, 90
    ax.plot([lo, hi], [lo, hi], color="#888", linewidth=1.4, linestyle="--", zorder=1)
    ax.text(85, 85 - 1.4, "零转型基准线（y = x）", color="#888", fontsize=9,
            ha="right", style="italic")

    # 上方 "+X 百分点" 等值线参考（仅示 +5pp）
    ax.plot([lo, hi - 5], [lo + 5, hi], color="#D4D4D4", linewidth=0.8, linestyle=":", zorder=1)
    ax.text(hi - 5.5, hi - 0.5, "+5 百分点", color="#AAA", fontsize=8,
            ha="right", va="center", style="italic")

    sizes = (both["gdp24"] / both["gdp24"].max()) * 900 + 50
    colors = []
    for p, delta in zip(both.index, both["转型幅度"]):
        if delta > 3:
            colors.append(INDUSTRY["第三产业"])   # 升级明显
        elif delta > 0:
            colors.append(SUPPORT)
        else:
            colors.append(MUTED)

    ax.scatter(both[2015], both[2024], s=sizes, c=colors, alpha=0.80,
               edgecolor="white", linewidth=1.4, zorder=3)

    # 标注重点省份
    for prov in HIGHLIGHT_PROVINCES:
        if prov not in both.index: continue
        x, y = both.loc[prov, 2015], both.loc[prov, 2024]
        ax.annotate(prov, (x, y), xytext=(6, 4), textcoords="offset points",
                    fontsize=9.5, color="#222", fontweight="bold")

    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("2015 年 第三产业占比（%）", fontsize=11)
    ax.set_ylabel("2024 年 第三产业占比（%）", fontsize=11)
    ax.grid(alpha=0.25, linestyle="--")
    ax.set_aspect("equal")

    # 自定义 legend
    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=INDUSTRY["第三产业"],
               markersize=13, label="转型 > 3 pp（显著升级）"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=SUPPORT,
               markersize=13, label="转型 0–3 pp（温和升级）"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=MUTED,
               markersize=13, label="基本持平或回落"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#BBB",
               markersize=8, label="点大小 ∝ 2024 GDP 总量"),
    ]
    ax.legend(handles=legend_elems, loc="lower right", frameon=False, fontsize=9.5)

    fig.subplots_adjust(top=0.88, bottom=0.07, left=0.08, right=0.96)
    editorial_title(fig,
                    "结构时钟：几乎所有省份都驶过对角线之上",
                    "横轴 2015、纵轴 2024 的第三产业占比；偏离 45° 线的距离 = 十年间服务化幅度。"
                    "点越大，经济体量越大。")
    source_footer(fig, "H2 · 结构时钟 Clock Chart")
    save_fig(fig, "task2_h2_clock")
    print("✓ outputs/task2_h2_clock.png")


if __name__ == "__main__":
    main()
