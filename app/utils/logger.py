from rich.console import Console
from rich.text import Text

console = Console()


def log_success(message: str):
    console.print(Text(f"✅ {message}", style="bold green"))


def log_error(message: str):
    console.print(Text(f"❌ {message}", style="bold red"))


def log_info(message: str):
    console.print(Text(f"ℹ️ {message}", style="bold cyan"))
