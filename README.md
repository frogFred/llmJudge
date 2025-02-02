# AI評審  

AI評審是一個用來判斷生成式 AI 回答是否符合問題需求的工具，旨在降低 AI 產生幻覺（Hallucination）的機率，確保回應的準確性與相關性。本專案可用於聊天機器人、問答系統或任何依賴生成式 AI 的應用程式，以提高答案的可靠性。  

## 功能與特色  

- **雙模型評審機制**  
  - 本專案採用兩個不同的 AI 模型作為評審系統，分別關注不同面向的評估標準：  
    1. **語言表達模型**：負責評估回答的清晰度與準確性。  
    2. **科學事實評估模型**：負責檢查回答內容的真實性與可靠性。  

- **評分機制**  
  - 兩個評審模型根據各自的標準，對 AI 生成的答案進行 1-5 分評分。  
  - 若最終平均分數低於 3 分，則該答案將被視為不可信，並自動回覆：「不好意思，我沒有相關的答案，請尋求專業人士的幫助。」  

- **提升回答可靠性**  
  - 透過雙重評審機制，有效減少 AI 產生幻覺（Hallucination）的可能性，確保回應的準確性與可信度。  

## 安裝與使用方式  

### 1. **環境需求**  
請確保您的系統已安裝以下環境與工具：  
- [Ollama](https://ollama.ai/)  
- Python 3.x  
- 瀏覽器（支援 HTML、CSS、JavaScript）  

### 2. **專案下載**  
請使用 Git 下載專案至本機：  
```bash
git clone https://github.com/frogFred/llmJudge.git
cd llmJudge
