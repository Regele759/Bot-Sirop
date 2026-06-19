import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from random_colors import get_random_color, display_random_colors, COLORS, RESET

# Load environment variables from .env file
load_dotenv()

# Get bot token and owner ID from environment
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', '0'))  # Set this in .env file

# Set up bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Called when bot successfully logs in"""
    print(f'{bot.user} has connected to Discord!')
    print('------')

async def send_help_notification(ctx, command_name):
    """Send a DM to the bot owner when someone uses a command"""
    if OWNER_ID == 0:
        print("WARNING: OWNER_ID not set in .env file")
        return
    
    try:
        owner = await bot.fetch_user(OWNER_ID)
        embed = discord.Embed(
            title="🆘 Help Request",
            description=f"**Command Used:** `{command_name}`",
            color=discord.Color.orange()
        )
        embed.add_field(name="User", value=f"{ctx.author.mention} ({ctx.author})", inline=False)
        embed.add_field(name="Server", value=ctx.guild.name if ctx.guild else "DM", inline=False)
        embed.add_field(name="Channel", value=ctx.channel.mention if hasattr(ctx.channel, 'mention') else "DM", inline=False)
        
        await owner.send(embed=embed)
    except Exception as e:
        print(f"Error sending notification: {e}")

@bot.command(name='color', help='Generate random colors')
async def color_command(ctx, count: int = 5):
    """
    Generate random colors
    Usage: !color or !color 10
    """
    await send_help_notification(ctx, 'color')
    
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
    await send_help_notification(ctx, 'colors')
    
    message = "🎨 **AVAILABLE COLORS** 🎨\n```\n"
    
    for color_name, (ansi_code, hex_code) in COLORS.items():
        message += f"● {color_name.upper():12} | Hex: {hex_code}\n"
    
    message += "```"
    await ctx.send(message)

@bot.command(name='ping', help='Check bot latency')
async def ping_command(ctx):
    """Display bot latency"""
    await send_help_notification(ctx, 'ping')
    
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latency: {latency}ms')

@bot.command(name='help', help='Show help information')
async def help_command(ctx):
    """Display custom help information"""
    await send_help_notification(ctx, 'help')
    
    embed = discord.Embed(
        title="🎨 Bot-Sirop Help",
        description="A Discord bot that generates random colors",
        color=discord.Color.blue()
    )
    embed.add_field(name="!color [count]", value="Generate random colors (default: 5, max: 20)", inline=False)
    embed.add_field(name="!colors", value="Show all available colors", inline=False)
    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!help", value="Show this help message", inline=False)
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env file!")
        print("Please create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        bot.run(TOKEN)
