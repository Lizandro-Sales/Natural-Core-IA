import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog  # ✅ Importação corrigida
from cryptography.fernet import Fernet
from datetime import datetime
import threading

class HUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Natural Core IA - HUD v5.0")
        self.root.geometry("640x420")
        self.root.configure(bg="#0b0b0b")
        self.root.resizable(False, False)

        # --- LOG VISUAL ---
        self.text_log = scrolledtext.ScrolledText(
            self.root, width=72, height=18, bg="#111", fg="#00FF66",
            insertbackground="white", font=("Consolas", 10)
        )
        self.text_log.pack(pady=15)
        self.text_log.insert(tk.END, "[HUD] v5.0 inicializado com sucesso.\n")

        # --- BOTÕES ---
        frame_buttons = tk.Frame(self.root, bg="#0b0b0b")
        frame_buttons.pack(pady=10)

        btn_build = tk.Button(
            frame_buttons, text="▶ Compilar e Sincronizar",
            command=self.executar_build, bg="#00AA66", fg="white",
            font=("Consolas", 10, "bold"), width=22
        )
        btn_build.grid(row=0, column=0, padx=5)

        btn_token = tk.Button(
            frame_buttons, text="🔒 Salvar Token",
            command=self.acao_salvar_token, bg="#0066CC", fg="white",
            font=("Consolas", 10, "bold"), width=14
        )
        btn_token.grid(row=0, column=1, padx=5)

        btn_fechar = tk.Button(
            frame_buttons, text="❌ Encerrar HUD",
            command=self.root.quit, bg="#CC3333", fg="white",
            font=("Consolas", 10, "bold"), width=14
        )
        btn_fechar.grid(row=0, column=2, padx=5)

    # --- Função para salvar o token ---
    def acao_salvar_token(self):
        try:
            token = simpledialog.askstring("Token GitHub", "Insira seu token pessoal:")
            if not token:
                self.log("[ERRO] Nenhum token inserido.")
                return

            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)

            fernet = Fernet(key)
            token_encrypted = fernet.encrypt(token.encode())

            with open("token.enc", "wb") as token_file:
                token_file.write(token_encrypted)

            self.log("[OK] Token GitHub salvo e criptografado com sucesso.")
        except Exception as e:
            self.log(f"[ERRO] Falha ao salvar token: {e}")

    # --- Logger ---
    def log(self, msg):
        now = datetime.now().strftime("%H:%M:%S")
        self.text_log.insert(tk.END, f"[{now}] {msg}\n")
        self.text_log.see(tk.END)

    # --- Função simulada de build (placeholder) ---
    def executar_build(self):
        self.log("Iniciando processo de build...")
        threading.Thread(target=self.simular_build, daemon=True).start()

    def simular_build(self):
        import time
        time.sleep(3)
        self.log("[OK] Build concluído com sucesso.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HUDApp(root)
    root.mainloop()