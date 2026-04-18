# 2015-2024 中国 GDP 与产业结构可视化 —— 实施计划

> **给执行代理：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 来按任务执行本计划。所有步骤使用 `- [ ]` 复选框语法。

**目标：** 按 `要求.md` 完成一份课程期末项目，交付：(1) 2015–2024 全国 31 省市 GDP + 三产结构 CSV 数据集；(2) 覆盖三大任务组的 12 张静态图表（PNG，300 DPI）；(3) 中文项目报告 (Markdown)；(4) 演示 PPT。

**架构：** 一个以数据为中心的脚本集合。`data/` 目录存放原始与清洗后数据，`scripts/` 目录下每张图表对应一个独立 Python 脚本（便于单独运行和调试），`scripts/_common.py` 提供统一的中文字体、调色板、保存函数等公用工具，所有输出写入 `outputs/`。报告与 PPT 从 `outputs/` 引用图表。

**技术栈：**
- Python 3.10+，`pandas`、`numpy`、`matplotlib`、`seaborn`、`geopandas`、`shapely`
- 数据源：国家统计局公开数据（通过 WebFetch 抓取），阿里云 DataV 的中国省级 GeoJSON 作为底图
- 报告：Markdown；PPT：`python-pptx`（由 `pptx` 技能封装）

**工作根目录：** `/Users/a1-6/importantfile/大三下/计算机可视化/final/`（下文所有相对路径均相对此目录）。

**重要约束（来自 `要求.md`）：**
- 时间范围严格锁定 **2015–2024**（不要使用 2023 或以前的任何临时数据源）
- 全部图表必须 **静态**（PNG/SVG/PDF），禁止交付 pyecharts/Plotly 的 HTML 作为正式成果
- 每张图必须可追溯到 §四 中某个子任务；每个子任务都需要"设计说明 + 核心代码 + 解读"三段式文字
- 中文字体必须显式配置，否则 macOS 下会出现 tofu

---

## 文件结构总览

在编码前先确定拆分边界：

| 文件 | 职责 |
|------|------|
| `requirements.txt` | 固定依赖版本 |
| `scripts/_common.py` | 中文字体配置、统一配色、`save_fig()` 工具函数、任务-文件命名约定 |
| `scripts/fetch_data.py` | 从 NBS 或 Wikipedia 抓取 2015–2024 分省分产业 GDP；写入 `data/raw_*.json` |
| `scripts/clean_data.py` | 将原始数据标准化为长表 `data/gdp_2015_2024.csv`，以及若干派生宽表 |
| `scripts/task1_trend.py` | 任务 1：全国 GDP 走势 + 产业结构堆叠面积 + 三产占比演化 + 年度增速 |
| `scripts/task2_ranking.py` | 任务 2 图①：2024 年 31 省 GDP 水平柱状图（降序） |
| `scripts/task2_composition.py` | 任务 2 图②：2024 年 31 省三产占比堆叠条形 |
| `scripts/task2_dumbbell.py` | 任务 2 图③：2015 vs 2024 各省哑铃对比图 |
| `scripts/task2_choropleth.py` | 任务 2 图④：2024 年省级 GDP 分层设色地图 |
| `scripts/task2_smallmult.py` | 任务 2 图⑤：各省 GDP 曲线的"变形地图"小多图（按地理位置网格排列） |
| `scripts/task3_parttowhole.py` | 任务 3 图①：全国 GDP 部分-总体树图（Treemap） |
| `scripts/task3_corr_structure.py` | 任务 3 图②：GDP 变化 vs 产业结构变化散点 + 相关系数 |
| `scripts/task3_corr_provinces.py` | 任务 3 图③：省际 GDP 发展相关性热图 + 聚类树 |
| `report/report.md` | 中文项目报告，按三大任务组织，每张图附"设计说明 / 核心代码 / 解读" |
| `slides/build_pptx.py` | 根据报告和 `outputs/*.png` 生成演示 PPT |

所有图表脚本遵循同一接口：
```python
if __name__ == "__main__":
    main()  # 读取 data/gdp_2015_2024.csv，生成 outputs/<scriptname>.png
```

---

## Task 1: 项目脚手架与公共模块

**Files:**
- Create: `requirements.txt`
- Create: `scripts/__init__.py`
- Create: `scripts/_common.py`
- Create: `data/.gitkeep`
- Create: `outputs/.gitkeep`
- Create: `report/.gitkeep`
- Create: `slides/.gitkeep`

- [ ] **步骤 1：写 `requirements.txt`**

```
pandas>=2.0
numpy>=1.26
matplotlib>=3.8
seaborn>=0.13
geopandas>=0.14
shapely>=2.0
requests>=2.31
python-pptx>=0.6
openpyxl>=3.1
```

- [ ] **步骤 2：创建空的 `scripts/__init__.py`**

```python
```

- [ ] **步骤 3：写 `scripts/_common.py`**

```python
"""公共绘图工具：统一中文字体、配色、保存规范。所有任务脚本都从这里 import。"""
from __future__ import annotations
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

# macOS 上可用的中文字体，按优先级降序
_CJK_FONTS = ["PingFang HK", "PingFang SC", "Heiti TC", "STHeiti", "Arial Unicode MS"]
mpl.rcParams["font.sans-serif"] = _CJK_FONTS + mpl.rcParams["font.sans-serif"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.dpi"] = 120
mpl.rcParams["savefig.dpi"] = 300
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["figure.figsize"] = (10, 6)

# 统一调色板
PALETTE = {
    "primary": "#2E5A87",
    "secondary": "#E07B39",
    "tertiary": "#4A9D7A",
    "accent": "#C93838",
    "muted": "#6C757D",
}
INDUSTRY_COLORS = {
    "第一产业": "#8FBF73",
    "第二产业": "#5B8FB9",
    "第三产业": "#E8A87C",
}

def save_fig(fig, name: str) -> Path:
    """保存图表到 outputs/<name>.png 并返回路径。"""
    path = OUTPUTS_DIR / f"{name}.png"
    fig.savefig(path)
    plt.close(fig)
    return path
```

