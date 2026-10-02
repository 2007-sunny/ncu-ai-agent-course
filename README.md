# NCU AI Agent Course

AI Agent 課程學習與實作紀錄。

| 單元 | 主題 | 學習文件 |
| --- | --- | --- |
| Unit 0 | 初步構想、使用場景與學習紀錄 | [docx](docs/Unit0_AI_Agent_Skill_學習文件.docx) |
| Unit 1 | 大腦核心：LLM 選擇與參數設定 | [docx](docs/Unit1_LLM參數與模型選擇_學習文件.docx)／[pdf](docs/Unit1_LLM參數與模型選擇_學習文件.pdf) |
| Unit 2 | Prompt 的應用場景、管理流程、安全防護 | [docx](docs/Unit2_Prompt應用與防護_學習文件.docx)／[pdf](docs/Unit2_Prompt應用與防護_學習文件.pdf)／[中文學習手冊](docs/Unit2_Prompt學習手冊.html) |

## 目前方向

長期興趣是從物理實驗的實際需求出發，探索如何讓 AI 在長對話中分清楚使用者的量測資料、使用者的猜測、AI 提出的假設，以及後續獲得獨立證據支持的結論（Scientific Common Ground Skill，見 Unit 0）。

依老師在 Unit 0 的回饋，目前先回到課程主線：理解 AI Agent 的核心元件。Unit 1 研究 Agent 的「大腦」（LLM）的參數與模型選擇；接下來將在 Coze 上實作客服 Agent，逐步加入 Knowledge、Memory、Plugin 與 Guardrail。

## Unit 1 學習成果：同一題問十次，AI 的回答會一樣嗎？

[Unit 1 學習文件（docx）](docs/Unit1_LLM參數與模型選擇_學習文件.docx)／[PDF](docs/Unit1_LLM參數與模型選擇_學習文件.pdf)

在 Coze 以 GPT-4o mini 做 temperature 0.1／0.5／0.8 對照，並以 Gemini Flash 2.0 做模型對照，對 54 筆回答做量化分析（Jaccard 相似度、數值檢驗、錯誤標記），並用物理量測的 precision（精密度）與 accuracy（準確度）解讀結果。主要發現：

- **溫度改變的是措辭，不是內容**：溫度升高時，回答的文字相似度從 0.60 降到 0.32，但列出的假設幾乎不變。
- **低溫是「一致地錯」**：GPT-4o mini 的 35 筆回答沒有一筆算出理論值；T0.1 算錯的 7 筆全是同一個錯誤答案，T0.8 算錯的 7 筆出現 6 種答案。調低 temperature 只能讓回答一致，不能讓回答正確。
- **換模型換到的是廣度與成本**：Gemini Flash 2.0 考慮的物理因素約是 4o mini 的 3 倍，但每題 token 約 3.9 倍，數值也沒有比較準。
- **模型選型**：整理 Gemini 官網的模型與價格、Coze 上最便宜的模型（GPT-4o mini），以及模型大小對精準度的影響與蒸餾模型。

### 資料與分析程式

| 路徑 | 內容 |
| --- | --- |
| [coze/temperture/棒球/](coze/temperture/棒球/) | 棒球題（拋體計算）的原始回答：4o mini 三個溫度、4o mini 與 Gemini 的模型對照 |
| [coze/temperture/彈珠/](coze/temperture/彈珠/) | 彈珠題（開放式機制題）的原始回答 |
| [coze/temperture/溫度/](coze/temperture/溫度/) | Coze 設定與回答截圖（「為甚麼高度上升溫度會降低？」三個溫度各 3 次） |
| [coze/temperture/analysis/](coze/temperture/analysis/) | 分析程式 `analyze.py`、結果表格 `results/`、圖表 `figures/`、分析摘要 `分析結果.md` |

重現分析：

```bash
cd coze/temperture/analysis
python analyze.py
```

需要 Python 3 與 numpy、pandas、matplotlib。

## Unit 0 學習成果

[Unit 0 AI Agent / Skill 學習文件](docs/Unit0_AI_Agent_Skill_學習文件.docx)

本次範圍是從應用場景出發，整理初步構想、核心名詞與知識結構，並以 GitHub 保存學習進度。文件中的 Skill 草稿與比較案例是 Unit 0 的探索紀錄，尚不代表完整 Agent 已完成，也不代表後續單元作業已完成。

文件記錄了：

- 以 BNC 傳輸線實驗問題，比較原始 Gemini 與第一版 Skill 的回答。
- 將頻率範圍延伸至 60 MHz 的後續量測與觀察。
- 根據比較結果，將設計方向調整為維護 Claim–Source–Status，並提出第二版 Skill 草稿。
- 整理應用場景、Unit 0 對應內容，以及 Claim–Source–Status 等核心名詞。

下一步是測試：在沒有新證據的多輪對話中，模型能否維持假設的原有狀態；加入獨立量測證據後，又能否合理更新結論。第二版的效果尚待驗證。

[討論過程（ChatGPT 分享連結）](https://chatgpt.com/share/6ab009b0-4614-83e8-8153-21b5d2bc62cd)

### Unit 0 原始紀錄

| 檔案 | 用途 |
| --- | --- |
| [應用 AI 網站題目建議](docs/references/應用AI網站題目建議.pdf) | 專案動機、Skill 設計演變與討論 |
| [BNC 線時間差估算](docs/references/BNC線時間差估算.pdf) | 物理實驗背景與後續量測討論 |
| [原始 Gemini 對話](<docs/references/BNC 線材 29 MHz 反射凹陷分析 - Google Gemini.pdf>) | 未使用 Skill 的對照紀錄 |
| [v0.1 自訂 Gem 對話](<docs/references/探討 29 MHz BNC 線反射陷波 - Google Gemini.pdf>) | 使用 Experimental Physics Reasoning v0.1 的測試紀錄 |

以上 PDF 保留原始對話內容；其中 AI 提出的解釋不代表已驗證的實驗結論。

Repository：[2007-sunny/ncu-ai-agent-course](https://github.com/2007-sunny/ncu-ai-agent-course)
