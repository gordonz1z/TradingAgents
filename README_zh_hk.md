<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- 保留這些鏈接。翻譯將隨README自動更新。 -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: 多智能體LLM金融交易框架

> 🎉 **TradingAgents** 正式發布！我們收到了許多關於這項工作的諮詢，感謝社區的熱情支持。
> 
> 因此，我們決定完全開源這個框架。期待與您一起打造更具影響力的項目！

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

<div align="center">

🚀 [TradingAgents](#tradingagents-框架) | ⚡ [安裝與CLI](#安裝與cli) | 🎬 [演示](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [套件使用](#tradingagents-套件) | 🤝 [貢獻](#貢獻) | 📄 [引用](#引用)

</div>

## TradingAgents 框架

TradingAgents是一個多智能體交易框架，模擬真實世界交易公司的動態。通過部署專門的LLM驅動智能體：從基本面分析師、情緒專家、技術分析師，到交易員、風險管理團隊，該平台協同評估市場狀況並提供交易決策。此外，這些智能體通過動態討論來確定最佳策略。

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents框架僅供研究用途。交易表現可能因多種因素而異，包括所選擇的基礎語言模型、模型溫度、交易周期、數據質量以及其他非確定性因素。[本框架不構成財務、投資或交易建議。](https://tauric.ai/disclaimer/)

我們的框架將複雜的交易任務分解為專門的角色。這確保系統實現強大、可擴展的市場分析和決策方法。

### 分析師團隊
- 基本面分析師：評估公司財務和業績指標，識別內在價值和潛在風險信號。
- 情緒分析師：使用情緒評分算法分析社交媒體和公眾情緒，以衡量短期市場情緒。
- 新聞分析師：監控全球新聞和宏觀經濟指標，解讀事件對市場狀況的影響。
- 技術分析師：利用技術指標（如MACD和RSI）檢測交易模式並預測價格走勢。

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### 研究員團隊
- 由看多和看空研究員組成，他們批判性地評估分析師團隊提供的見解。通過結構化辯論，他們平衡潛在收益與固有風險。

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 交易員智能體
- 綜合分析師和研究員的報告，做出明智的交易決策。它根據全面的市場見解確定交易的時機和規模。

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### 風險管理和投資組合經理
- 通過評估市場波動性、流動性和其他風險因素，持續評估投資組合風險。風險管理團隊評估和調整交易策略，向投資組合經理提供評估報告以供最終決策。
- 投資組合經理批准/拒絕交易提案。如果獲得批准，訂單將發送到模擬交易所並執行。

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## 安裝與CLI

### 安裝

克隆TradingAgents：
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

使用您喜歡的環境管理器創建虛擬環境：
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

安裝依賴項：
```bash
pip install -r requirements.txt
```

### 所需API

您還需要FinnHub API來獲取金融數據。我們所有的代碼都使用免費層實現。
```bash
export FINNHUB_API_KEY=d1k1m21r01ql1h3a3v00d1k1m21r01ql1h3a3v0g
```

#### LLM提供商設置

**選項1：OpenAI API**
```bash
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
```

**選項2：DeepSeek API**（推薦用於成本效益）
```bash
export OPENAI_API_KEY=sk-7ad0cd8f1a9544bda4bed6365655f3ff
```

**選項3：其他提供商**
該框架還支持Anthropic、Google、OpenRouter和Ollama。有關詳細配置說明，請參閱[DEEPSEEK_SETUP.md](DEEPSEEK_SETUP.md)。

> 💡 **DeepSeek集成**：我們現在支持DeepSeek API，用於經濟高效且高性能的交易分析。DeepSeek以具有競爭力的價格提供出色的推理能力。請參閱我們的[DeepSeek設置指南](DEEPSEEK_SETUP.md)了解詳細說明。

### CLI使用

您也可以直接運行CLI進行嘗試：
```bash
python -m cli.main
```
您將看到一個屏幕，您可以在其中選擇所需的股票代碼、日期、LLM、研究深度等。

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

將出現一個界面，顯示結果加載過程，讓您跟踪智能體運行時的進度。

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents套件

### 實現細節

我們使用LangGraph構建TradingAgents，以確保靈活性和模塊化。我們在實驗中使用`o1-preview`和`gpt-4o`作為深度思考和快速思考的LLM。然而，出於測試目的，我們建議您使用`o4-mini`和`gpt-4.1-mini`以節省成本，因為我們的框架會進行**大量**API調用。

### Python使用

要在代碼中使用TradingAgents，您可以導入`tradingagents`模塊並初始化`TradingAgentsGraph()`對象。`.propagate()`函數將返回一個決策。您可以運行`main.py`，這裡還有一個簡單示例：

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# 向前傳播
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

您還可以調整默認配置來設置自己選擇的LLM、辯論輪次等。

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 創建自定義配置
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4.1-nano"  # 使用不同的模型
config["quick_think_llm"] = "gpt-4.1-nano"  # 使用不同的模型
config["max_debate_rounds"] = 1  # 增加辯論輪次
config["online_tools"] = True # 使用在線工具或緩存數據

# 使用自定義配置初始化
ta = TradingAgentsGraph(debug=True, config=config)

# 向前傳播
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

> 對於`online_tools`，我們建議啟用它們進行實驗，因為它們提供對實時數據的訪問。智能體的離線工具依賴我們**Tauric TradingDB**的緩存數據，這是我們用於回測的精選數據集。我們目前正在改進這個數據集，計劃在即將推出的項目中與之一起發布。敬請期待！

您可以在`tradingagents/default_config.py`中查看完整的配置列表。

## 貢獻

我們歡迎社區的貢獻！無論是修復錯誤、改進文檔還是建議新功能，您的輸入都有助於使這個項目變得更好。如果您對這一研究領域感興趣，請考慮加入我們的開源金融AI研究社區[Tauric Research](https://tauric.ai/)。

## 引用

如果您發現*TradingAgents*對您有所幫助，請參考我們的工作：

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework},
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138},
}
```