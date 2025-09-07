import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True   # メッセージ内容
intents.members = True           # メンバー操作

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("環境変数 DISCORD_TOKEN が設定されていません！")

bot.run(TOKEN)
