import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True  # ← これが大事！
intents.members = True          # メンバー操作に必要

bot = commands.Bot(command_prefix="!", intents=intents)

move_settings = {}


class MoveButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for label, (user_id, channel_id) in MOVE_SETTINGS.items():
            self.add_item(MoveButton(label, user_id, channel_id))

class MoveButton(Button):
    def __init__(self, label, user_id, channel_id):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.user_id = user_id
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(self.user_id)
        channel = guild.get_channel(self.channel_id)

        if not member or not isinstance(channel, discord.VoiceChannel):
            await interaction.response.send_message(
                f"ユーザーまたはチャンネルが見つかりません: {self.label}", ephemeral=True
            )
            return

        try:
            await member.move_to(channel)
            await interaction.response.send_message(
                f"{member.display_name} を {channel.name} に移動しました ✅", ephemeral=False
            )
        except Exception as e:
            await interaction.response.send_message(f"移動に失敗しました: {e}", ephemeral=True)

# --- コマンド ---

@bot.command()
async def add_move(ctx, member: discord.Member, channel: discord.VoiceChannel, *, label: str):
    """新しい移動ボタンを追加する: !add_move @ユーザー #VC ボタン名"""
    MOVE_SETTINGS[label] = (member.id, channel.id)
    await ctx.send(f"登録しました: {label} → {member.display_name} を {channel.name} に移動")

@bot.command()
async def remove_move(ctx, *, label: str):
    """移動ボタンを削除する: !remove_move ボタン名"""
    if label in MOVE_SETTINGS:
        del MOVE_SETTINGS[label]
        await ctx.send(f"削除しました: {label}")
    else:
        await ctx.send("その名前の設定は存在しません。")

@bot.command()
async def setup_buttons(ctx):
    """現在の設定でボタンを表示"""
    if not MOVE_SETTINGS:
        await ctx.send("まだ移動設定がありません。まず !add_move で登録してください。")
        return
    view = MoveButtonView()
    await ctx.send("↓ ボタンを押すと指定のユーザーを移動できます ↓", view=view)

# --- 起動 ---
bot.run(TOKEN)
