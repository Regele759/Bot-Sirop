import discord
from discord.ext import commands

# Payment addresses configuration
PAYMENT_ADDRESSES = {
    "paysafecard": "edileoediboss@gmail.com",
    "ltc": "LU4tnmac98W2EjhuY1xqXRDMrSa6B55kph"
}

COMMISSION_RATE = 0.15  # 15% commission


class ExchangeAmountModal(discord.ui.Modal):
    """Modal to collect transaction amount from user"""
    def __init__(self, payment_method: str):
        super().__init__(title=f"Exchange - {payment_method.upper()}")
        self.payment_method = payment_method
        
        # Add input field for amount
        self.amount_input = discord.ui.TextInput(
            label="Transaction Amount ($)",
            placeholder="e.g., 5, 10, 25.50",
            required=True,
            min_length=1,
            max_length=10
        )
        self.add_item(self.amount_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle form submission"""
        try:
            # Parse the amount
            amount = float(self.amount_input.value)
            
            # Validate amount
            if amount <= 0:
                await interaction.response.send_message(
                    "❌ Amount must be greater than 0!",
                    ephemeral=True
                )
                return
            
            # Calculate commission and final amount
            commission = amount * COMMISSION_RATE
            final_amount = amount - commission
            
            # Get payment address
            payment_address = PAYMENT_ADDRESSES.get(self.payment_method, "N/A")
            
            # Create detailed embed with calculation
            embed = discord.Embed(
                title=f"💱 Exchange Summary - {self.payment_method.upper()}",
                description="Your transaction details below:",
                color=discord.Color.gold()
            )
            
            # Add transaction details
            embed.add_field(
                name="Transaction Amount",
                value=f"💵 ${amount:.2f}",
                inline=True
            )
            embed.add_field(
                name="Commission (15%)",
                value=f"💸 -${commission:.2f}",
                inline=True
            )
            embed.add_field(
                name="Amount After Commission",
                value=f"💰 ${final_amount:.2f}",
                inline=True
            )
            
            # Add payment address
            embed.add_field(
                name="Payment Address",
                value=f"```{payment_address}```",
                inline=False
            )
            
            # Add instructions
            embed.add_field(
                name="📋 Instructions",
                value=(
                    f"1. Copy the payment address above\n"
                    f"2. Send exactly **${amount:.2f}** using {self.payment_method.upper()}\n"
                    f"3. You will receive **${final_amount:.2f}** after the 15% commission is applied\n"
                    f"4. Keep proof of payment for your records\n"
                    f"5. Once received, your order will be processed immediately."
                ),
                inline=False
            )
            
            embed.set_footer(text="⚠️ Do not share this address with others. Do not modify the amount.")
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1995/1995467.png")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid amount! Please enter a valid number (e.g., 5, 10.50)",
                ephemeral=True
            )
        except Exception as e:
            print(f"Error in exchange modal: {e}")
            await interaction.response.send_message(
                f"❌ An error occurred: {str(e)}",
                ephemeral=True
            )


class ExchangePaymentSelect(discord.ui.Select):
    """Select menu to choose payment method"""
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Paysafecard",
                value="paysafecard",
                emoji="💳",
                description="Exchange using Paysafecard"
            ),
            discord.SelectOption(
                label="Litecoin (LTC)",
                value="ltc",
                emoji="₿",
                description="Exchange using Litecoin"
            ),
        ]
        super().__init__(
            placeholder="Select your payment method...",
            options=options,
            min_values=1,
            max_values=1
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle payment method selection"""
        payment_method = self.values[0]
        
        # Show modal for amount input
        modal = ExchangeAmountModal(payment_method)
        await interaction.response.send_modal(modal)


class ExchangeView(discord.ui.View):
    """View to hold the exchange payment select menu"""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ExchangePaymentSelect())


def setup_exchange_commands(bot: commands.Bot):
    """Set up exchange commands for the bot"""
    
    @bot.command(name='exchange', help='Start an exchange with automatic commission calculation')
    async def exchange_command(ctx):
        """
        Create an exchange panel with payment method selection
        Usage: !exchange
        """
        embed = discord.Embed(
            title="💱 Exchange System",
            description=(
                "Select your preferred payment method below to start the exchange!\n\n"
                "**Commission:** 15% fee applied to all transactions"
            ),
            color=discord.Color.gold()
        )
        embed.add_field(
            name="💳 Paysafecard",
            value="Fast and secure payments",
            inline=False
        )
        embed.add_field(
            name="₿ Litecoin (LTC)",
            value="Cryptocurrency payments",
            inline=False
        )
        embed.add_field(
            name="📊 Example Calculation",
            value="$5.00 transaction → $0.75 commission → $4.25 you receive",
            inline=False
        )
        embed.set_footer(text="Click the button below to select your payment method")
        
        await ctx.send(embed=embed, view=ExchangeView())
        
        # Optional: delete the command message to keep chat clean
        try:
            await ctx.message.delete()
        except:
            pass
