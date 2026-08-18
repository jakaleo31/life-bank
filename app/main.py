import customtkinter
from PIL import Image
import os

# Uvozi tvoje komponente
from ui.money_tab import MoneyFrame
from ui.life_tab import LifeFrame
from ui.settings_tab import SettingsFrame
from logika.database import get_db_connection
from ui.stats_tab import StatsFrame
from plyer import notification


class App(customtkinter.CTk):
    def __init__(self):

        # 2. Pridobimo shranjeno temo iz baze
        tema = self.get_saved_theme()

        # 3. NASTAVITEV VIDEZA (Svetlo/Temno) - To sledi sistemu
        customtkinter.set_appearance_mode("System")

        # 4. NASTAVITEV BARVNE TEME (Mora biti pred super().__init__())
        # Če v bazi piše 'System', uporabi privzeto 'blue', sicer pa JSON pot
        if tema == "System":
            customtkinter.set_default_color_theme("blue")
        else:
            try:
                customtkinter.set_default_color_theme(tema)
            except Exception as e:
                customtkinter.set_default_color_theme("blue")
                print(e)

        super().__init__()

        # Nastavitve okna
        self.title("Life & Money Manager")
        self.geometry("1000x800")

        # --- Nalaganje ikon in preostali UI ---
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.icons_path = os.path.join(self.base_path, "assets", "icons")

        try:
            self.money_icon = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(self.icons_path, "money_icon.png")), size=(24, 24))
            self.life_icon = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(self.icons_path, "life_icon.png")), size=(24, 24))
            self.stats_icon = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(self.icons_path, "stats.png")), size=(24, 24))
            self.settings_icon = customtkinter.CTkImage(
                light_image=Image.open(os.path.join(self.icons_path, "settings.png")), size=(24, 24))
        except Exception as e:
            print(f"Opozorilo: Ikone niso bile najdene: {e}")
            self.money_icon = self.life_icon = self.stats_icon = self.settings_icon = None

        # Taskbar
        self.taskbar = customtkinter.CTkFrame(self, height=70, fg_color="transparent", corner_radius=0)
        self.taskbar.pack(side="bottom", fill="x")

        # Container
        self.container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="top", fill="both", expand=True)

        # Gumbi
        self.stats_btn = customtkinter.CTkButton(self.taskbar, text="Stats", image=self.stats_icon, compound="top",
                                                 fg_color="transparent", hover_color="#333333",
                                                 command=lambda: self.switch_page("Stats"))
        self.stats_btn.pack(side="left", expand=True, fill="both")

        self.current_mode = "Money"
        self.toggle_btn = customtkinter.CTkButton(
            self.taskbar, text="Money", image=self.money_icon, compound="top",
            fg_color="#73b6f2", text_color="black", font=("Arial", 12, "bold"),
            command=self.toggle_action
        )
        self.toggle_btn.pack(side="left", expand=True, fill="both")

        self.settings_btn = customtkinter.CTkButton(self.taskbar, text="Nastavitve", image=self.settings_icon,
                                                    compound="top", fg_color="transparent", hover_color="#333333",
                                                    command=lambda: self.switch_page("Settings"))
        self.settings_btn.pack(side="left", expand=True, fill="both")

        self.switch_page("Money")
        try:
            notification.notify(
                title="Dobrodošel nazaj!",
                message="Tvoj Life & Money Manager je pripravljen.",
                timeout=5
            )
        except Exception as e:
            print(e)
    @staticmethod
    def get_saved_theme():
        """Preveri bazo in vrne pot do JSON teme ali 'System'."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # Preveri premium
                cursor.execute("SELECT value FROM settings WHERE key = 'premium' LIMIT 1")
                premium_row = cursor.fetchone()
                premium = str(premium_row[0]) if premium_row else "0"

                if premium in ['1', 'on', 'true']:
                    cursor.execute("SELECT value FROM settings WHERE key = 'theme_path' LIMIT 1")
                    theme_row = cursor.fetchone()
                    return theme_row[0] if theme_row else "System"

            return "System"
        except Exception as e:
            print(f"Napaka pri branju teme: {e}")
            return "System"



    def toggle_action(self):
        if self.current_mode == "Money":
            self.current_mode = "Life"
            self.toggle_btn.configure(text="Life", image=self.life_icon, fg_color="#5ed77a", hover_color="#3f8c51")
        else:
            self.current_mode = "Money"
            self.toggle_btn.configure(text="Money", image=self.money_icon, fg_color="#73b6f2", hover_color="#4e80ad")
        self.switch_page(self.current_mode)

    def switch_page(self, page_name):
        for widget in self.container.winfo_children():
            widget.destroy()
        if page_name == "Money":
            MoneyFrame(self.container).pack(fill="both", expand=True)
        elif page_name == "Life":
            LifeFrame(self.container).pack(fill="both", expand=True)
        elif page_name == "Settings":
            SettingsFrame(self.container).pack(fill="both", expand=True)
        elif page_name == "Stats":
            StatsFrame(self.container).pack(fill="both", expand=True)



if __name__ == "__main__":
    app = App()
    app.mainloop()