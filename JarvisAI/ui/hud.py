import customtkinter as ctk
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JarvisHUD:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.geometry("520x300")
        self.app.title("JARVIS HUD")
        self.app.attributes("-topmost", True)

        self.title = ctk.CTkLabel(
            self.app,
            text="JARVIS ONLINE",
            font=("Orbitron", 28)
        )
        self.title.pack(pady=25)

        self.status = ctk.CTkLabel(
            self.app,
            text="Standing by...",
            font=("Consolas", 16)
        )
        self.status.pack(pady=10)

    def set_status(self, text: str):
        self.status.configure(text=text)

    def run(self):
        self.app.mainloop()

def start_hud(hud: JarvisHUD):
    threading.Thread(target=hud.run, daemon=True).start()
