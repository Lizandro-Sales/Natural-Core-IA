import os
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import datetime
import winsound  # para alerta sonoro

class HUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚙ Natural Core IA - Visual HUD v4.9+")
        self.root.geometry("620x460")
        self.root.configure(bg="#0b0b0b")
        self.root.resizable(False, False)

        self.header = tk.Label(
            self.root,
            text="🧠 Natural Core IA - HUD Visual Interface v4.9+",
            fg="#00ff88",
            bg="#0b0b0b",
            font=("Consolas", 13, "bold"),
        )
        self.header.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(
            self.root, width=70, height=18, bg="#0f0f0f", fg="#00ff00", font=("Consolas", 10)
        )
        self.log_text.pack(padx=10, pady=10)
        self.log("[HUD] Iniciado com sucesso.")

        self.progress = ttk.Progressbar(
            self.root, orient="horizontal", length=550, mode="determinate"
        )
        self.progress.pack(pady=8)
        self.progress["value"] = 0

        button_frame = tk.Frame(self.root, bg="#0b0b0b")
        button_frame.pack(pady=8)

        tk.Button(button_frame, text="🚀 Compilar", width=18, command=self.compilar_async, bg="#202020", fg="#00ff00").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="⬆ Sincronizar GitHub", width=18, command=self.git_async, bg="#202020", fg="#00ffff").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="📁 Abrir Projeto", width=18, command=self.abrir_pasta, bg="#202020", fg="#ffb000").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="❌ Fechar", width=15, command=self.root.quit, bg="#202020", fg="#ff4040").grid(row=1, column=1, pady=10)

        self.versao_label = tk.Label(
            self.root,
            text=self.get_version_text(),
            fg="#00ffcc",
            bg="#0b0b0b",
            font=("Consolas", 10),
        )
        self.versao_label.pack(pady=2)

    # === LOG VISUAL ===
    def log(self, texto):
        hora = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.log_text.insert("end", f"{hora} {texto}\n")
        self.log_text.see("end")
        self.root.update_idletasks()

    # === PEGAR VERSÃO ===
    def get_version_text(self):
        update_file = r"E:\projetos\natural core\update_info.json"
        if os.path.exists(update_file):
            try:
                with open(update_file, "r", encoding="utf-8") as f:
                    info = json.load(f)
                    versao = info.get("version", "4.9")
                    data = info.get("last_update", "")
                    return f"📦 Versão atual: {versao}  |  Última atualização: {data}"
            except:
                return "📦 Versão: Indefinida"
        else:
            return "📦 update_info.json não encontrado"

    # === EXECUÇÃO ASSÍNCRONA ===
    def compilar_async(self):
        threading.Thread(target=self.compilar, daemon=True).start()

    def git_async(self):
        threading.Thread(target=self.atualizar_git, daemon=True).start()

    # === COMPILAR ===
    def compilar(self):
        self.progress["value"] = 10
        self.log("🚧 Iniciando compilação do projeto...")
        try:
            build_script = r"E:\projetos\natural core\build_visualsync_plus_v4_8.bat"
            if os.path.exists(build_script):
                subprocess.run(build_script, shell=True, cwd=r"E:\projetos\natural core")
                self.progress["value"] = 100
                self.log("✅ Compilação concluída com sucesso.")
                winsound.Beep(1200, 200)
            else:
                self.log("❌ Arquivo de build não encontrado.")
        except Exception as e:
            self.log(f"❌ Erro durante compilação: {e}")
            winsound.Beep(600, 500)

    # === SINCRONIZAR GITHUB ===
    def atualizar_git(self):
        self.progress["value"] = 20
        self.log("⬆ Iniciando sincronização com o GitHub...")
        try:
            subprocess.run(
                [r"C:\Python312\python.exe", r"E:\projetos\natural core\core\auto_updater.py"],
                shell=True,
                cwd=r"E:\projetos\natural core"
            )
            self.progress["value"] = 100
            self.log("✅ Sincronização concluída e publicada.")
            winsound.Beep(1500, 300)
            messagebox.showinfo("GitHub Sync", "Repositório sincronizado com sucesso!")
        except Exception as e:
            self.log(f"❌ Erro ao sincronizar: {e}")
            winsound.Beep(500, 700)

    # === ABRIR PASTA ===
    def abrir_pasta(self):
        path = r"E:\projetos\natural core"
        if os.path.exists(path):
            os.startfile(path)
            self.log("📁 Diretório do projeto aberto.")
        else:
            self.log("❌ Diretório do projeto não encontrado.")


if __name__ == "__main__":
    root = tk.Tk()
    app = HUDApp(root)
    root.mainloop()