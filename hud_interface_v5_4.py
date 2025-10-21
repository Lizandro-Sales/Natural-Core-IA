import subprocess
import winsound
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class NaturalCoreHUD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Natural Core IA - HUD v5.4")
        self.geometry("480x300")
        self.configure(bg="black")

        self.label_status = tk.Label(self, text="Status: Aguardando ação...", fg="cyan", bg="black", font=("Consolas", 11))
        self.label_status.pack(pady=20)

        self.btn_sync = tk.Button(self, text="🔄 Sincronizar com GitHub", font=("Consolas", 11), bg="#0078D7", fg="white", command=self.sincronizar)
        self.btn_sync.pack(pady=10)

        self.btn_logs = tk.Button(self, text="📂 Abrir Pasta de Logs", font=("Consolas", 11), bg="#444", fg="white", command=self.abrir_logs)
        self.btn_logs.pack(pady=10)

        self.btn_close = tk.Button(self, text="❌ Encerrar HUD", font=("Consolas", 11), bg="#a00", fg="white", command=self.destroy)
        self.btn_close.pack(pady=10)

    def sincronizar(self):
        self.label_status.config(text="🔄 Sincronizando com GitHub...", fg="yellow")
        self.update()

        try:
            result = subprocess.run(
                ['cmd', '/c', 'E:\\projetos\\natural core\\sincronizador_github.bat'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            log_dir = "E:\\projetos\\natural core\\logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "sync_log.txt")

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] STATUS: {'SUCESSO' if result.returncode == 0 else 'FALHA'}\n")
                f.write(result.stdout + "\n\n")

            if result.returncode == 0:
                self.label_status.config(text="✅ Sincronização concluída com sucesso!", fg="#00FF00")
                winsound.Beep(1200, 180)  # som metálico agudo
            else:
                self.label_status.config(text="❌ Falha na sincronização!", fg="#FF4444")
                winsound.Beep(400, 200)  # som metálico grave

        except Exception as e:
            self.label_status.config(text=f"⚠ Erro: {e}", fg="#FF4444")
            winsound.Beep(300, 400)

    def abrir_logs(self):
        log_path = "E:\\projetos\\natural core\\logs"
        os.makedirs(log_path, exist_ok=True)
        os.startfile(log_path)

if __name__ == "__main__":
    app = NaturalCoreHUD()
    app.mainloop()