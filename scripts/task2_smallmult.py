"""任务 2 图⑤：各省 2015-2024 GDP 发展曲线，按地理方位排列的小多图（变形地图）。"""
from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import (
    DATA_DIR, INDUSTRY, SUPPORT, editorial_title, source_footer, save_fig,
)

# (row, col) 8×7 网格，大致对应各省地理方位（北→南、西→东）
TILE_GRID: dict[str, tuple[int, int]] = {
    "黑龙江省":         (0, 5),
    "吉林省":           (1, 4),
    "辽宁省":           (1, 5),
    "内蒙古自治区":      (2, 3),
    "北京市":           (2, 5),
    "天津市":           (2, 6),
    "新疆维吾尔自治区":  (3, 0),
    "甘肃省":           (3, 1),
    "陕西省":           (3, 2),
    "山西省":           (3, 3),
    "河北省":           (3, 4),
    "山东省":           (3, 5),
    "青海省":           (4, 0),
    "宁夏回族自治区":    (4, 1),
    "河南省":           (4, 2),
    "安徽省":           (4, 3),
    "江苏省":           (4, 4),
    "上海市":           (4, 5),
    "西藏自治区":        (5, 0),
    "四川省":           (5, 1),
    "湖北省":           (5, 2),
    "浙江省":           (5, 4),
    "重庆市":           (6, 1),
    "贵州省":           (6, 2),
    "湖南省":           (6, 3),
    "江西省":           (6, 4),
    "福建省":           (6, 5),
    "云南省":           (7, 1),
    "广西壮族自治区":    (7, 2),
    "广东省":           (7, 3),
    "海南省":           (7, 4),
}


def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    n_rows = max(r for r, _ in TILE_GRID.values()) + 1
    n_cols = max(c for _, c in TILE_GRID.values()) + 1

    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=(n_cols * 2.0, n_rows * 1.55),
        sharex=True, sharey=False,
    )
    for ax in axes.flat:
        ax.set_axis_off()

    vmax = df["GDP总量"].max() / 1e4

    # 2024 头部 4 省用暖橙高亮
    top_4 = {"广东省", "江苏省", "山东省", "浙江省"}

    for prov, (r, c) in TILE_GRID.items():
        ax = axes[r, c]
        ax.set_axis_on()
        sub = df[df["省份"] == prov].sort_values("年份")
        y = sub["GDP总量"] / 1e4
        color = INDUSTRY["第三产业"] if prov in top_4 else SUPPORT
        ax.plot(sub["年份"], y, color=color, linewidth=2.0)
        ax.fill_between(sub["年份"], y, alpha=0.20, color=color)
        # 2024 终点标记
        ax.scatter([sub["年份"].iloc[-1]], [y.iloc[-1]], color=color, s=22, zorder=3)
        # 省份名 + 2024 值
        short = prov.replace("省", "").replace("市", "").replace("自治区", "")\
            .replace("壮族", "").replace("回族", "").replace("维吾尔", "")
        ax.text(0.03, 0.93, short, transform=ax.transAxes,
                fontsize=9, fontweight="bold", color="#222")
        ax.text(0.97, 0.93, f"{y.iloc[-1]:.1f}", transform=ax.transAxes,
                fontsize=8.5, color=color, ha="right", fontweight="bold")
        ax.set_xticks([2015, 2020, 2024])
        ax.tick_params(labelsize=6.5, pad=1)
        ax.set_ylim(0, max(y.max() * 1.18, 0.5))
        ax.set_xlim(2014.5, 2024.5)
        ax.grid(alpha=0.25, linestyle=":")
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.spines["left"].set_color("#AAA")
        ax.spines["bottom"].set_color("#AAA")

    fig.subplots_adjust(top=0.88, bottom=0.05, left=0.04, right=0.98,
                        hspace=0.6, wspace=0.35)
    editorial_title(fig,
                    "地理小多图：31 省十年 GDP 曲线（按方位排列）",
                    "橙色 = 头部四强（粤苏鲁浙），蓝色 = 其余 27 省。"
                    "每格右上数字 = 2024 年 GDP（万亿元）。")
    source_footer(fig, "Small Multiples · 近似变形地图排列")
    save_fig(fig, "task2_smallmult")
    print("✓ outputs/task2_smallmult.png")


if __name__ == "__main__":
    main()
