from typing import Optional
import datetime
import typer
from pathlib import Path
from functools import wraps
from rich.console import Console
from rich.panel import Panel
from rich.spinner import Spinner
from rich.live import Live
from rich.columns import Columns
from rich.markdown import Markdown
from rich.layout import Layout
from rich.text import Text
from rich.live import Live
from rich.table import Table
from collections import deque
import time
from rich.tree import Tree
from rich import box
from rich.align import Align
from rich.rule import Rule

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from cli.models import AnalystType
from cli.utils import *

console = Console()

app = typer.Typer(
    name="TradingAgents",
    help="TradingAgents CLI: Multi-Agents LLM Financial Trading Framework",
    add_completion=True,  # Enable shell completion
)


# Create a deque to store recent messages with a maximum length
class MessageBuffer:
    def __init__(self, max_length=100):
        self.messages = deque(maxlen=max_length)
        self.tool_calls = deque(maxlen=max_length)
        self.current_report = None
        self.final_report = None  # Store the complete final report
        self.agent_status = {
            # Analyst Team
            "市場分析師": "pending",
            "社交分析師": "pending",
            "新聞分析師": "pending",
            "基本面分析師": "pending",
            # Research Team
            "多頭研究員": "pending",
            "空頭研究員": "pending",
            "研究經理": "pending",
            # Trading Team
            "交易員": "pending",
            # Risk Management Team
            "積極分析師": "pending",
            "中性分析師": "pending",
            "保守分析師": "pending",
            # Portfolio Management Team
            "投資組合經理": "pending",
        }
        self.current_agent = None
        self.report_sections = {
            "market_report": None,
            "sentiment_report": None,
            "news_report": None,
            "fundamentals_report": None,
            "investment_plan": None,
            "trader_investment_plan": None,
            "final_trade_decision": None,
        }

    def add_message(self, message_type, content):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.messages.append((timestamp, message_type, content))

    def add_tool_call(self, tool_name, args):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.tool_calls.append((timestamp, tool_name, args))

    def update_agent_status(self, agent, status):
        if agent in self.agent_status:
            self.agent_status[agent] = status
            self.current_agent = agent

    def update_report_section(self, section_name, content):
        if section_name in self.report_sections:
            self.report_sections[section_name] = content
            self._update_current_report()

    def _update_current_report(self):
        # For the panel display, only show the most recently updated section
        latest_section = None
        latest_content = None

        # Find the most recently updated section
        for section, content in self.report_sections.items():
            if content is not None:
                latest_section = section
                latest_content = content
               
        if latest_section and latest_content:
            # Format the current section for display
            section_titles = {
                "market_report": "市場分析",
            "sentiment_report": "社交情緒",
            "news_report": "新聞分析",
            "fundamentals_report": "基本面分析",
            "investment_plan": "研究團隊決策",
            "trader_investment_plan": "交易團隊計劃",
            "final_trade_decision": "投資組合管理決策",
            }
            self.current_report = (
                f"### {section_titles[latest_section]}\n{latest_content}"
            )

        # Update the final complete report
        self._update_final_report()

    def _update_final_report(self):
        report_parts = []

        # Analyst Team Reports
        if any(
            self.report_sections[section]
            for section in [
                "market_report",
                "sentiment_report",
                "news_report",
                "fundamentals_report",
            ]
        ):
            report_parts.append("## 分析師團隊報告")
            if self.report_sections["market_report"]:
                report_parts.append(
                    f"### 市場分析\n{self.report_sections['market_report']}"
                )
            if self.report_sections["sentiment_report"]:
                report_parts.append(
                    f"### 社交情緒\n{self.report_sections['sentiment_report']}"
                )
            if self.report_sections["news_report"]:
                report_parts.append(
                    f"### 新聞分析\n{self.report_sections['news_report']}"
                )
            if self.report_sections["fundamentals_report"]:
                report_parts.append(
                    f"### 基本面分析\n{self.report_sections['fundamentals_report']}"
                )

        # Research Team Reports
        if self.report_sections["investment_plan"]:
            report_parts.append("## 研究團隊決策")
            report_parts.append(f"{self.report_sections['investment_plan']}")

        # Trading Team Reports
        if self.report_sections["trader_investment_plan"]:
            report_parts.append("## 交易團隊計劃")
            report_parts.append(f"{self.report_sections['trader_investment_plan']}")

        # Portfolio Management Decision
        if self.report_sections["final_trade_decision"]:
            report_parts.append("## 投資組合管理決策")
            report_parts.append(f"{self.report_sections['final_trade_decision']}")

        self.final_report = "\n\n".join(report_parts) if report_parts else None


