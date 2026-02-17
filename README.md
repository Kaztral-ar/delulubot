# 🚀 DeluluBot

> A modern, interactive CLI AI assistant — stylish, dynamic, and built for terminal lovers.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Interface-CLI-black?style=for-the-badge&logo=windowsterminal&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

---

## 💡 What is DeluluBot?

**DeluluBot** is a colorful, command-driven terminal AI chatbot that brings a premium chat experience straight to your shell. No browser, no bloat — just you, your terminal, and the power of OpenAI.

Built with:

| Tool | Purpose |
|------|---------|
| 🧠 **OpenAI API** | AI responses |
| 🎨 **Rich** | Beautiful terminal UI |
| 🖼 **PyFiglet** | ASCII art banners |
| 🗂 **Slash Commands** | Fast, intuitive controls |

---

## ✨ Features

**🖥 Clean Main Menu**
A structured, distraction-free home screen with API key status, clear navigation, and secure key input.

**💬 Slash Command Chat System**
Control your session without leaving the keyboard:

| Command | Description |
|---------|-------------|
| `/clear` | Clear the screen |
| `/new` | Start a fresh chat session |
| `/history` | View your conversation history |
| `/save` | Export the conversation to a file |
| `/help` | Show all available commands |
| `/exit` | Return to the main menu |

**🔐 API Key Management**
Set or update your OpenAI key at any time from the main menu. The interface reflects your key status instantly:

```
✅  API Key Configured
❌  API Key Not Set
```

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/Kaztral-ar/delulubot.git
cd delulubot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run DeluluBot**
```bash
python delulu_bot.py
```

---

## 🔑 First-Time Setup

1. Launch the app
2. Select **Set / Update API Key** from the main menu
3. Paste your [OpenAI API key](https://platform.openai.com/api-keys)
4. You're ready to chat

> ⚠️ Chat mode is disabled until an API key is configured.

---

## 📁 Project Structure

```
delulubot/
├── delulu_bot.py      # Main application
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

---

## 🛠 Requirements

- Python **3.9+**
- An active **OpenAI API key**
- Internet connection

```
openai
rich
pyfiglet
```

Install all at once:
```bash
pip install openai rich pyfiglet
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Commit** your changes (`git commit -m 'Add some feature'`)
4. **Push** to the branch (`git push origin feature/your-feature`)
5. **Open** a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<p align="center">
  <i>Because even your terminal deserves intelligence.</i>
</p>

# Configuration
Configuration settings can be adjusted in the `config.json` file. Ensure to provide the correct API keys for any third-party integrations.

# Architecture
The chatbot is built using a client-server architecture:
- **Client:** The user interface that interacts with users.
- **Server:** The backend that handles user requests and processes responses.

# Troubleshooting
- If the bot is not responding, ensure that you have a stable internet connection.
- Check the logs for any error messages that could indicate issues.

# Dependencies
- Node.js
- Express
- Body-parser

# Privacy Information
User data is collected only for the purpose of enhancing the chatbot experience. All data is handled in compliance with privacy regulations.

# Future Enhancements
- Support for voice commands
- Enhanced NLP capabilities
- More integrations with external APIs
