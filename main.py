from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Example 1: Using DeepSeek API
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "deepseek"  # Use DeepSeek
config["backend_url"] = "https://api.deepseek.com/v1"  # DeepSeek API endpoint
config["deep_think_llm"] = "deepseek-chat"  # DeepSeek reasoning model
config["quick_think_llm"] = "deepseek-chat"  # DeepSeek fast model
config["max_debate_rounds"] = 1  # Debate rounds
config["online_tools"] = True  # Use online tools

# Example 2: Using Google Gemini (alternative)
# config = DEFAULT_CONFIG.copy()
# config["llm_provider"] = "google"
# config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
# config["deep_think_llm"] = "gemini-2.0-flash"
# config["quick_think_llm"] = "gemini-2.0-flash"
# config["max_debate_rounds"] = 1
# config["online_tools"] = True

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)

# Memorize mistakes and reflect
# ta.reflect_and_remember(1000) # parameter is the position returns
