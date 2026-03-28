import discord
from discord.ext import commands
import os
from webserver import keep_alive

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- CONFIG ----------
PAYMENT_ADDRESS = "TFv3qV8p2B6oinNhGxC3nixGTZBqKGPXr4"
CRYPTO = "USDT (TRC20)"

PLANS = {
    "Bronze": "Bronze Plan Access",
    "Gold": "Gold Plan Access",
    "Diamond": "Diamond Plan Access",
    "Platinum": "Platinum Plan Access",
    "Obsidian": "Obsidian Plan Access"
}

LOG_CHANNEL_NAME = "payment-logs"
# ----------------------------


# ---------- EMBED ----------
def payment_embed():
    embed = discord.Embed(
        title="🛡️ Cyber Security Protection Plans",
        description="Professional Cyber Security Service Plans\nChoose your protection level below.",
        color=0x2b2d31
    )

    embed.add_field(
        name="🥉 Bronze",
        value="Basic Protection\n• Entry Level Security\n• Monitoring",
        inline=False
    )

    embed.add_field(
        name="🥇 Gold",
        value="Advanced Protection\n• Priority Support\n• Threat Detection",
        inline=False
    )

    embed.add_field(
        name="💎 Diamond",
        value="Professional Security\n• Full Monitoring\n• Rapid Response",
        inline=False
    )

    embed.add_field(
        name="🏆 Platinum",
        value="Enterprise Grade\n• Advanced Defense\n• Premium Support",
        inline=False
    )

    embed.add_field(
        name="🖤 Obsidian",
        value="Ultimate Protection\n• Maximum Security\n• VIP Priority",
        inline=False
    )

    embed.add_field(
        name="💳 Crypto Payment",
        value=f"**Coin:** {CRYPTO}\n"
              f"**Network:** TRON (TRC20)\n"
              f"**Wallet:** `{PAYMENT_ADDRESS}`\n\n"
              f"⚠️ Send ONLY TRC20",
        inline=False
    )

    embed.set_footer(text="Submit TXID after payment to receive access.")
    return embed
# ----------------------------


# ---------- BUTTON VIEW ----------
class PaymentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Buy / Upgrade Plan", style=discord.ButtonStyle.green)
    async def buy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TXIDModal())


# ---------- TXID MODAL ----------
class TXIDModal(discord.ui.Modal, title="Submit Payment TXID"):

    txid = discord.ui.TextInput(
        label="Transaction ID (TXID)",
        placeholder="Paste your crypto transaction ID here",
        required=True,
        max_length=200
    )

    plan = discord.ui.TextInput(
        label="Plan Purchased",
        placeholder="Bronze / Gold / Diamond / Platinum / Obsidian",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):

        guild = interaction.guild

        # Give role instantly (no waiting)
        role = discord.utils.get(guild.roles, name=self.plan.value)

        if role:
            await interaction.user.add_roles(role)

        # Log payment
        log_channel = discord.utils.get(
            guild.text_channels, name=LOG_CHANNEL_NAME
        )

        if log_channel:
            log_embed = discord.Embed(
                title="💰 New Payment Submitted",
                color=0x00ff88
            )
            log_embed.add_field(name="User", value=interaction.user.mention)
            log_embed.add_field(name="Plan", value=self.plan.value)
            log_embed.add_field(name="TXID", value=self.txid.value, inline=False)

            await log_channel.send(embed=log_embed)

        await interaction.response.send_message(
            "✅ Payment submitted! Access granted if valid.",
            ephemeral=True
        )


# ---------- EVENTS ----------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.add_view(PaymentView())


# ---------- COMMAND ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    """Send payment embed"""
    await ctx.send(embed=payment_embed(), view=PaymentView())


# ---------- KEEP ALIVE ----------
keep_alive()

# ---------- RUN ----------
bot.run(TOKEN)
