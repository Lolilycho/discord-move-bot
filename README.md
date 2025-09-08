# Discord Move Bot

Discordサーバー内でユーザーを任意のボイスチャンネルに移動させるBotです。  
ボタン操作でユーザー移動や遊びコマンドも利用できます。

---

## 🔹 コマンド一覧

| コマンド | 説明 | 備考 |
|----------|------|------|
| `!move @ユーザー #チャンネル` | 指定ユーザーを指定ボイスチャンネルに移動 | 管理者権限推奨 |
| `!button_move @ユーザー #チャンネル` | ボタンを生成してユーザー移動 | ボタン押すと即移動 |
| `!multi_move @ユーザー1 #チャンネル1 @ユーザー2 #チャンネル2 ...` | 複数ユーザーの移動ボタンを生成 | 引数はペアで指定 |
| `!ping` | Botの応答速度を確認 | 返答例: `pong (123ms)` |
| `!grilled_bottle` | 遊びコマンド | ボタンで操作可能、結果はランダム |
| `!help` | 全コマンド一覧を表示 | Discord.py標準ヘルプ |

---

## 🔹 ボタン操作まとめ

### ユーザー移動ボタン
- `!button_move` や `!multi_move` で生成  
- ボタンを押すと対象ユーザーを指定チャンネルへ移動  

### 遊び用ボタン
- `!grilled_bottle` など  
- 結果はランダムで表示される  
- 複数ユーザーで遊ぶことも可能  

---

## 🔹 必要権限

- ボイスチャンネル接続・移動
- メッセージ送信
- 管理者権限推奨（ボタン操作を使用する場合）

---

## 🔹 環境変数

Botトークンは `.env` で管理:

DISCORD_TOKEN=あなたのBotトークン


---

## 🔹 インストール手順

# ディレクトリ移動
cd /home/ec2-user/discord-move-bot

# 依存パッケージをインストール
pip3 install -r requirements.txt

# Bot起動
python3 bot.py

🔹 systemd サービス化（常時稼働）
サービスファイル作成
sudo nano /etc/systemd/system/discordbot.service

[Unit]
Description=Discord Bot
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/discord-move-bot
ExecStart=/usr/bin/python3 /home/ec2-user/discord-move-bot/bot.py
Restart=always
Environment="DISCORD_TOKEN=あなたのトークン"

[Install]
WantedBy=multi-user.target

起動・有効化
sudo systemctl daemon-reload
sudo systemctl enable discordbot
sudo systemctl start discordbot


フロー図：

systemd
   │
   ├─> bot.py 常時稼働
   │
   └─> ボタン/コマンドでユーザー移動や遊び操作

🔹 更新方法
サーバー上でワンコマンド更新
./update_bot.sh


GitHubから最新コードを取得

Python依存パッケージを更新

Botを再起動

フロー図：

./update_bot.sh
   ├─> git pull → 最新コード取得
   ├─> pip install → 依存パッケージ更新
   └─> systemctl restart discordbot → Bot再起動
