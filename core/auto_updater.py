import os
import subprocess
import datetime
import json
import tkinter as tk
from tkinter import ttk, scrolledtext

class VisualSyncHUD:
    def __init__(self, root):
        self.root = root
        self.root.title("⚙ Natural Core IA - Visual HUD v4.9 AutoSync+")
        self.root.geometry("580x440")
        self.root.configure(bg="#0b0b0b")
        self.root.resizable(False, False)

        # === LOG VISUAL ===
        self.text_area = scrolledtext.ScrolledText(self.root, bg="#0f0f0f", fg="#00ff00", font=("Consolas", 10))
        self.text_area.pack(fill="both", expand=True, padx=8, pady=8)
        self.text_area.insert("end", "[INFO] HUD Visual IA iniciado...\n")

        # === BARRA DE PROGRESSO ===
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=520, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["value"] = 0

        # === BOTÕES ===
        button_frame = tk.Frame(self.root, bg="#0b0b0b")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="🚀 Iniciar Build", command=self.start_build, width=20, bg="#202020", fg="#00ff00").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="⬆ Atualizar GitHub", command=self.sync_github, width=20, bg="#202020", fg="#00ff00").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="🔄 Atualização Completa", command=self.auto_full_update, width=22, bg="#202020", fg="#00ffff").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="❌ Fechar", command=self.root.quit, width=15, bg="#202020", fg="#ff4040").grid(row=1, column=1, pady=10)

    # === LOG VISUAL ===
    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        self.text_area.insert("end", f"{timestamp} {msg}\n")
        self.text_area.see("end")
        self.root.update_idletasks()

    # === FUNÇÃO: INCREMENTAR VERSÃO ===
    def increment_version(self):
        version_file = r"E:\projetos\natural core\update_info.json"
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            current = data.get("version", "4.8")
            major, minor = map(int, current.split("."))
            new_version = f"{major}.{minor + 1}"
            data["version"] = new_version
            data["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(version_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            self.log(f"🔢 Versão atualizada: {current} → {new_version}")
            return new_version
        except Exception as e:
            self.log(f"⚠ Erro ao atualizar versão: {e}")
            return "erro"

    # === BUILD ===
    def start_build(self):
        self.log("🚧 Iniciando build automática...")
        self.progress["value"] = 25
        build_script = r"E:\projetos\natural core\build_visualsync_plus_v4_8.bat"

        if not os.path.exists(build_script):
            self.log("❌ Script de build não encontrado.")
            return

        try:
            subprocess.run(build_script, shell=True)
            self.log("✅ Build concluída com sucesso.")
        except Exception as e:
            self.log(f"❌ ERRO durante o build: {e}")
        self.progress["value"] = 100

    # === SINCRONIZAÇÃO COM GITHUB ===
    def sync_github(self):
        self.log("⬆ Iniciando sincronização com o GitHub...")
        self.progress["value"] = 30
        version = self.increment_version()
        repo_dir = r"E:\projetos\natural core"
        os.chdir(repo_dir)

        try:
            subprocess.run(["git", "add", "."], shell=True)
            commit_msg = f"🚀 Build automática v{version} ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
            subprocess.run(["git", "commit", "-m", commit_msg], shell=True)
            subprocess.run(["git", "pull", "--no-edit", "origin", "main"], shell=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], shell=True)

            # CRIAR TAG E RELEASE
            subprocess.run(["git", "tag", f"v{version}"], shell=True)
            subprocess.run(["git", "push", "origin", f"v{version}"], shell=True)

            self.log(f"✅ Build v{version} publicada e sincronizada com sucesso no GitHub.")
        except Exception as e:
            self.log(f"❌ ERRO durante sincronização: {e}")

        self.progress["value"] = 100

    # === ATUALIZAÇÃO COMPLETA ===
    def auto_full_update(self):
        self.log("⚙ Iniciando atualização completa...")
        self.start_build()
        self.sync_github()
        self.log("🎉 Atualização completa e publicada com sucesso!")


# === INICIALIZAÇÃO ===
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualSyncHUD(root)
    root.mainloop()