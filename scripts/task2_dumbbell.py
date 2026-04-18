"""任务 2 图③：2015 vs 2024 各省 GDP 哑铃对比（含十年累计增长率）。"""
from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import (
    DATA_DIR, SUPPORT, HIGHLIGHT, MUTED, INDUSTRY,
    editorial_title, source_footer, save_fig,
)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    piv = df[df["年份"].isin([2015, 2024])].pivot(
        index="省份", columns="年份", values="GDP总量") / 1e4
    piv = piv.sort_values(2024, ascending=True)
    piv["growth"] = (piv[2024] / piv[2015] - 1) * 100

    fig, ax = plt.subplots(figsize=(11, 12.5))
    for y, (prov, row) in enumerate(piv.iterrows()):
        ax.plot([row[2015], row[2024]], [y, y], color="#CCCCCC", linewidth=3, zorder=1)
        ax.scatter(row[2015], y, color=MUTED, s=70, zorder=2, edgecolor="white", linewidth=1.2)
        ax.scatter(row[2024], y, color=INDUSTRY["第三产业"], s=90, zorder=3,
                   edgecolor="white", linewidth=1.2)
        ax.text(row[2024] + 0.25, y, f"+{row['growth']:.0f}%", va="center",
                fontsize=8.5, color=HIGHLIGHT, fontweight="bold")

    ax.set_yticks(range(len(piv))); ax.set_yticklabels(piv.index)
    ax.set_xlabel("GDP（万亿元）")
    ax.grid(alpha=0.25, axis="x", linestyle="--")
    ax.set_xlim(0, 16.5)

    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=MUTED,
               markersize=10, label="2015 GDP"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=INDUSTRY["第三产业"],
               markersize=11, label="2024 GDP"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=11)

    fig.subplots_adjust(top=0.90, bottom=0.06, left=0.14, right=0.96)
    editorial_title(fig,
                    "体量膨胀，位次重排：2015 → 2024 各省 GDP 对比",
                    "十年累计增长率最高者为西藏 +160%，头部省份绝对增量远大于尾部。")
    source_footer(fig)
    save_fig(fig, "task2_dumbbell")
    print("✓ outputs/task2_dumbbell.png")


if __name__ == "__main__":
    main()
