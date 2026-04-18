"""任务 1：总体经济发展趋势。

5 张图（FT 编辑部风，结构转型叙事）：
  T1.1 全国 GDP 总量折线
  T1.2 三次产业堆叠面积
  T1.3 三次产业占比演化折线（暖橙第三产业为主角）
  T1.4 年度名义增速柱状
  H1   31 省三元图轨迹 —— 封面级英雄图
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from scripts._common import (
    DATA_DIR, INDUSTRY, HIGHLIGHT, SUPPORT, MUTED,
    editorial_title, source_footer, save_fig,
)

# ----------------------------------------------------------------------
def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    long = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    nat = pd.read_csv(DATA_DIR / "gdp_national.csv")
    nat["同比增速"] = nat["GDP总量"].pct_change() * 100
    return long, nat


# ----------------------------------------------------------------------
def plot_t11_national_gdp(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.3))
    y = nat["GDP总量"] / 1e4                         # 万亿元
    ax.plot(nat["年份"], y, color=SUPPORT, linewidth=3,
            marker="o", markersize=8, markerfacecolor="white", markeredgewidth=2)
    ax.fill_between(nat["年份"], y, alpha=0.12, color=SUPPORT)
    for x, v in zip(nat["年份"], y):
        ax.annotate(f"{v:.1f}", (x, v), xytext=(0, 10),
                    textcoords="offset points", ha="center",
                    fontsize=9.5, color="#222")
    # 高亮 2020 年疫情拐点
    y2020 = nat.loc[nat["年份"] == 2020, "GDP总量"].iloc[0] / 1e4
    ax.annotate("2020 疫情\n增速明显回落", xy=(2020, y2020), xytext=(2017.6, y2020 + 2),
                fontsize=10, color=HIGHLIGHT, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.2))
    ax.set_xlabel("年份"); ax.set_ylabel("GDP（万亿元）")
    ax.set_xticks(nat["年份"])
    ax.grid(alpha=0.25, linestyle="--")
    ax.set_ylim(60, 145)
    fig.subplots_adjust(top=0.82, bottom=0.13, left=0.08, right=0.96)
    editorial_title(fig,
                    "十年翻倍：2015–2024 全国 GDP 走势",
                    "名义 GDP 从 70.3 万亿增至 134.8 万亿，十年间规模接近翻一番。")
    source_footer(fig)
    save_fig(fig, "task1_national_gdp")


# ----------------------------------------------------------------------
def plot_t12_industry_stack(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.3))
    years = nat["年份"]
    s1 = nat["第一产业"] / 1e4
    s2 = nat["第二产业"] / 1e4
    s3 = nat["第三产业"] / 1e4
    ax.stackplot(
        years, s1, s2, s3,
        labels=["第一产业", "第二产业", "第三产业"],
        colors=[INDUSTRY["第一产业"], INDUSTRY["第二产业"], INDUSTRY["第三产业"]],
        alpha=0.92, edgecolor="white", linewidth=0.8,
    )
    ax.set_xticks(years)
    ax.set_xlabel("年份"); ax.set_ylabel("增加值（万亿元）")
    ax.legend(loc="upper left", frameon=False, fontsize=11)
    ax.grid(alpha=0.2, linestyle="--")
    # 年度合计标注
    for x, total in zip(years, s1 + s2 + s3):
        ax.annotate(f"{total:.1f}", (x, total), xytext=(0, 6),
                    textcoords="offset points", ha="center",
                    fontsize=9, color="#444")
    fig.subplots_adjust(top=0.82, bottom=0.13, left=0.08, right=0.96)
    editorial_title(fig,
                    "结构换骨：三次产业增加值的十年积累",
                    "暖橙色的第三产业面积从 36.3 万亿长至 76.6 万亿，增量远超二产。")
    source_footer(fig)
    save_fig(fig, "task1_industry_stack")


# ----------------------------------------------------------------------
def plot_t13_industry_share(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.3))
    years = nat["年份"]
    for key in ["第一产业", "第二产业", "第三产业"]:
        lw = 3.2 if key == "第三产业" else 2
        ax.plot(years, nat[f"{key}占比"] * 100, marker="o", markersize=7,
                color=INDUSTRY[key], linewidth=lw, label=key)
    # 强调三产首尾值
    first = nat["第三产业占比"].iloc[0] * 100
    last = nat["第三产业占比"].iloc[-1] * 100
    ax.annotate(f"{first:.1f}%", (years.iloc[0], first), xytext=(-30, -4),
                textcoords="offset points", fontsize=11, color=INDUSTRY["第三产业"],
                fontweight="bold")
    ax.annotate(f"{last:.1f}%", (years.iloc[-1], last), xytext=(8, -4),
                textcoords="offset points", fontsize=11, color=INDUSTRY["第三产业"],
                fontweight="bold")
    ax.set_xticks(years)
    ax.set_xlabel("年份"); ax.set_ylabel("占 GDP 比重（%）")
    ax.legend(loc="center right", frameon=False, fontsize=11)
    ax.grid(alpha=0.25, linestyle="--")
    ax.set_ylim(0, 65)
    fig.subplots_adjust(top=0.82, bottom=0.13, left=0.08, right=0.96)
    editorial_title(fig,
                    "服务化加速：第三产业占比从 51.7% 升至 56.8%",
                    "十年间第三产业占比提升 5 个百分点，第二产业退让 3.5 个百分点，第一产业小幅下降。")
    source_footer(fig)
    save_fig(fig, "task1_industry_share")


# ----------------------------------------------------------------------
def plot_t14_growth(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.3))
    sub = nat.dropna(subset=["同比增速"])
    colors = [HIGHLIGHT if y == 2020 else SUPPORT for y in sub["年份"]]
    bars = ax.bar(sub["年份"], sub["同比增速"], color=colors, width=0.6, edgecolor="white")
    for bar, val in zip(bars, sub["同比增速"]):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.2, f"{val:.1f}%",
                ha="center", fontsize=10, color="#333")
    ax.axhline(0, color="#333", linewidth=0.8)
    ax.set_xticks(sub["年份"])
    ax.set_xlabel("年份"); ax.set_ylabel("名义 GDP 同比增速（%）")
    ax.grid(alpha=0.25, axis="y", linestyle="--")
    ax.set_ylim(0, 16)
    legend_elems = [
        Line2D([0], [0], marker="s", color=SUPPORT, linestyle="",
               markersize=11, label="常规年份"),
        Line2D([0], [0], marker="s", color=HIGHLIGHT, linestyle="",
               markersize=11, label="2020 疫情冲击"),
    ]
    ax.legend(handles=legend_elems, loc="upper right", frameon=False, fontsize=10)
    fig.subplots_adjust(top=0.82, bottom=0.13, left=0.08, right=0.96)
    editorial_title(fig,
                    "V 型恢复：名义 GDP 增速在疫情后显著反弹",
                    "2020 年增速跌至 2.9%，2021 年反弹至 13.4%，此后回归中速区间。")
    source_footer(fig)
    save_fig(fig, "task1_growth_rate")


# ----------------------------------------------------------------------
def plot_h1_ternary(long: pd.DataFrame) -> None:
    """英雄图 H1 —— 31 省三次产业占比三元图轨迹。"""
    def tri_to_xy(p1, p2, p3):
        # 三元坐标到直角坐标（等边三角形）
        x = 0.5 * (2 * p2 + p3) / (p1 + p2 + p3)
        y = 0.5 * np.sqrt(3) * p3 / (p1 + p2 + p3)
        return x, y

    fig, ax = plt.subplots(figsize=(12.5, 10.5))
    # 三角框架
    corners = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2], [0, 0]])
    ax.plot(corners[:, 0], corners[:, 1], color="#333", linewidth=1.2)

    # 等占比参考线（每 20%）
    for k in np.arange(0.2, 1.0, 0.2):
        # 平行于第一产业轴
        p1, p2 = np.linspace(0, 1 - k, 50), np.linspace(1 - k, 0, 50)
        p3 = np.full_like(p1, k)
        xs, ys = tri_to_xy(p1, p2, p3)
        ax.plot(xs, ys, color="#CCCCCC", linewidth=0.6, linestyle="--")
        # 第二产业
        p1, p3 = np.linspace(0, 1 - k, 50), np.linspace(1 - k, 0, 50)
        p2 = np.full_like(p1, k)
        xs, ys = tri_to_xy(p1, p2, p3)
        ax.plot(xs, ys, color="#CCCCCC", linewidth=0.6, linestyle="--")
        # 第一产业
        p2, p3 = np.linspace(0, 1 - k, 50), np.linspace(1 - k, 0, 50)
        p1 = np.full_like(p2, k)
        xs, ys = tri_to_xy(p1, p2, p3)
        ax.plot(xs, ys, color="#CCCCCC", linewidth=0.6, linestyle="--")

    # 三顶点标签
    ax.text(-0.035, -0.03, "第一产业 100%", fontsize=12, fontweight="bold",
            color=INDUSTRY["第一产业"], ha="right")
    ax.text(1.035, -0.03, "第二产业 100%", fontsize=12, fontweight="bold",
            color=INDUSTRY["第二产业"], ha="left")
    ax.text(0.5, np.sqrt(3) / 2 + 0.028, "第三产业 100%", fontsize=12, fontweight="bold",
            color=INDUSTRY["第三产业"], ha="center")

    # 31 省轨迹 —— 所有轨迹浅灰，只对 4 个标志性极端省高亮 + 标注
    extremes = {
        "北京市":    (+0.020, +0.015, "left"),
        "上海市":    (+0.020, -0.018, "left"),
        "黑龙江省":  (-0.020, +0.010, "right"),
        "西藏自治区": (-0.020, -0.010, "right"),
    }
    for prov, sub in long.groupby("省份"):
        sub = sub.sort_values("年份")
        xs, ys = tri_to_xy(sub["第一产业占比"].values,
                           sub["第二产业占比"].values,
                           sub["第三产业占比"].values)
        if prov in extremes:
            color, alpha, lw = HIGHLIGHT, 0.95, 2.4
        else:
            color, alpha, lw = MUTED, 0.45, 1.1
        ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha, zorder=2 if prov in extremes else 1)
        ax.scatter(xs[0], ys[0], s=22, color=color, alpha=alpha * 0.7, zorder=3)
        ax.annotate("", xy=(xs[-1], ys[-1]), xytext=(xs[-2], ys[-2]),
                    arrowprops=dict(arrowstyle="->", color=color, alpha=alpha, lw=lw),
                    zorder=3)
        if prov in extremes:
            dx, dy, align = extremes[prov]
            ax.text(xs[-1] + dx, ys[-1] + dy, prov, ha=align, va="center",
                    fontsize=11, color=HIGHLIGHT, fontweight="bold")

    # 聚焦数据实际分布区域
    ax.set_xlim(0.22, 0.70)
    ax.set_ylim(0.28, 0.82)
    ax.set_aspect("equal")
    ax.set_axis_off()
    fig.subplots_adjust(top=0.82, bottom=0.06, left=0.02, right=0.98)
    editorial_title(fig,
                    "漂向第三产业顶点：31 省十年产业结构轨迹",
                    "灰色 = 全部 31 省轨迹；红色 = 4 个极端代表（京沪服务化、黑龙江一产最高、西藏三产最高）。")
    source_footer(fig, "三元图（Ternary Plot）· 已缩放至数据实际分布区")
    save_fig(fig, "task1_h1_ternary")


def main() -> None:
    long, nat = load()
    plot_t11_national_gdp(nat)
    plot_t12_industry_stack(nat)
    plot_t13_industry_share(nat)
    plot_t14_growth(nat)
    plot_h1_ternary(long)
    print("✓ 任务 1 共生成 5 张图 (含 H1 英雄图)：outputs/task1_*.png")


if __name__ == "__main__":
    main()
