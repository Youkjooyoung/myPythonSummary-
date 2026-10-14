# 수집한 인파밀집 데이터(v02_1_crowd_data.py 결과)로 그래프 그리기
# data 폴더에서 가장 최근 CSV를 읽어 PNG로 저장합니다.

import csv
import glob
import os
import sys

# conda 환경이 활성화되지 않은 터미널에서 matplotlib DLL 오류가 나는 것 방지
conda_bin = os.path.join(sys.prefix, "Library", "bin")
if os.name == "nt" and os.path.isdir(conda_bin):
    os.environ["PATH"] = conda_bin + os.pathsep + os.environ["PATH"]

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# 혼잡도 단계별 색 (여유 → 붐빔)
LEVEL_COLORS = {
    "여유": "#0ca30c",
    "보통": "#fab219",
    "약간 붐빔": "#ec835a",
    "붐빔": "#d03b3b",
}
BAR_COLOR = "#2a78d6"
INK = "#0b0b0b"
INK_SUB = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"

plt.rcParams.update({
    "font.family": "Malgun Gothic",  # 한글 폰트
    "axes.unicode_minus": False,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_SUB,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


# 1. 가장 최근 CSV 읽기
def read_latest(pattern):
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"{pattern} 파일이 없습니다. 먼저 v02_1_crowd_data.py 를 실행하세요.")
        sys.exit()
    with open(files[-1], "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f)), files[-1]


now_rows, now_file = read_latest("data/crowd_now_*.csv")
fc_rows, _ = read_latest("data/crowd_forecast_*.csv")
stamp = now_file.split("crowd_now_")[1].replace(".csv", "")
print(f"읽은 파일: {now_file} (장소 {len(now_rows)}곳)")


def level_legend(ax, loc="upper right"):
    handles = [Patch(color=c, label=lv) for lv, c in LEVEL_COLORS.items()]
    ax.legend(handles=handles, title="혼잡도", frameon=False, loc=loc)


def style_grid(ax, axis):
    ax.grid(axis=axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


# 그래프 1, 2는 첫 번째 장소 기준 (여러 곳이면 혼잡도가 가장 높은 곳)
LEVEL_ORDER = list(LEVEL_COLORS)
target = max(now_rows, key=lambda r: (LEVEL_ORDER.index(r["AREA_CONGEST_LVL"]), int(r["AREA_PPLTN_MAX"])))
name = target["AREA_NM"]

# 2. 그래프 1 - 앞으로 12시간 예상 인구
fc = [r for r in fc_rows if r["AREA_CD"] == target["AREA_CD"]]
hours = [r["FCST_TIME"][-5:] for r in fc]
pop_min = [int(r["FCST_PPLTN_MIN"]) for r in fc]
pop_max = [int(r["FCST_PPLTN_MAX"]) for r in fc]
colors = [LEVEL_COLORS.get(r["FCST_CONGEST_LVL"], MUTED) for r in fc]

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(hours, pop_max, color=colors, width=0.7, edgecolor=SURFACE, linewidth=2)
# 최소~최대 범위를 막대 위 가는 선으로 표시
ax.vlines(hours, pop_min, pop_max, color=INK_SUB, linewidth=2)

peak = pop_max.index(max(pop_max))
ax.annotate(f"최대 {pop_min[peak]:,}~{pop_max[peak]:,}명", (peak, pop_max[peak]),
            xytext=(0, 8), textcoords="offset points", ha="center", color=INK_SUB)

ax.set_title(f"{name} 앞으로 12시간 예상 인구", loc="left", fontsize=14, pad=14)
ax.set_ylabel("인구 (명)")
ax.set_ylim(0, max(pop_max) * 1.15)  # 위쪽 라벨 공간 확보
ax.yaxis.set_major_formatter(lambda v, _: f"{int(v):,}")
style_grid(ax, "y")
level_legend(ax)
fig.tight_layout()
fig.savefig(f"data/chart_forecast_{stamp}.png", dpi=150)
print(f"저장 완료: data/chart_forecast_{stamp}.png")

# 3. 그래프 2 - 연령대별 인구 비율
ages = ["0~9세", "10대", "20대", "30대", "40대", "50대", "60대", "70대 이상"]
keys = ["PPLTN_RATE_0", "PPLTN_RATE_10", "PPLTN_RATE_20", "PPLTN_RATE_30",
        "PPLTN_RATE_40", "PPLTN_RATE_50", "PPLTN_RATE_60", "PPLTN_RATE_70"]
rates = [float(target[k]) for k in keys]

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(ages, rates, color=BAR_COLOR, height=0.6)
ax.invert_yaxis()  # 0~9세가 위로
for y, v in enumerate(rates):
    ax.text(v + 0.4, y, f"{v}%", va="center", color=INK_SUB)

ax.set_title(f"{name} 연령대별 인구 비율 ({target['PPLTN_TIME']})", loc="left", fontsize=14, pad=14)
ax.set_xlabel(f"비율 (%)    남성 {target['MALE_PPLTN_RATE']}% · 여성 {target['FEMALE_PPLTN_RATE']}%")
ax.set_xlim(0, max(rates) * 1.15)
style_grid(ax, "x")
fig.tight_layout()
fig.savefig(f"data/chart_age_{stamp}.png", dpi=150)
print(f"저장 완료: data/chart_age_{stamp}.png")

# 4. 그래프 3 - 장소별 현재 인구 TOP 15 (인증키로 여러 곳을 수집했을 때만)
if len(now_rows) > 1:
    top = sorted(now_rows, key=lambda r: int(r["AREA_PPLTN_MAX"]), reverse=True)[:15]
    names = [r["AREA_NM"] for r in top]
    values = [int(r["AREA_PPLTN_MAX"]) for r in top]
    colors = [LEVEL_COLORS.get(r["AREA_CONGEST_LVL"], MUTED) for r in top]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(names, values, color=colors, height=0.7, edgecolor=SURFACE, linewidth=2)
    ax.invert_yaxis()
    ax.set_title(f"현재 인구가 많은 장소 TOP {len(top)} ({top[0]['PPLTN_TIME']})", loc="left", fontsize=14, pad=14)
    ax.set_xlabel("최대 인구 (명)")
    ax.xaxis.set_major_formatter(lambda v, _: f"{int(v):,}")
    style_grid(ax, "x")
    level_legend(ax, "lower right")
    fig.tight_layout()
    fig.savefig(f"data/chart_top_{stamp}.png", dpi=150)
    print(f"저장 완료: data/chart_top_{stamp}.png")
else:
    print("장소가 1곳뿐이라 장소별 비교 그래프는 건너뜁니다. (인증키로 수집하면 생성됨)")

plt.show()
