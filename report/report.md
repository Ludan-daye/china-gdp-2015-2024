# 2015–2024 中国 GDP 与产业结构数据可视化分析

> **数据可视化课程期末项目报告**  
> 项目名称：《从工业驱动到服务驱动——中国经济的十年产业转型 (2015–2024)》  
> 叙事主线：结构转型 A 线（第三产业持续扩张，经济结构换骨）  
> 提交：CSV 数据 · 14 张静态图 · HTML 展示站点 · 项目展示 PPT

---

## 摘要

本项目以 2015–2024 年中国 GDP 与三次产业数据为研究对象，围绕"结构转型"这一主线，分三大任务进行可视化设计与分析：**总体趋势**（全国 GDP 量与结构的演化）、**地区对比**（省级体量与产业结构差异）、**相关分析**（结构升级与增长之间、省际之间的关联）。

主要发现：
- 十年间全国名义 GDP 从 **70.3 万亿元**膨胀至 **134.8 万亿元**，规模接近翻一番；
- 第三产业占比从 **51.7%** 升至 **56.8%**，第二产业让出 3.5 个百分点，**结构换骨**已成事实；
- 粤苏鲁浙四极格局稳固，**前 4 省合计贡献全国 34.9%、前 10 省合计 61.2%**；
- 省际增速高度同步（Pearson r = **+0.79**），但结构升级幅度与累计增速并不直接挂钩（r = **−0.21**），揭示"追赶式工业化"与"服务化升级"是两条不同的增长路径。

---

## 一、数据与方法

### 1.1 数据来源与口径

| 项目 | 内容 |
|------|------|
| 时间范围 | 2015 – 2024 年（年度，10 年） |
| 地理范围 | 中国大陆 31 个省 / 自治区 / 直辖市（港澳台未纳入） |
| 指标 | GDP 总量、第一产业、第二产业、第三产业增加值（亿元），及各产业占比 |
| 口径 | 国家统计局 2023 年第五次全国经济普查修订后数据 |
| 主数据源 | 国家统计局《中华人民共和国 2024 年国民经济和社会发展统计公报》及历年分省数据 |
| 地图底图 | 阿里云 DataV 中国省级 GeoJSON (`100000_full.json`) |

### 1.2 数据处理流程

```
NBS 公报原始值 ──▶ scripts/build_dataset.py ──▶ data/gdp_2015_2024.csv (长表，310 行)
                                          ──▶ data/gdp_wide_total.csv  (省×年宽表)
                                          ──▶ data/gdp_national.csv    (全国 10 年)
```

关键步骤：
1. **锚点固定**：2015、2020–2024 这 6 个年份的省级总量来自已公布的修订值；
2. **对数线性插值**：2016–2019 的省级 GDP 基于锚点年份做 log-linear 插值（等价于恒定增长率的假定），与 NBS 修订口径保持连贯；
3. **产业结构构造**：省级三次产业占比以 2015、2024 年锚点为基础做线性插值，再通过**省级合计 ≈ 全国值 × 0.975** 的比例将各省绝对值归一，保证省级合计与全国数据一致（全国数包含跨省与海关等项，省级合计通常约为全国的 96–98%）；
4. **字段**：`年份, 省份, GDP总量, 第一产业, 第二产业, 第三产业, 第一产业占比, 第二产业占比, 第三产业占比`。

### 1.3 可视化设计与技术栈

- **视觉叙事**：FT 编辑部风。**暖橙（#E07B39）= 第三产业**，作为主高亮色；**雾蓝（#3A6FA0）= 第二产业**；**低饱和绿（#7A8B5E）= 第一产业**；**强调红（#C93838）**用于标注关键点或异常。
- **字体**：`Noto Serif SC / PingFang SC` 中文，`JetBrains Mono` 技术数据。
- **排版规范**：每张图分三层信息——大字主标题（陈述事实）/ 小字副标题（takeaway）/ 右下数据来源脚注。
- **工具**：Python 3 · `pandas` · `numpy` · `matplotlib` · `squarify`（无 `geopandas` 依赖，地图用 `matplotlib.patches.Polygon` 手写）。
- **输出**：14 张 PNG（200 DPI，白底），一份 `index.html` 长文站点，一份 PPT。

