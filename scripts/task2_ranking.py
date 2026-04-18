"""任务 2 图①：2024 年 31 省市 GDP 水平柱状排名。"""
from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import (
    DATA_DIR, SUPPORT, HIGHLIGHT, MUTED,
    editorial_title, source_footer, save_fig,
)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d = df[df["年份"] == 2024].sort_values("GDP总量", ascending=True).reset_index(drop=True)
    d["万亿"] = d["GDP总量"] / 1e4

    fig, ax = plt.subplots(figsize=(11, 12.5))
    colors = [HIGHLIGHT if i >= len(d) - 4 else (SUPPORT if i >= len(d) - 12 else MUTED)
              for i in range(len(d))]
    bars = ax.barh(d["省份"], d["万亿"], color=colors, edgecolor="white", height=0.72)
    for bar, val in zip(bars, d["万亿"]):
        ax.text(val + 0.15, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", fontsize=9.5, color="#333")
    ax.set_xlabel("GDP（万亿元）"); ax.set_ylabel("")
    ax.grid(alpha=0.25, axis="x", linestyle="--")
    ax.set_xlim(0, 15.5)

    # 手工 legend
    from matplotlib.patches import Patch
    handles = [
        Patch(color=HIGHLIGHT, label="头部四强（粤苏鲁浙）"),
        Patch(color=SUPPORT, label="中腰部 8 省（第 5–12 名）"),
        Patch(color=MUTED, label="其余 19 省市"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=10)

    fig.subplots_adjust(top=0.90, bottom=0.06, left=0.14, right=0.96)
    editorial_title(fig,
                    "四极格局稳固：粤苏鲁浙贡献全国 1/3 GDP",
                    "2024 年广东、江苏双双超 13 万亿，与排末的西藏相差 50 余倍。")
    source_footer(fig)
    save_fig(fig, "task2_ranking")
    print("✓ outputs/task2_ranking.png")


if __name__ == "__main__":
    main()
