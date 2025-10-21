import subprocess
import winsound
import os
import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class NaturalCoreHUD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Natural Core IA - HUD v5.5")
        self.geometry("520x320")
        self.configure(bg="black")

        # Título
        tk.Label(self, text="🌐 Natural Core IA - GitHub Sync", fg="cyan", bg="black", font=("Consolas", 13, "bold")).pack(pady=15)

        # Status
        self.label_status = tk.Label(self, text="Status: Aguardando ação...", fg="white", bg="black", font=("Consolas", 11))
        self.label_status.pack(pady=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(self, orient="horizontal", length=420, mode="indeterminate")
        self.progress.pack(pady=10)

        # Botões
        self.btn_sync = tk.Button(self, text="🔄 Sincronizar com GitHub", font=("Consolas", 11), bg="#0078D7", fg="white", command=self.sincronizar)
        self.btn_sync.pack(pady=5)

        self.btn_logs = tk.Button(self, text="📂 Abrir Pasta de Logs", font=("Consolas", 11), bg="#444", fg="white", command=self.abrir_logs)
        self.btn_logs.pack(pady=5)

        self.btn_close = tk.Button(self, text="❌ Encerrar HUD", font=("Consolas", 11), bg="#a00", fg="white", command=self.destroy)
        self.btn_close.pack(pady=15)

    def sincronizar(self):
        # Thread separada para manter a UI responsiva
        threading.Thread(target=self.executar_sync, daemon=True).start()

    def executar_sync(self):
        self.label_status.config(text="🔄 Sincronizando com GitHub...", fg="yellow")
        self.btn_sync.config(state="disabled")
        self.progress.start(12)
        self.update()

        try:
            result = subprocess.run(
                ['cmd', '/c', 'E:\\projetos\\natural core\\sincronizador_github.bat'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            # Cria pasta de logs
            log_dir = "E:\\projetos\\natural core\\logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "sync_log.txt")

            # Salva logs com data e status
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] STATUS: {'SUCESSO' if result.returncode == 0 else 'FALHA'}\n")
                f.write(result.stdout + "\n\n")

            time.sleep(1)  # pequeno delay visual

            if result.returncode == 0:
                self.progress.stop()
                self.label_status.config(text="✅ Sincronização concluída com sucesso!", fg="#00FF00")
                winsound.Beep(1200, 180)
            else:
                self.progress.stop()
                self.label_status.config(text="❌ Falha na sincronização!", fg="#FF4444")
                winsound.Beep(400, 200)

        except Exception as e:
            self.progress.stop()
            self.label_status.config(text=f"⚠ Erro: {e}", fg="#FF4444")
            winsound.Beep(300, 400)

        finally:
            self.progress.stop()
            self.btn_sync.config(state="normal")
            self.update()

    def abrir_logs(self):
        log_path = "E:\\projetos\\natural core\\logs"
        os.makedirs(log_path, exist_ok=True)
        os.startfile(log_path)

if __name__ == "__main__":
    app = NaturalCoreHUD()
    app.mainloop()