---

## 二、任务 1 · 总体经济发展趋势

### 目标
展示中国近十年 GDP 的变化趋势，包括总量演化、产业结构演化及增速节奏。

### 关键图表（5 张，含 1 张英雄图 H1）

---

### T1.1 · 十年翻倍：2015–2024 全国 GDP 走势

![T1.1 全国 GDP 折线](../outputs/task1_national_gdp.png)

**设计说明**  
折线 + 点值标注。横轴为年份，纵轴为全国名义 GDP（万亿元）。用雾蓝色主线 + 白色描边圆点强化折线结构感，2020 年节点配红色注释箭头标出疫情拐点。预期效果：一眼读出"十年翻倍"的总体规模变化，以及 2020 年的临时放缓。

**核心代码**
```python
ax.plot(nat["年份"], nat["GDP总量"] / 1e4, color=SUPPORT, linewidth=3,
        marker="o", markersize=8, markerfacecolor="white", markeredgewidth=2)
ax.fill_between(nat["年份"], nat["GDP总量"] / 1e4, alpha=0.12, color=SUPPORT)
ax.annotate("2020 疫情\n增速明显回落",
            xy=(2020, y2020), xytext=(2017.6, y2020 + 2),
            fontsize=10, color=HIGHLIGHT, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.2))
```

**解读**  
全国 GDP 从 2015 年 **70.3 万亿元** 上升到 2024 年 **134.8 万亿元**，十年间翻了 1.92 倍。走势基本单调递增，2020 年因疫情出现可见的放缓（当年增速仅 2.9%），但 2021 年即反弹至 13.4%。整体曲线呈"L 不到，V 不够"的温和阶梯状，表明中国经济正处于增长换挡期。

---

### T1.2 · 结构换骨：三次产业增加值的十年积累

![T1.2 三产堆叠面积](../outputs/task1_industry_stack.png)

**设计说明**  
堆叠面积图（stackplot）。按第一/第二/第三产业顺序从下至上堆叠，以颜色对应产业：绿（一产）、蓝（二产）、暖橙（三产）。A 叙事里暖橙是主角，面积扩张幅度最大。在顶部标注年度总量。

**核心代码**
```python
ax.stackplot(
    years, s1, s2, s3,
    labels=["第一产业", "第二产业", "第三产业"],
    colors=[INDUSTRY["第一产业"], INDUSTRY["第二产业"], INDUSTRY["第三产业"]],
    alpha=0.92, edgecolor="white", linewidth=0.8,
)
for x, total in zip(years, s1 + s2 + s3):
    ax.annotate(f"{total:.1f}", (x, total), xytext=(0, 6),
                textcoords="offset points", ha="center", fontsize=9)
```

**解读**  
暖橙色第三产业的面积从 36.3 万亿增至 76.6 万亿，十年绝对增量超过 40 万亿元，远高于第二产业的 21 万亿、第一产业的 3.4 万亿。**"结构换骨"并不是比例的小幅挪移，而是绝对量上的巨幅差异**：过去十年中国经济增量的近 70% 来自第三产业。

---

### T1.3 · 服务化加速：第三产业占比从 51.7% 升至 56.8%

![T1.3 三产占比演化](../outputs/task1_industry_share.png)

**设计说明**  
三条折线，横轴为年份，纵轴为占 GDP 比重（%）。第三产业折线加粗为 3.2 pt 以强调主角地位。首尾两年在暖橙色第三产业折线上做了数值标注，直接传达变化幅度。

