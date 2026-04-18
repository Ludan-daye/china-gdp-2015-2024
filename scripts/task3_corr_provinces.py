"""任务 3 图③：省际 GDP 年度增速相关性热图（基于 2016-2024 年增速序列）。"""
from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from scripts._common import (
    DATA_DIR, editorial_title, source_footer, save_fig,
)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    wide = df.pivot(index="年份", columns="省份", values="GDP总量")
    growth = wide.pct_change().dropna()                # 9 年增速序列 × 31 省
    corr = growth.corr()

    # 按 2024 GDP 降序排
    order = (df[df["年份"] == 2024].sort_values("GDP总量", ascending=False)["省份"].tolist())
    corr = corr.loc[order, order]
    short_names = [p.replace("省", "").replace("市", "").replace("自治区", "")
                    .replace("壮族", "").replace("回族", "").replace("维吾尔", "")
                   for p in corr.index]

    fig, ax = plt.subplots(figsize=(14, 12))
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "corr", ["#2A6399", "#FFFFFF", "#C93838"], N=256)
    im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1, aspect="equal")

    # 刻度
    ax.set_xticks(range(len(short_names)))
    ax.set_yticks(range(len(short_names)))
    ax.set_xticklabels(short_names, rotation=60, ha="right", fontsize=9)
    ax.set_yticklabels(short_names, fontsize=9)
    ax.tick_params(length=0)
    # 白色网格线
    ax.set_xticks(np.arange(-0.5, len(short_names), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(short_names), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.5)
    ax.tick_params(which="minor", length=0)

    # 上对角线标注数值
    for i in range(len(corr)):
        for j in range(len(corr)):
            if j <= i: continue
            v = corr.values[i, j]
            if abs(v) >= 0.6:
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        fontsize=6.2, color="#1A1A1A" if abs(v) < 0.85 else "white",
                        alpha=0.9)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.55, pad=0.02)
    cbar.set_label("Pearson r（名义 GDP 年度增速同期相关系数）", fontsize=10)
    cbar.ax.tick_params(labelsize=9)

    # 统计要点
    off = corr.where(~np.eye(len(corr), dtype=bool))
    mean_r = off.stack().mean()
    pos_ratio = (off.stack() > 0).mean() * 100

    fig.subplots_adjust(top=0.92, bottom=0.10, left=0.10, right=0.96)
    editorial_title(fig,
                    "增速的一盘棋：省际年度增速高度同步",
                    f"31 省两两 Pearson r 均值 {mean_r:+.2f}，"
                    f"{pos_ratio:.0f}% 的省份对为正相关，验证宏观周期共振显著。")
    source_footer(fig, "Pearson 相关热图 · 行列按 2024 GDP 降序排列")
    save_fig(fig, "task3_corr_provinces")
    print(f"✓ outputs/task3_corr_provinces.png  (mean r = {mean_r:+.3f})")


if __name__ == "__main__":
    main()
