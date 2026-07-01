import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from random_colors import get_random_color, display_random_colors, COLORS, RESET

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = 1167122755800547483  # Direct ID - hardcoded

# Payment addresses configuration
PAYMENT_ADDRESSES = {
    "paysafecard": "edileoediboss@gmail.com",
    "ltc": "LU4tnmac98W2EjhuY1xqXRDMrSa6B55kph"
}

# Set up bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Ticket counter
ticket_counter = {}

# Custom Select Menu for Tickets
class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Help/Question", value="help", emoji="❓"),
            discord.SelectOption(label="Purchase", value="purchase", emoji="🛒"),
            discord.SelectOption(label="Claim Reward", value="reward", emoji="🎁"),
        ]
        super().__init__(placeholder="Select a ticket type...", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        ticket_type = self.values[0]
        
        # Initialize counter for this guild
        if guild.id not in ticket_counter:
            ticket_counter[guild.id] = 0
        
        ticket_counter[guild.id] += 1
        ticket_number = ticket_counter[guild.id]
        
        # Create ticket channel name based on type
        type_names = {
            "help": "help",
            "purchase": "purchase",
            "reward": "reward"
        }
        
        channel_name = f"ticket-{type_names[ticket_type]}-{ticket_number}"
        
        # Create the ticket channel
        try:
            # Get or create a category for tickets
            category = None
            for cat in guild.categories:
                if cat.name.lower() == "tickets":
                    category = cat
                    break
            
            # Create permissions for the channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            
            # Create the channel
            ticket_channel = await guild.create_text_channel(
                channel_name,
                category=category,
                overwrites=overwrites
            )
            
            # Send ticket info embed
            embed = discord.Embed(
                title=f"🎫 Ticket #{ticket_number}",
                description=f"**Type:** {ticket_type.upper()}\n**User:** {user.mention}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Status", value="🟢 Open", inline=False)
            embed.add_field(name="Instructions", value="Describe your issue or request below.", inline=False)
            embed.set_footer(text=f"Ticket ID: {ticket_number}")
            
            await ticket_channel.send(embed=embed)
            await ticket_channel.send(f"Welcome {user.mention}! A staff member will assist you shortly.")
            
            # Respond to user
            await interaction.response.send_message(
                f"✅ Ticket created! Check {ticket_channel.mention}",
                ephemeral=True
            )
            
        except Exception as e:
            print(f"Error creating ticket: {e}")
            await interaction.response.send_message(
                "❌ Error creating ticket. Please try again.",
                ephemeral=True
            )

# Payment Select Menu for Trade
class PaymentSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Paysafecard", value="paysafecard", emoji="💳"),
            discord.SelectOption(label="LTC", value="ltc", emoji="₿"),
        ]
        super().__init__(placeholder="Select payment method...", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: discord.Interaction):
        payment_method = self.values[0]
        payment_address = PAYMENT_ADDRESSES.get(payment_method, "N/A")
        
        # Create embed with payment address
        embed = discord.Embed(
            title=f"💰 {payment_method.upper()} Payment Address",
            description=f"Send your payment to the address below:",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="Payment Address",
            value=f"```{payment_address}```",
            inline=False
        )
        embed.add_field(
            name="Instructions",
            value="Please copy the address above and send your payment. Once received, your order will be processed immediately.",
            inline=False
        )
        embed.set_footer(text="Do not share this address with others.")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# View class to hold the ticket select menu
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

# View class to hold the payment select menu
class PaymentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(PaymentSelect())