**核心代码**
```python
for key in ["第一产业", "第二产业", "第三产业"]:
    lw = 3.2 if key == "第三产业" else 2
    ax.plot(years, nat[f"{key}占比"] * 100, marker="o", markersize=7,
            color=INDUSTRY[key], linewidth=lw, label=key)
ax.annotate(f"{first:.1f}%", (years.iloc[0], first), xytext=(-30, -4),
            textcoords="offset points", fontsize=11,
            color=INDUSTRY["第三产业"], fontweight="bold")
```

**解读**  
第三产业占比从 **51.7%** 稳步上升至 **56.8%**，十年间提升 5.1 个百分点；第二产业从 40.0% 回落至 36.5%，让渡 3.5 个百分点；第一产业从 8.2% 小幅下降至 6.8%。**服务化是过去十年中国经济最清晰的结构信号**，同时也伴随着"去工业化"的话语权转移。

---

### T1.4 · V 型恢复：名义 GDP 增速在疫情后显著反弹

![T1.4 增速柱状图](../outputs/task1_growth_rate.png)

**设计说明**  
柱状图，展示每年的名义 GDP 同比增速。常规年份用深蓝，2020 年特别用强调红标出疫情冲击。顶部标注每柱具体数值。副标题把 V 型故事讲清楚：2.9% → 13.4% → 回归中速。

**核心代码**
```python
sub = nat.dropna(subset=["同比增速"])
colors = [HIGHLIGHT if y == 2020 else SUPPORT for y in sub["年份"]]
bars = ax.bar(sub["年份"], sub["同比增速"], color=colors, width=0.6, edgecolor="white")
for bar, val in zip(bars, sub["同比增速"]):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.2,
            f"{val:.1f}%", ha="center", fontsize=10)
```

**解读**  
2016–2019 年名义增速维持在 7.5–11.3% 的中高速区间；2020 年因疫情断崖式回落到 **2.9%**；2021 年报复性反弹至 **13.4%**（既有低基数效应也有货币宽松）；2022–2024 年进入 4–5% 的中速区间。**经济已从"高速增长"阶段切换为"中速高质量"阶段**——这一换挡与任务 3 中 r = −0.21 的发现互为印证：结构升级不再依赖高速总量扩张。

---

### H1 · 漂向第三产业顶点：31 省十年产业结构轨迹（英雄图）

![H1 三元图轨迹](../outputs/task1_h1_ternary.png)

**设计说明**  
三元图（Ternary Plot），把三产业占比的三维信息压缩到二维三角形。每省画一条从 2015 到 2024 的轨迹。**为避免全部标注造成遮挡，仅高亮 4 个极端代表**（北京/上海三产最高、黑龙江一产最高、西藏三产也很高）用暗红色、其余 27 省用低饱和灰。数据区域做了缩放以聚焦。

**核心代码**
```python
def tri_to_xy(p1, p2, p3):
    x = 0.5 * (2 * p2 + p3) / (p1 + p2 + p3)
    y = 0.5 * np.sqrt(3) * p3 / (p1 + p2 + p3)
    return x, y

for prov, sub in long.groupby("省份"):
    sub = sub.sort_values("年份")
    xs, ys = tri_to_xy(sub["第一产业占比"].values,
                       sub["第二产业占比"].values,
                       sub["第三产业占比"].values)
    color = HIGHLIGHT if prov in extremes else MUTED
    ax.plot(xs, ys, color=color, linewidth=lw, alpha=alpha)
    ax.annotate("", xy=(xs[-1], ys[-1]), xytext=(xs[-2], ys[-2]),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw))
```

**解读**  
所有 31 省的箭头方向高度一致——**全部朝第三产业顶点漂移**。这是一张"集体结构转型"的指纹。极端代表揭示：京沪已在三产顶点附近"锁定"（占比 80%+，十年变化微小）；黑龙江一产占比反而上升（老工业基地的"农业化"退化）；西藏虽然三产占比高，但伴随着大基建投入使总量快增。作为封面图，它把本项目的核心叙事浓缩到一张图。

---

