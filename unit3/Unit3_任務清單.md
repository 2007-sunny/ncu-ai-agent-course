# Unit 3 任務清單：狀態管理－記憶機制 (Memory)

> 依課綱 `115-1_中央大學AI-Agent課綱.xlsx` 單元 3 整理。評分是逐項檢核，**每一項都要有自己的截圖**，名稱照課綱原文寫。
> 實作紀錄：[unit3_note.md](unit3_note.md)；截圖：[images/](images/)
> 最後更新：2026-10-10

## A. 課綱實作（AI 評分核心）
- [x] A1. 為 agent 建立 Variable，名稱叫 `gender`
- [x] A2. 用戶說出自己性別時，`gender` 會更新（note「gender-log測試流程」，image ～ image-4）
- [x] A3. 「進行變化紀錄」：Table `gender_log` 記錄時間、原值、新值、原因（image-4 成功；reason 需在 prompt 明寫才會填）
  - 注意：之後把 gender_log 換成 identity_log，**繳交時要用 gender 的截圖**，課綱名稱是 `gender`
- [x] A4. Context of round 實驗：輪數 2／10 對照，10 題腳本（note「A4、A5 實驗結果分析」）
  - [x] 腳本設計（note「設計A4實驗」）
  - [x] 卡關：identity_log 不寫入（note 1-1 ～ 2-7；模型只呼叫 setKeywordMemory，不呼叫資料庫）
  - [x] 改用 chatflow `client_data_process` 寫入，已驗證成功並掛到 Agent（note 2-8，wf-01 ～ wf-12）
  - [x] 在 Agent 的 Model settings 設輪數 2／10，跑 10 題腳本（LLM_1 沒有對話歷史設定）
- [x] A5. 三種記憶對照：同一資訊靠 round／variable／table 記住的差異（開新對話後誰還記得？截圖）

## B. 課綱知識點（用自己的話＋例子）
- [x] B1. 短期記憶 vs 長期記憶
- [x] B2. Context of round（對話輪數）
- [x] B3. Variable（特定重點）
- [x] B4. Table（重複行為）
- [x] B5. 進階：Memory Summarization（參考 LangChain memory 文件）
- [x] B6. Long-context prompting 要點（參考 Claude 文件）

## C. 老師回饋／延伸
- [x] C1. 為什麼 Variable 要搭 Table：Variable 存「現在」，Table 存「歷史」
- [x] C2. Hot-path 寫入 vs 背景寫入（LangChain 文件用語）
- [x] C3. 踩坑論證：prompt 驅動的工具呼叫不可靠 → 為什麼需要 workflow（note 1-3、2-5 ～ 2-8）

## D. 報告與繳交
- [x] D1. 結論與心得放最前面
- [x] D2. 第一頁課綱對照表，每項標截圖編號
- [x] D3. 記錄踩坑過程（XML 防護規則排除 memory、log 不寫入、雙大括號變數）
- [ ] D4.（報告已產出 unit3/docs/Unit3_記憶機制_學習文件.docx/.pdf，待 commit／push） 上傳 GitHub、更新 README 單元表與 `進度.md`

## E. 創意階段（完成 A～D 後）
- [x] E1. 新點子：Knowledge 優惠活動表 `discount_event`＋依身分給折扣（note「設計優惠活動」，已測可讀取，image-5 ～ image-8）
- [x] E1. 新點子：模型不知道今天日期 → 以客人說的日期為準／Code 節點產生時間
- [ ] E2. 與舊點子（Unit 2 客服、Claim–Source–Status）結合，提案 1～2 個
- [ ] E3. 實作＋截圖，寫成報告附錄
- [ ] E4. 若失敗 → 提前做 Unit 4（上傳課程列表並讓 agent 引用）；Knowledge 的使用已有雛形
