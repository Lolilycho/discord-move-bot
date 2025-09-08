import os
import random
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

# -------------------------
# ping コマンド
# -------------------------
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! {latency}ms")

# -------------------------
# 単体移動ボタン
# -------------------------
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
    await ctx.send(f"{member.display_name} を {channel.name} に移動させるボタンです", view=view)

# -------------------------
# 複数ユーザー個別ボタン
# -------------------------
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

class MultiMoveView(discord.ui.View):
    def __init__(self, moves: list[tuple[discord.Member, discord.VoiceChannel]]):
        super().__init__(timeout=None)
        for member, channel in moves:
            self.add_item(MultiMoveButton(member, channel))

@bot.command()
async def multi_move(ctx, *args):
    if len(args) % 2 != 0:
        await ctx.send("引数は「@ユーザー #チャンネル」のセットで入力してください")
        return
    moves = []
    for i in range(0, len(args), 2):
        member = await commands.MemberConverter().convert(ctx, args[i])
        channel = await commands.VoiceChannelConverter().convert(ctx, args[i+1])
        moves.append((member, channel))
    view = MultiMoveView(moves)
    await ctx.send("移動ボタンです", view=view)

# -------------------------
# まとめて移動ボタン
# -------------------------
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
    if not members:
        await ctx.send("移動するメンバーを1人以上指定してください")
        return
    view = MoveAllView(list(members), channel)
    await ctx.send(f"{channel.name} にまとめて移動させるボタンです", view=view)

# -------------------------
# 遊びコマンド
# -------------------------
@bot.command()
async def janken(ctx, hand: str):
    choices = ["グー", "チョキ", "パー"]
    if hand not in choices:
        await ctx.send("「グー」「チョキ」「パー」のいずれかで入力してください")
        return
    bot_hand = random.choice(choices)
    if hand == bot_hand:
        result = "引き分け！"
    elif (hand=="グー" and bot_hand=="チョキ") or \
         (hand=="チョキ" and bot_hand=="パー") or \
         (hand=="パー" and bot_hand=="グー"):
        result = "あなたの勝ち！🎉"
    else:
        result = "あなたの負け…💦"
    await ctx.send(f"あなた: {hand}\nBot: {bot_hand}\n{result}")

@bot.command()
async def omikuji(ctx):
    results = ["大吉🍀", "中吉🌸", "小吉🍁", "凶💧"]
    await ctx.send(f"あなたのおみくじ結果は… **{random.choice(results)}** です！")

@bot.command()
async def dice(ctx, sides: int = 6):
    if sides < 2:
        await ctx.send("サイコロの目は2以上にしてください")
        return
    result = random.randint(1, sides)
    await ctx.send(f"{sides}面サイコロの結果: **{result}**")

@bot.command()
async def lucky(ctx, name: str = None):
    if not name:
        name = ctx.author.display_name
    number = random.randint(1, 100)
    await ctx.send(f"{name} さんの今日のラッキーナンバーは **{number}** です✨")

@bot.command()
async def grilled_bottle(ctx):
    result = random.choices(["成功", "失敗"], weights=[70,30], k=1)[0]
    if result == "成功":
        await ctx.send("ビンが溶けちゃった……ガラス細工、とか……？")
    else:
        await ctx.send("🔥 ビンを炙ったら【炙りビン】になるよ！")

# -------------------------
# Bot起動
# -------------------------
bot.run(TOKEN)
