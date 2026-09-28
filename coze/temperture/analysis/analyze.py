"""
Unit 1 實驗分析：Temperature 與模型大小對 LLM 回答行為的影響

資料來源（上一層資料夾）：
  棒球/T_01.txt, T_05.txt, T_08.txt     gpt-4o mini，temperature 0.1 / 0.5 / 0.8
  棒球/chatgpt4o_mini_T05.txt          gpt-4o mini，T=0.5，max length 8192（模型比較對照組）
  棒球/gemini_flash2_0_T05.txt         Gemini Flash 2.0，T=0.5，max length 8192
  彈珠/T_01.txt, T_05txt, T_08.txt      gpt-4o mini，temperature 0.1 / 0.5 / 0.8

排除規則：
  - 標記「使用到了4o」的回答（誤用 gpt-4o，非 4o mini）
  - Gemini 在 max length 1024 / 4096 下被截斷的回答（test 1~3）

執行：python analyze.py
輸出：results/*.csv、figures/*.png，並在終端機印出摘要
"""
import itertools
import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent
OUT_RES = HERE / "results"
OUT_FIG = HERE / "figures"
OUT_RES.mkdir(exist_ok=True)
OUT_FIG.mkdir(exist_ok=True)

# ---------------------------------------------------------------- 讀檔與切分

def split_tests(path):
    """把檔案依 'test N' 標題切成多筆回答，回傳 [(編號, 標題其餘文字, 內文)]。"""
    text = path.read_text(encoding="utf-8")
    heads = list(re.finditer(r"^test\s*(\d+)[ \t]*(.*)$", text, re.M))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end():end].strip().strip('"').strip()
        out.append((int(m.group(1)), m.group(2).strip(), body))
    return out


def load():
    rows = []
    specs = [
        ("棒球", "棒球/T_01.txt", "4o-mini", 0.1, 1024),
        ("棒球", "棒球/T_05.txt", "4o-mini", 0.5, 1024),
        ("棒球", "棒球/T_08.txt", "4o-mini", 0.8, 1024),
        ("棒球", "棒球/chatgpt4o_mini_T05.txt", "4o-mini", 0.5, 8192),
        ("棒球", "棒球/gemini_flash2_0_T05.txt", "Gemini-Flash-2.0", 0.5, 8192),
        ("彈珠", "彈珠/T_01.txt", "4o-mini", 0.1, 1024),
        ("彈珠", "彈珠/T_05txt", "4o-mini", 0.5, 1024),
        ("彈珠", "彈珠/T_08.txt", "4o-mini", 0.8, 1024),
    ]
    for problem, rel, model, temp, maxlen in specs:
        for n, head, body in split_tests(DATA / rel):
            excluded = ""
            if "4o)" in head or "使用到了4o" in head:
                excluded = "誤用 gpt-4o"
            m_len = re.match(r"(\d{4})", head)
            run_len = int(m_len.group(1)) if m_len else maxlen
            if run_len < 8192 and model.startswith("Gemini"):
                excluded = f"max length {run_len} 截斷"
            m_tok = re.search(r"(\d+)\s*token", head)
            rows.append(dict(
                problem=problem, file=rel, model=model, temp=temp,
                maxlen=run_len, test=n, excluded=excluded,
                tokens=int(m_tok.group(1)) if m_tok else np.nan, text=body,
            ))
    return pd.DataFrame(rows)


def group_label(r):
    if r.model.startswith("Gemini"):
        return "Gemini T0.5"
    suffix = " (8192)" if r.maxlen == 8192 else ""
    return f"4o-mini T{r.temp}{suffix}"

# ---------------------------------------------------------------- 文字相似度

def normalize(text):
    text = re.sub(r"\\[a-zA-Z]+", "", text)            # 去掉 LaTeX 指令
    return "".join(ch for ch in text if ch.isalnum())  # 只留中英文與數字


