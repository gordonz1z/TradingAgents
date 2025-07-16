import questionary
from typing import List, Optional, Tuple, Dict

from cli.models import AnalystType

ANALYST_ORDER = [
    ("市場分析師", AnalystType.MARKET),
    ("社交分析師", AnalystType.SOCIAL),
    ("新聞分析師", AnalystType.NEWS),
    ("基本面分析師", AnalystType.FUNDAMENTALS),
]


def get_ticker():
    """提示用戶輸入股票代碼。"""
    ticker = questionary.text(
        "請輸入要分析的股票代號：",
        validate=lambda x: len(x.strip()) > 0 or "請輸入有效的股票代號。",
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not ticker:
        console.print("\n[red]未提供股票代號。正在退出...[/red]")
        exit(1)

    return ticker.strip().upper()


def get_analysis_date():
    """提示用戶輸入 YYYY-MM-DD 格式的日期。"""
    import re
    from datetime import datetime

    def validate_date(date_str: str) -> bool:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    date = questionary.text(
        "請輸入分析日期 (YYYY-MM-DD)：",
        validate=lambda x: validate_date(x.strip())
        or "請輸入有效的日期格式 YYYY-MM-DD。",
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not date:
        console.print("\n[red]未提供日期。正在退出...[/red]")
        exit(1)

    return date.strip()


def select_analysts() -> List[AnalystType]:
    """使用互動式複選框選擇分析師。"""
    choices = questionary.checkbox(
        "選擇您的 [分析師團隊]：",
        choices=[
            questionary.Choice(display, value=value) for display, value in ANALYST_ORDER
        ],
        instruction="\n- 按空白鍵選擇/取消選擇分析師\n- 按 'a' 全選/全不選\n- 按 Enter 完成選擇",
        validate=lambda x: len(x) > 0 or "您必須至少選擇一位分析師。",
        style=questionary.Style(
            [
                ("checkbox-selected", "fg:green"),
                ("selected", "fg:green noinherit"),
                ("highlighted", "noinherit"),
                ("pointer", "noinherit"),
            ]
        ),
    ).ask()

    if not choices:
        console.print("\n[red]未選擇分析師。正在退出...[/red]")
        exit(1)

    return choices


def select_research_depth() -> int:
    """使用互動式選擇器選擇研究深度。"""

    # Define research depth options with their corresponding values
    DEPTH_OPTIONS = [
        ("淺層 - 快速研究，較少辯論和策略討論輪次", 1),
        ("中等 - 中等程度，適度的辯論輪次和策略討論", 3),
        ("深度 - 全面研究，深入的辯論和策略討論", 5),
    ]

    choice = questionary.select(
        "選擇您的 [研究深度]：",
        choices=[
            questionary.Choice(display, value=value) for display, value in DEPTH_OPTIONS
        ],
        instruction="\n- 使用方向鍵導航\n- 按 Enter 選擇",
        style=questionary.Style(
            [
                ("selected", "fg:yellow noinherit"),
                ("highlighted", "fg:yellow noinherit"),
                ("pointer", "fg:yellow noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]未選擇研究深度。正在退出...[/red]")
        exit(1)

    return choice


def select_shallow_thinking_agent(provider) -> str:
    """使用互動式選擇器選擇快速思考 LLM 引擎。"""

    # Define shallow thinking llm engine options with their corresponding model names
    SHALLOW_AGENT_OPTIONS = {
        "openai": [
            ("GPT-4o-mini - Fast and efficient for quick tasks", "gpt-4o-mini"),
            ("GPT-4.1-nano - Ultra-lightweight model for basic operations", "gpt-4.1-nano"),
            ("GPT-4.1-mini - Compact model with good performance", "gpt-4.1-mini"),
            ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
        ],
        "anthropic": [
            ("Claude Haiku 3.5 - Fast inference and standard capabilities", "claude-3-5-haiku-latest"),
            ("Claude Sonnet 3.5 - Highly capable standard model", "claude-3-5-sonnet-latest"),
            ("Claude Sonnet 3.7 - Exceptional hybrid reasoning and agentic capabilities", "claude-3-7-sonnet-latest"),
            ("Claude Sonnet 4 - High performance and excellent reasoning", "claude-sonnet-4-0"),
        ],
        "google": [
            ("Gemini 2.0 Flash-Lite - Cost efficiency and low latency", "gemini-2.0-flash-lite"),
            ("Gemini 2.0 Flash - Next generation features, speed, and thinking", "gemini-2.0-flash"),
            ("Gemini 2.5 Flash - Adaptive thinking, cost efficiency", "gemini-2.5-flash-preview-05-20"),
        ],
        "deepseek": [
            ("DeepSeek Chat - Fast and efficient reasoning model", "deepseek-chat"),
            ("DeepSeek Coder - Specialized for coding tasks", "deepseek-coder"),
        ],
        "openrouter": [
            ("Meta: Llama 4 Scout", "meta-llama/llama-4-scout:free"),
            ("Meta: Llama 3.3 8B Instruct - A lightweight and ultra-fast variant of Llama 3.3 70B", "meta-llama/llama-3.3-8b-instruct:free"),
            ("google/gemini-2.0-flash-exp:free - Gemini Flash 2.0 offers a significantly faster time to first token", "google/gemini-2.0-flash-exp:free"),
        ],
        "ollama": [
            ("llama3.1 local", "llama3.1"),
            ("llama3.2 local", "llama3.2"),
        ]
    }

    choice = questionary.select(
        "選擇您的 [快速思考 LLM 引擎]：",
        choices=[
            questionary.Choice(display, value=value)
            for display, value in SHALLOW_AGENT_OPTIONS[provider.lower()]
        ],
        instruction="\n- 使用方向鍵導航\n- 按 Enter 選擇",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print(
            "\n[red]未選擇快速思考 LLM 引擎。正在退出...[/red]"
        )
        exit(1)

    return choice


def select_deep_thinking_agent(provider) -> str:
    """使用互動式選擇器選擇深度思考 LLM 引擎。"""

    # Define deep thinking llm engine options with their corresponding model names
    DEEP_AGENT_OPTIONS = {
        "openai": [
            ("GPT-4.1-nano - Ultra-lightweight model for basic operations", "gpt-4.1-nano"),
            ("GPT-4.1-mini - Compact model with good performance", "gpt-4.1-mini"),
            ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
            ("o4-mini - Specialized reasoning model (compact)", "o4-mini"),
            ("o3-mini - Advanced reasoning model (lightweight)", "o3-mini"),
            ("o3 - Full advanced reasoning model", "o3"),
            ("o1 - Premier reasoning and problem-solving model", "o1"),
        ],
        "anthropic": [
            ("Claude Haiku 3.5 - Fast inference and standard capabilities", "claude-3-5-haiku-latest"),
            ("Claude Sonnet 3.5 - Highly capable standard model", "claude-3-5-sonnet-latest"),
            ("Claude Sonnet 3.7 - Exceptional hybrid reasoning and agentic capabilities", "claude-3-7-sonnet-latest"),
            ("Claude Sonnet 4 - High performance and excellent reasoning", "claude-sonnet-4-0"),
            ("Claude Opus 4 - Most powerful Anthropic model", "	claude-opus-4-0"),
        ],
        "google": [
            ("Gemini 2.0 Flash-Lite - Cost efficiency and low latency", "gemini-2.0-flash-lite"),
            ("Gemini 2.0 Flash - Next generation features, speed, and thinking", "gemini-2.0-flash"),
            ("Gemini 2.5 Flash - Adaptive thinking, cost efficiency", "gemini-2.5-flash-preview-05-20"),
            ("Gemini 2.5 Pro", "gemini-2.5-pro-preview-06-05"),
        ],
        "deepseek": [
            ("DeepSeek Chat - Advanced reasoning and problem-solving", "deepseek-chat"),
            ("DeepSeek Coder - Specialized for complex coding tasks", "deepseek-coder"),
            ("DeepSeek Reasoner - Enhanced reasoning capabilities", "deepseek-reasoner"),
        ],
        "openrouter": [
            ("DeepSeek V3 - a 685B-parameter, mixture-of-experts model", "deepseek/deepseek-chat-v3-0324:free"),
            ("Deepseek - latest iteration of the flagship chat model family from the DeepSeek team.", "deepseek/deepseek-chat-v3-0324:free"),
        ],
        "ollama": [
            ("llama3.1 local", "llama3.1"),
            ("qwen3", "qwen3"),
        ]
    }
    
    choice = questionary.select(
        "選擇您的 [深度思考 LLM 引擎]：",
        choices=[
            questionary.Choice(display, value=value)
            for display, value in DEEP_AGENT_OPTIONS[provider.lower()]
        ],
        instruction="\n- 使用方向鍵導航\n- 按 Enter 選擇",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]未選擇深度思考 LLM 引擎。正在退出...[/red]")
        exit(1)

    return choice

def select_llm_provider() -> tuple[str, str]:
    """使用互動式選擇器選擇 LLM 提供者。"""
    # Define LLM provider options with their corresponding endpoints
    BASE_URLS = [
        ("DeepSeek", "https://api.deepseek.com/v1"),
        ("OpenAI", "https://api.openai.com/v1"),
        ("Anthropic", "https://api.anthropic.com/"),
        ("Google", "https://generativelanguage.googleapis.com/v1"),
        ("Openrouter", "https://openrouter.ai/api/v1"),
        ("Ollama", "http://localhost:11434/v1"),        
    ]
    
    choice = questionary.select(
        "選擇您的 LLM 提供者：",
        choices=[
            questionary.Choice(display, value=(display, value))
            for display, value in BASE_URLS
        ],
        instruction="\n- 使用方向鍵導航\n- 按 Enter 選擇",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()
    
    if choice is None:
        console.print("\n[red]未選擇 LLM 後端。正在退出...[/red]")
        exit(1)
    
    display_name, url = choice
    print(f"您選擇了：{display_name}\t網址：{url}")
    
    return display_name, url
