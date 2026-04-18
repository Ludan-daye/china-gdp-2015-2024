"""公共绘图工具：统一 FT 编辑部风视觉体系 + 中文字体。"""
from __future__ import annotations
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DATA_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

# macOS 中文字体优先级
_CJK_FONTS = [
    "PingFang SC", "PingFang HK", "Heiti SC", "Heiti TC",
    "STHeiti", "Songti SC", "Arial Unicode MS",
]
mpl.rcParams["font.sans-serif"] = _CJK_FONTS + mpl.rcParams["font.sans-serif"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.dpi"] = 120
mpl.rcParams["savefig.dpi"] = 200
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["figure.figsize"] = (11, 6.5)
mpl.rcParams["figure.facecolor"] = "#FFFFFF"
mpl.rcParams["axes.facecolor"] = "#FFFFFF"
mpl.rcParams["axes.edgecolor"] = "#333333"
mpl.rcParams["axes.labelcolor"] = "#222222"
mpl.rcParams["xtick.color"] = "#333333"
mpl.rcParams["ytick.color"] = "#333333"
mpl.rcParams["axes.spines.top"] = False
mpl.rcParams["axes.spines.right"] = False

# FT 编辑部风配色（结构转型叙事：第三产业 = 暖橙主角）
BG = "#F5F1E8"          # 米白背景
INK = "#1E1E1E"
MUTED = "#7A8B8F"

INDUSTRY = {
    "第一产业": "#7A8B5E",   # 低饱和绿
    "第二产业": "#3A6FA0",   # 雾蓝
    "第三产业": "#E07B39",   # 暖橙 —— A 叙事的主角
}
HIGHLIGHT = "#C93838"      # 暗红 · 强调/注释
SUPPORT = "#2C5F8D"        # 深蓝 · 次强调

DATA_SOURCE = "数据来源：国家统计局《中华人民共和国 2024 年国民经济和社会发展统计公报》及各年度分省数据"


def editorial_title(fig, title: str, subtitle: str = "") -> None:
    """FT 风三行标题：大字主标题 + 小字 takeaway 副标题。

    调用前必须已经 fig.subplots_adjust(top=0.80) 预留顶部空间。
    """
    fig.text(0.03, 0.945, title, fontsize=17, fontweight="bold", color=INK, ha="left")
    if subtitle:
        fig.text(0.03, 0.895, subtitle, fontsize=10.5,
                 color="#555555", ha="left", style="italic")
    # 标题下方细分隔线
    fig.add_artist(plt.Line2D([0.03, 0.97], [0.865, 0.865],
                              color="#CCCCCC", linewidth=0.8,
                              transform=fig.transFigure))


def source_footer(fig, extra: str = "") -> None:
    text = DATA_SOURCE + (f"  |  {extra}" if extra else "")
    fig.text(0.03, 0.015, text, fontsize=8, color=MUTED, ha="left", alpha=0.9)


def save_fig(fig, name: str) -> Path:
    path = OUTPUTS_DIR / f"{name}.png"
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return path
