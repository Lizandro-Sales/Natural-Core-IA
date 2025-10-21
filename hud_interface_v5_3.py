import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import datetime
import winsound
import threading

# === CONFIGURAÇÕES === #
PASTA_LOGS = r"E:\projetos\natural core\logs"
ARQUIVO_LOG = os.path.join(PASTA_LOGS, "sync_history.log")
BAT_GITHUB = r"E:\projetos\natural core\sincronizador_github.bat"

os.makedirs(PASTA_LOGS, exist_ok=True)

# === FUNÇÕES === #
def registrar_log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

def emitir_som(tipo="clique"):
    sons = {
        "clique": "SystemAsterisk",
        "sucesso": "SystemExclamation",
        "erro": "SystemHand"
    }
    winsound.PlaySound(sons.get(tipo, "SystemAsterisk"), winsound.SND_ALIAS)

def executar_sincronizacao():
    emitir_som("clique")
    atualizar_status("Sincronizando com o GitHub...")
    registrar_log("Iniciando sincronização com GitHub...")

    try:
        if not os.path.exists(BAT_GITHUB):
            registrar_log("❌ Arquivo .BAT não encontrado!")
            emitir_som("erro")
            messagebox.showerror("Erro", f"Arquivo não encontrado:\n{BAT_GITHUB}")
            atualizar_status("Erro: .BAT não encontrado")
            return
        
        # Abre o .bat em uma nova janela visível
        processo = subprocess.Popen(
            f'cmd /k "{BAT_GITHUB}"',
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        registrar_log("✅ Processo de sincronização iniciado com sucesso.")
        emitir_som("sucesso")
        atualizar_status("Sincronização iniciada em nova janela.")

    except Exception as e:
        registrar_log(f"❌ Erro na sincronização: {e}")
        emitir_som("erro")
        messagebox.showerror("Erro", str(e))
        atualizar_status("Erro durante sincronização.")

def encerrar_hud():
    emitir_som("clique")
    registrar_log("HUD encerrado manualmente.")
    root.destroy()

# === INTERFACE === #
root = tk.Tk()
root.title("Natural Core IA - HUD v5.3")
root.geometry("480x300")
root.configure(bg="#1a1a1a")
root.attributes("-topmost", True)

# Estilo metálico escuro
style = ttk.Style()
style.theme_use("clam")
style.configure("Metal.TButton", font=("Segoe UI", 10, "bold"),
                foreground="#cce7ff", background="#2b2b2b",
                borderwidth=1, focusthickness=3, focuscolor="#4f4f4f")
style.map("Metal.TButton",
          background=[("active", "#3a3a3a"), ("pressed", "#1f1f1f")],
          foreground=[("active", "#99ccff")])

# Layout
titulo = tk.Label(root, text="NATURAL CORE IA", font=("Segoe UI", 14, "bold"),
                  fg="#80bfff", bg="#1a1a1a")
titulo.pack(pady=15)

frame_botoes = tk.Frame(root, bg="#1a1a1a")
frame_botoes.pack(pady=10)

btn_sync = ttk.Button(frame_botoes, text="🔄 Sincronizar com GitHub",
                      style="Metal.TButton",
                      command=lambda: threading.Thread(target=executar_sincronizacao).start())
btn_sync.grid(row=0, column=0, padx=10, pady=10)

btn_logs = ttk.Button(frame_botoes, text="📁 Abrir Pasta de Logs",
                      style="Metal.TButton",
                      command=lambda: os.startfile(PASTA_LOGS))
btn_logs.grid(row=0, column=1, padx=10, pady=10)

btn_sair = ttk.Button(root, text="❌ Encerrar HUD", style="Metal.TButton",
                      command=encerrar_hud)
btn_sair.pack(pady=15)

lbl_status = tk.Label(root, text="Status: Aguardando ação...",
                      fg="#80bfff", bg="#1a1a1a", font=("Consolas", 9))
lbl_status.pack(pady=10)

def atualizar_status(msg):
    lbl_status.config(text=f"Status: {msg}")
    registrar_log(msg)

atualizar_status("HUD inicializado e pronto.")
root.mainloop()