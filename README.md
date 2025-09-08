# Discord Move Bot

Discordサーバー内でユーザーを任意のボイスチャンネルに移動させるBotです。  
ボタン操作でユーザー移動や遊びコマンドが利用できます。

---

## 🔹 機能

### 1. ユーザー移動
- コマンド:
!move @ユーザー #ボイスチャンネル

markdown
コードをコピーする
- 指定ユーザーを指定のボイスチャンネルに移動

### 2. ボタンで移動
- コマンド:
!button_move @ユーザー #ボイスチャンネル

markdown
コードをコピーする
- ボタンを押すとユーザーを移動可能

### 3. 複数ユーザー対応
- コマンド:
!multi_move @ユーザー1 #チャンネル1 @ユーザー2 #チャンネル2 ...

markdown
コードをコピーする
- 複数ユーザーを一括で移動させるボタンを生成

### 4. Ping確認
- コマンド:
!ping

markdown
コードをコピーする
- Botの応答速度を確認可能

### 5. 遊びコマンド（ボタン対応）
- 例:
!grilled_bottle

yaml
コードをコピーする
- Discord上でボタン操作で遊べます

---

## 🔹 必要権限

- ボイスチャンネル接続・移動
- メッセージ送信
- 管理者権限推奨（ボタン操作を使用する場合）

---

## 🔹 環境変数

Botトークンは `.env` で管理:

DISCORD_TOKEN=あなたのBotトークン

yaml
コードをコピーする

---

## 🔹 インストール手順

```bash
# ディレクトリ移動
cd /home/ec2-user/discord-move-bot

# 依存パッケージをインストール
pip3 install -r requirements.txt

# Bot起動
python3 bot.py
🔹 systemd サービス化（常時稼働）
サービスファイル作成
bash
コードをコピーする
sudo nano /etc/systemd/system/discordbot.service
ini
コードをコピーする
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
bash
コードをコピーする
sudo systemctl daemon-reload
sudo systemctl enable discordbot
sudo systemctl start discordbot
フロー図：

nginx
コードをコピーする
systemd
   │
   ├─> bot.py 常時稼働
   │
   └─> ボタン/コマンドでユーザー移動や遊び操作
🔹 更新方法
サーバー上でワンコマンド更新
bash
コードをコピーする
./update_bot.sh
GitHubから最新コードを取得

Python依存パッケージを更新

Botを再起動

フロー図：

bash
コードをコピーする
./update_bot.sh
   ├─> git pull → 最新コード取得
   ├─> pip install → 依存パッケージ更新
   └─> systemctl restart discordbot → Bot再起動