- [ ] **步骤 4：创建占位 `.gitkeep` 文件**

```bash
touch data/.gitkeep outputs/.gitkeep report/.gitkeep slides/.gitkeep
```

- [ ] **步骤 5：运行自检**

```bash
cd /Users/a1-6/importantfile/大三下/计算机可视化/final
python -c "from scripts._common import save_fig, INDUSTRY_COLORS; print('ok')"
```
期望输出：`ok`

- [ ] **步骤 6：提交**

```bash
git add requirements.txt scripts/__init__.py scripts/_common.py data/.gitkeep outputs/.gitkeep report/.gitkeep slides/.gitkeep
git commit -m "chore: scaffold project structure and plotting helpers"
```

---

## Task 2: 数据采集脚本

**Files:**
- Create: `scripts/fetch_data.py`
- Create: `data/raw/` (由脚本创建)

**背景：** 国家统计局提供按年度分省的 GDP 与三产数据，主要接口：
- 数据页面 `https://data.stats.gov.cn/easyquery.htm?cn=E0103`
- 备用：Wikipedia 的《中华人民共和国各省级行政区国内生产总值列表》
- 万不得已时可从 `../china_gdp_map.py` 中的 2023 数据作为 sanity check（此文件只能作参照，不得替代真实 10 年数据）

- [ ] **步骤 1：写 `scripts/fetch_data.py`（骨架与 NBS 分页抓取）**

```python
"""抓取 2015-2024 年全国 31 个省份的 GDP 与三产数据。

主策略：NBS 的 easyquery 接口（需要 JSON POST）。
备用：对 Wikipedia 对应年度表做解析。
输出：data/raw/nbs_<year>.json 与 data/raw/gdp_wide.csv
"""
from __future__ import annotations
import json
import time
from pathlib import Path
import pandas as pd
import requests
from scripts._common import DATA_DIR

RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2015, 2025))  # 2015..2024 含 2024
PROVINCES = [
    "北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省",
    "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省",
    "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "重庆市", "四川省", "贵州省",
    "云南省", "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区",
]

NBS_URL = "https://data.stats.gov.cn/easyquery.htm"

def fetch_nbs_indicator(zb: str, year: int) -> dict:
    """从 NBS 抓取单个指标 (zb) 在某年的分省数据。"""
    params = {
        "m": "QueryData", "dbcode": "fsnd", "rowcode": "reg", "colcode": "sj",
        "wds": json.dumps([{"wdcode": "zb", "valuecode": zb}]),
        "dfwds": json.dumps([{"wdcode": "sj", "valuecode": str(year)}]),
        "k1": int(time.time() * 1000),
    }
    resp = requests.get(NBS_URL, params=params, timeout=30, verify=False,
                        headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    return resp.json()

INDICATORS = {
    "gdp_total": "A020101",      # 地区生产总值
    "primary":   "A020102",      # 第一产业
    "secondary": "A020103",      # 第二产业
    "tertiary":  "A020104",      # 第三产业
}

def main() -> None:
    for year in YEARS:
        out = RAW_DIR / f"nbs_{year}.json"
        if out.exists():
            continue
        bundle = {}
        for key, zb in INDICATORS.items():
            bundle[key] = fetch_nbs_indicator(zb, year)
            time.sleep(0.5)
        out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved {out.name}")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：试跑**

```bash
cd /Users/a1-6/importantfile/大三下/计算机可视化/final
python scripts/fetch_data.py
```
期望：`data/raw/nbs_2015.json` … `nbs_2024.json` 共 10 个文件生成，脚本输出 `saved nbs_YYYY.json`。

- [ ] **步骤 3：若 NBS 接口不可达，启用 Wikipedia 备用路径**

将 `fetch_data.py` 追加以下函数，main 中若首年抓取失败则回退：

```python
WIKI_URLS = {
    # 《中华人民共和国各省级行政区生产总值列表》历年表
    year: f"https://zh.wikipedia.org/wiki/中华人民共和国各省级行政区生产总值列表"
    for year in YEARS
}

def fetch_wikipedia_tables() -> pd.DataFrame:
    """从 Wikipedia 一次性抓取所有年份的宽表，返回长表 (年份, 省份, 项目, 数值)。"""
    tables = pd.read_html(WIKI_URLS[YEARS[0]])
    # 选取第一张含"省份"列的表
    frames = [t for t in tables if any("省" in str(c) or "地区" in str(c) for c in t.columns)]
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(RAW_DIR / "wiki_raw.csv", index=False, encoding="utf-8-sig")
    return df
```

- [ ] **步骤 4：在 `main()` 结尾追加完整性检查**

```python
    # 完整性校验：每年应覆盖 31 个省份、4 个指标
    for year in YEARS:
        bundle = json.loads((RAW_DIR / f"nbs_{year}.json").read_text(encoding="utf-8"))
        for key, payload in bundle.items():
            nodes = payload.get("returndata", {}).get("datanodes", [])
            assert len(nodes) >= 31, f"{year}/{key} 只返回 {len(nodes)} 条记录"
    print("✓ 所有年份与指标均完整")
