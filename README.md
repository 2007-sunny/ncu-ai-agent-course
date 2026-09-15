# NCU AI Agent Course

中央大學 AI Agent 課程的作業與實驗紀錄。先建立 Unit 0～2 的基礎，專題方向會隨課程進度調整。

## 暫定構想：AI Course Assistant

建立協助大學生了解課程資訊的 AI 助理，逐步整合 Memory、RAG、Tools 與 Workflow。

### 使用場景

- 學生詢問課程主題、先備知識與作業要求。
- 學生描述背景與需求，助理整理成結構化資料。
- 資訊不足時，助理明確說明不知道，請使用者補充課程資料。

### MVP 目標（尚未實作）

- 使用繁體中文進行基本自然語言對話。
- 根據使用者提供的課程資訊回答問題。
- 將簡單人物描述轉成符合指定格式的 JSON。

### 後續方向

- Memory：記錄使用者需求。
- RAG：查詢課程 Knowledge Base。
- Tools：呼叫外部工具。
- Workflow：串接任務處理流程。

目前僅建立文件、Prompt 與測試模板，尚未建立可執行服務或完成 Coze Agent。以上功能不代表已完成；期末題目尚未決定。

> 依目前提供的作業描述，Unit 0 提到「產品客服 Agent」。此處先採用課程助理作為暫定構想；繳交前需確認教師是否接受此方向，必要時再調整。

## 專案結構

```text
ncu-ai-agent-course/
├── README.md
├── assignments/
│   ├── unit0/README.md
│   ├── unit1/
│   │   ├── README.md
│   │   └── system_prompt.md
│   └── unit2/
│       ├── README.md
│       ├── system_prompt.md
│       └── example_output.json
├── docs/project_ideas.md
└── final-project/README.md
```

## 開始順序

1. [Unit 0：專案構想](assignments/unit0/README.md)：整理使用情境與 README。
2. [Unit 1：Agent 設定與參數](assignments/unit1/README.md)：在 Coze 建立 Agent，記錄模型與參數測試。
3. [Unit 2：Prompt 與 JSON](assignments/unit2/README.md)：測試結構化輸出及 Prompt Injection。
4. 有想法時再填寫 [期末專題構想](docs/project_ideas.md)。

## 第一階段檢查表

- [x] 建立 Repo 文件與 Unit 0～2 框架。
- [ ] 確認 Unit 0 題目符合教師要求。
- [ ] 建立第一個 Coze Agent。
- [ ] 完成一次模型參數比較並保存結果。
- [ ] 實測一次 Structured JSON Output。

本專案會隨課程進度持續修改。不要將 API Key、密碼或含個資的測試截圖提交到 Repo。
