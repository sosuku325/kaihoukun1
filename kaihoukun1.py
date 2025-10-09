import tkinter as tk
from tkinter import messagebox, scrolledtext
import miniupnpc
import socket
import webbrowser
from PIL import Image, ImageTk
import os
import sys
import requests

def set_window_icon(window):
    try:
        window.iconbitmap(icon_path)
    except:
        try:
            icon_img = Image.open(icon_path)
            window.iconphoto(False, ImageTk.PhotoImage(icon_img))
        except:
            pass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        local_ip_var.set(ip)
    except Exception as e:
        messagebox.showerror("Error", f"ローカルIP取得失敗: {e}")

def get_global_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        response.raise_for_status()
        ip = response.text
        port = port_var.get().strip()
        if port:
            global_ip_var.set(f"{ip}:{port}")
        else:
            global_ip_var.set(ip)
    except Exception as e:
        messagebox.showerror("Error", f"グローバルIP取得失敗: {e}")

def copy_to_clipboard(text_var):
    root.clipboard_clear()
    root.clipboard_append(text_var.get())
    messagebox.showinfo("コピー完了", f"{text_var.get()} をクリップボードにコピーしました")

def open_port():
    port = port_var.get()
    ip = local_ip_var.get()
    protocol = protocol_var.get()
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        upnp.discover()
        upnp.selectigd()
        upnp.addportmapping(int(port), protocol, ip, int(port), 'Port Forwarder', '')
        status_var.set(f"{protocol} ポート {port} を開放しました")
    except Exception as e:
        messagebox.showerror("Error", f"ポート開放失敗: {e}")

def close_port():
    port = port_var.get()
    protocol = protocol_var.get()
    try:
        upnp = miniupnpc.UPnP()
        upnp.discoverdelay = 200
        upnp.discover()
        upnp.selectigd()
        upnp.deleteportmapping(int(port), protocol)
        status_var.set(f"{protocol} ポート {port} を閉鎖しました")
    except Exception as e:
        messagebox.showerror("Error", f"ポート閉鎖失敗: {e}")

def test_external_reachability():
    port = port_var.get().strip()
    protocol = protocol_var.get()
    if not port.isdigit():
        messagebox.showerror("Error", "ポート番号を正しく入力してください")
        return
    port = int(port)
    output_text.delete(1.0, tk.END)
    if protocol == "UDP":
        output_text.insert(tk.END, "⚠️ UDP の外部到達性テストはサポートされていません。\n")
        return
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text.strip()
        url = "https://ports.yougetsignal.com/check-port.php"
        data = {"remoteAddress": ip, "portNumber": str(port)}
        r = requests.post(url, data=data, timeout=10)
        try:
            result = r.json()
            if result.get("status") == "open":
                output_text.insert(tk.END, f"✅ このポートは開放されています。（{protocol} {port}）\n")
            else:
                output_text.insert(tk.END, f"❌ このポートは開放されていません。（{protocol} {port}）\n")
        except Exception:
            if "open" in r.text.lower():
                output_text.insert(tk.END, f"✅ このポートは開放されています。（{protocol} {port}）\n")
            else:
                output_text.insert(tk.END, f"❌ このポートは開放されていません。（{protocol} {port}）\n")
    except Exception as e:
        output_text.insert(tk.END, f"外部到達性テスト失敗: {e}\n")

def open_discord_link():
    webbrowser.open("https://disboard.org/ja/server/1383423417348395078")

