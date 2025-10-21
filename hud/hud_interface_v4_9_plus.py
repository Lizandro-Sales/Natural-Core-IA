import os
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import datetime
import winsound

class HUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚙ Natural Core IA - Visual HUD v4.9+ Plus")
        self.root.geometry("640x470")
        self.root.configure(bg="#0b0b0b")
        self.root.resizable(False, False)

        # === HEADER ===
        header = tk.Label(
            self.root,
            text="🧠 Natural Core IA - HUD Visual Interface v4.9+ Plus",
            fg="#00ffaa", bg="#0b0b0b", font=("Consolas", 13, "bold")
        )
        header.pack(pady=8)

        # === LOG ===
        self.text_area = scrolledtext.ScrolledText(
            self.root, bg="#101010", fg="#00ff00",
            font=("Consolas", 10), width=72, height=18, wrap="word"
        )
        self.text_area.pack(padx=8, pady=8)
        self.text_area.insert("end", "[HUD] Inicializado com sucesso.\n")

        # === PROGRESS BAR ===
        self.progress = ttk.Progressbar(
            self.root, orient="horizontal", length=560, mode="determinate"
        )
        self.progress.pack(pady=5)
        self.progress["value"] = 0

        # === BOTÕES ===
        frame = tk.Frame(self.root, bg="#0b0b0b")
        frame.pack(pady=8)

        tk.Button(frame, text="🚀 Compilar", width=18, bg="#202020", fg="#00ff00",
                  command=self.compilar_async).grid(row=0, column=0, padx=6)
        tk.Button(frame, text="⬆ Sincronizar GitHub", width=18, bg="#202020", fg="#00ffff",
                  command=self.git_async).grid(row=0, column=1, padx=6)
        tk.Button(frame, text="📁 Abrir Projeto", width=18, bg="#202020", fg="#ffaa00",
                  command=self.abrir_pasta).grid(row=0, column=2, padx=6)
        tk.Button(frame, text="❌ Fechar", width=16, bg="#202020", fg="#ff4040",
                  command=self.root.quit).grid(row=1, column=1, pady=10)

        # === VERSÃO ===
        self.versao = tk.Label(
            self.root, text=self.get_version_text(),
            fg="#00cccc", bg="#0b0b0b", font=("Consolas", 10)
        )
        self.versao.pack(pady=2)

    # --- Função de log colorido ---
    def log(self, texto, tipo="info"):
        hora = datetime.datetime.now().strftime("[%H:%M:%S]")
        if tipo == "erro":
            cor = "#ff4040"
        elif tipo == "aviso":
            cor = "#ffb000"
        else:
            cor = "#00ff66"

        self.text_area.insert("end", f"{hora} {texto}\n", tipo)
        self.text_area.tag_config(tipo, foreground=cor)
        self.text_area.see("end")
        self.root.update_idletasks()

    def get_version_text(self):
        file = r"E:\projetos\natural core\update_info.json"
        if os.path.exists(file):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return f"📦 Versão atual: {data.get('version', '?')}  |  Última atualização: {data.get('last_update', '?')}"
            except:
                return "📦 Versão: indefinida"
        return "📦 Arquivo de versão não encontrado"

    # --- Execução assíncrona ---
    def compilar_async(self): threading.Thread(target=self.compilar, daemon=True).start()
    def git_async(self): threading.Thread(target=self.atualizar_git, daemon=True).start()

    # --- Compilação ---
    def compilar(self):
        self.progress["value"] = 10
        self.log("🚧 Iniciando compilação do projeto...")
        try:
            build_script = r"E:\projetos\natural core\build_visualsync_plus_v4_8.bat"
            if os.path.exists(build_script):
                subprocess.run(build_script, shell=True, cwd=r"E:\projetos\natural core")
                self.progress["value"] = 100
                self.log("✅ Compilação concluída com sucesso!")
                winsound.Beep(1200, 180)
                messagebox.showinfo("Compilação", "Compilação finalizada com sucesso!")
            else:
                self.log("❌ Script de build não encontrado!", "erro")
                winsound.Beep(600, 400)
        except Exception as e:
            self.log(f"❌ Erro ao compilar: {e}", "erro")
            winsound.Beep(500, 700)

    # --- Sincronização Git ---
    def atualizar_git(self):
        self.progress["value"] = 25
        self.log("⬆ Sincronizando repositório com GitHub...")
        try:
            repo_dir = r"E:\projetos\natural core"
            if not os.path.exists(os.path.join(repo_dir, ".git")):
                self.log("⚠ Repositório Git não inicializado! Corrigindo automaticamente...", "aviso")
                subprocess.run(["git", "init"], cwd=repo_dir, shell=True)
                subprocess.run(["git", "remote", "add", "origin",
                                "https://github.com/Lizandro-Sales/Natural-Core-IA.git"],
                               cwd=repo_dir, shell=True)

            subprocess.run(["git", "add", "."], cwd=repo_dir, shell=True)
            msg = f"🚀 Build automática - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", msg], cwd=repo_dir, shell=True)
            subprocess.run(["git", "pull", "--no-edit", "origin", "main"], cwd=repo_dir, shell=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_dir, shell=True)

            self.log("✅ Sincronização com GitHub concluída com sucesso!")
            self.progress["value"] = 100
            winsound.Beep(1400, 250)
            messagebox.showinfo("GitHub Sync", "Repositório atualizado com sucesso!")
        except Exception as e:
            self.log(f"❌ Erro ao sincronizar com GitHub: {e}", "erro")
            winsound.Beep(400, 600)

    # --- Abrir pasta ---
    def abrir_pasta(self):
        path = r"E:\projetos\natural core"
        if os.path.exists(path):
            os.startfile(path)
            self.log("📂 Diretório do projeto aberto.")
        else:
            self.log("❌ Diretório do projeto não encontrado.", "erro")

if __name__ == "__main__":
    root = tk.Tk()
    app = HUDApp(root)
    root.mainloop()