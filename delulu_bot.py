from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, TypedDict

from openai import OpenAI
from openai import APIConnectionError, APIError, AuthenticationError, RateLimitError
from pyfiglet import figlet_format
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
CONFIG_FILE = Path(".delulu_config")
SYSTEM_PROMPT = "You are Delulu Bot."
MODEL_NAME = "gpt-4o-mini"


class ChatMessage(TypedDict):
    role: str
    content: str


@dataclass
class ConfigStore:
    """Persistent storage for CLI configuration."""

    config_file: Path = CONFIG_FILE

    def save_api_key(self, key: str) -> None:
        cleaned_key = key.strip()
        if not cleaned_key:
            raise ValueError("API key cannot be empty.")

        self.config_file.write_text(cleaned_key, encoding="utf-8")

    def load_api_key(self) -> str | None:
        if not self.config_file.exists():
            return None

        api_key = self.config_file.read_text(encoding="utf-8").strip()
        return api_key or None


@dataclass
class DeluluChatService:
    """Handles interactions with OpenAI Chat Completions API."""

    api_key: str
    model_name: str = MODEL_NAME

    def __post_init__(self) -> None:
        self.client = OpenAI(api_key=self.api_key)

    def ask(self, messages: List[ChatMessage]) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )

        reply = response.choices[0].message.content
        if not reply:
            raise RuntimeError("Model returned an empty response.")

        return reply


@dataclass
class DeluluBotApp:
    config: ConfigStore

    @staticmethod
    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def status_badge(api_key: str | None) -> str:
        return "[green]● API Configured[/green]" if api_key else "[red]● API Not Set[/red]"

    @staticmethod
    def new_conversation() -> List[ChatMessage]:
        return [{"role": "system", "content": SYSTEM_PROMPT}]

    @staticmethod
    def save_conversation(conversation: List[ChatMessage]) -> str:
        filename = f"delulu_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w", encoding="utf-8") as file:
            for msg in conversation:
                if msg["role"] == "user":
                    file.write(f"You: {msg['content']}\n")
                elif msg["role"] == "assistant":
                    file.write(f"Delulu: {msg['content']}\n")

        return filename

    def show_menu(self, api_key: str | None) -> None:
        self.clear()
        banner = figlet_format("Delulu Bot", font="slant")

        console.print(f"[bold cyan]{banner}[/bold cyan]")
        console.print(Panel.fit(self.status_badge(api_key), border_style="blue"))
        console.print(
            Panel(
                "[1] Run Chat\n"
                "[2] Set / Update API Key\n"
                "[3] About\n"
                "[4] Exit",
                title="Main Menu",
                border_style="magenta",
            )
        )

    def show_about(self) -> None:
        self.clear()
        console.print(
            Panel.fit(
                "[bold cyan]Delulu Bot v1.0[/bold cyan]\n\n"
                "Rich CLI AI Chatbot\n"
                "GitHub Deployable\n\n"
                "Built with Python + OpenAI API",
                border_style="green",
            )
        )
        input("\nPress Enter to return...")

    def run_chat(self, api_key: str) -> None:
        self.clear()
        console.print(
            Panel.fit(
                "[bold green]Chat Mode[/bold green]\n"
                "Commands: /clear  /new  /save  /history  /help  /exit",
                border_style="green",
            )
        )

        chat_service = DeluluChatService(api_key=api_key)
        conversation = self.new_conversation()

        while True:
            user_input = Prompt.ask("[bold yellow]You").strip()
            if not user_input:
                continue

            command = user_input.lower()
            if command == "/exit":
                break
            if command == "/clear":
                self.clear()
                continue
            if command == "/new":
                conversation = self.new_conversation()
                console.print("[bold cyan]New chat started.[/bold cyan]")
                continue
            if command == "/history":
                self.show_history(conversation)
                continue
            if command == "/save":
                filename = self.save_conversation(conversation)
                console.print(f"[bold cyan]Saved as {filename}[/bold cyan]")
                continue
            if command == "/help":
                console.print(
                    """
[bold cyan]Available Commands:[/bold cyan]
/clear    - Clear screen
/new      - Start new chat
/history  - Show chat history
/save     - Save chat to file
/help     - Show commands
/exit     - Return to menu
"""
                )
                continue

            conversation.append({"role": "user", "content": user_input})

            try:
                with console.status("[bold green]Delulu is thinking..."):
                    reply = chat_service.ask(conversation)
            except AuthenticationError:
                console.print("[bold red]Authentication failed. Please verify your API key.[/bold red]")
                conversation.pop()
                continue
            except RateLimitError:
                console.print("[bold red]Rate limit exceeded. Please try again shortly.[/bold red]")
                conversation.pop()
                continue
            except APIConnectionError:
                console.print("[bold red]Network error while contacting OpenAI.[/bold red]")
                conversation.pop()
                continue
            except APIError as error:
                console.print(f"[bold red]OpenAI API error: {error}[/bold red]")
                conversation.pop()
                continue
            except Exception as error:  # fallback guard for unexpected runtime errors
                console.print(f"[bold red]Unexpected error: {error}[/bold red]")
                conversation.pop()
                continue

            conversation.append({"role": "assistant", "content": reply})
            console.print(Panel(reply, title="[bold green]Delulu[/bold green]", border_style="cyan"))

    @staticmethod
    def show_history(conversation: List[ChatMessage]) -> None:
        console.print("\n[bold magenta]Chat History[/bold magenta]\n")
        for msg in conversation:
            if msg["role"] == "user":
                console.print(f"[bold yellow]You:[/bold yellow] {msg['content']}")
            elif msg["role"] == "assistant":
                console.print(f"[bold green]Delulu:[/bold green] {msg['content']}")
        console.print()

    def run(self) -> None:
        while True:
            api_key = self.config.load_api_key()
            self.show_menu(api_key)

            choice = Prompt.ask("[bold white]Select option").strip()
            if choice == "1":
                if not api_key:
                    console.print("[bold red]API key not configured.[/bold red]")
                    input("Press Enter to continue...")
                else:
                    self.run_chat(api_key)
            elif choice == "2":
                key = Prompt.ask("Enter API Key", password=True)
                try:
                    self.config.save_api_key(key)
                    console.print("[bold green]API Key saved.[/bold green]")
                except ValueError as error:
                    console.print(f"[bold red]{error}[/bold red]")
                input("Press Enter to continue...")
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                self.clear()
                sys.exit(0)
            else:
                console.print("[bold red]Invalid option.[/bold red]")
                input("Press Enter to continue...")


def main() -> None:
    app = DeluluBotApp(config=ConfigStore())
    app.run()


if __name__ == "__main__":
    main()