def bigrams(text):
    t = normalize(text)
    return {t[i:i + 2] for i in range(len(t) - 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 1.0


def pairwise(sets):
    return [jaccard(a, b) for a, b in itertools.combinations(sets, 2)]

# ---------------------------------------------------------------- 棒球：數值

V0, THETA = 20.0, math.radians(37)
EXACT = {g: dict(H=(V0 * math.sin(THETA)) ** 2 / (2 * g),
                 R=V0 ** 2 * math.sin(2 * THETA) / g) for g in (9.8, 9.81)}

OTHER_HEAD = re.compile(r"(#+[^\n]*(其他|討論))|(\*\*其他)")


def main_part(text):
    """截掉「其他模型」討論段，避免抓到那裡提到的數字。"""
    m = OTHER_HEAD.search(text)
    return text[:m.start()] if m else text


def last_number(pattern, text, raw=False):
    hits = re.findall(pattern + r"[^\d\n]{0,40}?(\d+\.\d+)", text)
    if raw:
        return hits[-1] if hits else ""
    return float(hits[-1]) if hits else np.nan


def baseball_numbers(text):
    body = main_part(text)
    g = 9.81 if "9.81" in body else 9.8
    if "15.97" in body:
        trig = "0.7986（4位）"
    elif "15.96" in body:
        trig = "0.798（3位，截位）"
    else:
        trig = "0.8（近似）"
    # 模型自己寫出的 R = v_x × t，拿它自己的兩個數重新相乘，檢查最後一步乘法
    prod = re.findall(r"(1[56]\.\d+|16)[^\d\n]{0,25}?(?:\\cdot|\\times|×|\*)[^\d\n]{0,5}(2\.\d+)", body)
    vx, t = (float(prod[-1][0]), float(prod[-1][1])) if prod else (np.nan, np.nan)
    r_raw = last_number("水平射程", body, raw=True)
    R = float(r_raw) if r_raw else np.nan
    decimals = len(r_raw.split(".")[1]) if "." in r_raw else 0
    # 依模型自己回報的小數位數四捨五入後比較，只把「真的乘錯」算成錯
    wrong = bool(prod) and round(vx * t, decimals) != R
    return dict(H=last_number("最大高度", body), R=R, g=g, trig=trig, vx=vx, t=t,
                R_self=round(vx * t, 3), R_arith_wrong=wrong)

# ---------------------------------------------------------------- 分類編碼

def section(text, start_pat, end_pat):
    m = re.search(start_pat, text)
    if not m:
        return ""
    rest = text[m.end():]
    e = re.search(end_pat, rest)
    return rest[:e.start()] if e else rest


def items(sec):
    """切出條列項目；沒有編號時退而用含冒號的行。"""
    lines = [l.strip() for l in sec.splitlines() if l.strip()]
    numbered = [l for l in lines if re.match(r"^(\d+\.|[*-]\s)", l)]
    if numbered:
        return numbered
    return [l for l in lines if "：" in l[:25]]


def code(item, rules, title_only=False):
    title = re.split(r"[：:]", item, 1)[0]
    target = title if title_only else item
    hits = [name for name, pat in rules if re.search(pat, target)]
    if title_only and not hits:  # 標題沒命中時再看全文
        hits = [name for name, pat in rules if re.search(pat, item)][:1]
    return hits


ASSUMPTION_RULES = [
    ("忽略空氣阻力", r"空氣阻力|真空|只受到?重力"),
    ("重力加速度為常數", r"重力加速度|重力為常數|地球引力|地球重力"),
    ("發射與落地同高/地面平坦", r"同一高度|高度相同|高度相等|平坦|水平面|地面高度|落回|同一水平|地面是水平|地面水平|均為零"),
    ("重述題目給定值", r"(初速度?|初始速度)[^。]*20|仰角[^。]*37|角度[^。]*37"),
    ("速度分解（方法，非假設）", r"分解"),
    ("視為質點", r"質點"),
    ("忽略旋轉（Magnus）", r"旋轉|自旋|馬格"),
    ("無風", r"無風|沒有風|沒有任何風"),
    ("忽略地球曲率", r"曲率|地球是平坦"),
    ("三角函數近似", r"近似值"),
    ("錯誤：速度保持不變", r"(?<![水平加])速度(不變|保持不變|為常數)|方向與大小保持不變"),
]

OTHER_MODEL_RULES = [
    ("空氣阻力", r"空氣阻力|阻力"),
    ("旋轉/Magnus", r"旋轉|自旋|馬格|德雷克"),
    ("風", r"風"),
    ("發射/落地高度差", r"高度差|從高處|高於地面|非平坦|起始高度|發射點高於|落地點低於|擊球點"),
    ("空氣密度/海拔", r"海拔|空氣密度變化|密度越高"),
    ("最佳仰角", r"最佳|45"),
    ("數值方法", r"數值|龍格|模擬"),
    ("軌跡不對稱", r"不對稱|陡峭"),
    ("定量估計影響幅度", r"\d+%|一半"),
]

MECHANISM_RULES = [
    ("熱效應", r"熱"),
    ("接觸時間", r"接觸時間"),
    ("振動/共振", r"振動|共振"),
    ("旋轉", r"旋轉|角動量|傾斜"),
    ("空氣阻力", r"空氣"),
    ("能量損失/恢復係數非線性", r"能量|恢復係數|非線性|非彈性"),
    ("彈珠材料變化", r"疲勞|磨損|變形|內部結構"),
    ("地面性質", r"地面|粗糙"),
]

DESIGN_RULES = [
    ("改變空氣條件（真空/氣壓/風）", r"真空|空氣|風|氣壓"),
    ("更換地面材料", r"地面|木板|混凝土|橡膠"),
    ("高速攝影", r"攝影|高速"),
    ("量測溫度", r"溫度|測溫|紅外"),
    ("顯微/材料檢測", r"顯微|X射線|材料強度|材料分析"),
    ("振動感測", r"振動"),
    ("量測能量/恢復係數", r"能量|恢復係數|動能"),
    ("電腦模擬", r"模擬"),
    ("控制旋轉", r"旋轉"),
]

ERROR_CHECKS = [
    ("捏造名詞「德雷克效應」", r"德雷克"),
    ("算術錯誤 12.04²=145.06", r"145\.06"),
    ("錯誤假設：速度保持不變", r"(?<!水平)速度(不變|保持不變)|方向與大小保持不變"),
    ("上旋標成 Backspin（術語混淆）", r"上旋\s*[（(]\s*Backspin"),
    ("回答混入當下日期（平台注入）", r"現在是\d{4}年"),
]

# ---------------------------------------------------------------- 主流程

def main():
    df = load()
    df["group"] = df.apply(group_label, axis=1)
    df["chars"] = df.text.map(lambda t: len(normalize(t)))
    df["bigrams"] = df.text.map(bigrams)

    used = df[df.excluded == ""].copy()
    print("排除的樣本：")
    print(df[df.excluded != ""][["file", "test", "excluded"]].to_string(index=False), "\n")

    # --- 棒球
    bb = used[used.problem == "棒球"].copy()
    nums = bb.text.map(baseball_numbers).apply(pd.Series)
    bb = pd.concat([bb, nums], axis=1)
    # 假設段：從含「假設」的標題行開始，到下一個標題或計算段為止
    bb["assumptions"] = bb.text.map(lambda t: sorted({c for it in items(section(
        t, r"(#+|\*\*)[^\n]*假設[^\n]*\n",
        r"\n#+|\*\*根據|計算步驟|計算過程|接下來|已知條件|有了這些假設|在這些假設下|\n---"))
        for c in code(it, ASSUMPTION_RULES)}))
    bb["other_models"] = bb.text.map(lambda t: sorted({
        c for c, pat in OTHER_MODEL_RULES if re.search(pat, t[len(main_part(t)):])}))
    bb["errors"] = bb.text.map(lambda t: [n for n, p in ERROR_CHECKS if re.search(p, t)])

    # --- 彈珠
    mb = used[used.problem == "彈珠"].copy()
    split_pat = r"###\s*實驗設計|###\s*設計實驗|為了設計實驗|^實驗設計|為了判斷哪一個機制最重要|為了確定哪一個機制最重要"
    mb["mechanisms"] = mb.text.map(lambda t: [code(it, MECHANISM_RULES, title_only=True)[0]
                                              for it in items(re.split(split_pat, t, 1, flags=re.M)[0])])
    mb["designs"] = mb.text.map(lambda t: sorted({c for it in items(re.split(split_pat, t, 1, flags=re.M)[-1])
                                                  for c in code(it, DESIGN_RULES)}))
    mb["changes_marble"] = mb.text.map(lambda t: bool(re.search(r"更換彈珠|不同的彈珠|換彈珠|不同彈珠", t)))

    # ------------------------------------------------ 表 1：各組摘要
    groups_bb = ["4o-mini T0.1", "4o-mini T0.5", "4o-mini T0.8", "4o-mini T0.5 (8192)", "Gemini T0.5"]
    summary = []
    for g in groups_bb:
        s = bb[bb.group == g]
        sim = pairwise(list(s.bigrams))
        asim = pairwise([set(a) for a in s.assumptions])
        summary.append(dict(
            組別=g, 樣本數=len(s),
            文字Jaccard平均=np.mean(sim), 文字Jaccard標準差=np.std(sim),
            假設集合Jaccard平均=np.mean(asim),
            平均字數=s.chars.mean(), 平均tokens=s.tokens.mean(),
            R平均=s.R.mean(), R標準差=s.R.std(), R相異值數=s.R.nunique(),
            H平均=s.H.mean(), H標準差=s.H.std(), H相異值數=s.H.nunique(),
            平均假設數=s.assumptions.map(len).mean(),
            平均其他模型數=s.other_models.map(len).mean(),
            有錯誤的回答數=int((s.errors.map(len) > 0).sum()),
            R最後乘法算錯數=int(s.R_arith_wrong.sum()),
            算錯時的相異答案數=s[s.R_arith_wrong].R.nunique(),
        ))
    summary = pd.DataFrame(summary)

    mb_summary = []
    for t in (0.1, 0.5, 0.8):
        s = mb[mb.temp == t]
        mb_summary.append(dict(
            組別=f"4o-mini T{t}", 樣本數=len(s),
            文字Jaccard平均=np.mean(pairwise(list(s.bigrams))),
            機制集合Jaccard平均=np.mean(pairwise([set(m) for m in s.mechanisms])),
            相異機制類別數=len({c for m in s.mechanisms for c in m}),
            相異實驗設計類別數=len({c for d in s.designs for c in d}),
            平均字數=s.chars.mean(),
            違反不換彈珠限制=int(s.changes_marble.sum()),
        ))
    mb_summary = pd.DataFrame(mb_summary)

    # 跨溫度的文字相似度（組間 vs 組內）
    cross = []
    for prob, frame, labels in (("棒球", bb, groups_bb[:3]), ("彈珠", mb, [f"4o-mini T{t}" for t in (0.1, 0.5, 0.8)])):
        for a, b in itertools.combinations_with_replacement(labels, 2):
            A, B = list(frame[frame.group == a].bigrams), list(frame[frame.group == b].bigrams)
            vals = pairwise(A) if a == b else [jaccard(x, y) for x in A for y in B]
            cross.append(dict(題目=prob, 組別A=a, 組別B=b, 文字Jaccard平均=np.mean(vals)))
    cross = pd.DataFrame(cross)

    # 類別出現頻率（佔該組回答的比例）
    def freq(frame, col, labels, rules):
        out = pd.DataFrame(0.0, index=[r[0] for r in rules], columns=labels)
        for g in labels:
            s = frame[frame.group == g]
            for cats in s[col]:
                for c in set(cats):
                    out.loc[c, g] += 1 / len(s)
        return out

    f_assume = freq(bb, "assumptions", groups_bb, ASSUMPTION_RULES)
    f_other = freq(bb, "other_models", groups_bb, OTHER_MODEL_RULES)
    mb_labels = [f"4o-mini T{t}" for t in (0.1, 0.5, 0.8)]
    f_mech = freq(mb, "mechanisms", mb_labels, MECHANISM_RULES)
    f_design = freq(mb, "designs", mb_labels, DESIGN_RULES)

    # ------------------------------------------------ 輸出 CSV
    per = bb[["group", "test", "chars", "tokens", "H", "R", "g", "trig", "vx", "t", "R_self", "R_arith_wrong",
              "assumptions", "other_models", "errors"]]
    per.to_csv(OUT_RES / "棒球_逐筆.csv", index=False, encoding="utf-8-sig")
    mb[["group", "test", "chars", "mechanisms", "designs", "changes_marble"]].to_csv(
        OUT_RES / "彈珠_逐筆.csv", index=False, encoding="utf-8-sig")
    summary.to_csv(OUT_RES / "棒球_各組摘要.csv", index=False, encoding="utf-8-sig")
    mb_summary.to_csv(OUT_RES / "彈珠_各組摘要.csv", index=False, encoding="utf-8-sig")
    cross.to_csv(OUT_RES / "跨溫度文字相似度.csv", index=False, encoding="utf-8-sig")
    for name, f in (("棒球_假設類別頻率", f_assume), ("棒球_其他模型類別頻率", f_other),
                    ("彈珠_機制類別頻率", f_mech), ("彈珠_實驗設計類別頻率", f_design)):
        f.to_csv(OUT_RES / f"{name}.csv", encoding="utf-8-sig")
    pd.DataFrame([dict(g=g, **v) for g, v in EXACT.items()]).to_csv(
        OUT_RES / "理論值.csv", index=False, encoding="utf-8-sig")

    # ------------------------------------------------ 終端機摘要
    pd.set_option("display.width", 200, "display.max_columns", 30, "display.max_colwidth", 80)
    print("理論值：", {g: {k: round(v, 3) for k, v in d.items()} for g, d in EXACT.items()}, "\n")
    print("棒球逐筆數值：")
    print(bb[["group", "test", "H", "R", "vx", "t", "R_self", "R_arith_wrong", "trig", "errors"]].to_string(index=False), "\n")
    print("棒球各組摘要：\n", summary.round(3).T.to_string(), "\n")
    print("彈珠各組摘要：\n", mb_summary.round(3).T.to_string(), "\n")
    print("跨溫度文字相似度：\n", cross.round(3).to_string(index=False), "\n")
    print("棒球假設類別頻率：\n", f_assume.round(2).to_string(), "\n")
    print("棒球其他模型類別頻率：\n", f_other.round(2).to_string(), "\n")
    print("彈珠機制類別頻率：\n", f_mech.round(2).to_string(), "\n")
    print("彈珠實驗設計類別頻率：\n", f_design.round(2).to_string(), "\n")
    print("彈珠逐筆機制：")
    print(mb[["group", "test", "mechanisms"]].to_string(index=False))

    plot(bb, mb, summary, mb_summary, cross, f_assume, f_other, f_mech, groups_bb)

# ---------------------------------------------------------------- 圖表

COLORS = {"4o-mini T0.1": "#2a78d6", "4o-mini T0.5": "#eb6834", "4o-mini T0.8": "#1baf7a",
          "4o-mini T0.5 (8192)": "#eb6834", "Gemini T0.5": "#4a3aa7"}
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
BLUE_RAMP = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

plt.rcParams.update({
    "font.family": ["Microsoft JhengHei", "sans-serif"], "font.size": 10,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURFACE,
    "figure.facecolor": SURFACE, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
})


def short(g):
    return g.replace("4o-mini ", "4o-mini\n").replace(" (8192)", "\n(8192)").replace("Gemini ", "Gemini\n")


def bar_panel(ax, labels, values, title, ylabel, fmt="{:.2f}"):
    x = np.arange(len(labels))
    ax.bar(x, values, width=0.6, color=[COLORS[l] for l in labels], edgecolor=SURFACE, linewidth=2)
    for xi, v in zip(x, values):
        ax.text(xi, v, fmt.format(v), ha="center", va="bottom", fontsize=9, color=INK)
    ax.set_xticks(x, [short(l) for l in labels])
    ax.set_title(title, loc="left", fontsize=11)
    ax.set_ylabel(ylabel)
    ax.grid(axis="x", visible=False)


def plot(bb, mb, summary, mb_summary, cross, f_assume, f_other, f_mech, groups_bb):
    temps = groups_bb[:3]
    s = summary.set_index("組別")
    ms = mb_summary.set_index("組別")

    # 圖 1：溫度 vs 相似度
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6))
    bar_panel(axes[0], temps, s.loc[temps, "文字Jaccard平均"], "棒球：回答文字相似度", "組內兩兩 Jaccard（字元 bigram）")
    bar_panel(axes[1], temps, s.loc[temps, "假設集合Jaccard平均"], "棒球：列出的假設相似度", "組內兩兩 Jaccard（假設類別）")
    bar_panel(axes[2], temps, ms.loc[temps, "機制集合Jaccard平均"], "彈珠：提出的機制相似度", "組內兩兩 Jaccard（機制類別）")
    for ax in axes:
        ax.set_ylim(0, 1)
    fig.suptitle("溫度升高時，措辭越來越分散；但列出的假設與機制並沒有跟著變", x=0.01, ha="left", fontsize=13, color=INK)
    fig.tight_layout()
    fig.savefig(OUT_FIG / "fig1_溫度與相似度.png", dpi=200)
    plt.close(fig)

    # 圖 2：數值答案分布
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    order = groups_bb
    rng = np.random.default_rng(0)
    for ax, key, title in ((axes[0], "R", "水平射程 R（m）"), (axes[1], "H", "最大高度 H（m）")):
        for i, g in enumerate(order):
            v = bb[bb.group == g][key].dropna().values
            ax.scatter(i + rng.uniform(-0.12, 0.12, len(v)), v, s=40, color=COLORS[g],
                       edgecolor=SURFACE, linewidth=1.5, zorder=3)
        for gval, ls in ((9.81, "-"), (9.8, "--")):
            ax.axhline(EXACT[gval][key], color=INK2, lw=1, ls=ls, zorder=2)
            ax.text(2.5, EXACT[gval][key], f"理論值 g={gval}：{EXACT[gval][key]:.2f}",
                    va="bottom", ha="center", fontsize=8, color=INK2,
                    bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1))
        ax.set_xticks(range(len(order)), [short(g) for g in order])
        ax.set_title(title, loc="left", fontsize=11)
        ax.grid(axis="x", visible=False)
    fig.suptitle("數值答案：模型只在少數幾個「版本」間切換，且普遍略低於理論值", x=0.01, ha="left", fontsize=13, color=INK)
    fig.tight_layout()
    fig.savefig(OUT_FIG / "fig2_數值答案分布.png", dpi=200)
    plt.close(fig)

    # 圖 3：類別頻率熱圖
    def heat(ax, f, title):
        data = f.values
        cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("blue", BLUE_RAMP)
        ax.imshow(data, cmap=cmap, vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(f.shape[1]), [short(c) for c in f.columns], fontsize=8)
        ax.set_yticks(range(f.shape[0]), f.index, fontsize=9)
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for (i, j), v in np.ndenumerate(data):
            if v > 0:
                ax.text(j, i, f"{v:.0%}", ha="center", va="center", fontsize=8,
                        color="#ffffff" if v > 0.55 else INK)
        ax.set_title(title, loc="left", fontsize=11)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw=dict(width_ratios=[1, 1]))
    heat(axes[0], f_assume, "棒球：列出的假設（出現比例）")
    heat(axes[1], f_other, "棒球：討論的其他物理模型（出現比例）")
    fig.suptitle("Gemini 幾乎每次都補上旋轉、風、發射高度；4o-mini 多半只提空氣阻力", x=0.01, ha="left", fontsize=13, color=INK)
    fig.tight_layout()
    fig.savefig(OUT_FIG / "fig3_棒球類別頻率.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 4))
    heat(ax, f_mech, "彈珠：提出的機制（出現比例，每組僅 3 筆）")
    fig.tight_layout()
    fig.savefig(OUT_FIG / "fig4_彈珠機制頻率.png", dpi=200)
    plt.close(fig)

    # 圖 5：成本（長度 / tokens）
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    g2 = ["4o-mini T0.5 (8192)", "Gemini T0.5"]
    bar_panel(axes[0], g2, s.loc[g2, "平均tokens"], "每題平均 token 用量（Coze 顯示）", "tokens", fmt="{:.0f}")
    bar_panel(axes[1], groups_bb, s.loc[groups_bb, "平均字數"], "回答平均長度", "字數（去除空白與符號）", fmt="{:.0f}")
    fig.suptitle("同樣的上限 8192，Gemini 每題用掉約 4 倍 token", x=0.01, ha="left", fontsize=13, color=INK)
    fig.tight_layout()
    fig.savefig(OUT_FIG / "fig5_長度與token.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
