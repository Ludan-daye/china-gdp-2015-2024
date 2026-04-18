"""任务 2 图④：2024 年中国各省 GDP 分层设色地图。

不依赖 geopandas —— 用 GeoJSON + matplotlib Polygon 直接画。
"""
from __future__ import annotations
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from scripts._common import (
    DATA_DIR, editorial_title, source_footer, save_fig,
)


def iter_polygons(geom: dict):
    """统一处理 Polygon 与 MultiPolygon，返回 [外环坐标] 序列。"""
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            yield ring
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                yield ring


def main() -> None:
    gj = json.loads((DATA_DIR / "china_provinces.geojson").read_text(encoding="utf-8"))
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d24 = df[df["年份"] == 2024].set_index("省份")["GDP总量"] / 1e4  # 万亿

    # 离散分箱配色（Blues 单色系由浅至深）
    edges = [0, 1, 2, 3, 5, 7, 10, 12, 15]
    labels = ["< 1", "1–2", "2–3", "3–5", "5–7", "7–10", "10–12", "≥ 12"]
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "gdp_blues",
        ["#E8F1FA", "#C9DEEC", "#9FC3DC", "#6BA3C9", "#3E83B6", "#2A6399",
         "#1C4C7D", "#0F335C"],
        N=len(labels),
    )

    def bin_color(v: float) -> str:
        if np.isnan(v): return "#EEEEEE"
        for i in range(len(edges) - 1):
            if edges[i] <= v < edges[i + 1]:
                return mcolors.to_hex(cmap(i / (len(labels) - 1)))
        return mcolors.to_hex(cmap(1.0))

    fig, ax = plt.subplots(figsize=(13, 10.5))
    label_points: dict[str, tuple[float, float, float]] = {}

    for feat in gj["features"]:
        name = feat["properties"]["name"]
        gdp = d24.get(name, np.nan)
        # 香港/澳门/台湾 在本项目不使用，留白
        face = bin_color(gdp) if not np.isnan(gdp) else "#F4F4F4"
        patches = []
        for ring in iter_polygons(feat["geometry"]):
            patches.append(Polygon(np.array(ring), closed=True))
        pc = PatchCollection(patches, facecolor=face, edgecolor="white", linewidth=0.6)
        ax.add_collection(pc)

        # 为每省计算一个标签位置（最大多边形的几何中心）
        if not np.isnan(gdp):
            biggest = max(iter_polygons(feat["geometry"]), key=lambda r: len(r))
            arr = np.array(biggest)
            cx, cy = arr[:, 0].mean(), arr[:, 1].mean()
            # 手工修正几个地理中心偏移较大的省
            fixes = {
                "内蒙古自治区": (112, 43.5), "甘肃省": (101, 38),
                "黑龙江省": (128, 48), "新疆维吾尔自治区": (84, 41.5),
            }
            if name in fixes:
                cx, cy = fixes[name]
            label_points[name] = (cx, cy, gdp)

    # 标注
    for name, (cx, cy, v) in label_points.items():
        short = name.replace("省", "").replace("市", "").replace("自治区", "").replace("壮族", "").replace("回族", "").replace("维吾尔", "")
        ax.text(cx, cy + 0.4, short, ha="center", va="bottom", fontsize=8,
                color="#1A1A1A", fontweight="bold")
        ax.text(cx, cy - 0.4, f"{v:.1f}", ha="center", va="top", fontsize=8, color="#333")

    ax.set_xlim(72, 136); ax.set_ylim(17, 54)
    ax.set_aspect(1.25)
    ax.set_axis_off()

    # 自定义 legend（色块 + 区间）
    from matplotlib.patches import Patch
    n_bins = len(labels)
    handles = [Patch(facecolor=mcolors.to_hex(cmap(i / (n_bins - 1))),
                     edgecolor="white", label=f"{labels[i]} 万亿")
               for i in range(n_bins)]
    ax.legend(handles=handles, loc="lower left", frameon=False,
              fontsize=9.5, title="2024 年 GDP 区间",
              title_fontsize=10, bbox_to_anchor=(0.01, 0.01))

    fig.subplots_adjust(top=0.90, bottom=0.05, left=0.02, right=0.98)
    editorial_title(fig,
                    "东南沿海深蓝，西部高原浅淡：2024 年省级 GDP 分布",
                    "颜色越深表示该省 2024 年 GDP 总量越高。"
                    "粤苏两省独占深蓝，鲁浙川豫紧随其后。")
    source_footer(fig, "分层设色 Choropleth · GeoJSON: 阿里云 DataV")
    save_fig(fig, "task2_choropleth")
    print("✓ outputs/task2_choropleth.png")


if __name__ == "__main__":
    main()