message_buffer = MessageBuffer()


def create_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3),
    )
    layout["main"].split_column(
        Layout(name="upper", ratio=3), Layout(name="analysis", ratio=5)
    )
    layout["upper"].split_row(
        Layout(name="progress", ratio=2), Layout(name="messages", ratio=3)
    )
    return layout


def update_display(layout, spinner_text=None):
    # Header with welcome message
    layout["header"].update(
        Panel(
            "[bold green]Welcome to TradingAgents CLI[/bold green]\n"
            "[dim]© [Tauric Research](https://github.com/TauricResearch)[/dim]",
            title="Welcome to 2023HK [TradingAgents]",
            border_style="green",
            padding=(1, 2),
            expand=True,
        )
    )

    # Progress panel showing agent status
    progress_table = Table(
        show_header=True,
        header_style="bold magenta",
        show_footer=False,
        box=box.SIMPLE_HEAD,  # Use simple header with horizontal lines
        title=None,  # Remove the redundant Progress title
        padding=(0, 2),  # Add horizontal padding
        expand=True,  # Make table expand to fill available space
    )
    progress_table.add_column("團隊", style="cyan", justify="center", width=20)
    progress_table.add_column("代理", style="green", justify="center", width=20)
    progress_table.add_column("狀態", style="yellow", justify="center", width=20)

    # Group agents by team
    teams = {
        "Analyst Team": [
            "市場分析師",
            "社交分析師",
            "新聞分析師",
            "基本面分析師",
        ],
        "Research Team": ["多頭研究員", "空頭研究員", "研究經理"],
        "Trading Team": ["交易員"],
        "Risk Management": ["積極分析師", "中性分析師", "保守分析師"],
        "Portfolio Management": ["投資組合經理"],
    }

    for team, agents in teams.items():
        # Add first agent with team name
        first_agent = agents[0]
        status = message_buffer.agent_status[first_agent]
        if status == "in_progress":
            spinner = Spinner(
                "dots", text="[blue]進行中[/blue]", style="bold cyan"
            )
            status_cell = spinner
        else:
            status_color = {
                "pending": "yellow",
                "completed": "green",
                "error": "red",
            }.get(status, "white")
            status_text = {
                "pending": "等待中",
                "completed": "已完成",
                "error": "錯誤",
            }.get(status, status)
            status_cell = f"[{status_color}]{status_text}[/{status_color}]"
        progress_table.add_row(team, first_agent, status_cell)

        # Add remaining agents in team
        for agent in agents[1:]:
            status = message_buffer.agent_status[agent]
            if status == "in_progress":
                spinner = Spinner(
                    "dots", text="[blue]進行中[/blue]", style="bold cyan"
                )
                status_cell = spinner
            else:
                status_color = {
                    "pending": "yellow",
                    "completed": "green",
                    "error": "red",
                }.get(status, "white")
                status_text = {
                    "pending": "等待中",
                    "completed": "已完成",
                    "error": "錯誤",
                }.get(status, status)
                status_cell = f"[{status_color}]{status_text}[/{status_color}]"
            progress_table.add_row("", agent, status_cell)

        # Add horizontal line after each team
        progress_table.add_row("─" * 20, "─" * 20, "─" * 20, style="dim")

    layout["progress"].update(
        Panel(progress_table, title="Progress", border_style="cyan", padding=(1, 2))
    )

    # Messages panel showing recent messages and tool calls
    messages_table = Table(
        show_header=True,
        header_style="bold magenta",
        show_footer=False,
        expand=True,  # Make table expand to fill available space
        box=box.MINIMAL,  # Use minimal box style for a lighter look
        show_lines=True,  # Keep horizontal lines
        padding=(0, 1),  # Add some padding between columns
    )
    messages_table.add_column("時間", style="cyan", width=8, justify="center")
    messages_table.add_column("類型", style="green", width=10, justify="center")
    messages_table.add_column(
        "Content", style="white", no_wrap=False, ratio=1
    )  # Make content column expand

    # Combine tool calls and messages
    all_messages = []

    # Add tool calls
    for timestamp, tool_name, args in message_buffer.tool_calls:
        # Truncate tool call args if too long
        if isinstance(args, str) and len(args) > 100:
            args = args[:97] + "..."
        all_messages.append((timestamp, "Tool", f"{tool_name}: {args}"))

    # Add regular messages
    for timestamp, msg_type, content in message_buffer.messages:
        # Convert content to string if it's not already
        content_str = content
        if isinstance(content, list):
            # Handle list of content blocks (Anthropic format)
            text_parts = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'text':
                        text_parts.append(item.get('text', ''))
                    elif item.get('type') == 'tool_use':
                        text_parts.append(f"[Tool: {item.get('name', 'unknown')}]")
                else:
                    text_parts.append(str(item))
            content_str = ' '.join(text_parts)
        elif not isinstance(content_str, str):
            content_str = str(content)
            
        # Truncate message content if too long
        if len(content_str) > 200:
            content_str = content_str[:197] + "..."
        all_messages.append((timestamp, msg_type, content_str))

    # Sort by timestamp
    all_messages.sort(key=lambda x: x[0])

    # Calculate how many messages we can show based on available space
    # Start with a reasonable number and adjust based on content length
    max_messages = 12  # Increased from 8 to better fill the space

    # Get the last N messages that will fit in the panel
    recent_messages = all_messages[-max_messages:]

    # Add messages to table
    for timestamp, msg_type, content in recent_messages:
        # Format content with word wrapping
        wrapped_content = Text(content, overflow="fold")
        messages_table.add_row(timestamp, msg_type, wrapped_content)

    if spinner_text:
        messages_table.add_row("", "Spinner", spinner_text)

    # Add a footer to indicate if messages were truncated
    if len(all_messages) > max_messages:
        messages_table.footer = (
            f"[dim]Showing last {max_messages} of {len(all_messages)} messages[/dim]"
        )

    layout["messages"].update(
        Panel(
            messages_table,
            title="Messages & Tools",
            border_style="blue",
            padding=(1, 2),
        )
    )

    # Analysis panel showing current report
    if message_buffer.current_report:
        layout["analysis"].update(
            Panel(
                Markdown(message_buffer.current_report),
                title="當前報告",
                border_style="green",
                padding=(1, 2),
            )
        )
    else:
        layout["analysis"].update(
            Panel(
                "[italic]等待分析報告...[/italic]",
            title="當前報告",
                border_style="green",
                padding=(1, 2),
            )
        )

    # Footer with statistics
    tool_calls_count = len(message_buffer.tool_calls)
    llm_calls_count = sum(
        1 for _, msg_type, _ in message_buffer.messages if msg_type == "Reasoning"
    )
    reports_count = sum(
        1 for content in message_buffer.report_sections.values() if content is not None
    )

    stats_table = Table(show_header=False, box=None, padding=(0, 2), expand=True)
    stats_table.add_column("統計", justify="center")
    stats_table.add_row(
        f"工具調用: {tool_calls_count} | LLM 調用: {llm_calls_count} | 生成報告: {reports_count}"
    )

    layout["footer"].update(Panel(stats_table, border_style="grey50"))


