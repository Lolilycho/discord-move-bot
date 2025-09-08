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

# -----------------------------------------
# ping コマンド
# -----------------------------------------
@bot.command()
async def ping(ctx):
    """
    !ping と送信すると応答時間を返す
    """
    latency = round(bot.latency * 1000)  # ミリ秒に変換
    await ctx.send(f"Pong! ({latency}ms)")

# -----------------------------------------
# 単体ユーザー移動ボタン
# -----------------------------------------
class SingleMoveButtonView(discord.ui.View):
    def __init__(self, member: discord.Member, channel: discord.VoiceChannel):
        super().__init__(timeout=None)
        self.member = member
        self.channel = channel

    @discord.ui.button(label="移動", style=discord.ButtonStyle.primary)
    async def move_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await self.member.move_to(self.channel)
            await interaction.response.send_message(
                f"✅ {self.member.display_name} を {self.channel.name} に移動しました", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ 移動に失敗しました: {e}", ephemeral=True
            )

@bot.command()
async def button_move(ctx, member: discord.Member, channel: discord.VoiceChannel):
    view = SingleMoveButtonView(member, channel)
    await ctx.send(
        f"{member.display_name} を {channel.name} に移動させるボタンです",
        view=view
    )

# -----------------------------------------
# 複数ユーザー個別ボタン
# -----------------------------------------
class MultiMoveView(discord.ui.View):
    def __init__(self, moves: list[tuple[discord.Member, discord.VoiceChannel]]):
        super().__init__(timeout=None)
        for member, channel in moves:
            self.add_item(MultiMoveButton(member, channel))

class MultiMoveButton(discord.ui.Button):
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

# -----------------------------------------
# まとめて移動ボタン（1つのボタンで全員）
# -----------------------------------------
class MoveAllView(discord.ui.View):
    def __init__(self, members: list[discord.Member], channel: discord.VoiceChannel):
        super().__init__(timeout=None)
        self.members = members
        self.channel = channel

        button = discord.ui.Button(label=f"まとめて {channel.name} に移動", style=discord.ButtonStyle.success)
        button.callback = self.move_all_callback
        self.add_item(button)

    async def move_all_callback(self, interaction: discord.Interaction):
        moved = []
        failed = []
        for member in self.members:
            try:
                await member.move_to(self.channel)
                moved.append(member.display_name)
            except Exception as e:
                failed.append(f"{member.display_name} ({e})")

        msg = ""
        if moved:
            msg += f"✅ 移動成功: {', '.join(moved)}\n"
        if failed:
            msg += f"❌ 移動失敗: {', '.join(failed)}"
        await interaction.response.send_message(msg, ephemeral=True)

@bot.command()
async def move_all(ctx, channel: discord.VoiceChannel, *members: discord.Member):
    """
    使い方例:
    !move_all #会議室 @太郎 @花子 @次郎
    """
    if not members:
        await ctx.send("移動するメンバーを1人以上指定してください")
        return

    view = MoveAllView(list(members), channel)
    await ctx.send(f"{channel.name} にまとめて移動させるボタンです", view=view)

# -----------------------------------------
# Bot起動
# -----------------------------------------
bot.run(TOKEN)
