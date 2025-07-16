# DeepSeek API 集成指南

本指南介紹如何將DeepSeek API與TradingAgents框架集成和使用。

## 先決條件

1. **DeepSeek API 金鑰**：從[DeepSeek平台](https://platform.deepseek.com/)獲取您的API金鑰
2. **環境設置**：將您的API金鑰設置為環境變數

```bash
export OPENAI_API_KEY="your-deepseek-api-key-here"
```

> 注意：DeepSeek API與OpenAI的API格式兼容，因此我們使用`OPENAI_API_KEY`環境變數。

## 配置選項

### 方法1：使用CLI互動式設置

運行CLI並在提示時選擇DeepSeek：

```bash
python -m cli.main
```

1. 選擇「DeepSeek」作為您的LLM提供商
2. 從可用的DeepSeek模型中選擇：
   - **DeepSeek Chat**：通用推理模型
   - **DeepSeek Coder**：專門用於編碼任務
   - **DeepSeek Reasoner**：增強推理能力

### 方法2：在代碼中直接配置

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 創建DeepSeek配置
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"
config["backend_url"] = "https://api.deepseek.com/v1"
config["deep_think_llm"] = "deepseek-chat"  # 用於複雜推理
config["quick_think_llm"] = "deepseek-chat"  # 用於快速操作
config["max_debate_rounds"] = 1
config["online_tools"] = True

# 使用DeepSeek初始化TradingAgents
ta = TradingAgentsGraph(debug=True, config=config)

# 運行分析
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

### 方法3：通過OpenRouter使用DeepSeek（替代方案）

如果您更喜歡使用OpenRouter的免費層：

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openrouter"
config["backend_url"] = "https://openrouter.ai/api/v1"
config["deep_think_llm"] = "deepseek/deepseek-chat-v3-0324:free"
config["quick_think_llm"] = "deepseek/deepseek-chat-v3-0324:free"
```

## 可用的DeepSeek模型

| 模型 | 描述 | 最佳用途 |
|-------|-------------|----------|
| `deepseek-chat` | 通用模型 | 交易分析、研究 |
| `deepseek-coder` | 代碼專用模型 | 技術分析、數據處理 |
| `deepseek-reasoner` | 增強推理 | 複雜金融決策 |

## 成本優化技巧

1. **使用適當的模型**：
   - `deepseek-chat` 用於一般分析
   - `deepseek-coder` 用於技術指標
   - `deepseek-reasoner` 用於最終決策

2. **調整辯論輪次**：
   ```python
   config["max_debate_rounds"] = 1  # 減少以節省成本
   config["max_risk_discuss_rounds"] = 1
   ```

3. **盡可能使用緩存數據**：
   ```python
   config["online_tools"] = False  # 使用緩存數據而非實時API
   ```

## 環境變數

設置這些環境變數以獲得完整功能：

```bash
# DeepSeek API 必需
export OPENAI_API_KEY="your-deepseek-api-key"

# 可選：用於增強數據來源
export FINNHUB_API_KEY="your-finnhub-key"
export GOOGLE_API_KEY="your-google-key"
export REDDIT_CLIENT_ID="your-reddit-client-id"
export REDDIT_CLIENT_SECRET="your-reddit-client-secret"
```

## 示例用法

```python
import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 確保API金鑰已設置
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("請將OPENAI_API_KEY環境變數設置為您的DeepSeek API金鑰")

# 配置DeepSeek
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "deepseek",
    "backend_url": "https://api.deepseek.com/v1",
    "deep_think_llm": "deepseek-chat",
    "quick_think_llm": "deepseek-chat",
    "max_debate_rounds": 2,
    "online_tools": True
})

# 初始化並運行
ta = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals"],
    debug=True,
    config=config
)

# 分析股票
final_state, decision = ta.propagate("AAPL", "2024-01-15")
print(f"交易決策：{decision}")
```

## 故障排除

### 常見問題

1. **API金鑰錯誤**：
   ```
   Error: Invalid API key
   ```
   **解決方案**：確保您的DeepSeek API金鑰已正確設置在`OPENAI_API_KEY`環境變數中。

2. **模型未找到**：
   ```
   Error: Model 'deepseek-chat' not found
   ```
   **解決方案**：查看DeepSeek的文檔以獲取當前模型名稱並相應更新。

3. **速率限制**：
   ```
   Error: Rate limit exceeded
   ```
   **解決方案**：減少`max_debate_rounds`或在請求之間添加延遲。

### 性能提示

- **內存使用**：DeepSeek模型效率很高，但處理大型數據集時請監控內存使用
- **響應時間**：DeepSeek通常比大型模型提供更快的響應
- **準確性**：DeepSeek在推理任務方面表現出色，非常適合金融分析

## 與現有工作流程集成

DeepSeek與現有的TradingAgents工作流程無縫集成：

- **回測**：使用DeepSeek進行歷史分析
- **實時交易**：配置用於實時決策
- **研究**：利用DeepSeek的推理能力進行市場研究

有關更多信息，請參閱主要[README.md](README.md)和[TradingAgents文檔](https://github.com/your-repo/TradingAgents)。