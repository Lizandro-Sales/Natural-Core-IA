import os
import subprocess
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog  # <-- Importação correta
from cryptography.fernet import Fernet
from datetime import datetime
import threading

# === CONFIGURAÇÕES GERAIS ===
BASE_DIR = r"E:\projetos\natural core"
TOKEN_KEY_PATH = os.path.join(BASE_DIR, "key.key")
TOKEN_ENC_PATH = os.path.join(BASE_DIR, "token.enc")
LOG_FILE = os.path.join(BASE_DIR, "hud_log.txt")
GIT_EXE = r"E:\Git\bin\git.exe"  # Caminho do Git
REPO_DIR = BASE_DIR

# === GERENCIAMENTO DE TOKEN ===
def gerar_chave():
    if not os.path.exists(TOKEN_KEY_PATH):
        key = Fernet.generate_key()
        with open(TOKEN_KEY_PATH, "wb") as key_file:
            key_file.write(key)

def carregar_chave():
    with open(TOKEN_KEY_PATH, "rb") as key_file:
        return key_file.read()

def salvar_token(token):
    try:
        gerar_chave()
        key = carregar_chave()
        fernet = Fernet(key)
        token_enc = fernet.encrypt(token.encode())
        with open(TOKEN_ENC_PATH, "wb") as token_file:
            token_file.write(token_enc)
        logar("Token GitHub salvo com sucesso.", "green")
    except Exception as e:
        logar(f"Erro ao salvar token: {e}", "red")

def obter_token():
    try:
        key = carregar_chave()
        fernet = Fernet(key)
        with open(TOKEN_ENC_PATH, "rb") as token_file:
            token_enc = token_file.read()
        return fernet.decrypt(token_enc).decode()
    except:
        return None

# === FUNÇÕES DE LOG ===
def logar(texto, cor="white"):
    agora = datetime.now().strftime("%H:%M:%S")
    linha = f"[{agora}] {texto}\n"
    log_box.config(state='normal')
    log_box.insert(tk.END, linha, cor)
    log_box.config(state='disabled')
    log_box.see(tk.END)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(linha)

# === OPERAÇÕES GIT ===
def executar_comando(comando):
    try:
        resultado = subprocess.run(
            comando, cwd=REPO_DIR, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return resultado.stdout.strip(), resultado.stderr.strip()
    except Exception as e:
        return "", str(e)

def sincronizar_github():
    logar("Iniciando sincronização com o GitHub...", "yellow")
    token = obter_token()
    if not token:
        messagebox.showerror("Erro", "Token GitHub não encontrado! Salve o token antes.")
        logar("Token GitHub ausente.", "red")
        return

    os.environ["GITHUB_TOKEN"] = token
    comandos = [
        [GIT_EXE, "add", "."],
        [GIT_EXE, "commit", "-m", "Atualização automática [v5.0]"],
        [GIT_EXE, "push", "origin", "main"]
    ]

    for comando in comandos:
        out, err = executar_comando(comando)
        if err and "nothing to commit" not in err.lower():
            logar(f"Erro: {err}", "red")
        if out:
            logar(out, "green")

    logar("Sincronização concluída ✅", "green")

def iniciar_sincronizacao():
    threading.Thread(target=sincronizar_github, daemon=True).start()

# === INTERFACE VISUAL (HUD) ===
janela = tk.Tk()
janela.title("🌿 Natural Core IA - HUD v5.0")
janela.geometry("720x480")
janela.configure(bg="#0F2027")

# === SEÇÃO DE LOG VISUAL ===
log_box = scrolledtext.ScrolledText(
    janela, bg="#1B1B1B", fg="white", font=("Consolas", 10),
    wrap=tk.WORD, state='disabled', height=18
)
log_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# === CONFIGURAÇÃO DE CORES ===
log_box.tag_config("red", foreground="#FF5555")
log_box.tag_config("green", foreground="#50FA7B")
log_box.tag_config("yellow", foreground="#F1FA8C")
log_box.tag_config("white", foreground="#FFFFFF")

# === BOTÕES ===
frame_botoes = tk.Frame(janela, bg="#0F2027")
frame_botoes.pack(pady=10)

btn_sync = tk.Button(frame_botoes, text="▶ Compilar e Sincronizar", command=iniciar_sincronizacao,
                     bg="#00BFA5", fg="white", font=("Segoe UI", 11, "bold"), width=25)
btn_sync.grid(row=0, column=0, padx=10)

def acao_salvar_token():
    token = tk.simpledialog.askstring("Token GitHub", "Insira seu token pessoal:")
    if token:
        salvar_token(token)

btn_token = tk.Button(frame_botoes, text="🔒 Salvar Token", command=acao_salvar_token,
                      bg="#2196F3", fg="white", font=("Segoe UI", 11, "bold"), width=20)
btn_token.grid(row=0, column=1, padx=10)

def encerrar():
    logar("Encerrando HUD...", "yellow")
    janela.destroy()

btn_encerrar = tk.Button(frame_botoes, text="🛑 Encerrar HUD", command=encerrar,
                         bg="#E53935", fg="white", font=("Segoe UI", 11, "bold"), width=20)
btn_encerrar.grid(row=0, column=2, padx=10)

logar("HUD v5.0 inicializado com sucesso.", "green")

janela.mainloop()