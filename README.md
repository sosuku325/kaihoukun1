# 🔓 開放くん1（Port Opener GUI）

![App Screenshot](https://img.shields.io/badge/Tkinter-GUI-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

ポート開放を簡単に行える Windows 向けツールです。  
UPnP を使ってワンクリックでポートを開放／閉鎖できます。  
さらに、複数ポートをまとめて設定できる「複数ポート開放モード」も搭載！

---

## 🖼️ 主な機能

✅ ローカルIP・グローバルIPの自動取得  
✅ UPnPを利用したポート開放・閉鎖  
✅ 複数ポート開放／閉鎖対応（例：ゲームサーバー複数対応）  
✅ TCP / UDP 切り替え  
✅ 外部到達性テスト（ポートが開放されているか確認）  
✅ カラーログ表示（成功・失敗・警告が色分け）  
✅ Discordリンクボタン（アップデート配布先）  
✅ シンプルで直感的なGUI

---

## ⚙️ インストール & 実行

### 🐍 1. Pythonで実行する場合
```bash
pip install pillow requests miniupnpc
python main.py
```

### 💾 2. EXEにビルドする場合（Windows）

1. 依存ライブラリをインストール：
   ```bash
   pip install pyinstaller pillow requests miniupnpc
   ```

2. `icon.ico` と `main.py` を同じフォルダに置く。

3. 以下のコマンドでビルド：
   ```bash
   pyinstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." --clean kaihoukun1.py
   ```

4. 完成した `dist/kaihoukun1.exe` を起動！

---

## 🧱 複数ポート開放モード

GUI中央の「複数ポート開放」ボタンをクリックすると、  
まとめて設定できるウィンドウが開きます。

```
25565 TCP
19132 UDP
```

といった形式で入力し、「開放」または「閉鎖」をクリック。

成功・失敗ログは色分け表示され、リアルタイムで確認可能です。

---

## 🧩 必要環境

- Windows 10 / 11  
- Python 3.8 以上  
- UPnP対応ルーター

---

## ⚠️ 注意

- 一部のルーターではUPnPが無効になっている場合があります。  
  → ルーター設定画面で「UPnPを有効化」してください。  
- セキュリティソフトがポート開放をブロックする場合があります。  
- UDPの外部到達性テストは非対応です（仕様上確認困難なため）。

---

## 💬 開発者リンク

- Discordサーバー: [開発者のディスコード（アップデート版配布場所）](https://disboard.org/ja/server/1383423417348395078)

---

## 📜 ライセンス

MIT License © 2025  

このソフトウェアは自由に改変・再配布が可能です。  
クレジットを残しての利用を推奨します。

---

## 🌟 作者メッセージ

ポート開放で困っている人の助けになれば嬉しいです！  
バグ報告・改善案・コントリビューションは大歓迎です 🚀