@bot.event
async def on_ready():
    """Called when bot successfully logs in"""
    print(f'{bot.user} has connected to Discord!')
    print('------')

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    """Detect when a member boosts the server"""
    # Check if the member just started boosting
    if before.premium_since is None and after.premium_since is not None:
        # Member just boosted the server
        guild = after.guild
        
        # Try to find a general or announcements channel
        channel = None
        for ch in guild.text_channels:
            if ch.name in ['general', 'announcements', 'boost', 'boosts']:
                if ch.permissions_for(guild.me).send_messages:
                    channel = ch
                    break
        
        # If no specific channel found, use the first available text channel
        if channel is None:
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).send_messages:
                    channel = ch
                    break
        
        if channel:
            # Create embed with boost message
            embed = discord.Embed(
                title="⭐ Thank You for Boosting!",
                description="Iti multumim pentru boost ⭐ Speram sa ai o zi buna !",
                color=discord.Color.pink()
            )
            embed.set_author(name=after.name, icon_url=after.avatar.url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1/default_boost_image.png")
            
            # Send the message with the Discord boost card image
            await channel.send(
                embed=embed,
                file=discord.File("https://media.discordapp.net/attachments/1/boost_card.png") if os.path.exists("boost_card.png") else None
            )

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
        description="A Discord bot that generates random colors and manages support tickets",
        color=discord.Color.blue()
    )
    embed.add_field(name="!color [count]", value="Generate random colors (default: 5, max: 20)", inline=False)
    embed.add_field(name="!colors", value="Show all available colors", inline=False)
    embed.add_field(name="!ping", value="Check bot latency", inline=False)
    embed.add_field(name="!dmsiropel", value="Request help from Siropel", inline=False)
    embed.add_field(name="!ticketpanel", value="Create a ticket support panel", inline=False)
    embed.add_field(name="!trade", value="Start a trade and select payment method", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='dmsiropel', help='Request help from Siropel')
async def dmsiropel_command(ctx):
    """
    Send a help request DM to Siropel
    Usage: !dmsiropel
    """
    try:
        owner = await bot.fetch_user(OWNER_ID)
        
        # Create embed for the notification
        embed = discord.Embed(
            title="🆘 HELP REQUEST",
            description=f"{ctx.author} needs help!",
            color=discord.Color.red()
        )
        embed.add_field(name="User", value=f"{ctx.author.mention}\n{ctx.author}", inline=False)
        embed.add_field(name="User ID", value=ctx.author.id, inline=False)
        embed.add_field(name="Server", value=ctx.guild.name if ctx.guild else "Direct Message", inline=False)
        embed.add_field(name="Channel", value=ctx.channel.mention if hasattr(ctx.channel, 'mention') else "Direct Message", inline=False)
        
        # Send DM to Siropel
        await owner.send(embed=embed)
        
        # Confirm to user
        await ctx.send(f"✅ Help request sent to Siropel!")
        
    except Exception as e:
        print(f"Error sending help notification: {e}")
        await ctx.send("❌ Error sending help request. Please try again later.")

@bot.command(name='ticketpanel', help='Create a support ticket panel')
async def ticketpanel_command(ctx):
    """
    Create a ticket panel with select menu
    Usage: !ticketpanel
    """
    embed = discord.Embed(
        title="🎫 Support Ticket System",
        description="Select a ticket type below to get started!",
        color=discord.Color.green()
    )
    embed.add_field(name="❓ Help/Question", value="Ask a question or get help", inline=False)
    embed.add_field(name="🛒 Purchase", value="Purchase-related inquiries", inline=False)
    embed.add_field(name="🎁 Claim Reward", value="Claim your rewards", inline=False)
    
    await ctx.send(embed=embed, view=TicketView())
    await ctx.message.delete()  # Optional: delete the command message

@bot.command(name='trade', help='Start a trade and select payment method')
async def trade_command(ctx):
    """
    Create a trade panel with payment method selection
    Usage: !trade
    """
    embed = discord.Embed(
        title="💱 Trade - Select Payment Method",
        description="Choose your preferred payment method below to start the trade!",
        color=discord.Color.gold()
    )
    embed.add_field(name="💳 Paysafecard", value="Pay with Paysafecard", inline=False)
    embed.add_field(name="₿ LTC", value="Pay with Litecoin", inline=False)
    
    await ctx.send(embed=embed, view=PaymentView())

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env file!")
        print("Please create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        bot.run(TOKEN)
