# NCU AI Agent Course

AI Agent 課程學習與實作紀錄。目前收錄 **Unit 0：初步構想、使用場景與學習紀錄**。

## 目前方向

從物理實驗的實際需求出發，探索如何讓 AI 在長對話中分清楚使用者的量測資料、使用者的猜測、AI 提出的假設，以及後續獲得獨立證據支持的結論。

目前嘗試設計輕量的 **Scientific Common Ground Skill**，維護說法、來源與狀態（Claim–Source–Status），避免假設只因被反覆討論或被使用者追問，就被當成已確認的事實。

## Unit 0 學習成果

[Unit 0 AI Agent / Skill 學習文件](docs/Unit0_AI_Agent_Skill_學習文件.docx)

本次範圍是從應用場景出發，整理初步構想、核心名詞與知識結構，並以 GitHub 保存學習進度。文件中的 Skill 草稿與比較案例是 Unit 0 的探索紀錄，尚不代表完整 Agent 已完成，也不代表後續單元作業已完成。

Repository：[2007-sunny/ncu-ai-agent-course](https://github.com/2007-sunny/ncu-ai-agent-course)

文件記錄了：

- 以 BNC 傳輸線實驗問題，比較原始 Gemini 與第一版 Skill 的回答。
- 將頻率範圍延伸至 60 MHz 的後續量測與觀察。
- 根據比較結果，將設計方向調整為維護 Claim–Source–Status，並提出第二版 Skill 草稿。
- 整理應用場景、Unit 0 對應內容，以及 Claim–Source–Status 等核心名詞。

下一步是測試：在沒有新證據的多輪對話中，模型能否維持假設的原有狀態；加入獨立量測證據後，又能否合理更新結論。第二版的效果尚待驗證。

[討論過程（ChatGPT 分享連結）](https://chatgpt.com/share/6ab009b0-4614-83e8-8153-21b5d2bc62cd)

## 原始紀錄

| 檔案 | 用途 |
| --- | --- |
| [應用 AI 網站題目建議](docs/references/應用AI網站題目建議.pdf) | 專案動機、Skill 設計演變與討論 |
| [BNC 線時間差估算](docs/references/BNC線時間差估算.pdf) | 物理實驗背景與後續量測討論 |
| [原始 Gemini 對話](<docs/references/BNC 線材 29 MHz 反射凹陷分析 - Google Gemini.pdf>) | 未使用 Skill 的對照紀錄 |
| [v0.1 自訂 Gem 對話](<docs/references/探討 29 MHz BNC 線反射陷波 - Google Gemini.pdf>) | 使用 Experimental Physics Reasoning v0.1 的測試紀錄 |

以上 PDF 保留原始對話內容；其中 AI 提出的解釋不代表已驗證的實驗結論。
