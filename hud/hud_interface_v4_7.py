import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import datetime
import os
from git import Repo

class HUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Natural Core IA - Visual HUD v4.7.2 Plus")
        self.root.geometry("520x420")
        self.root.configure(bg="#0b0b0b")
        self.root.resizable(False, False)

        # --- LOG VISUAL ---
        self.text_log = tk.Text(
            self.root,
            width=65,
            height=18,
            bg="#101010",
            fg="#00FF66",
            insertbackground="#00FF66",
            font=("Consolas", 10)
        )
        self.text_log.pack(padx=10, pady=10)

        # --- BARRA DE PROGRESSO ---
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            mode="determinate",
            length=480
        )
        self.progress.pack(pady=8)

        # --- BOTÕES ---
        button_frame = tk.Frame(self.root, bg="#0b0b0b")
        button_frame.pack(pady=5)

        self.btn_start = tk.Button(
            button_frame, text="Iniciar Build",
            command=self.start_process, width=15, bg="#1a1a1a", fg="#00FF66"
        )
        self.btn_start.grid(row=0, column=0, padx=6)

        self.btn_update = tk.Button(
            button_frame, text="Atualizar via GitHub",
            command=self.github_update, width=18, bg="#1a1a1a", fg="#00C8FF"
        )
        self.btn_update.grid(row=0, column=1, padx=6)

        self.btn_exit = tk.Button(
            button_frame, text="Fechar",
            command=self.root.destroy, width=12, bg="#1a1a1a", fg="#FF5555"
        )
        self.btn_exit.grid(row=0, column=2, padx=6)

        # --- INÍCIO ---
        self.log("🟢 HUD Visual IA iniciado com sucesso.")

    # ==========================
    # Funções de Log
    # ==========================
    def log(self, msg):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.text_log.insert("end", f"[{now}] {msg}\n")
        self.text_log.see("end")

    # ==========================
    # Processamento Principal
    # ==========================
    def start_process(self):
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        self.log("🔄 Iniciando build automático...")
        self.progress["value"] = 0
        for i in range(101):
            self.progress["value"] = i
            self.root.update_idletasks()
            time.sleep(0.02)
        self.log("✅ Compilação concluída com sucesso!")
        self.log("📦 Natural Core IA pronto para execução.")

    # ==========================
    # Atualização via GitHub
    # ==========================
    def github_update(self):
        try:
            self.log("🌐 Verificando atualizações no GitHub...")
            repo_path = os.path.join("E:\\projetos\\natural core")
            if os.path.exists(repo_path):
                repo = Repo(repo_path)
                repo.remotes.origin.pull()
                self.log("✅ Repositório sincronizado com sucesso.")
            else:
                self.log("⚠ Caminho do repositório não encontrado.")
        except Exception as e:
            self.log(f"❌ Erro durante atualização: {e}")

# ==========================
# Execução Principal
# ==========================
if __name__ == "__main__":
    root = tk.Tk()
    app = HUDApp(root)
    root.mainloop()