def get_user_selections():
    """在開始分析顯示之前獲取所有用戶選擇。"""
    # Display ASCII art welcome message
    with open("./cli/static/welcome.txt", "r") as f:
        welcome_ascii = f.read()

    # Create welcome box content
    welcome_content = f"{welcome_ascii}\n"
    welcome_content += "[bold green]TradingAgents: 多代理 LLM 金融交易框架 - CLI[/bold green]\n\n"
    welcome_content += "[bold]工作流程步驟：[/bold]\n"
    welcome_content += "I. 分析師團隊 → II. 研究團隊 → III. 交易員 → IV. 風險管理 → V. 投資組合管理\n\n"
    welcome_content += (
        "[dim]Built by [Tauric Research](https://github.com/TauricResearch)[/dim]"
    )

    # Create and center the welcome box
    welcome_box = Panel(
        welcome_content,
        border_style="green",
        padding=(1, 2),
        title="歡迎使用 TradingAgents",
        subtitle="多代理 LLM 金融交易框架",
    )
    console.print(Align.center(welcome_box))
    console.print()  # Add a blank line after the welcome box

    # Create a boxed questionnaire for each step
    def create_question_box(title, prompt, default=None):
        box_content = f"[bold]{title}[/bold]\n"
        box_content += f"[dim]{prompt}[/dim]"
        if default:
            box_content += f"\n[dim]Default: {default}[/dim]"
        return Panel(box_content, border_style="blue", padding=(1, 2))

    # Step 1: Ticker symbol
    console.print(
        create_question_box(
            "步驟 1：股票代號", "請輸入要分析的股票代號", "SPY"
        )
    )
    selected_ticker = get_ticker()

    # Step 2: Analysis date
    default_date = datetime.datetime.now().strftime("%Y-%m-%d")
    console.print(
        create_question_box(
            "步驟 2：分析日期",
            "請輸入分析日期 (YYYY-MM-DD)",
            default_date,
        )
    )
    analysis_date = get_analysis_date()

    # Step 3: Select analysts
    console.print(
        create_question_box(
            "步驟 3：分析師團隊", "選擇您的 LLM 分析師代理進行分析"
        )
    )
    selected_analysts = select_analysts()
    console.print(
        f"[green]已選擇的分析師：[/green] {', '.join(analyst.value for analyst in selected_analysts)}"
    )

    # Step 4: Research depth
    console.print(
        create_question_box(
            "步驟 4：研究深度", "選擇您的研究深度級別"
        )
    )
    selected_research_depth = select_research_depth()

    # Step 5: LLM backend
    console.print(
        create_question_box(
            "步驟 5：LLM 後端", "選擇要使用的服務"
        )
    )
    selected_llm_provider, backend_url = select_llm_provider()
    
    # Step 6: Thinking agents
    console.print(
        create_question_box(
            "步驟 6：思考代理", "選擇您的思考代理進行分析"
        )
    )
    selected_shallow_thinker = select_shallow_thinking_agent(selected_llm_provider)
    selected_deep_thinker = select_deep_thinking_agent(selected_llm_provider)

    return {
        "ticker": selected_ticker,
        "analysis_date": analysis_date,
        "analysts": selected_analysts,
        "research_depth": selected_research_depth,
        "llm_provider": selected_llm_provider.lower(),
        "backend_url": backend_url,
        "shallow_thinker": selected_shallow_thinker,
        "deep_thinker": selected_deep_thinker,
    }