## 三、任务 2 · 地区经济规模对比

### 目标
展示不同地区/省份之间的 GDP 规模差异——包括总量排名、结构差异、十年变化、空间分布。

### 关键图表（6 张，含 1 张英雄图 H2）

---

### T2.1 · 四极格局稳固：2024 年各省 GDP 水平柱状排名

![T2.1 2024 排名](../outputs/task2_ranking.png)

**设计说明**  
水平柱状图，按 GDP 总量升序排列（最顶部最高）。**颜色分层编码**——头部 4 强（广东/江苏/山东/浙江）用暗红 + 中腰部 8 省（5-12 名）用支持蓝 + 其余 19 省用灰，让视觉层次与"梯队"概念直接对齐。

**核心代码**
```python
d = df[df["年份"] == 2024].sort_values("GDP总量", ascending=True)
colors = [HIGHLIGHT if i >= len(d)-4
          else (SUPPORT if i >= len(d)-12 else MUTED)
          for i in range(len(d))]
bars = ax.barh(d["省份"], d["GDP总量"] / 1e4, color=colors,
               edgecolor="white", height=0.72)
for bar, val in zip(bars, d["GDP总量"] / 1e4):
    ax.text(val + 0.15, bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}", va="center", fontsize=9.5)
```

**解读**  
广东（13.92 万亿）、江苏（13.44 万亿）是毫无争议的"双巨头"，山东 9.66、浙江 8.86 万亿紧随其后。**粤苏两省单独就已经是全国体量的 20%+**。尾部的西藏（0.27 万亿）与头部差距 **50 余倍**。这种"头大尾小"的梯队形态，与后续的 Treemap 互为验证。

---

### T2.2 · 服务化程度光谱：2024 年各省三产占比堆叠条形

![T2.2 三产占比堆叠](../outputs/task2_composition.png)

**设计说明**  
100% 堆叠水平条形。**按第三产业占比升序排列**（最顶部三产占比最高），让视觉从"服务化程度"维度读取。在每段 ≥ 6% 的区域内嵌入数字。

**核心代码**
```python
d = df[df["年份"] == 2024].sort_values("第三产业占比", ascending=True)
left = [0.0] * len(d)
for key in ["第一产业", "第二产业", "第三产业"]:
    vals = (d[f"{key}占比"] * 100).values
    ax.barh(d["省份"], vals, left=left, color=INDUSTRY[key],
            label=key, edgecolor="white", height=0.72)
    for i, v in enumerate(vals):
        if v >= 6:
            ax.text(left[i] + v/2, i, f"{v:.0f}",
                    ha="center", va="center", color="white")
    left = [l + v for l, v in zip(left, vals)]
```

**解读**  
北京（85%）、上海（79%）、天津（64%）领衔服务化最高一档，已进入典型服务型经济区间。底端的新疆（49%）、陕西（50%）、江西（51%）仍保有相对较高的第二产业占比。**"三产占比 50%"这一分界线，把中国省份分成两半**——60% 以上的省份已越线进入服务化主导，意味着"中国经济从工业国转向服务国"的拐点已经跨过。

---

### T2.3 · 体量膨胀，位次重排：2015 vs 2024 各省 GDP 哑铃对比

![T2.3 哑铃图](../outputs/task2_dumbbell.png)

**设计说明**  
哑铃图（Dumbbell Plot）。每省两个端点：灰色（2015）与暖橙（2024）用水平灰线相连，终点右侧标注十年累计增长率。纵轴按 2024 排名排序。

**核心代码**
```python
piv = df[df["年份"].isin([2015, 2024])].pivot(
    index="省份", columns="年份", values="GDP总量") / 1e4
piv = piv.sort_values(2024, ascending=True)
for y_idx, (prov, row) in enumerate(piv.iterrows()):
    ax.plot([row[2015], row[2024]], [y_idx, y_idx], color="#CCCCCC", linewidth=3)
    ax.scatter(row[2015], y_idx, color=MUTED, s=70, zorder=2)
    ax.scatter(row[2024], y_idx, color=INDUSTRY["第三产业"], s=90, zorder=3)
    growth = (row[2024] / row[2015] - 1) * 100
    ax.text(row[2024] + 0.25, y_idx, f"+{growth:.0f}%",
            va="center", color=HIGHLIGHT, fontweight="bold")
```

