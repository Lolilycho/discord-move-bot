import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# .env を読み込む
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError(".envにDISCORD_TOKENが設定されていません！")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

# 複数ユーザー用のView
class MultiMoveView(discord.ui.View):
    def __init__(self, moves: list[tuple[discord.Member, discord.VoiceChannel]]):
        super().__init__(timeout=None)
        for member, channel in moves:
            self.add_item(MoveButton(member, channel))

class MoveButton(discord.ui.Button):
    def __init__(self, member: discord.Member, channel: discord.VoiceChannel):
        super().__init__(label=f"{member.display_name} → {channel.name}", style=discord.ButtonStyle.primary)
        self.member = member
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        try:
            await self.member.move_to(self.channel)
            await interaction.response.send_message(
                f"✅ {self.member.display_name} を {self.channel.name} に移動しました", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ 移動に失敗しました: {e}", ephemeral=True
            )

# コマンドで複数ユーザーのボタンを作成
@bot.command()
async def multi_move(ctx, *args):
    """
    使い方例:
    !multi_move @太郎 #会議室 @花子 #会議室
    """
    if len(args) % 2 != 0:
        await ctx.send("引数は「@ユーザー #チャンネル」のセットで入力してください")
        return

    moves = []
    for i in range(0, len(args), 2):
        member = await commands.MemberConverter().convert(ctx, args[i])
        channel = await commands.VoiceChannelConverter().convert(ctx, args[i + 1])
        moves.append((member, channel))

    view = MultiMoveView(moves)
    await ctx.send("移動ボタンです", view=view)

bot.run(TOKEN)