def get_ticker():
    """Get ticker symbol from user input."""
    return typer.prompt("", default="SPY")


def get_analysis_date():
    """從用戶輸入獲取分析日期。"""
    while True:
        date_str = typer.prompt(
            "", default=datetime.datetime.now().strftime("%Y-%m-%d")
        )
        try:
            # Validate date format and ensure it's not in the future
            analysis_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if analysis_date.date() > datetime.datetime.now().date():
                console.print("[red]錯誤：分析日期不能是未來日期[/red]")
                continue
            return date_str
        except ValueError:
            console.print(
                "[red]錯誤：無效的日期格式。請使用 YYYY-MM-DD[/red]"
            )


def display_complete_report(final_state):
    """顯示基於團隊面板的完整分析報告。"""
    console.print("\n[bold green]完整分析報告[/bold green]\n")

    # I. Analyst Team Reports
    analyst_reports = []

    # 市場分析師報告
    if final_state.get("market_report"):
        analyst_reports.append(
            Panel(
                Markdown(final_state["market_report"]),
                title="市場分析師",
                border_style="blue",
                padding=(1, 2),
            )
        )

    # 社交分析師報告
    if final_state.get("sentiment_report"):
        analyst_reports.append(
            Panel(
                Markdown(final_state["sentiment_report"]),
                title="社交分析師",
                border_style="blue",
                padding=(1, 2),
            )
        )

    # 新聞分析師報告
    if final_state.get("news_report"):
        analyst_reports.append(
            Panel(
                Markdown(final_state["news_report"]),
                title="新聞分析師",
                border_style="blue",
                padding=(1, 2),
            )
        )

    # 基本面分析師報告
    if final_state.get("fundamentals_report"):
        analyst_reports.append(
            Panel(
                Markdown(final_state["fundamentals_report"]),
                title="基本面分析師",
                border_style="blue",
                padding=(1, 2),
            )
        )

    if analyst_reports:
        console.print(
            Panel(
                Columns(analyst_reports, equal=True, expand=True),
                title="I. 分析師團隊報告",
                border_style="cyan",
                padding=(1, 2),
            )
        )

    # II. Research Team Reports
    if final_state.get("investment_debate_state"):
        research_reports = []
        debate_state = final_state["investment_debate_state"]

        # 多頭研究員分析
        if debate_state.get("bull_history"):
            research_reports.append(
                Panel(
                    Markdown(debate_state["bull_history"]),
                    title="多頭研究員",
                    border_style="blue",
                    padding=(1, 2),
                )
            )

        # 空頭研究員分析
        if debate_state.get("bear_history"):
            research_reports.append(
                Panel(
                    Markdown(debate_state["bear_history"]),
                    title="空頭研究員",
                    border_style="blue",
                    padding=(1, 2),
                )
            )

        # 研究經理決策
        if debate_state.get("judge_decision"):
            research_reports.append(
                Panel(
                    Markdown(debate_state["judge_decision"]),
                    title="研究經理",
                    border_style="blue",
                    padding=(1, 2),
                )
            )

        if research_reports:
            console.print(
                Panel(
                    Columns(research_reports, equal=True, expand=True),
                    title="II. 研究團隊決策",
                    border_style="magenta",
                    padding=(1, 2),
                )
            )

    # III. Trading Team Reports
    if final_state.get("trader_investment_plan"):
        console.print(
            Panel(
                Panel(
                    Markdown(final_state["trader_investment_plan"]),
                    title="交易員",
                    border_style="blue",
                    padding=(1, 2),
                ),
                title="III. 交易團隊計劃",
                border_style="yellow",
                padding=(1, 2),
            )
        )

    # IV. Risk Management Team Reports
    if final_state.get("risk_debate_state"):
        risk_reports = []
        risk_state = final_state["risk_debate_state"]

        # Aggressive (Risky) Analyst Analysis
        if risk_state.get("risky_history"):
            risk_reports.append(
                Panel(
                    Markdown(risk_state["risky_history"]),
                    title="積極分析師",
                    border_style="blue",
                    padding=(1, 2),
                )
            )

        # Conservative (Safe) Analyst Analysis
        if risk_state.get("safe_history"):
            risk_reports.append(
                Panel(
                    Markdown(risk_state["safe_history"]),
                    title="保守分析師",
                    border_style="blue",
                    padding=(1, 2),
                )
            )

        # 中性分析師分析
        if risk_state.get("neutral_history"):
            risk_reports.append(
                Panel(
                    Markdown(risk_state["neutral_history"]),
                    title="中性分析師",
                    border_style="blue",
                    padding=(1, 2),
                )
            )

        if risk_reports:
            console.print(
                Panel(
                    Columns(risk_reports, equal=True, expand=True),
                    title="IV. 風險管理團隊決策",
                    border_style="red",
                    padding=(1, 2),
                )
            )

        # V. 投資組合經理決策
        if risk_state.get("judge_decision"):
            console.print(
                Panel(
                    Panel(
                        Markdown(risk_state["judge_decision"]),
                        title="投資組合經理",
                        border_style="blue",
                        padding=(1, 2),
                    ),
                    title="V. 投資組合經理決策",
                    border_style="green",
                    padding=(1, 2),
                )
            )


