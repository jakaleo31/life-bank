import customtkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
from logika.database import get_db_connection


class StatsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # Razdelitev na levo (Life) in desno (Money)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- LIFE PANEL ---
        self.life_panel = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=15)
        self.life_panel.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")
        customtkinter.CTkLabel(self.life_panel, text="Life", font=("Arial", 24, "bold")).pack(pady=10)
        self.fire_label = customtkinter.CTkLabel(self.life_panel, font=("Arial", 60))
        self.fire_label.pack(pady=20)
        self.streak_desc = customtkinter.CTkLabel(self.life_panel, text="", font=("Arial", 12))
        self.streak_desc.pack()

        # --- MONEY PANEL ---
        self.money_panel = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=15)
        self.money_panel.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        customtkinter.CTkLabel(self.money_panel, text="Money", font=("Arial", 24, "bold")).pack(pady=10)

        self.pie_chart_box = customtkinter.CTkFrame(self.money_panel, fg_color="#2b2b2b", height=200)
        self.pie_chart_box.pack(fill="x", padx=20, pady=10)

        # Popravljeno ime labele za porabo
        self.label_mesecna_poraba = customtkinter.CTkLabel(self.money_panel, text="Poraba: 0€", font=("Arial", 20))
        self.label_mesecna_poraba.pack(pady=10)

        # --- PROGRESS BAR (Spodaj čez celo širino) ---
        self.progress_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=40, sticky="ew")

        self.goal_label = customtkinter.CTkLabel(self.progress_frame, text="Napredek do cilja",
                                                 font=("Arial", 14, "bold"))
        self.goal_label.pack(pady=(0, 5))

        self.savings_progress = customtkinter.CTkProgressBar(self.progress_frame, height=20, progress_color="#5ed77a")
        self.savings_progress.pack(fill="x", pady=5)
        self.savings_progress.set(0)

        self.percent_label = customtkinter.CTkLabel(self.progress_frame, text="0%", font=("Arial", 12))
        self.percent_label.pack()

        # Zaženemo posodobitev vseh podatkov
        self.update_stats()

    def update_stats(self):
        # Pokličemo vse pod-funkcije za posodobitev
        self.ogenj()
        self.posodobi_graf_in_porabo()
        self.update_progress()  # POMEMBNO: To si prej pozabil poklicati!

    def posodobi_graf_in_porabo(self):
        try:
            conn = get_db_connection()
            vnos = conn.cursor()
            mesec_leto = datetime.datetime.now().strftime("%Y-%m")

            # Top 5 kategorij odhodkov (uporabimo opis kot kategorijo)
            vnos.execute("""
                SELECT opis, SUM(abs(znesek)) 
                FROM transakcije 
                WHERE tip='odhodek' 
                GROUP BY opis 
                ORDER BY SUM(abs(znesek)) DESC 
                LIMIT 5
            """)
            podatki_torta = vnos.fetchall()

            vnos.execute("SELECT SUM(abs(znesek)) FROM transakcije WHERE tip='odhodek' AND datum LIKE ?",
                         (f'{mesec_leto}%',))
            poraba_mesec = vnos.fetchone()[0] or 0.0

            conn.close()

            self.label_mesecna_poraba.configure(text=f'Poraba ta mesec: {poraba_mesec:.2f} €')
            self.narisi_graf(podatki_torta)
        except Exception as e:
            print(f"Napaka graf/poraba: {e}")

    def update_progress(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT SUM(znesek) FROM transakcije")
            rezultat = cursor.fetchone()[0]
            trenutno_stanje = float(rezultat) if rezultat is not None else 0.0

            cursor.execute("SELECT value FROM settings WHERE key = 'savings_goal' LIMIT 1")
            res = cursor.fetchone()
            cilj = float(res[0]) if res else 1000.0
            conn.close()

            napredek = trenutno_stanje / cilj if cilj > 0 else 0
            napredek = max(0, min(napredek, 1.0))

            self.savings_progress.set(napredek)
            self.goal_label.configure(text=f"Stanje: {trenutno_stanje:.2f}€ / Cilj: {cilj:.2f}€")
            self.percent_label.configure(text=f"{int(napredek * 100)}%")
        except Exception as e:
            print(f"Napaka pri progress baru: {e}")

    def ogenj(self):
        try:
            conn = get_db_connection()
            vnos = conn.cursor()
            danes = datetime.datetime.now().strftime("%Y-%m-%d")

            # Preverimo današnje aktivnosti
            t1 = vnos.execute('SELECT COUNT(*) FROM transakcije WHERE datum = ?', (danes,)).fetchone()[0]
            t2 = vnos.execute("SELECT COUNT(*) FROM dogodki WHERE datum_zacetek LIKE ?", (f'{danes}%',)).fetchone()[0]

            if (t1 + t2) > 0:
                self.fire_label.configure(text_color="#ff8c00", text="1🔥")
                self.streak_desc.configure(text="Aktivno danes!", text_color="#5ed77a")
            else:
                self.fire_label.configure(text_color="#9f9f9f", text="0🔥")
                self.streak_desc.configure(text="Danes še nimaš vnosa", text_color="gray")
            conn.close()
        except Exception as e:
            print(f"Napaka pri ognju: {e}")

    def narisi_graf(self, podatki_torta):
        # Odstranimo stare grafe
        for widget in self.pie_chart_box.winfo_children():
            widget.destroy()

        if not podatki_torta or sum(p[1] for p in podatki_torta) == 0:
            customtkinter.CTkLabel(self.pie_chart_box, text="Ni podatkov o porabi").pack(pady=20)
            return

        imena = [str(i[0]) if i[0] else "Ostalo" for i in podatki_torta]
        velikosti = [i[1] for i in podatki_torta]

        # MODERNA VERZIJA GRAFA
        fig = Figure(figsize=(3, 3), dpi=100)
        fig.patch.set_facecolor('#1a1a1a')  # Temno ozadje, da paše v panel
        ax = fig.add_subplot(111)

        # Barvna paleta
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

        wedges, texts, autotexts = ax.pie(
            velikosti,
            labels=imena,
            autopct='%1.0f%%',
            startangle=140,
            colors=colors,
            textprops={'color': "w", 'fontsize': 8}
        )

        ax.set_title("Poraba po opisih", color="white", fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=self.pie_chart_box)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)