import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import time
import winsound
import os
from datetime import datetime

# Caminhos base
BASE_DIR = r"E:\projetos\natural core"
LOG_FILE = os.path.join(BASE_DIR, "log_hud.txt")
SYNC_SCRIPT = os.path.join(BASE_DIR, "sincronizador_github.bat")

# Configurações da janela principal
class NaturalCoreHUD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Natural Core IA - HUD v5.2")
        self.geometry("640x400")
        self.configure(bg="#1b1b1b")
        self.resizable(False, False)
        self.attributes("-topmost", True)  # Mantém sempre no topo

        # Layout principal
        self.create_widgets()

    def create_widgets(self):
        # Título
        title = tk.Label(
            self,
            text="🚀 Natural Core IA - HUD v5.2",
            font=("Segoe UI", 16, "bold"),
            fg="#00FFAA",
            bg="#1b1b1b",
        )
        title.pack(pady=10)

        # Botão principal
        self.start_button = tk.Button(
            self,
            text="Compilar e Sincronizar",
            command=self.start_sync,
            font=("Segoe UI", 12, "bold"),
            bg="#00AAFF",
            fg="white",
            activebackground="#0099EE",
            relief="flat",
            width=25,
            height=2,
        )
        self.start_button.pack(pady=15)

        # Barra de progresso
        self.progress = ttk.Progressbar(
            self, orient="horizontal", mode="determinate", length=500
        )
        self.progress.pack(pady=10)

        # Dashboard lateral
        self.dashboard = tk.Frame(self, bg="#222222", width=250, height=400)
        self.dashboard.place(x=380, y=0)

        tk.Label(
            self.dashboard, text="📊 Status do Sistema", fg="#00FFAA", bg="#222222",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=10)

        self.lbl_status = tk.Label(self.dashboard, text="Aguardando...", fg="white", bg="#222222")
        self.lbl_status.pack()

        self.lbl_last_sync = tk.Label(self.dashboard, text="Última Sync: --", fg="white", bg="#222222")
        self.lbl_last_sync.pack()

        self.lbl_duration = tk.Label(self.dashboard, text="Duração: --", fg="white", bg="#222222")
        self.lbl_duration.pack()

        self.lbl_commit = tk.Label(self.dashboard, text="Tamanho do Commit: --", fg="white", bg="#222222")
        self.lbl_commit.pack()

        # Caixa de logs
        self.log_text = tk.Text(
            self, width=60, height=10, bg="#111111", fg="#00FFAA", insertbackground="white"
        )
        self.log_text.pack(pady=10)
        self.log_text.insert("end", "HUD iniciado...\n")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        self.log_text.insert("end", line)
        self.log_text.see("end")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)

    def start_sync(self):
        self.start_button.config(state="disabled")
        self.progress.start(10)
        self.log("Iniciando sincronização com o GitHub...")

        t = threading.Thread(target=self.run_sync)
        t.start()

    def run_sync(self):
        start_time = time.time()
        try:
            result = subprocess.run(
                [SYNC_SCRIPT], capture_output=True, text=True, shell=True
            )

            duration = time.time() - start_time
            duration_str = f"{duration:.1f}s"
            self.lbl_duration.config(text=f"Duração: {duration_str}")

            if result.returncode == 0:
                self.progress.stop()
                self.progress["value"] = 100
                self.lbl_status.config(text="✅ Sincronizado com sucesso!", fg="#00FF00")
                self.lbl_last_sync.config(
                    text=f"Última Sync: {datetime.now().strftime('%H:%M:%S')}"
                )
                self.log("✅ Sincronização concluída com sucesso.")
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            else:
                self.progress.stop()
                self.lbl_status.config(text="❌ Falha na sincronização!", fg="#FF4444")
                self.log(f"❌ Erro durante o push:\n{result.stderr}")
                winsound.MessageBeep(winsound.MB_ICONHAND)

            commit_size = len(result.stdout.encode("utf-8")) / 1024
            self.lbl_commit.config(text=f"Tamanho do Commit: {commit_size:.1f} KB")

        except Exception as e:
            self.log(f"⚠ Erro crítico: {e}")
            self.lbl_status.config(text="⚠ Erro inesperado", fg="#FFFF00")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

        finally:
            self.start_button.config(state="normal")
            self.progress.stop()

# Execução principal
if __name__ == "__main__":
    app = NaturalCoreHUD()
    app.mainloop()