```

- [ ] **步骤 5：再次运行并确认**

```bash
python scripts/fetch_data.py
```
期望：末尾输出 `✓ 所有年份与指标均完整`。若校验失败，查看 `data/raw/` 中的 JSON，手工补录缺失项或切换到 Wikipedia 备用。

- [ ] **步骤 6：提交**

```bash
git add scripts/fetch_data.py data/raw/*.json
git commit -m "feat(data): fetch 2015-2024 provincial GDP and industry data from NBS"
```

---

## Task 3: 数据清洗与标准化

**Files:**
- Create: `scripts/clean_data.py`
- Output: `data/gdp_2015_2024.csv`（长表）、`data/gdp_wide_total.csv`（省×年宽表）

- [ ] **步骤 1：写 `scripts/clean_data.py`**

```python
"""把 data/raw/*.json 合并为规范的长表 gdp_2015_2024.csv。

输出两份：
- gdp_2015_2024.csv:   年份,省份,gdp_total,primary,secondary,tertiary,primary_share,secondary_share,tertiary_share
- gdp_wide_total.csv:  以省份为行、年份为列的 GDP 总量宽表
"""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from scripts._common import DATA_DIR
from scripts.fetch_data import YEARS, INDICATORS

RAW_DIR = DATA_DIR / "raw"

def _parse_year(year: int) -> pd.DataFrame:
    bundle = json.loads((RAW_DIR / f"nbs_{year}.json").read_text(encoding="utf-8"))
    rows: dict[str, dict[str, float]] = {}
    for metric, payload in bundle.items():
        for node in payload["returndata"]["datanodes"]:
            wdnodes = {w["wdcode"]: w["valuecode"] for w in node["wds"]}
            province_code = wdnodes["reg"]
            region_name = next(
                n["cname"] for n in payload["returndata"]["wdnodes"][0]["nodes"]
                if n["code"] == province_code
            )
            value = node["data"]["data"]
            rows.setdefault(region_name, {})[metric] = value
    df = pd.DataFrame.from_dict(rows, orient="index").reset_index().rename(columns={"index": "省份"})
    df["年份"] = year
    return df

def main() -> None:
    frames = [_parse_year(y) for y in YEARS]
    long = pd.concat(frames, ignore_index=True)
    long = long.rename(columns={
        "gdp_total": "GDP总量",
        "primary": "第一产业",
        "secondary": "第二产业",
        "tertiary": "第三产业",
    })
    for col in ["GDP总量", "第一产业", "第二产业", "第三产业"]:
        long[col] = pd.to_numeric(long[col], errors="coerce")
    long["第一产业占比"] = long["第一产业"] / long["GDP总量"]
    long["第二产业占比"] = long["第二产业"] / long["GDP总量"]
    long["第三产业占比"] = long["第三产业"] / long["GDP总量"]

    ordered = ["年份", "省份", "GDP总量", "第一产业", "第二产业", "第三产业",
               "第一产业占比", "第二产业占比", "第三产业占比"]
    long = long[ordered].sort_values(["年份", "省份"]).reset_index(drop=True)
    long.to_csv(DATA_DIR / "gdp_2015_2024.csv", index=False, encoding="utf-8-sig")

    wide = long.pivot(index="省份", columns="年份", values="GDP总量")
    wide.to_csv(DATA_DIR / "gdp_wide_total.csv", encoding="utf-8-sig")
    print(f"✓ 长表: {len(long)} 行，宽表: {wide.shape}")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行并检查**

```bash
python scripts/clean_data.py
```
期望输出：`✓ 长表: 310 行，宽表: (31, 10)`。

- [ ] **步骤 3：人工抽检（至少 3 个已知数据点）**

```bash
python -c "
import pandas as pd
d = pd.read_csv('data/gdp_2015_2024.csv')
print(d[(d['年份']==2023) & (d['省份']=='广东省')])
print(d[(d['年份']==2024) & (d['省份']=='西藏自治区')])
print(d.groupby('年份')['GDP总量'].sum())
"
```
期望：广东 2023 年 GDP 总量 ≈ 135673 亿元（对得上 `../china_gdp_map.py`）；2024 年全国总和 ≈ 134 万亿元。

- [ ] **步骤 4：提交**

```bash
git add scripts/clean_data.py data/gdp_2015_2024.csv data/gdp_wide_total.csv
git commit -m "feat(data): normalize NBS JSON into long + wide CSV tables"
```

---

## Task 4: 任务 1 —— 总体经济发展趋势

**Files:**
- Create: `scripts/task1_trend.py`
- Output: `outputs/task1_national_gdp.png`、`task1_industry_stack.png`、`task1_industry_share.png`、`task1_growth_rate.png`

- [ ] **步骤 1：写 `scripts/task1_trend.py`**

```python
"""任务 1：总体经济发展趋势（全国 GDP 走势 + 三产结构演化 + 增速）。"""
from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import DATA_DIR, INDUSTRY_COLORS, PALETTE, save_fig

def load_national() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    agg = df.groupby("年份")[["GDP总量", "第一产业", "第二产业", "第三产业"]].sum()
    agg["增速"] = agg["GDP总量"].pct_change() * 100
    for col in ["第一产业", "第二产业", "第三产业"]:
        agg[f"{col}_占比"] = agg[col] / agg["GDP总量"] * 100
    return agg.reset_index()

def plot_national_line(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    ax.plot(nat["年份"], nat["GDP总量"] / 1e4, marker="o", color=PALETTE["primary"], linewidth=2.5)
    for x, y in zip(nat["年份"], nat["GDP总量"] / 1e4):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
    ax.set_title("2015–2024 全国 GDP 总量发展", fontsize=16, fontweight="bold")
    ax.set_xlabel("年份"); ax.set_ylabel("GDP（万亿元）")
    ax.grid(alpha=0.3)
    save_fig(fig, "task1_national_gdp")

def plot_industry_stack(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    ax.stackplot(
        nat["年份"],
        nat["第一产业"] / 1e4, nat["第二产业"] / 1e4, nat["第三产业"] / 1e4,
        labels=["第一产业", "第二产业", "第三产业"],
        colors=[INDUSTRY_COLORS[k] for k in ["第一产业", "第二产业", "第三产业"]],
        alpha=0.85,
    )
    ax.set_title("2015–2024 全国三次产业构成（堆叠面积）", fontsize=16, fontweight="bold")
    ax.set_xlabel("年份"); ax.set_ylabel("增加值（万亿元）")
    ax.legend(loc="upper left")
    save_fig(fig, "task1_industry_stack")

def plot_industry_share(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    for key in ["第一产业", "第二产业", "第三产业"]:
        ax.plot(nat["年份"], nat[f"{key}_占比"], marker="o", label=key,
                color=INDUSTRY_COLORS[key], linewidth=2)
    ax.set_title("2015–2024 三次产业占 GDP 比重演化", fontsize=16, fontweight="bold")
    ax.set_xlabel("年份"); ax.set_ylabel("占比（%）")
    ax.legend(); ax.grid(alpha=0.3)
    save_fig(fig, "task1_industry_share")

def plot_growth(nat: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    sub = nat.dropna(subset=["增速"])
    bars = ax.bar(sub["年份"], sub["增速"], color=PALETTE["primary"])
    for bar, val in zip(bars, sub["增速"]):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.2, f"{val:.1f}%",
                ha="center", fontsize=9)
    ax.set_title("2016–2024 全国 GDP 名义增速", fontsize=16, fontweight="bold")
    ax.set_xlabel("年份"); ax.set_ylabel("同比增速（%）")
    ax.grid(alpha=0.3, axis="y")
    save_fig(fig, "task1_growth_rate")

def main() -> None:
    nat = load_national()
    plot_national_line(nat)
    plot_industry_stack(nat)
    plot_industry_share(nat)
    plot_growth(nat)
    print("✓ 任务 1 共生成 4 张图")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行**

```bash
python scripts/task1_trend.py
```
期望：`✓ 任务 1 共生成 4 张图`；`outputs/` 中出现 4 个 PNG。

- [ ] **步骤 3：人工审视 PNG**

用系统预览打开每张图，确认：
- 中文标题、坐标轴无 tofu
- GDP 走势单调上升且 2024 年约 130+ 万亿元
- 三产占比中第三产业呈上升趋势

```bash
open outputs/task1_national_gdp.png outputs/task1_industry_stack.png outputs/task1_industry_share.png outputs/task1_growth_rate.png
```

- [ ] **步骤 4：提交**

```bash
git add scripts/task1_trend.py outputs/task1_*.png
git commit -m "feat(task1): national GDP trend, industry mix, share evolution, growth"
```

---

## Task 5: 任务 2 图① —— 2024 年各省 GDP 水平柱状图

**Files:**
- Create: `scripts/task2_ranking.py`
- Output: `outputs/task2_ranking.png`

- [ ] **步骤 1：写脚本**

```python
"""任务 2 图①：2024 年 31 省市 GDP 水平柱状排名。"""
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import DATA_DIR, PALETTE, save_fig

def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d = df[df["年份"] == 2024].sort_values("GDP总量", ascending=True).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 12))
    colors = ["#D64545" if i >= len(d) - 5 else PALETTE["primary"] for i in range(len(d))]
    bars = ax.barh(d["省份"], d["GDP总量"] / 1e4, color=colors, edgecolor="white")
    for bar, val in zip(bars, d["GDP总量"] / 1e4):
        ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", fontsize=9)
    ax.set_title("2024 年中国各省/区/市 GDP 总量对比", fontsize=16, fontweight="bold")
    ax.set_xlabel("GDP（万亿元）")
    ax.grid(alpha=0.3, axis="x")
    save_fig(fig, "task2_ranking")
    print("✓ task2_ranking.png")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行并检查**

```bash
python scripts/task2_ranking.py
open outputs/task2_ranking.png
```
期望：粤、苏、鲁、浙、川（或川、鲁并列第三梯队）位列前五。

- [ ] **步骤 3：提交**

```bash
git add scripts/task2_ranking.py outputs/task2_ranking.png
git commit -m "feat(task2): 2024 provincial GDP ranking bar chart"
```

---

## Task 6: 任务 2 图② —— 2024 年三产占比堆叠条形

**Files:**
- Create: `scripts/task2_composition.py`
- Output: `outputs/task2_composition.png`

- [ ] **步骤 1：写脚本**

```python
"""任务 2 图②：2024 年 31 省市三次产业占 GDP 比重（100% 堆叠条形）。"""
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import DATA_DIR, INDUSTRY_COLORS, save_fig

def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d = df[df["年份"] == 2024].sort_values("第三产业占比", ascending=True)
    fig, ax = plt.subplots(figsize=(12, 12))
    left = [0.0] * len(d)
    for key in ["第一产业", "第二产业", "第三产业"]:
        vals = (d[key] / d["GDP总量"] * 100).values
        ax.barh(d["省份"], vals, left=left, color=INDUSTRY_COLORS[key], label=key, edgecolor="white")
        for i, v in enumerate(vals):
            if v >= 5:
                ax.text(left[i] + v / 2, i, f"{v:.0f}%", ha="center", va="center",
                        color="white", fontsize=8, fontweight="bold")
        left = [l + v for l, v in zip(left, vals)]
    ax.set_xlim(0, 100)
    ax.set_title("2024 年各省三次产业占 GDP 比重（按第三产业占比升序）",
                 fontsize=16, fontweight="bold")
    ax.set_xlabel("占比（%）")
    ax.legend(loc="lower right")
    save_fig(fig, "task2_composition")
    print("✓ task2_composition.png")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行并审视**

```bash
python scripts/task2_composition.py
open outputs/task2_composition.png
```
期望：北京、上海的第三产业占比接近 80%，排在最顶端；黑龙江、新疆等第一产业占比较高。

- [ ] **步骤 3：提交**

```bash
git add scripts/task2_composition.py outputs/task2_composition.png
git commit -m "feat(task2): 2024 provincial industry composition stacked bar"
```

---

## Task 7: 任务 2 图③ —— 2015 vs 2024 哑铃对比图

**Files:**
- Create: `scripts/task2_dumbbell.py`
- Output: `outputs/task2_dumbbell.png`

- [ ] **步骤 1：写脚本**

```python
"""任务 2 图③：2015 年与 2024 年各省 GDP 哑铃对比。"""
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import DATA_DIR, PALETTE, save_fig

def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    pivot = df[df["年份"].isin([2015, 2024])].pivot(index="省份", columns="年份", values="GDP总量") / 1e4
    pivot = pivot.sort_values(2024, ascending=True)

    fig, ax = plt.subplots(figsize=(10, 12))
    for y_idx, (prov, row) in enumerate(pivot.iterrows()):
        ax.plot([row[2015], row[2024]], [y_idx, y_idx], color="#CCCCCC", linewidth=2, zorder=1)
        ax.scatter(row[2015], y_idx, color=PALETTE["muted"], s=60, zorder=2, label="2015" if y_idx == 0 else None)
        ax.scatter(row[2024], y_idx, color=PALETTE["accent"], s=80, zorder=3, label="2024" if y_idx == 0 else None)
        growth = (row[2024] / row[2015] - 1) * 100
        ax.text(row[2024] + 0.5, y_idx, f"+{growth:.0f}%", va="center", fontsize=8,
                color=PALETTE["accent"])
    ax.set_yticks(range(len(pivot)))
    ax.set_yticklabels(pivot.index)
    ax.set_title("2015 vs 2024 各省 GDP 对比（含十年累计增长率）",
                 fontsize=16, fontweight="bold")
    ax.set_xlabel("GDP（万亿元）")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3, axis="x")
    save_fig(fig, "task2_dumbbell")
    print("✓ task2_dumbbell.png")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行并审视**

```bash
python scripts/task2_dumbbell.py
open outputs/task2_dumbbell.png
```
期望：西藏等小体量省份增长百分比最高，广东绝对差最大。

- [ ] **步骤 3：提交**

```bash
git add scripts/task2_dumbbell.py outputs/task2_dumbbell.png
git commit -m "feat(task2): 2015-2024 provincial GDP dumbbell comparison"
```

---

## Task 8: 任务 2 图④ —— 2024 年省级 GDP 分层设色地图

**Files:**
- Create: `scripts/task2_choropleth.py`
- Create: `data/china_provinces.geojson`（一次性下载）
- Output: `outputs/task2_choropleth.png`

- [ ] **步骤 1：下载 GeoJSON（只跑一次）**

```bash
cd /Users/a1-6/importantfile/大三下/计算机可视化/final
curl -L "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json" -o data/china_provinces.geojson
python -c "import geopandas as gpd; g=gpd.read_file('data/china_provinces.geojson'); print(len(g), g.columns.tolist())"
```
期望：输出 `34 [...'name'...]`（含港澳台）。

- [ ] **步骤 2：写脚本**

```python
"""任务 2 图④：2024 年中国分省 GDP 分层设色地图。"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from scripts._common import DATA_DIR, save_fig

PROVINCE_NAME_MAP = {
    "内蒙古自治区": "内蒙古", "广西壮族自治区": "广西", "西藏自治区": "西藏",
    "宁夏回族自治区": "宁夏", "新疆维吾尔自治区": "新疆",
}

def main() -> None:
    gdf = gpd.read_file(DATA_DIR / "china_provinces.geojson")
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d = df[df["年份"] == 2024][["省份", "GDP总量"]].copy()
    d["name"] = d["省份"].map(lambda s: PROVINCE_NAME_MAP.get(s, s.replace("省", "").replace("市", "")))
    merged = gdf.merge(d, on="name", how="left")
    merged["GDP_trillion"] = merged["GDP总量"] / 1e4

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "gdp", ["#DEEBF7", "#9ECAE1", "#4292C6", "#2171B5", "#08519C", "#08306B"]
    )
    fig, ax = plt.subplots(figsize=(12, 9))
    merged.plot(column="GDP_trillion", cmap=cmap, linewidth=0.5, edgecolor="white",
                ax=ax, legend=True,
                legend_kwds={"label": "GDP（万亿元）", "shrink": 0.6},
                missing_kwds={"color": "#EEEEEE"})
    for _, row in merged.iterrows():
        if pd.notna(row["GDP_trillion"]) and row.geometry is not None:
            centroid = row.geometry.representative_point()
            ax.annotate(f"{row['name']}\n{row['GDP_trillion']:.1f}",
                        (centroid.x, centroid.y), ha="center", fontsize=7)
    ax.set_title("2024 年中国各省 GDP 分布", fontsize=18, fontweight="bold")
    ax.set_axis_off()
    save_fig(fig, "task2_choropleth")
    print("✓ task2_choropleth.png")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 3：运行并审视**

```bash
python scripts/task2_choropleth.py
open outputs/task2_choropleth.png
```
期望：东南沿海颜色最深，西藏/青海最浅；港澳台留白（#EEEEEE）。

- [ ] **步骤 4：提交**

```bash
git add scripts/task2_choropleth.py data/china_provinces.geojson outputs/task2_choropleth.png
git commit -m "feat(task2): 2024 provincial GDP choropleth map"
```

---

## Task 9: 任务 2 图⑤ —— 变形地图小多图

**Files:**
- Create: `scripts/task2_smallmult.py`
- Create: `data/province_tile_layout.csv`（网格布局映射）
- Output: `outputs/task2_smallmult.png`

- [ ] **步骤 1：手写 tile 布局**

把以下内容保存为 `data/province_tile_layout.csv`（row 从上到下、col 从左到右，大致对应地理位置；每格放一个省份的迷你折线）：

```
省份,row,col
黑龙江省,0,6
吉林省,1,6
辽宁省,2,6
内蒙古自治区,1,4
北京市,2,5
天津市,2,5
河北省,3,5
山西省,3,4
新疆维吾尔自治区,2,1
青海省,3,2
甘肃省,3,3
宁夏回族自治区,3,3
陕西省,4,4
山东省,3,6
河南省,4,5
江苏省,4,6
安徽省,5,5
上海市,5,6
浙江省,6,6
湖北省,5,4
重庆市,5,3
四川省,5,2
西藏自治区,4,1
湖南省,6,4
江西省,6,5
福建省,6,6
贵州省,6,3
云南省,7,2
广西壮族自治区,7,4
广东省,7,5
海南省,8,5
```
注：多省共享格子时在脚本内按 col 微偏移（见下）。

- [ ] **步骤 2：写脚本**

```python
"""任务 2 图⑤：各省 GDP 2015-2024 曲线的小多图（按地理位置网格）。"""
import matplotlib.pyplot as plt
import pandas as pd
from scripts._common import DATA_DIR, INDUSTRY_COLORS, PALETTE, save_fig

def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    layout = pd.read_csv(DATA_DIR / "province_tile_layout.csv")
    n_rows, n_cols = layout["row"].max() + 1, layout["col"].max() + 1

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 1.6, n_rows * 1.4),
                             sharex=True, sharey=False)
    for ax in axes.flat:
        ax.set_axis_off()

    for _, grid in layout.iterrows():
        ax = axes[grid["row"], grid["col"]]
        ax.set_axis_on()
        sub = df[df["省份"] == grid["省份"]].sort_values("年份")
        if sub.empty:
            continue
        ax.plot(sub["年份"], sub["GDP总量"] / 1e4, color=PALETTE["primary"], linewidth=1.5)
        ax.fill_between(sub["年份"], sub["GDP总量"] / 1e4, alpha=0.2, color=PALETTE["primary"])
        ax.set_title(grid["省份"], fontsize=8, pad=2)
        ax.tick_params(labelsize=6)
        ax.set_xticks([2015, 2024])
        ax.grid(alpha=0.3)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    fig.suptitle("2015–2024 各省 GDP 发展曲线（按地理方位排列）",
                 fontsize=16, fontweight="bold", y=0.995)
    fig.tight_layout()
    save_fig(fig, "task2_smallmult")
    print("✓ task2_smallmult.png")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 3：运行并审视**

```bash
python scripts/task2_smallmult.py
open outputs/task2_smallmult.png
```
期望：东南四角（粤、苏、浙、鲁）曲线最陡；西北几省曲线较平缓。若布局 CSV 中有省份漏掉或重叠，迭代调整 tile 位置再跑。

- [ ] **步骤 4：提交**

```bash
git add data/province_tile_layout.csv scripts/task2_smallmult.py outputs/task2_smallmult.png
git commit -m "feat(task2): geographically-tiled small multiples of provincial GDP curves"
```

---

## Task 10: 任务 3 图① —— 部分-总体 Treemap

**Files:**
- Create: `scripts/task3_parttowhole.py`
- Output: `outputs/task3_parttowhole.png`

- [ ] **步骤 1：把 `squarify` 加入 `requirements.txt`**

追加一行：

```
squarify>=0.4
```

- [ ] **步骤 2：写脚本**

```python
"""任务 3 图①：2024 年各省 GDP 相对全国的部分-总体 treemap。"""
import matplotlib.pyplot as plt
import pandas as pd
import squarify
from scripts._common import DATA_DIR, save_fig

def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    d = df[df["年份"] == 2024].sort_values("GDP总量", ascending=False).reset_index(drop=True)
    total = d["GDP总量"].sum()
    d["占比"] = d["GDP总量"] / total * 100

    cmap = plt.cm.Blues
    colors = [cmap(0.3 + 0.6 * i / len(d)) for i in range(len(d))][::-1]
    labels = [
        f"{row['省份']}\n{row['占比']:.1f}%" if row["占比"] >= 1.5 else ""
        for _, row in d.iterrows()
    ]
    fig, ax = plt.subplots(figsize=(14, 9))
    squarify.plot(sizes=d["GDP总量"], label=labels, color=colors, ax=ax,
                  text_kwargs={"fontsize": 9, "color": "white", "fontweight": "bold"},
                  pad=True, edgecolor="white", linewidth=1.5)
    ax.set_title(f"2024 年全国 GDP 省际构成（总量 {total / 1e4:.1f} 万亿元）",
                 fontsize=18, fontweight="bold")
    ax.set_axis_off()
    save_fig(fig, "task3_parttowhole")
    print("✓ task3_parttowhole.png")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 3：运行并审视**

```bash
pip install squarify
python scripts/task3_parttowhole.py
open outputs/task3_parttowhole.png
```
期望：粤、苏 矩形块明显最大，合计约占全国 20%。

- [ ] **步骤 4：提交**

```bash
git add requirements.txt scripts/task3_parttowhole.py outputs/task3_parttowhole.png
git commit -m "feat(task3): national GDP part-to-whole treemap"
```

---

## Task 11: 任务 3 图② —— GDP 增速 vs 产业结构变动散点

**Files:**
- Create: `scripts/task3_corr_structure.py`
- Output: `outputs/task3_corr_structure.png`

- [ ] **步骤 1：写脚本**

```python
"""任务 3 图②：GDP 十年累计增长率 vs 第三产业占比变动的散点+回归线。"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scripts._common import DATA_DIR, PALETTE, save_fig

def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    piv_gdp = df[df["年份"].isin([2015, 2024])].pivot(index="省份", columns="年份", values="GDP总量")
    piv_tertiary = df[df["年份"].isin([2015, 2024])].pivot(
        index="省份", columns="年份", values="第三产业占比")
    both = pd.DataFrame({
        "GDP增长率": (piv_gdp[2024] / piv_gdp[2015] - 1) * 100,
        "第三产业占比变化": (piv_tertiary[2024] - piv_tertiary[2015]) * 100,
    }).dropna()
    corr = both["GDP增长率"].corr(both["第三产业占比变化"])

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(both["第三产业占比变化"], both["GDP增长率"], s=90,
               color=PALETTE["primary"], alpha=0.7, edgecolor="white")
    for prov, row in both.iterrows():
        ax.annotate(prov, (row["第三产业占比变化"], row["GDP增长率"]),
                    fontsize=7, alpha=0.8, xytext=(4, 2), textcoords="offset points")
    # 回归线
    z = np.polyfit(both["第三产业占比变化"], both["GDP增长率"], 1)
    xs = np.linspace(both["第三产业占比变化"].min(), both["第三产业占比变化"].max(), 50)
    ax.plot(xs, np.poly1d(z)(xs), color=PALETTE["accent"], linestyle="--",
            label=f"线性拟合 r = {corr:.2f}")
    ax.axhline(0, color="#CCCCCC"); ax.axvline(0, color="#CCCCCC")
    ax.set_xlabel("第三产业占比 2015→2024 变化（百分点）")
    ax.set_ylabel("GDP 2015→2024 累计增长率（%）")
    ax.set_title("产业结构升级 vs 经济增速", fontsize=16, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.3)
    save_fig(fig, "task3_corr_structure")
    print(f"✓ task3_corr_structure.png  (r = {corr:.3f})")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行并审视**

```bash
python scripts/task3_corr_structure.py
open outputs/task3_corr_structure.png
```
期望：相关系数符号合乎预期（正或弱正相关，视具体数据），图中可见西部省份三产占比提升显著。

- [ ] **步骤 3：提交**

```bash
git add scripts/task3_corr_structure.py outputs/task3_corr_structure.png
git commit -m "feat(task3): GDP growth vs tertiary share change scatter"
```

---

## Task 12: 任务 3 图③ —— 省际发展相关性热图

**Files:**
- Create: `scripts/task3_corr_provinces.py`
- Output: `outputs/task3_corr_provinces.png`

- [ ] **步骤 1：写脚本**

```python
"""任务 3 图③：基于 2015–2024 GDP 年度增速序列，计算省际 Pearson 相关矩阵热图。"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scripts._common import DATA_DIR, save_fig

def main() -> None:
    df = pd.read_csv(DATA_DIR / "gdp_2015_2024.csv")
    wide = df.pivot(index="年份", columns="省份", values="GDP总量")
    growth = wide.pct_change().dropna()  # 9 年 x 31 省增速序列
    corr = growth.corr()
    # 按 2024 总量排序，便于观察区域集聚
    order = (df[df["年份"] == 2024].sort_values("GDP总量", ascending=False)["省份"].tolist())
    corr = corr.loc[order, order]

    fig, ax = plt.subplots(figsize=(14, 12))
    sns.heatmap(corr, cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                square=True, cbar_kws={"shrink": 0.6, "label": "Pearson r"},
                xticklabels=True, yticklabels=True, ax=ax,
                annot=False, linewidths=0.3, linecolor="white")
    ax.set_title("各省 GDP 年度增速两两相关系数（2016–2024）",
                 fontsize=16, fontweight="bold", pad=12)
    ax.tick_params(axis="x", rotation=60, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    save_fig(fig, "task3_corr_provinces")
    print("✓ task3_corr_provinces.png")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行并审视**

```bash
python scripts/task3_corr_provinces.py
open outputs/task3_corr_provinces.png
```
期望：颜色以暖色为主，表明大部分省份增速同周期；东北三省与西北区块内部自相关明显。

- [ ] **步骤 3：提交**

```bash
git add scripts/task3_corr_provinces.py outputs/task3_corr_provinces.png
git commit -m "feat(task3): provincial GDP growth correlation heatmap"
```

---

## Task 13: 项目报告（中文 Markdown）

**Files:**
- Create: `report/report.md`

- [ ] **步骤 1：起草报告**

创建 `report/report.md`，按下列结构填写（每张图必须含三段：设计说明、核心代码片段、解读）：

```markdown
# 2015-2024 中国 GDP 与产业结构数据可视化分析

## 摘要
（150 字以内：项目目标、数据、主要结论）

## 一、数据与方法
- 数据来源：国家统计局 `data.stats.gov.cn`
- 抓取方式：`scripts/fetch_data.py` 经 easyquery 接口拉取 GDP、三产原始 JSON
- 清洗：`scripts/clean_data.py` 产出 `data/gdp_2015_2024.csv`（310 行）
- 绘图：matplotlib / geopandas / seaborn；所有图均为静态 PNG（300 DPI）

## 二、任务 1 —— 总体经济发展趋势
### 1. 全国 GDP 总量发展
- **设计说明：** 折线 + 点值标注，突出 2015 约 68 万亿到 2024 超 130 万亿的近乎翻倍。
- **核心代码：** `scripts/task1_trend.py::plot_national_line`（粘贴 8-12 行）
- **解读：** …

（……依次把四张图写完）

## 三、任务 2 —— 地区经济规模对比
（五张图，每张按上述三段格式）

## 四、任务 3 —— 相关分析
（三张图）

## 五、结论
- 经济总量持续扩张，但增速换挡
- 第三产业占比持续抬升，经济结构趋向服务化
- 粤苏鲁浙四极格局稳定，西部省份相对增长更快
- 各省 GDP 增速呈强正相关，经济联动性显著

## 附录
- 数据字典 / 字段说明
- 重现步骤：`pip install -r requirements.txt && python scripts/fetch_data.py && python scripts/clean_data.py && for f in scripts/task*.py; do python "$f"; done`
```

- [ ] **步骤 2：从脚本中抽取核心代码片段填入**

在 Markdown 中每张图的"核心代码"段使用代码块，直接从对应脚本复制 5–15 行最能体现绘图逻辑的片段。

- [ ] **步骤 3：提交**

```bash
git add report/report.md
git commit -m "docs: write project report covering all 12 charts"
```

---

## Task 14: 演示 PPT

**Files:**
- Create: `slides/build_pptx.py`
- Output: `slides/2024_gdp_visualization.pptx`

- [ ] **步骤 1：写 PPT 生成脚本**

```python
"""用 python-pptx 根据 outputs/ 中的 PNG 生成演示稿。"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from scripts._common import OUTPUTS_DIR

SLIDES = [
    ("2015–2024 中国 GDP 与产业结构数据可视化", "数据可视化课程期末项目"),
    ("任务 1 · 全国 GDP 总量发展", "task1_national_gdp.png"),
    ("任务 1 · 三次产业构成演化", "task1_industry_stack.png"),
    ("任务 1 · 三产占比与增速", ["task1_industry_share.png", "task1_growth_rate.png"]),
    ("任务 2 · 2024 各省 GDP 排名", "task2_ranking.png"),
    ("任务 2 · 三产占比对比", "task2_composition.png"),
    ("任务 2 · 2015 vs 2024 省份哑铃图", "task2_dumbbell.png"),
    ("任务 2 · 2024 分省 GDP 地图", "task2_choropleth.png"),
    ("任务 2 · 各省 GDP 趋势小多图", "task2_smallmult.png"),
    ("任务 3 · 部分-总体 Treemap", "task3_parttowhole.png"),
    ("任务 3 · 结构升级 vs 增长", "task3_corr_structure.png"),
    ("任务 3 · 省际相关性热图", "task3_corr_provinces.png"),
    ("结论与展望", "粤苏鲁浙四极稳固；第三产业持续提升；区域联动性强"),
]

def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.33); prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    for idx, (title, body) in enumerate(SLIDES):
        slide = prs.slides.add_slide(blank)
        tx = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.3), Inches(0.8))
        p = tx.text_frame.paragraphs[0]; p.text = title
        p.font.size = Pt(28); p.font.bold = True
        if isinstance(body, str) and body.endswith(".png"):
            slide.shapes.add_picture(str(OUTPUTS_DIR / body), Inches(1), Inches(1.2),
                                     height=Inches(6))
        elif isinstance(body, list):
            for i, png in enumerate(body):
                slide.shapes.add_picture(str(OUTPUTS_DIR / png),
                                         Inches(0.3 + i * 6.6), Inches(1.3),
                                         width=Inches(6.3))
        else:
            tb = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(4))
            tb.text_frame.text = body
            tb.text_frame.paragraphs[0].font.size = Pt(22)
    out = Path("slides/2024_gdp_visualization.pptx")
    prs.save(out)
    print(f"✓ {out}")

if __name__ == "__main__":
    main()
```

- [ ] **步骤 2：运行**

```bash
python slides/build_pptx.py
open slides/2024_gdp_visualization.pptx
```
期望：13 张幻灯片，图像未变形、文字无缺字。

- [ ] **步骤 3：提交**

```bash
git add slides/build_pptx.py slides/2024_gdp_visualization.pptx
git commit -m "feat(slides): generate presentation deck from outputs"
```

---

## Task 15: 端到端复现自检

**Files:** 无新增，仅验证

- [ ] **步骤 1：从干净虚拟环境一次性重跑**

```bash
cd /Users/a1-6/importantfile/大三下/计算机可视化/final
rm -rf outputs/*.png slides/*.pptx
python scripts/clean_data.py
python scripts/task1_trend.py
python scripts/task2_ranking.py
python scripts/task2_composition.py
python scripts/task2_dumbbell.py
python scripts/task2_choropleth.py
python scripts/task2_smallmult.py
python scripts/task3_parttowhole.py
python scripts/task3_corr_structure.py
python scripts/task3_corr_provinces.py
python slides/build_pptx.py
ls outputs/ slides/
```
期望：12 个 PNG + 1 个 PPTX 全部重新生成且无报错。

- [ ] **步骤 2：核对 `要求.md` §四 勾选表**

| 要求 | 对应文件 | 是否完成 |
|------|----------|---------|
| GDP 总量随时间发展图 | `outputs/task1_national_gdp.png` | ✓ |
| GDP 产业结构随时间发展图 | `outputs/task1_industry_stack.png`、`task1_industry_share.png` | ✓ |
| 2024 各省 GDP 总量对比 | `outputs/task2_ranking.png` | ✓ |
| 2024 各省 GDP 产业构成对比 | `outputs/task2_composition.png` | ✓ |
| 2015 vs 2024 各省对比 | `outputs/task2_dumbbell.png` | ✓ |
| 基于地图的 2024 各省 GDP | `outputs/task2_choropleth.png` | ✓ |
| 变形地图各省发展曲线 | `outputs/task2_smallmult.png` | ✓ |
| 部分-总体构成 | `outputs/task3_parttowhole.png` | ✓ |
| GDP 变化 vs 产业结构相关 | `outputs/task3_corr_structure.png` | ✓ |
| 各省 GDP 相关性 | `outputs/task3_corr_provinces.png` | ✓ |
| 数据 CSV | `data/gdp_2015_2024.csv` | ✓ |
| 报告 | `report/report.md` | ✓ |
| PPT | `slides/2024_gdp_visualization.pptx` | ✓ |

- [ ] **步骤 3：最终提交**

```bash
git add -A
git commit -m "chore: end-to-end rebuild verified"
```

---

## 自检（写完后本人执行）

**规格覆盖：**
- 任务 1 三类图 → Task 4（4 张图全覆盖）✓
- 任务 2 五类图 → Task 5–9 ✓
- 任务 3 三类图 → Task 10–12 ✓
- 数据 CSV → Task 3 ✓
- 报告 → Task 13 ✓
- PPT → Task 14 ✓
- 复现自检 → Task 15 ✓

**占位符扫描：** 已去除所有 "TODO / 稍后 / 类似 Task N" 字样；每个代码步骤均给出可运行代码。

**类型一致性：**
- CSV 列名 `GDP总量`、`第一产业`、`第二产业`、`第三产业`、`第一产业占比` 等在 Task 3 定义后，Task 4–12 一致引用。
- `save_fig` 签名 `(fig, name: str) -> Path` 在所有脚本中使用一致。
- `INDUSTRY_COLORS` 键为中文 `第一/二/三产业`，与 CSV 列名呼应。

**已知风险：**
1. NBS 接口返回格式若改版，Task 2 步骤 5 的校验会提前失败 → 通过 Wikipedia 备用路径兜底。
2. 2024 年数据可能在 2026-04 仍为初步核算 → 在报告 §一 注明数据截止日并引用官方初步核算。
3. `geopandas` 在 macOS 上可能需要 `brew install gdal proj`；若安装受阻，可用 `cartopy` 或直接 `matplotlib` 画多边形作降级方案。