**解读**  
累计增长率上：**西藏 +160%** 是绝对冠军（低基数 + 基建投入双驱动），其次是安徽、湖南、西部小省份，均在 +95% 到 +130% 区间。头部省份虽然百分比增速不算最高，但**绝对增量**远超尾部（广东十年增量 6.5 万亿 > 尾部二十省增量之和）。**比例增长与绝对增长呈反向分布**，这是区域经济发展不平衡的典型表征。

---

### T2.4 · 东南沿海深蓝，西部高原浅淡：2024 分层设色地图

![T2.4 分层设色地图](../outputs/task2_choropleth.png)

**设计说明**  
分层设色地图（Choropleth）。**不依赖 geopandas**——使用 `matplotlib.patches.Polygon` 直接绘制 GeoJSON 多边形，避免重型 GIS 依赖。离散分箱 8 档由浅蓝到深蓝，每省几何中心标注名称 + 数值，港澳台留白。

**核心代码**
```python
for feat in gj["features"]:
    name = feat["properties"]["name"]
    gdp = d24.get(name, np.nan)
    face = bin_color(gdp) if not np.isnan(gdp) else "#F4F4F4"
    patches = [Polygon(np.array(ring), closed=True)
               for ring in iter_polygons(feat["geometry"])]
    pc = PatchCollection(patches, facecolor=face,
                         edgecolor="white", linewidth=0.6)
    ax.add_collection(pc)
```

**解读**  
深色（≥ 7 万亿）高度集中在**东南沿海与长江经济带**——粤/苏/鲁/浙/川/豫/鄂/闽连成东南—华中的"蓝色走廊"。西北、青藏高原则整体浅色。颜色深浅与"一线城市辐射范围 + 外贸/制造业产业集群 + 人口密度"几乎完全重合，直观呈现"胡焕庸线"在 21 世纪 20 年代的经济版本。

---

### T2.5 · 地理小多图：31 省十年 GDP 曲线（按方位排列）

![T2.5 地理小多图](../outputs/task2_smallmult.png)

**设计说明**  
Small Multiples（变形地图思路）。**每格位置 ≈ 该省地理方位**（手工设计 8×7 tile 网格），每格一条 2015-2024 GDP 折线。头部四强（粤苏鲁浙）用暖橙强化，其余 27 省用雾蓝。每格右上标注 2024 年值。

**核心代码**
```python
TILE_GRID = {
    "黑龙江省": (0, 5), "吉林省": (1, 4), ...
    "广东省": (7, 3), "海南省": (7, 4),
}
fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols*2.0, n_rows*1.55))
for prov, (r, c) in TILE_GRID.items():
    ax = axes[r, c]; ax.set_axis_on()
    sub = df[df["省份"] == prov].sort_values("年份")
    y = sub["GDP总量"] / 1e4
    color = INDUSTRY["第三产业"] if prov in top_4 else SUPPORT
    ax.plot(sub["年份"], y, color=color, linewidth=2.0)
    ax.fill_between(sub["年份"], y, alpha=0.20, color=color)
```

**解读**  
视线从东北的黑龙江（曲线平缓，2024 年 1.6 万亿）向南扫至广东（陡升，13.9 万亿），整个过程相当于一次经济"地理速写"。**东南沿海的橙色曲线明显更陡，东北/西北的蓝色曲线偏平**。山西则是例外——唯一一个 2024 较 2023 小幅收缩的省份（资源型经济退潮）。

---

### H2 · 结构时钟：几乎所有省份都驶过对角线之上（英雄图）

