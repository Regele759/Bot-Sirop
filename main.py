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

@bot.command(name='help', help='Show help information')
async def help_command(ctx):
    """Display custom help information"""
    embed = discord.Embed(
        title="🎨 Bot-Sirop Help",
        description="A Discord bot that generates random colors",
        color=discord.Color.blue()
    )
    embed.add_field(name="!color [count]", value="Generate random colors (default: 5, max: 20)", inline=False)
    embed.add_field(name="!colors", value="Show all available colors", inline=False)
    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!needhelp [message]", value="Request help from the bot owner", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='needhelp', help='Request help from the bot owner')
async def needhelp_command(ctx, *, message: str = None):
    """
    Request help from the bot owner
    Usage: !needhelp or !needhelp I need help with something
    """
    if OWNER_ID == 0:
        await ctx.send("❌ Bot owner not configured. Please contact the administrator.")
        return
    
    try:
        owner = await bot.fetch_user(OWNER_ID)
        
        # Create embed for the notification
        embed = discord.Embed(
            title="🆘 HELP REQUEST",
            description=f"**Message:** {message if message else '(No message provided)'}",
            color=discord.Color.red()
        )
        embed.add_field(name="User", value=f"{ctx.author.mention}\n{ctx.author}", inline=False)
        embed.add_field(name="Server", value=ctx.guild.name if ctx.guild else "Direct Message", inline=False)
        embed.add_field(name="Channel", value=ctx.channel.mention if hasattr(ctx.channel, 'mention') else "Direct Message", inline=False)
        embed.add_field(name="User ID", value=ctx.author.id, inline=False)
        
        # Send DM to owner
        await owner.send(embed=embed)
        
        # Confirm to user
        await ctx.send(f"✅ Help request sent! {ctx.author.mention} will be notified shortly.")
        
    except Exception as e:
        print(f"Error sending help notification: {e}")
        await ctx.send("❌ Error sending help request. Please try again later.")

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env file!")
        print("Please create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        bot.run(TOKEN)
