# NCU AI Agent Course

AI Agent 課程學習與實作紀錄。

## 目前方向

從物理實驗的實際需求出發，探索如何讓 AI 在長對話中分清楚使用者的量測資料、使用者的猜測、AI 提出的假設，以及後續獲得獨立證據支持的結論。

目前嘗試設計輕量的 **Scientific Common Ground Skill**，維護說法、來源與狀態（Claim–Source–Status），避免假設只因被反覆討論或被使用者追問，就被當成已確認的事實。

## 最新成果

[AI Skill 學習文件（含實作過程）](docs/AI_Skill_學習文件_含實作過程版.docx)

文件記錄了：

- 以 BNC 傳輸線實驗問題，比較原始 Gemini 與第一版 Skill 的回答。
- 將頻率範圍延伸至 60 MHz 的後續量測與觀察。
- 根據比較結果，將設計方向調整為維護 Claim–Source–Status，並提出第二版 Skill 草稿。

下一步是測試：在沒有新證據的多輪對話中，模型能否維持假設的原有狀態；加入獨立量測證據後，又能否合理更新結論。第二版的效果尚待驗證。

[討論過程（ChatGPT 分享連結）](https://chatgpt.com/share/6ab009b0-4614-83e8-8153-21b5d2bc62cd)
