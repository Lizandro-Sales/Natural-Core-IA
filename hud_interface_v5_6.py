import subprocess
import winsound
import os
import threading
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext

class NaturalCoreHUD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Natural Core IA - HUD v5.6")
        self.geometry("720x480")
        self.configure(bg="black")

        # Cabeçalho
        tk.Label(self, text="🚀 Natural Core IA - GitHub Sync v5.6", 
                 fg="cyan", bg="black", font=("Consolas", 14, "bold")).pack(pady=10)

        # Status
        self.label_status = tk.Label(self, text="Status: Aguardando ação...", 
                                     fg="white", bg="black", font=("Consolas", 11))
        self.label_status.pack(pady=5)

        # Barra de progresso
        self.progress = ttk.Progressbar(self, orient="horizontal", length=680, mode="indeterminate")
        self.progress.pack(pady=8)

        # Terminal embutido
        self.console = scrolledtext.ScrolledText(self, width=85, height=18, bg="#111", fg="#00FF66", 
                                                 insertbackground="white", font=("Consolas", 10))
        self.console.pack(padx=10, pady=10)
        self.console.insert(tk.END, "[HUD] Inicializado e pronto para sincronizar.\n")
        self.console.configure(state="disabled")

        # Botões
        self.btn_sync = tk.Button(self, text="🔄 Sincronizar com GitHub", font=("Consolas", 11), 
                                  bg="#0078D7", fg="white", command=self.sincronizar)
        self.btn_sync.pack(pady=5)

        self.btn_logs = tk.Button(self, text="📂 Abrir Pasta de Logs", font=("Consolas", 11), 
                                  bg="#444", fg="white", command=self.abrir_logs)
        self.btn_logs.pack(pady=5)

        self.btn_close = tk.Button(self, text="❌ Encerrar HUD", font=("Consolas", 11), 
                                   bg="#a00", fg="white", command=self.destroy)
        self.btn_close.pack(pady=8)

    def log(self, message):
        """Adiciona texto no terminal interno"""
        self.console.configure(state="normal")
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.configure(state="disabled")
        self.update()

    def sincronizar(self):
        threading.Thread(target=self.executar_sync, daemon=True).start()

    def executar_sync(self):
        self.label_status.config(text="🔄 Sincronizando com GitHub...", fg="yellow")
        self.btn_sync.config(state="disabled")
        self.progress.start(12)
        self.log("\n[INFO] Iniciando sincronização com o repositório remoto...")
        self.update()

        try:
            # Executa o .bat em tempo real
            process = subprocess.Popen(
                ['cmd', '/c', 'E:\\projetos\\natural core\\sincronizador_github.bat'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8'
            )

            # Lê a saída linha a linha e mostra no terminal
            for line in process.stdout:
                self.log(line.strip())

            process.wait()

            # Cria logs
            log_dir = "E:\\projetos\\natural core\\logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, "sync_log.txt")

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] STATUS: {'SUCESSO' if process.returncode == 0 else 'FALHA'}\n")
                f.write("="*60 + "\n")

            if process.returncode == 0:
                self.label_status.config(text="✅ Sincronização concluída com sucesso!", fg="#00FF00")
                self.log("[SUCESSO] Sincronização concluída com sucesso.")
                winsound.Beep(1200, 180)
            else:
                self.label_status.config(text="❌ Falha na sincronização!", fg="#FF4444")
                self.log("[ERRO] Falha na sincronização! Verifique o log.")
                winsound.Beep(400, 200)

        except Exception as e:
            self.label_status.config(text=f"⚠ Erro: {e}", fg="#FF4444")
            self.log(f"[ERRO CRÍTICO] {e}")
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