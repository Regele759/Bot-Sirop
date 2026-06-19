import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from random_colors import get_random_color, display_random_colors, COLORS, RESET

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Called when bot successfully logs in"""
    print(f'{bot.user} has connected to Discord!')
    print('------')

@bot.command(name='color', help='Generate random colors')
async def color_command(ctx, count: int = 5):
    """
    Generate random colors
    Usage: !color or !color 10
    """
    if count < 1:
        await ctx.send("Please specify a number greater than 0")
        return
    
    if count > 20:
        await ctx.send("Maximum 20 colors at a time!")
        return
    
    # Build the color message
    message = "🎨 **RANDOM COLORS** 🎨\n```\n"
    
    for i in range(count):
        color_name, (ansi_code, hex_code) = get_random_color()
        message += f"● {color_name.upper():12} | Hex: {hex_code}\n"
    
    message += "```"
    await ctx.send(message)

@bot.command(name='colors', help='Show all available colors')
async def colors_command(ctx):
    """Display all available colors"""
    message = "🎨 **AVAILABLE COLORS** 🎨\n```\n"
    
    for color_name, (ansi_code, hex_code) in COLORS.items():
        message += f"● {color_name.upper():12} | Hex: {hex_code}\n"
    
    message += "```"
    await ctx.send(message)

@bot.command(name='ping', help='Check bot latency')
async def ping_command(ctx):
    """Display bot latency"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latency: {latency}ms')

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env file!")
        print("Please create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        bot.run(TOKEN)
