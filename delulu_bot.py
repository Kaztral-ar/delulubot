import os
import sys
from datetime import datetime
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pyfiglet import figlet_format

CONFIG_FILE = ".delulu_config"
console = Console()


# ---------------- CONFIG ---------------- #

def save_api_key(key):
    with open(CONFIG_FILE, "w") as f:
        f.write(key.strip())


def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return None


def clear():
    os.system("clear" if os.name == "posix" else "cls")


# ---------------- UI ---------------- #

def status_badge(api_key):
    if api_key:
        return "[bold green]● API Key Configured[/bold green]"
    return "[bold red]● API Key Not Set[/bold red]"


def show_menu(api_key):
    clear()

    banner = figlet_format("Delulu Bot", font="slant")
    console.print(f"[bold cyan]{banner}[/bold cyan]")

    console.print(Panel.fit(
        status_badge(api_key),
        border_style="blue"
    ))

    menu = """
[1] Run Chat
[2] Set / Update API Key
[3] About
[4] Exit
"""
    console.print(Panel(menu, title="Main Menu", border_style="magenta"))


# ---------------- CHAT ---------------- #

def run_chat(api_key):
    clear()

    console.print(Panel.fit(
        "[bold green]Chat Mode[/bold green]\n"
        "Commands: /clear  /new  /save  /history  /help  /exit",
        border_style="green"
    ))

    client = OpenAI(api_key=api_key)

    def new_conversation():
        return [{"role": "system", "content": "You are Delulu Bot."}]

    def show_history(conv):
        console.print("\n[bold magenta]Chat History[/bold magenta]\n")
        for msg in conv:
            if msg["role"] == "user":
                console.print(f"[bold yellow]You:[/bold yellow] {msg['content']}")
            elif msg["role"] == "assistant":
                console.print(f"[bold green]Delulu:[/bold green] {msg['content']}")
        console.print()

    def save_conversation(conv):
        filename = f"delulu_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for msg in conv:
                if msg["role"] == "user":
                    f.write(f"You: {msg['content']}\n")
                elif msg["role"] == "assistant":
                    f.write(f"Delulu: {msg['content']}\n")
        console.print(f"[bold cyan]Saved as {filename}[/bold cyan]")

    conversation = new_conversation()

    while True:
        user = Prompt.ask("[bold yellow]You")
        cmd = user.lower().strip()

        # ---------- COMMANDS ---------- #
        if cmd == "/exit":
            break

        if cmd == "/clear":
            clear()
            continue

        if cmd == "/new":
            conversation = new_conversation()
            console.print("[bold cyan]New chat started.[/bold cyan]")
            continue

        if cmd == "/history":
            show_history(conversation)
            continue

        if cmd == "/save":
            save_conversation(conversation)
            continue

        if cmd == "/help":
            console.print("""
[bold cyan]Available Commands:[/bold cyan]
/clear    - Clear screen
/new      - Start new chat
/history  - Show chat history
/save     - Save chat to file
/help     - Show commands
/exit     - Return to menu
""")
            continue
        # -------------------------------- #

        conversation.append({"role": "user", "content": user})

        with console.status("[bold green]Delulu is thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation
            )

        reply = response.choices[0].message.content

        console.print(Panel(
            reply,
            title="[bold green]Delulu[/bold green]",
            border_style="cyan"
        ))

        conversation.append({"role": "assistant", "content": reply})


# ---------------- MAIN ---------------- #

def about():
    clear()
    console.print(Panel.fit(
        "[bold cyan]Delulu Bot v1.0[/bold cyan]\n\n"
        "Rich CLI AI Chatbot\n"
        "GitHub Deployable\n\n"
        "Built with Python + OpenAI API",
        border_style="green"
    ))
    input("\nPress Enter to return...")


def main():
    while True:
        api_key = load_api_key()
        show_menu(api_key)

        choice = Prompt.ask("[bold white]Select option")

        if choice == "1":
            if not api_key:
                console.print("[bold red]API key not configured.[/bold red]")
                input("Press Enter to continue...")
            else:
                run_chat(api_key)

        elif choice == "2":
            key = Prompt.ask("Enter API Key", password=True)
            save_api_key(key)
            console.print("[bold green]API Key saved.[/bold green]")
            input("Press Enter to continue...")

        elif choice == "3":
            about()

        elif choice == "4":
            clear()
            sys.exit()

        else:
            console.print("[bold red]Invalid option.[/bold red]")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