def update_research_team_status(status):
    """Update status for all research team members and 交易員."""
    research_team = ["多頭研究員", "空頭研究員", "研究經理", "交易員"]
    for agent in research_team:
        message_buffer.update_agent_status(agent, status)

def extract_content_string(content):
    """Extract string content from various message formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # Handle Anthropic's list format
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
                elif item.get('type') == 'tool_use':
                    text_parts.append(f"[Tool: {item.get('name', 'unknown')}]")
            else:
                text_parts.append(str(item))
        return ' '.join(text_parts)
    else:
        return str(content)

def run_analysis():
    # First get all user selections
    selections = get_user_selections()

    # Create config with selected research depth
    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = selections["research_depth"]
    config["max_risk_discuss_rounds"] = selections["research_depth"]
    config["quick_think_llm"] = selections["shallow_thinker"]
    config["deep_think_llm"] = selections["deep_thinker"]
    config["backend_url"] = selections["backend_url"]
    config["llm_provider"] = selections["llm_provider"].lower()

    # Initialize the graph
    graph = TradingAgentsGraph(
        [analyst.value for analyst in selections["analysts"]], config=config, debug=True
    )

    # Create result directory
    results_dir = Path(config["results_dir"]) / selections["ticker"] / selections["analysis_date"]
    results_dir.mkdir(parents=True, exist_ok=True)
    report_dir = results_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    log_file = results_dir / "message_tool.log"
    log_file.touch(exist_ok=True)

    def save_message_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, message_type, content = obj.messages[-1]
            content = content.replace("\n", " ")  # Replace newlines with spaces
            with open(log_file, "a") as f:
                f.write(f"{timestamp} [{message_type}] {content}\n")
        return wrapper
    
    def save_tool_call_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            timestamp, tool_name, args = obj.tool_calls[-1]
            args_str = ", ".join(f"{k}={v}" for k, v in args.items())
            with open(log_file, "a") as f:
                f.write(f"{timestamp} [Tool Call] {tool_name}({args_str})\n")
        return wrapper

    def save_report_section_decorator(obj, func_name):
        func = getattr(obj, func_name)
        @wraps(func)
        def wrapper(section_name, content):
            func(section_name, content)
            if section_name in obj.report_sections and obj.report_sections[section_name] is not None:
                content = obj.report_sections[section_name]
                if content:
                    file_name = f"{section_name}.md"
                    with open(report_dir / file_name, "w") as f:
                        f.write(content)
        return wrapper

    message_buffer.add_message = save_message_decorator(message_buffer, "add_message")
    message_buffer.add_tool_call = save_tool_call_decorator(message_buffer, "add_tool_call")
    message_buffer.update_report_section = save_report_section_decorator(message_buffer, "update_report_section")

    # Now start the display layout
    layout = create_layout()

    with Live(layout, refresh_per_second=4) as live:
        # Initial display
        update_display(layout)

        # Add initial messages
        message_buffer.add_message("System", f"Selected ticker: {selections['ticker']}")
        message_buffer.add_message(
            "System", f"Analysis date: {selections['analysis_date']}"
        )
        message_buffer.add_message(
            "System",
            f"Selected analysts: {', '.join(analyst.value for analyst in selections['analysts'])}",
        )
        update_display(layout)

        # Reset agent statuses
        for agent in message_buffer.agent_status:
            message_buffer.update_agent_status(agent, "pending")

        # Reset report sections
        for section in message_buffer.report_sections:
            message_buffer.report_sections[section] = None
        message_buffer.current_report = None
        message_buffer.final_report = None

        # Update agent status to in_progress for the first analyst
        first_analyst = f"{selections['analysts'][0].value.capitalize()} Analyst"
        message_buffer.update_agent_status(first_analyst, "in_progress")
        update_display(layout)

        # Create spinner text
        spinner_text = (
            f"Analyzing {selections['ticker']} on {selections['analysis_date']}..."
        )
        update_display(layout, spinner_text)

        # Initialize state and get graph args
        init_agent_state = graph.propagator.create_initial_state(
            selections["ticker"], selections["analysis_date"]
        )
        args = graph.propagator.get_graph_args()

        # Stream the analysis
        trace = []
        for chunk in graph.graph.stream(init_agent_state, **args):
            if len(chunk["messages"]) > 0:
                # Get the last message from the chunk
                last_message = chunk["messages"][-1]

                # Extract message content and type
                if hasattr(last_message, "content"):
                    content = extract_content_string(last_message.content)  # Use the helper function
                    msg_type = "Reasoning"
                else:
                    content = str(last_message)
                    msg_type = "System"

                # Add message to buffer
                message_buffer.add_message(msg_type, content)                

                # If it's a tool call, add it to tool calls
                if hasattr(last_message, "tool_calls"):
                    for tool_call in last_message.tool_calls:
                        # Handle both dictionary and object tool calls
                        if isinstance(tool_call, dict):
                            message_buffer.add_tool_call(
                                tool_call["name"], tool_call["args"]
                            )
                        else:
                            message_buffer.add_tool_call(tool_call.name, tool_call.args)

                # Update reports and agent status based on chunk content
                # Analyst Team Reports
                if "market_report" in chunk and chunk["market_report"]:
                    message_buffer.update_report_section(
                        "market_report", chunk["market_report"]
                    )
                    message_buffer.update_agent_status("市場分析師", "completed")
                    # Set next analyst to in_progress
                    if "social" in selections["analysts"]:
                        message_buffer.update_agent_status(
                            "社交分析師", "in_progress"
                        )

                if "sentiment_report" in chunk and chunk["sentiment_report"]:
                    message_buffer.update_report_section(
                        "sentiment_report", chunk["sentiment_report"]
                    )
                    message_buffer.update_agent_status("社交分析師", "completed")
                    # Set next analyst to in_progress
                    if "news" in selections["analysts"]:
                        message_buffer.update_agent_status(
                            "新聞分析師", "in_progress"
                        )

                if "news_report" in chunk and chunk["news_report"]:
                    message_buffer.update_report_section(
                        "news_report", chunk["news_report"]
                    )
                    message_buffer.update_agent_status("新聞分析師", "completed")
                    # Set next analyst to in_progress
                    if "fundamentals" in selections["analysts"]:
                        message_buffer.update_agent_status(
                            "基本面分析師", "in_progress"
                        )

                if "fundamentals_report" in chunk and chunk["fundamentals_report"]:
                    message_buffer.update_report_section(
                        "fundamentals_report", chunk["fundamentals_report"]
                    )
                    message_buffer.update_agent_status(
                        "基本面分析師", "completed"
                    )
                    # Set all research team members to in_progress
                    update_research_team_status("in_progress")

                # Research Team - Handle Investment Debate State
                if (
                    "investment_debate_state" in chunk
                    and chunk["investment_debate_state"]
                ):
                    debate_state = chunk["investment_debate_state"]

                    # Update 多頭研究員 status and report
                    if "bull_history" in debate_state and debate_state["bull_history"]:
                        # Keep all research team members in progress
                        update_research_team_status("in_progress")
                        # Extract latest bull response
                        bull_responses = debate_state["bull_history"].split("\n")
                        latest_bull = bull_responses[-1] if bull_responses else ""
                        if latest_bull:
                            message_buffer.add_message("Reasoning", latest_bull)
                            # Update research report with bull's latest analysis
                            message_buffer.update_report_section(
                                "investment_plan",
                                f"### 多頭研究員分析\n{latest_bull}",
                            )

                    # Update 空頭研究員 status and report
                    if "bear_history" in debate_state and debate_state["bear_history"]:
                        # Keep all research team members in progress
                        update_research_team_status("in_progress")
                        # Extract latest bear response
                        bear_responses = debate_state["bear_history"].split("\n")
                        latest_bear = bear_responses[-1] if bear_responses else ""
                        if latest_bear:
                            message_buffer.add_message("Reasoning", latest_bear)
                            # Update research report with bear's latest analysis
                            message_buffer.update_report_section(
                                "investment_plan",
                                f"{message_buffer.report_sections['investment_plan']}\n\n### 空頭研究員分析\n{latest_bear}",
                            )

                    # Update 研究經理 status and final decision
                    if (
                        "judge_decision" in debate_state
                        and debate_state["judge_decision"]
                    ):
                        # Keep all research team members in progress until final decision
                        update_research_team_status("in_progress")
                        message_buffer.add_message(
                            "Reasoning",
                            f"研究經理: {debate_state['judge_decision']}",
                        )
                        # Update research report with final decision
                        message_buffer.update_report_section(
                            "investment_plan",
                            f"{message_buffer.report_sections['investment_plan']}\n\n### 研究經理決策\n{debate_state['judge_decision']}",
                        )
                        # Mark all research team members as completed
                        update_research_team_status("completed")
                        # Set first risk analyst to in_progress
                        message_buffer.update_agent_status(
                            "積極分析師", "in_progress"
                        )

                # Trading Team
                if (
                    "trader_investment_plan" in chunk
                    and chunk["trader_investment_plan"]
                ):
                    message_buffer.update_report_section(
                        "trader_investment_plan", chunk["trader_investment_plan"]
                    )
                    # Set first risk analyst to in_progress
                    message_buffer.update_agent_status("積極分析師", "in_progress")

                # Risk Management Team - Handle Risk Debate State
                if "risk_debate_state" in chunk and chunk["risk_debate_state"]:
                    risk_state = chunk["risk_debate_state"]

                    # Update 積極分析師 status and report
                    if (
                        "current_risky_response" in risk_state
                        and risk_state["current_risky_response"]
                    ):
                        message_buffer.update_agent_status(
                            "積極分析師", "in_progress"
                        )
                        message_buffer.add_message(
                            "Reasoning",
                            f"積極分析師: {risk_state['current_risky_response']}",
                        )
                        # Update risk report with 積極分析師's latest analysis only
                        message_buffer.update_report_section(
                            "final_trade_decision",
                            f"### 積極分析師分析\n{risk_state['current_risky_response']}",
                        )

                    # Update 保守分析師 status and report
                    if (
                        "current_safe_response" in risk_state
                        and risk_state["current_safe_response"]
                    ):
                        message_buffer.update_agent_status(
                            "保守分析師", "in_progress"
                        )
                        message_buffer.add_message(
                            "Reasoning",
                            f"保守分析師: {risk_state['current_safe_response']}",
                        )
                        # Update risk report with 保守分析師's latest analysis only
                        message_buffer.update_report_section(
                            "final_trade_decision",
                            f"### 保守分析師分析\n{risk_state['current_safe_response']}",
                        )

                    # Update 中性分析師 status and report
                    if (
                        "current_neutral_response" in risk_state
                        and risk_state["current_neutral_response"]
                    ):
                        message_buffer.update_agent_status(
                            "中性分析師", "in_progress"
                        )
                        message_buffer.add_message(
                            "Reasoning",
                            f"中性分析師: {risk_state['current_neutral_response']}",
                        )
                        # Update risk report with 中性分析師's latest analysis only
                        message_buffer.update_report_section(
                            "final_trade_decision",
                            f"### 中性分析師分析\n{risk_state['current_neutral_response']}",
                        )

                    # Update 投資組合經理 status and final decision
                    if "judge_decision" in risk_state and risk_state["judge_decision"]:
                        message_buffer.update_agent_status(
                            "投資組合經理", "in_progress"
                        )
                        message_buffer.add_message(
                            "Reasoning",
                            f"投資組合經理: {risk_state['judge_decision']}",
                        )
                        # Update risk report with final decision only
                        message_buffer.update_report_section(
                            "final_trade_decision",
                            f"### 投資組合經理決策\n{risk_state['judge_decision']}",
                        )
                        # Mark risk analysts as completed
                        message_buffer.update_agent_status("積極分析師", "completed")
                        message_buffer.update_agent_status("保守分析師", "completed")
                        message_buffer.update_agent_status(
                            "中性分析師", "completed"
                        )
                        message_buffer.update_agent_status(
                            "投資組合經理", "completed"
                        )

                # Update the display
                update_display(layout)

            trace.append(chunk)

        # Get final state and decision
        final_state = trace[-1]
        decision = graph.process_signal(final_state["final_trade_decision"])

        # Update all agent statuses to completed
        for agent in message_buffer.agent_status:
            message_buffer.update_agent_status(agent, "completed")

        message_buffer.add_message(
            "分析", f"已完成 {selections['analysis_date']} 的分析"
        )

        # Update final report sections
        for section in message_buffer.report_sections.keys():
            if section in final_state:
                message_buffer.update_report_section(section, final_state[section])

        # Display the complete final report
        display_complete_report(final_state)

        update_display(layout)


@app.command()
def analyze():
    run_analysis()


if __name__ == "__main__":
    app()