def open_multi_port_window():
    multi_window = tk.Toplevel(root)
    multi_window.title("複数ポート開放・閉鎖")
    multi_window.geometry("420x360")
    multi_window.resizable(False, False)
    set_window_icon(multi_window)

    tk.Label(multi_window, text="以下の形式で入力してください：", fg="blue").pack(pady=5)
    tk.Label(multi_window, text="例：25565 TCP\n　　19132 UDP").pack()

    text_box = scrolledtext.ScrolledText(multi_window, width=45, height=8)
    text_box.pack(padx=10, pady=5)

    tk.Label(multi_window, text="📜 実行ログ").pack(pady=(5, 0))

    result_box = scrolledtext.ScrolledText(multi_window, width=45, height=5, state="disabled")
    result_box.pack(padx=10, pady=5, fill="both", expand=True)

    result_box.tag_config("success", foreground="#2ECC71")
    result_box.tag_config("error", foreground="#E74C3C")
    result_box.tag_config("warning", foreground="#E67E22")
    result_box.tag_config("info", foreground="#3498DB")

    def log_result(message, tag="info"):
        result_box.config(state="normal")
        result_box.insert(tk.END, message + "\n", tag)
        result_box.config(state="disabled")
        result_box.see(tk.END)

    def process_ports(action):
        ip = local_ip_var.get().strip()
        if not ip:
            log_result("⚠️ 先にローカルIPを取得してください。", "warning")
            return
        lines = text_box.get("1.0", tk.END).strip().splitlines()
        if not lines:
            log_result("⚠️ ポート設定を入力してください。", "warning")
            return
        for line in lines:
            parts = line.split()
            if len(parts) != 2:
                log_result(f"❌ フォーマットエラー: {line}", "error")
                continue
            port, proto = parts
            if not port.isdigit():
                log_result(f"❌ ポート番号エラー: {line}", "error")
                continue
            try:
                upnp = miniupnpc.UPnP()
                upnp.discoverdelay = 200
                upnp.discover()
                upnp.selectigd()
                if action == "open":
                    upnp.addportmapping(int(port), proto.upper(), ip, int(port), 'MultiPort', '')
                    log_result(f"✅ 開放成功: {ip} {port} {proto.upper()}", "success")
                else:
                    upnp.deleteportmapping(int(port), proto.upper())
                    log_result(f"🧱 閉鎖成功: {ip} {port} {proto.upper()}", "info")
            except Exception as e:
                log_result(f"⚠️ 失敗: {ip} {port} {proto} -> {e}", "warning")

    button_frame = tk.Frame(multi_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="開放", width=14, height=2,
              command=lambda: process_ports("open")).pack(side="left", padx=15)
    tk.Button(button_frame, text="閉鎖", width=14, height=2,
              command=lambda: process_ports("close")).pack(side="left", padx=15)

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)
icon_path = os.path.join(base_path, "icon.ico")

root = tk.Tk()
root.title("kaihoukun1")
root.resizable(False, False)
set_window_icon(root)

local_ip_var = tk.StringVar()
global_ip_var = tk.StringVar()
port_var = tk.StringVar()
status_var = tk.StringVar()
protocol_var = tk.StringVar(value="TCP")

tk.Label(root, text="ローカルIP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=local_ip_var, width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="取得", command=get_local_ip).grid(row=0, column=2, padx=5, pady=5)
tk.Button(root, text="コピー", command=lambda: copy_to_clipboard(local_ip_var)).grid(row=0, column=3, padx=5, pady=5)

tk.Label(root, text="グローバルIP:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=global_ip_var, width=20).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="取得", command=get_global_ip).grid(row=1, column=2, padx=5, pady=5)
tk.Button(root, text="コピー", command=lambda: copy_to_clipboard(global_ip_var)).grid(row=1, column=3, padx=5, pady=5)

tk.Label(root, text="ポート:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
tk.Entry(root, textvariable=port_var, width=20).grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="プロトコル:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
tk.Radiobutton(root, text="TCP", variable=protocol_var, value="TCP").grid(row=2, column=3, sticky="w")
tk.Radiobutton(root, text="UDP", variable=protocol_var, value="UDP").grid(row=2, column=3, sticky="e")

button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=4, pady=10)
tk.Button(button_frame, text="公開", width=10, command=open_port).pack(side="left", padx=10)
tk.Button(button_frame, text="閉鎖", width=10, command=close_port).pack(side="left", padx=10)
tk.Button(button_frame, text="外部到達性テスト", width=18, command=test_external_reachability).pack(side="left", padx=10)
tk.Button(button_frame, text="複数ポート開放", width=15, command=open_multi_port_window).pack(side="left", padx=10)

tk.Label(root, textvariable=status_var, fg="blue").grid(row=4, column=0, columnspan=4, pady=5)
output_text = scrolledtext.ScrolledText(root, width=50, height=5)
output_text.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
tk.Button(root, text="開発者のディスコード(アップデート版配布場所)", fg="white", bg="#7289DA",
          command=open_discord_link).grid(row=6, column=0, columnspan=4, pady=10)

root.mainloop()

