import customtkinter
from PIL import Image


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")

        # --- TASKBAR FRAME ---
        self.taskbar = customtkinter.CTkFrame(self, height=60, fg_color="#1f1f1f")
        self.taskbar.pack(side="bottom", fill="x")

        # Load icons
        home_icon = customtkinter.CTkImage(Image.open("home.png"), size=(26, 26))
        stats_icon = customtkinter.CTkImage(Image.open("stats-removebg-preview.png"), size=(26, 26))
        settings_icon = customtkinter.CTkImage(Image.open("settings-removebg-preview.png"), size=(26, 26))

        # Buttons inside taskbar
        self.stats_btn = customtkinter.CTkButton(
            self.taskbar, text="Stats", image=stats_icon, compound="top",
            fg_color="transparent", hover_color="#333333"
        )
        self.stats_btn.pack(side="left", expand=True, fill="both")

        self.home_btn = customtkinter.CTkButton(
            self.taskbar, text="Home", image=home_icon, compound="top",
            fg_color="transparent", hover_color="#333333"
        )
        self.home_btn.pack(side="left", expand=True, fill="both")

        self.settings_btn = customtkinter.CTkButton(
            self.taskbar, text="Settings", image=settings_icon, compound="top",
            fg_color="transparent", hover_color="#333333"
        )
        self.settings_btn.pack(side="left", expand=True, fill="both")

app = App()
app.mainloop()