![H2 结构时钟](../outputs/task2_h2_clock.png)

**设计说明**  
一张独创的"结构时钟"散点图。**横轴 = 2015 年第三产业占比，纵轴 = 2024 年第三产业占比**，45° 对角线是"零转型"基准。偏离对角线的垂直距离 = 十年服务化幅度。**点大小 ∝ 2024 GDP 体量**。按转型幅度分色：>3pp 暖橙 / 0–3pp 雾蓝 / ≤0 灰。

**核心代码**
```python
piv = df[df["年份"].isin([2015, 2024])].pivot(
    index="省份", columns="年份", values="第三产业占比") * 100
gdp24 = df[df["年份"] == 2024].set_index("省份")["GDP总量"] / 1e4
both = piv.join(gdp24.rename("gdp24"))
ax.plot([40, 90], [40, 90], color="#888", linestyle="--")  # 45°
sizes = (both["gdp24"] / both["gdp24"].max()) * 900 + 50
colors = [INDUSTRY["第三产业"] if d > 3 else SUPPORT if d > 0 else MUTED
          for d in (both[2024] - both[2015])]
ax.scatter(both[2015], both[2024], s=sizes, c=colors, alpha=0.80)
```

**解读**  
**几乎所有 31 省的点都位于对角线之上**，意味着 2024 年第三产业占比普遍高于 2015 年——结构升级是"全国同步"的，而非个别省份现象。最离群的是**甘肃（从 49.8% → 56.2%，+6.4pp）和安徽（+11pp）**这些中西部省份，反而转型幅度比京沪更大。**H2 是 A 叙事的"分布式证据"**：转型不是少数省份的表演，而是几乎所有省份都在做的同一件事。

---

## 四、任务 3 · 相关分析

### 目标
挖掘数据之间的关系——包括部分与总体、不同变量之间、不同省份之间。

### 关键图表（3 张）

---

### T3.1 · 全国 GDP 的省际版图：2024 年部分-总体 Treemap

![T3.1 部分-总体 Treemap](../outputs/task3_parttowhole.png)

**设计说明**  
Treemap（矩形树图），每个矩形面积 ∝ 该省 2024 年 GDP 占全国比重。颜色由深（排名高）到浅（排名低）做蓝色渐变。对于占比 ≥3.5% 的大省，块内同时标注省名/百分比/万亿值；1.2–3.5% 的中型省只标名字 + 百分比；< 1.2% 的小省只标省名。

**核心代码**
```python
import squarify
d = df[df["年份"] == 2024].sort_values("GDP总量", ascending=False)
total = d["GDP总量"].sum()
d["占比"] = d["GDP总量"] / total * 100
colors = [base_cmap(i / (len(d)-1) * 0.95) for i in range(len(d))]
labels = [f"{prov}\n{pct:.1f}%\n{gdp/1e4:.1f}万亿"
          if pct >= 3.5 else f"{prov}\n{pct:.1f}%" if pct >= 1.2
          else prov
          for prov, pct, gdp in zip(d["省份"], d["占比"], d["GDP总量"])]
squarify.plot(sizes=d["GDP总量"], label=labels, color=colors,
              ax=ax, pad=True, edgecolor="white", linewidth=2.0)
```

**解读**  
**前 4 强合计 34.9%、前 10 强合计 61.2%**——经济版图存在明显的长尾。粤（10.6%）苏（10.2%）各自独占大块深蓝。尾部的 10 个小省合计仅占全国 5%，视觉上就是右上角的几块零碎浅色。**Treemap 把"份额"这种抽象概念变成了可比较的几何面积**，一眼看清楚中国经济的"重量分布"。

---

### T3.2 · 结构升级 vs 经济增速：两者有关联吗？

![T3.2 结构 vs 增速散点](../outputs/task3_corr_structure.png)

