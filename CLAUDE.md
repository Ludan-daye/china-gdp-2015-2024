# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

数据可视化课程期末项目：**2015-2024 中国 GDP 与产业结构数据可视化分析**。

Source of truth for scope and deliverables is `要求.md` in this directory. A PDF copy of the spec also lives at `../期末/数据可视化课程期末项目说明书.pdf`.

### Hard constraints from the spec

- **Time range: 2015–2024** (ten years). Do not use 2023-only data even though older drafts in the parent directory (e.g. `../china_gdp_map.py`) use 2023.
- **All charts must be static** (`全部使用静态图表表达`). Do not ship interactive pyecharts/Plotly HTML as a primary deliverable — export to PNG/SVG/PDF.
- **Data must include both GDP totals and three-industry structure** (第一/第二/第三产业 + each industry's share of GDP) per year per province/region.
- **Deliverables** (per §七 提交内容): data files (CSV/Excel), static visualization outputs, project report, presentation PPT.

### Required visualizations (per §四 项目任务)

Three task groups that every chart must clearly belong to:

1. **Overall trend** — national GDP over time; national industry-structure evolution over time.
2. **Regional comparison** — 2024 provincial GDP ranking; 2024 provincial industry composition; 2015-vs-2024 per-province growth; choropleth map of 2024 GDP; cartogram-style small-multiples of per-province GDP trend curves.
3. **Correlation analysis** — part-to-whole composition of national GDP by province (2024); correlation between GDP change and industry-structure change; inter-provincial GDP development correlation.

## Data

Authoritative source: 国家统计局 (National Bureau of Statistics) + 中国统计年鉴. Older pyecharts demo at `../china_gdp_map.py` contains 2023 provincial totals that can serve as a sanity check but is **not** a sufficient dataset on its own.

Canonical dataset schema (see `要求.md` §三 for the example table):

| 年份 | 省份 | GDP | 第一产业 | 第二产业 | 第三产业 |

Store cleaned data as CSV (UTF-8) under `data/` so both Python scripts and the report can consume it.

## Expected repository layout

As implementation proceeds, organize work as:

```
final/
├── 要求.md                # spec (do not modify)
├── CLAUDE.md              # this file
├── data/                  # CSV/Excel sources + cleaned outputs
├── scripts/               # one script per chart family; writes PNGs/SVGs to outputs/
├── outputs/               # rendered static charts (PNG/SVG/PDF)
├── report/                # project report (Markdown or Word)
└── slides/                # presentation PPT
```

## Commands

No build system is wired up yet. Use a fresh Python 3 environment with matplotlib, pandas, and (for the choropleth) a China province shapefile or geopandas + NBS map data. Each visualization script in `scripts/` should be directly runnable via `python scripts/<name>.py` and must write its output into `outputs/`.

When you add dependencies, record them in `requirements.txt` at the repo root.

## Notes for future Claude sessions

- The parent directory (`../`) contains unrelated coursework (`class4/`, `class4.9/`, `4.12/`, `4.16/`) and a bulky `可视化.zip`. Do not touch these — work stays inside `final/`.
- Chinese fonts must be configured explicitly in matplotlib (`plt.rcParams['font.sans-serif']`) or labels will render as tofu boxes on macOS.
- Treat `要求.md` as the spec. If a design choice is ambiguous, re-read it before inventing requirements.
