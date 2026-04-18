"""任务 2 图②：2024 年 31 省市三次产业占比 100% 堆叠条形（按第三产业占比升序）。"""
from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import (
    DATA_DIR, INDUSTRY, editorial_title, source_footer, save_fig,
)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d = df[df["年份"] == 2024].sort_values("第三产业占比", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(13, 13))
    left = [0.0] * len(d)
    for key in ["第一产业", "第二产业", "第三产业"]:
        share_col = f"{key}占比"
        vals = (d[share_col] * 100).values
        ax.barh(d["省份"], vals, left=left, color=INDUSTRY[key],
                label=key, edgecolor="white", height=0.72)
        for i, v in enumerate(vals):
            if v >= 6:
                ax.text(left[i] + v / 2, i, f"{v:.0f}",
                        ha="center", va="center", color="white",
                        fontsize=9, fontweight="bold")
        left = [l + v for l, v in zip(left, vals)]

    ax.set_xlim(0, 100)
    ax.set_xlabel("占 GDP 比重（%）")
    ax.grid(alpha=0.25, axis="x", linestyle="--")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=3,
              frameon=False, fontsize=11)

    fig.subplots_adjust(top=0.90, bottom=0.10, left=0.14, right=0.97)
    editorial_title(fig,
                    "服务化程度光谱：从新疆 47% 到北京 85%",
                    "按第三产业占比升序排列，北京、上海、海南已进入"
                    "典型服务型经济区间（三产 ≥ 60%）。")
    source_footer(fig)
    save_fig(fig, "task2_composition")
    print("✓ outputs/task2_composition.png")


if __name__ == "__main__":
    main()