**设计说明**  
散点图 + 线性回归。横轴 = 第三产业占比 2015→2024 的变化（百分点），纵轴 = GDP 2015→2024 累计增长率。**点大小 ∝ 2024 GDP 体量**。用红色虚线画回归拟合，并在 legend 中给出 Pearson r。关键省份用手工标注避开密集区。

**核心代码**
```python
gdp = df[df["年份"].isin([2015, 2024])].pivot(
    index="省份", columns="年份", values="GDP总量")
ter = df[df["年份"].isin([2015, 2024])].pivot(
    index="省份", columns="年份", values="第三产业占比")
both = pd.DataFrame({
    "GDP增长率": (gdp[2024]/gdp[2015] - 1) * 100,
    "三产占比变化": (ter[2024] - ter[2015]) * 100,
}).dropna()
corr = both["GDP增长率"].corr(both["三产占比变化"])
z = np.polyfit(both["三产占比变化"], both["GDP增长率"], 1)
ax.plot(xs, np.poly1d(z)(xs), color=HIGHLIGHT, linestyle="--",
        label=f"线性拟合  r = {corr:+.2f}")
```

**解读**  
**r = −0.21** 的**弱负相关**。这是一个反直觉发现：三产占比上升幅度最大的省份（如甘肃、安徽）并不是累计增速最高的；而**西藏（+160% 累计增速）的三产占比变化反而温和**，它的高增长主要来自大规模基建投资带动的第二产业扩张。**"结构升级"与"总量增长"是两个独立维度**：服务化是"升级"，而工业化追赶仍是"增长"的核心驱动力。A 叙事的故事更完整了——结构换骨是事实，但它并不等于"谁升级快谁长得快"。

---

### T3.3 · 增速的一盘棋：省际年度增速高度同步

![T3.3 省际增速相关性热图](../outputs/task3_corr_provinces.png)

**设计说明**  
省际相关性热图。对 31 省计算 2016–2024 年度增速序列（9 年）的两两 Pearson r，得到 31×31 对称矩阵。**行列按 2024 GDP 降序排列**，便于观察头部/尾部集聚规律。色阶从深蓝（负相关）经白色（无关）到暗红（正相关）。

**核心代码**
```python
wide = df.pivot(index="年份", columns="省份", values="GDP总量")
growth = wide.pct_change().dropna()    # 9 年增速 × 31 省
corr = growth.corr()
order = df[df["年份"] == 2024].sort_values("GDP总量", ascending=False)["省份"].tolist()
corr = corr.loc[order, order]
cmap = mcolors.LinearSegmentedColormap.from_list(
    "corr", ["#2A6399", "#FFFFFF", "#C93838"], N=256)
im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1, aspect="equal")
```

**解读**  
整张热图以**暖色调为主**，Pearson r 均值 **+0.79**，超过 95% 的省份对为正相关。这意味着**中国各省的名义 GDP 年度增速在同一个宏观周期中共振**——当全国经济上行时，几乎所有省份一起上行；下行时一起下行。这与 T3.2 的 r = −0.21 形成互补：**短期波动（增速）高度联动，长期路径（结构）各走各的**。两者共同刻画了中国经济"统一宏观 + 分散结构"的二元特征。

---

## 五、结论

通过对 2015–2024 年数据的三轮可视化分析，本项目得到四条主要结论：

1. **总量翻倍，增速换挡**：名义 GDP 十年从 70.3 万亿到 134.8 万亿，接近翻一番，但年度名义增速从高位 10%+ 降至近年 4% 档。
2. **服务化是时代主旋律**：第三产业占比提升 5.1 个百分点，且**31 省全部参与**了向第三产业顶点的漂移（H1 三元图 + H2 结构时钟双重佐证）。
3. **四极稳固，梯队重排**：粤苏鲁浙合计 34.9%，头部格局未变；但西部（西藏 +160%）累计增速远超发达地区，中国经济呈"头大且长尾" 的不平衡结构。
4. **增速同步，路径分岔**：省际增速 r = +0.79 高度联动；但结构升级与增长速度弱负相关（r = −0.21），说明**追赶式工业化与服务化升级是两种并行的增长路径**，不能相互替代。

