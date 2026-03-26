import customtkinter
from PIL import Image



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")

        # -------------------------
        #   TOGGLE STATE
        # -------------------------
        self.toggle_state = 0
        self.text = "Bank"
        self.color = "#73b6f2"
        self.hover_color = "#507fa9"
        self.icon = customtkinter.CTkImage(
            Image.open("prenos__1_-removebg-preview.png"), size=(24, 24)
        )

        # -------------------------
        #   TASKBAR
        # -------------------------
        self.taskbar = customtkinter.CTkFrame(self, height=60, fg_color="#1f1f1f")
        self.taskbar.pack(side="bottom", fill="x")

        # Load icons
        stats_icon = customtkinter.CTkImage(Image.open("stats-removebg-preview.png"), size=(26, 26))
        settings_icon = customtkinter.CTkImage(Image.open("settings-removebg-preview.png"), size=(26, 26))

        # --- Stats button ---
        self.stats_btn = customtkinter.CTkButton(
            self.taskbar, text="Stats", image=stats_icon, compound="top",
            fg_color="transparent", hover_color="#333333"
        )
        self.stats_btn.pack(side="left", expand=True, fill="both")

        # --- Bank/Life toggle button ---
        self.toggle_btn = customtkinter.CTkButton(
            self.taskbar,
            text=self.text,
            command=self.toggle_callback,
            fg_color=self.color,
            hover_color=self.hover_color,
            image=self.icon,
            compound="top"
        )
        self.toggle_btn.pack(side="left", expand=True, fill="both")

        # --- Settings button ---
        self.settings_btn = customtkinter.CTkButton(
            self.taskbar, text="Settings", image=settings_icon, compound="top",
            fg_color="transparent", hover_color="#333333"
        )
        self.settings_btn.pack(side="left", expand=True, fill="both")

    # -------------------------
    #   TOGGLE LOGIC
    # -------------------------
    def toggle_callback(self):
        if self.toggle_state % 2 == 0:
            self.text = "Life"
            self.color = "#5ed77a"
            self.hover_color = "#49a75f"
            self.icon = customtkinter.CTkImage(
                Image.open("prenos-removebg-preview1.png"), size=(24, 24)
            )
        else:
            self.text = "Bank"
            self.color = "#73b6f2"
            self.hover_color = "#507fa9"
            self.icon = customtkinter.CTkImage(
                Image.open("prenos__1_-removebg-preview.png"), size=(24, 24)
            )

        self.toggle_btn.configure(
            text=self.text,
            fg_color=self.color,
            hover_color=self.hover_color,
            image=self.icon
        )

        self.toggle_state += 1


app = App()
app.mainloop()
