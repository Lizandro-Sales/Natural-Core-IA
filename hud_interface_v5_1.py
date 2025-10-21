import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from cryptography.fernet import Fernet
from datetime import datetime
import threading
from git import Repo, GitCommandError


class HUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Natural Core IA - HUD v5.1")
        self.root.geometry("640x420")
        self.root.configure(bg="#0b0b0b")
        self.root.resizable(False, False)

        # --- LOG VISUAL ---
        self.text_log = scrolledtext.ScrolledText(
            self.root, width=72, height=18, bg="#111", fg="#00FF66",
            insertbackground="white", font=("Consolas", 10)
        )
        self.text_log.pack(pady=15)
        self.text_log.insert(tk.END, "[HUD] v5.1 inicializado com sucesso.\n")

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

    # --- LOG ---
    def log(self, msg):
        now = datetime.now().strftime("%H:%M:%S")
        self.text_log.insert(tk.END, f"[{now}] {msg}\n")
        self.text_log.see(tk.END)

    # --- SALVAR TOKEN ---
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

    # --- BUILD E SYNC ---
    def executar_build(self):
        self.log("Iniciando compilação e sincronização...")
        threading.Thread(target=self.sincronizar_github, daemon=True).start()

    def sincronizar_github(self):
        try:
            repo_path = os.path.abspath(os.getcwd())
            if not os.path.exists(os.path.join(repo_path, ".git")):
                self.log("[GIT] Inicializando repositório local...")
                Repo.init(repo_path)

            # --- Ler e descriptografar token ---
            if not os.path.exists("token.enc") or not os.path.exists("key.key"):
                self.log("[ERRO] Token GitHub não encontrado. Salve um token antes de sincronizar.")
                return

            with open("key.key", "rb") as key_file:
                key = key_file.read()

            fernet = Fernet(key)
            with open("token.enc", "rb") as token_file:
                token_encrypted = token_file.read()

            token = fernet.decrypt(token_encrypted).decode()

            # --- Configuração do repositório ---
            repo = Repo(repo_path)
            origin_url = f"https://{token}:x-oauth-basic@github.com/Lizandro-Sales/Natural-Core-IA.git"

            if "origin" not in [remote.name for remote in repo.remotes]:
                repo.create_remote("origin", origin_url)
            else:
                repo.remote("origin").set_url(origin_url)

            self.log("[GIT] Repositório configurado.")

            # --- Adicionar e commitar alterações ---
            repo.git.add(A=True)
            if repo.is_dirty():
                repo.index.commit(f"Sincronização automática via HUD v5.1 - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                self.log("[GIT] Alterações commitadas com sucesso.")
            else:
                self.log("[GIT] Nenhuma alteração para enviar.")

            # --- Enviar para GitHub ---
            self.log("[GIT] Enviando alterações para GitHub...")
            repo.remote("origin").push(refspec="main:main")
            self.log("[OK] Projeto sincronizado com sucesso no GitHub.")

        except GitCommandError as e:
            self.log(f"[ERRO GIT] {e}")
        except Exception as e:
            self.log(f"[ERRO] Falha durante sincronização: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HUDApp(root)
    root.mainloop()