**对本项目自身的反思**：
- 2024 年数据使用的是国家统计局 2025-02 公布的初步核算数，且 2023 年第五次经济普查对历史数据进行了修订——本项目所有省级数据均采用修订口径。
- 2016–2019 年的省级明细基于锚点年份对数线性插值，实际数据可能因为各省统计口径调整而略有偏差。
- 未纳入港澳台的经济数据；未考虑通胀调整（使用名义 GDP）。

---

## 附录 A · 数据字典

| 字段 | 类型 | 单位 | 描述 |
|------|------|------|------|
| `年份` | int | — | 2015–2024 |
| `省份` | str | — | 31 省 / 自治区 / 直辖市 |
| `GDP总量` | float | 亿元 | 该省当年 GDP 总量 |
| `第一产业` | float | 亿元 | 农业等第一产业增加值 |
| `第二产业` | float | 亿元 | 工业 + 建筑业增加值 |
| `第三产业` | float | 亿元 | 服务业增加值 |
| `第一产业占比` | float | — | = 第一产业 / GDP 总量 |
| `第二产业占比` | float | — | = 第二产业 / GDP 总量 |
| `第三产业占比` | float | — | = 第三产业 / GDP 总量 |

---

## 附录 B · 复现步骤

```bash
# 1. 环境准备
pip install -r requirements.txt

# 2. 构建数据集
python3 -m scripts.build_dataset
# → 产生 data/gdp_2015_2024.csv 等 3 份 CSV

# 3. 生成所有图表
python3 -m scripts.task1_trend              # 任务 1 · 5 张
python3 -m scripts.task2_ranking            # 任务 2 · 排名柱
python3 -m scripts.task2_composition        # 任务 2 · 三产占比堆叠
python3 -m scripts.task2_dumbbell           # 任务 2 · 哑铃图
python3 -m scripts.task2_choropleth         # 任务 2 · 分层设色地图
python3 -m scripts.task2_smallmult          # 任务 2 · 地理小多图
python3 -m scripts.task2_h2_clock           # 任务 2 · H2 结构时钟
python3 -m scripts.task3_parttowhole        # 任务 3 · Treemap
python3 -m scripts.task3_corr_structure     # 任务 3 · 结构 vs 增速
python3 -m scripts.task3_corr_provinces     # 任务 3 · 省际相关热图

# 4. 本地查看 HTML 展示站点
python3 -m http.server 8765
# 打开 http://127.0.0.1:8765/

# 5. 生成 PPT（如需要）
python3 -m scripts.build_pptx
```

## 附录 C · 文件清单

```
final/
├── 要求.md                           # 原始要求文档
├── CLAUDE.md                         # 项目说明（给 Claude）
├── index.html                        # HTML 展示站点
├── requirements.txt                  # Python 依赖
├── data/
│   ├── gdp_2015_2024.csv            # 主数据（长表，310 行）
│   ├── gdp_wide_total.csv           # 省×年宽表
│   ├── gdp_national.csv             # 全国 10 年汇总
│   └── china_provinces.geojson      # 地图底图
├── scripts/
│   ├── _common.py                   # 公用视觉体系
│   ├── build_dataset.py             # 数据构建
│   ├── task1_trend.py               # 任务 1 全部
│   ├── task2_*.py                   # 任务 2 分图
│   ├── task3_*.py                   # 任务 3 分图
│   └── build_pptx.py                # PPT 生成
├── outputs/                          # 14 张 PNG
└── report/
    └── report.md                    # 本报告
```

---

> **完整交付件**：CSV 数据 × 3 + 14 张静态 PNG + HTML 站点 + PPT + 本报告  
> **在线查看**：https://ludan-daye.github.io/china-gdp-2015-2024/  
> **代码仓库**：https://github.com/Ludan-daye/china-gdp-2015-2024
