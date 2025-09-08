import os
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

# ユーザーを指定VCに移動
@bot.command()
async def move(ctx, member: discord.Member, channel: discord.VoiceChannel):
    try:
        await member.move_to(channel)
        await ctx.send(f"✅ {member.display_name} を {channel.name} に移動しました")
    except Exception as e:
        await ctx.send(f"❌ 移動に失敗しました: {e}")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("環境変数 DISCORD_TOKEN が設定されていません！")

bot.run(TOKEN)
