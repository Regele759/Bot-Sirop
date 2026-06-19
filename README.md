# Bot-Sirop 🎨

A Discord bot that generates random colors with hex codes.

## Features

- 🎨 Generate random colors with ANSI codes and hex values
- 🤖 Discord bot integration
- 💻 Interactive color generation
- 📋 View all available colors

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Regele759/Bot-Sirop.git
cd Bot-Sirop
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your Discord bot token:
```
DISCORD_TOKEN=your_actual_discord_bot_token_here
```

### 4. Run the bot
```bash
python main.py
```

## Commands

- `!color` - Generate 5 random colors
- `!color <number>` - Generate N random colors (max 20)
- `!colors` - Show all 12 available colors
- `!ping` - Check bot latency

## Available Colors

- Red, Green, Yellow, Blue
- Magenta, Cyan, White, Orange
- Purple, Pink, Lime, Navy

## Requirements

- Python 3.8+
- discord.py 2.3.2
- python-dotenv 1.0.0

## License

MIT

## Author

Regele759
