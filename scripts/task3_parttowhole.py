"""任务 3 图①：2024 年各省 GDP 相对全国的部分-总体 Treemap。"""
from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import squarify
from scripts._common import (
    DATA_DIR, SUPPORT, HIGHLIGHT, editorial_title, source_footer, save_fig,
)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d = df[df["年份"] == 2024].sort_values("GDP总量", ascending=False).reset_index(drop=True)
    total = d["GDP总量"].sum()
    d["占比"] = d["GDP总量"] / total * 100

    # 蓝色渐变：排名越靠前颜色越深
    n = len(d)
    base_cmap = mcolors.LinearSegmentedColormap.from_list(
        "gdp_rank",
        ["#0F335C", "#1C4C7D", "#2A6399", "#3E83B6", "#6BA3C9", "#9FC3DC", "#C9DEEC"],
    )
    colors = [base_cmap(i / max(n - 1, 1) * 0.95) for i in range(n)]

    labels = []
    for _, row in d.iterrows():
        short = row["省份"].replace("省", "").replace("市", "").replace("自治区", "")\
            .replace("壮族", "").replace("回族", "").replace("维吾尔", "")
        if row["占比"] >= 3.5:
            labels.append(f"{short}\n{row['占比']:.1f}%\n{row['GDP总量']/1e4:.1f}万亿")
        elif row["占比"] >= 1.2:
            labels.append(f"{short}\n{row['占比']:.1f}%")
        else:
            labels.append(short)

    fig, ax = plt.subplots(figsize=(14, 9))
    squarify.plot(
        sizes=d["GDP总量"], label=labels, color=colors,
        ax=ax, pad=True, edgecolor="white", linewidth=2.0,
        text_kwargs={"fontsize": 10.5, "color": "white", "fontweight": "bold"},
    )
    ax.set_axis_off()

    # 头部省份占比小结
    top4 = d.head(4)["占比"].sum()
    top10 = d.head(10)["占比"].sum()
    fig.text(0.02, 0.04,
             f"前 4 强合计 {top4:.1f}%  ·  前 10 强合计 {top10:.1f}%  ·  全国 2024 年 GDP 合计 {total/1e4:.1f} 万亿元",
             fontsize=10.5, color=HIGHLIGHT, fontweight="bold")

    fig.subplots_adjust(top=0.90, bottom=0.11, left=0.02, right=0.98)
    editorial_title(fig,
                    "全国 GDP 的省际版图：谁贡献了多少？",
                    "每个矩形面积 = 该省 2024 年 GDP 占全国比重。"
                    "粤苏两省相加已超全国 1/5。")
    source_footer(fig, "部分-总体 Treemap · 2024 年全国 GDP 构成")
    save_fig(fig, "task3_parttowhole")
    print("✓ outputs/task3_parttowhole.png")


if __name__ == "__main__":
    main()
