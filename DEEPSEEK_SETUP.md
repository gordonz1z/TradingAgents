# DeepSeek API Integration Guide

This guide explains how to integrate and use DeepSeek API with the TradingAgents framework.

## Prerequisites

1. **DeepSeek API Key**: Get your API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. **Environment Setup**: Set your API key as an environment variable

```bash
export OPENAI_API_KEY="your-deepseek-api-key-here"
```

> Note: DeepSeek API is compatible with OpenAI's API format, so we use the `OPENAI_API_KEY` environment variable.

## Configuration Options

### Method 1: Using CLI Interactive Setup

Run the CLI and select DeepSeek when prompted:

```bash
python -m cli.main
```

1. Select "DeepSeek" as your LLM Provider
2. Choose from available DeepSeek models:
   - **DeepSeek Chat**: General-purpose reasoning model
   - **DeepSeek Coder**: Specialized for coding tasks
   - **DeepSeek Reasoner**: Enhanced reasoning capabilities

### Method 2: Direct Configuration in Code

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create DeepSeek configuration
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"
config["backend_url"] = "https://api.deepseek.com/v1"
config["deep_think_llm"] = "deepseek-chat"  # For complex reasoning
config["quick_think_llm"] = "deepseek-chat"  # For fast operations
config["max_debate_rounds"] = 1
config["online_tools"] = True

# Initialize TradingAgents with DeepSeek
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

### Method 3: Using DeepSeek via OpenRouter (Alternative)

If you prefer using OpenRouter's free tier:

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openrouter"
config["backend_url"] = "https://openrouter.ai/api/v1"
config["deep_think_llm"] = "deepseek/deepseek-chat-v3-0324:free"
config["quick_think_llm"] = "deepseek/deepseek-chat-v3-0324:free"
```

## Available DeepSeek Models

| Model | Description | Best For |
|-------|-------------|----------|
| `deepseek-chat` | General-purpose model | Trading analysis, research |
| `deepseek-coder` | Code-specialized model | Technical analysis, data processing |
| `deepseek-reasoner` | Enhanced reasoning | Complex financial decisions |

## Cost Optimization Tips

1. **Use appropriate models**: 
   - `deepseek-chat` for general analysis
   - `deepseek-coder` for technical indicators
   - `deepseek-reasoner` for final decisions

2. **Adjust debate rounds**:
   ```python
   config["max_debate_rounds"] = 1  # Reduce for cost savings
   config["max_risk_discuss_rounds"] = 1
   ```

3. **Use cached data when possible**:
   ```python
   config["online_tools"] = False  # Use cached data instead of live APIs
   ```

## Environment Variables

Set these environment variables for full functionality:

```bash
# Required for DeepSeek API
export OPENAI_API_KEY="your-deepseek-api-key"

# Optional: For enhanced data sources
export FINNHUB_API_KEY="your-finnhub-key"
export GOOGLE_API_KEY="your-google-key"
export REDDIT_CLIENT_ID="your-reddit-client-id"
export REDDIT_CLIENT_SECRET="your-reddit-client-secret"
```

## Example Usage

```python
import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Ensure API key is set
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("Please set OPENAI_API_KEY environment variable with your DeepSeek API key")

# Configure for DeepSeek
config = DEFAULT_CONFIG.copy()
config.update({
    "llm_provider": "deepseek",
    "backend_url": "https://api.deepseek.com/v1",
    "deep_think_llm": "deepseek-chat",
    "quick_think_llm": "deepseek-chat",
    "max_debate_rounds": 2,
    "online_tools": True
})

# Initialize and run
ta = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals"],
    debug=True,
    config=config
)

# Analyze a stock
final_state, decision = ta.propagate("AAPL", "2024-01-15")
print(f"Trading Decision: {decision}")
```

## Troubleshooting

### Common Issues

1. **API Key Error**:
   ```
   Error: Invalid API key
   ```
   **Solution**: Ensure your DeepSeek API key is correctly set in the `OPENAI_API_KEY` environment variable.

2. **Model Not Found**:
   ```
   Error: Model 'deepseek-chat' not found
   ```
   **Solution**: Check DeepSeek's documentation for current model names and update accordingly.

3. **Rate Limiting**:
   ```
   Error: Rate limit exceeded
   ```
   **Solution**: Reduce `max_debate_rounds` or add delays between requests.

### Performance Tips

- **Memory Usage**: DeepSeek models are efficient, but monitor memory usage with large datasets
- **Response Time**: DeepSeek typically provides faster responses than larger models
- **Accuracy**: DeepSeek excels at reasoning tasks, making it ideal for financial analysis

## Integration with Existing Workflows

DeepSeek integrates seamlessly with existing TradingAgents workflows:

- **Backtesting**: Use DeepSeek for historical analysis
- **Live Trading**: Configure for real-time decision making
- **Research**: Leverage DeepSeek's reasoning for market research

For more information, see the main [README.md](README.md) and [TradingAgents documentation](https://github.com/your-repo/TradingAgents).