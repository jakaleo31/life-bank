import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import webbrowser

# UVOZI LOGIKE
from logika.finance import calculate_work_hours, get_hourly_rate, savings_plan
from logika.database import get_db_connection


class MoneyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # Razporeditev: Leva stran (2/3), Desna stran (1/3)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= LEVA STRAN (Graf + Stanje + Gumbi+ scrollbar) =================
        self.left_panel = customtkinter.CTkFrame(self, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # 1. Graf
        self.graph_box = customtkinter.CTkFrame(self.left_panel, fg_color="#2b2b2b", height=250)
        self.graph_box.pack(fill="x", pady=(0, 10))

        # 2. Stanje
        self.status_box = customtkinter.CTkFrame(self.left_panel, fg_color="#1f1f1f", border_width=1,
                                                 border_color="#333333")
        self.status_box.pack(fill="x", pady=10)
        customtkinter.CTkLabel(self.status_box, text="TRENUTNO STANJE", font=("Arial", 12), text_color="gray").pack(
            pady=(10, 0))
        self.status_amount = customtkinter.CTkLabel(self.status_box, text="0.00 €", font=("Arial", 28, "bold"),
                                                    text_color="#73b6f2")
        self.status_amount.pack(pady=(0, 10))
        self.create_graph()
        # Scrool bar (gor->dol)
        self.seznam_transakcij_okvir = customtkinter.CTkScrollableFrame(self.left_panel, fg_color="transparent",
                                                                        height=300)
        self.seznam_transakcij_okvir.pack(fill='both', expand=True, pady=10)
        # 3. Gumbi (Prihodek/Odhodek)
        self.button_row = customtkinter.CTkFrame(self.left_panel, fg_color="transparent")
        self.button_row.pack(fill="x", side="bottom", pady=10)
        customtkinter.CTkButton(self.button_row, text="PRIHODEK", fg_color="#5ed77a", text_color="black",
                                font=("Arial", 14, "bold"), height=50, hover_color="#429656",
                                command=lambda: self.odpri_vnos('prihodek')).pack(side="left",
                                                                                  expand=True,
                                                                                  padx=(0, 5))

        customtkinter.CTkButton(self.button_row, text="ODHODEK", fg_color="#e74c3c", font=("Arial", 14, "bold"),
                                height=50, hover_color="#9c3025", command=lambda: self.odpri_vnos('odhodek')).pack(
            side="left", expand=True,
            padx=(5, 0))

        # ================= DESNA STRAN (Oba kalkulatorja hkrati) =================
        # V __init__ spremeni desni panel v scrollable:
        self.right_panel = customtkinter.CTkScrollableFrame(self, fg_color="#1a1a1a", corner_radius=15)
        self.right_panel.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        # --- ZGORNJI DEL: Koliko moram delati ---
        self.work_section = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        self.work_section.pack(fill="x", padx=20, pady=(10, 5))

        customtkinter.CTkLabel(self.work_section, text="Koliko moram delati?", font=("Arial", 18, "bold")).pack(
            pady=(0, 10))
        self.item_entry = customtkinter.CTkEntry(self.work_section, placeholder_text="Cena izdelka (€)", height=35)
        self.item_entry.pack(fill="x", pady=30)
        customtkinter.CTkButton(self.work_section, text="Izračunaj", fg_color="#73b6f2", text_color="black",
                                command=self.show_work_hours).pack(fill="x", pady=5)
        self.result_label = customtkinter.CTkLabel(self.work_section, text="", font=("Arial", 13))
        self.result_label.pack(pady=5)

        # Črta za ločevanje (vizualni dodatek)
        customtkinter.CTkFrame(self.right_panel, height=2, fg_color="#333333").pack(fill="x", padx=30, pady=5)

        # --- SPODNJI DEL: Kreditni kalkulator ---
        self.credit_section = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        self.credit_section.pack(fill="x", padx=20, pady=5)

        customtkinter.CTkLabel(self.credit_section, text="Kreditni kalkulator", font=("Arial", 18, "bold")).pack(
            pady=(0, 10))
        self.kredit_znesek = customtkinter.CTkEntry(self.credit_section, placeholder_text="Znesek kredita (€)",
                                                    height=30)
        self.kredit_znesek.pack(fill="x", pady=5)
        self.kredit_obresti = customtkinter.CTkEntry(self.credit_section, placeholder_text="Obrestna mera (%)",
                                                     height=30)
        self.kredit_obresti.pack(fill="x", pady=5)
        self.kredit_doba = customtkinter.CTkEntry(self.credit_section, placeholder_text="Doba (leta)", height=30)
        self.kredit_doba.pack(fill="x", pady=5)

        customtkinter.CTkButton(self.credit_section, text="Izračunaj obrok", fg_color="#73b6f2",
                                text_color="black", command=self.calculate).pack(fill="x", pady=15)
        self.res_label = customtkinter.CTkLabel(self.credit_section, text="", font=("Arial", 16, "bold"))
        self.res_label.pack(pady=5)
        # Črta za ločevanje
        customtkinter.CTkFrame(self.right_panel, height=2, fg_color="#333333").pack(fill="x", padx=30, pady=5)

        # --- SPODNJI DEL: Varčevalni načrt ---
        self.savings_section = customtkinter.CTkFrame(self.right_panel, fg_color="transparent")
        self.savings_section.pack(fill="x", padx=20, pady=5)

        customtkinter.CTkLabel(self.savings_section, text="Varčevalni cilj", font=("Arial", 18, "bold")).pack(
            pady=(0, 10))

        self.goal_entry = customtkinter.CTkEntry(self.savings_section, placeholder_text="Želeni znesek (€)", height=30)
        self.goal_entry.pack(fill="x", pady=5)

        self.current_savings_entry = customtkinter.CTkEntry(self.savings_section,
                                                            placeholder_text="Že privarčevano (€)", height=30)
        self.current_savings_entry.pack(fill="x", pady=5)

        customtkinter.CTkButton(self.savings_section, text="Izračunaj ure", fg_color="#5ed77a",
                                text_color="black", command=self.prikazi_savings_plan).pack(fill="x", pady=15)

        self.savings_res_label = customtkinter.CTkLabel(self.savings_section, text="", font=("Arial", 14, "bold"))
        self.savings_res_label.pack(pady=5)

        self.ai()
        self.osvezi_seznam()

    def create_graph(self):
        # 1. PRIDOBIVANJE PODATKOV
        try:
            with get_db_connection() as conn:
                vnos = conn.cursor()

                vnos.execute('SELECT znesek FROM transakcije')
                podatki = vnos.fetchall()
                cisti_zneski = [vrstica[0] for vrstica in podatki]

                vnos.execute("SELECT value FROM settings WHERE key = 'premium' LIMIT 1")
                rezultat = vnos.fetchone()
                premium = rezultat[0] if rezultat else 0
        except Exception as e:
            print(f"Napaka pri branju baze za graf: {e}")
            return

        # Izračun točk
        stanje = 0
        tocke_za_graf = []
        for z in cisti_zneski:
            stanje += z
            tocke_za_graf.append(stanje)

        self.status_amount.configure(text=f"{stanje:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

        # 2. DEFINICIJA BARV
        videz = customtkinter.get_appearance_mode()
        bg_barva = '#2b2b2b' if videz == "Dark" else '#ebebeb'
        text_barva = 'white' if videz == "Dark" else 'black'

        # 3. EXPLICIT FIGURE MANAGEMENT (Brez plt. klicev)
        # Ustvarimo objekt Figure neposredno
        fig = Figure(figsize=(4, 2.5), dpi=100)
        fig.patch.set_facecolor(bg_barva)

        ax = fig.add_subplot(111)  # Doda osi na sliko
        ax.set_facecolor(bg_barva)

        if tocke_za_graf:
            ax.plot(tocke_za_graf, color='#e74c3c', marker='o', markersize=4, linewidth=2)

            # Logika za meje in korake
            trenutni_max = max(tocke_za_graf)
            spodnja_meja = -500 if str(premium) in ["1", "on"] else 0
            zgornja_meja = max(trenutni_max * 1.15, 100)  # Preprečimo 0

            if zgornja_meja <= 500:
                korak = 100
            elif zgornja_meja < 2000:
                korak = 500
            else:
                korak = 1000

            ax.set_ylim(spodnja_meja, zgornja_meja)
            ax.yaxis.set_ticks(range(int(spodnja_meja), int(zgornja_meja) + korak, korak))
        else:
            ax.text(0.5, 0.5, "Ni podatkov", color=text_barva, ha='center')

        ax.grid(True, axis="y", linestyle="--", alpha=0.3)
        ax.tick_params(axis='both', labelcolor=text_barva, labelsize=8)

        # Odstranimo robove (spines) za lepši izgled
        for spine in ax.spines.values():
            spine.set_visible(False)

        # 4. ČIŠČENJE IN PRIKAZ
        for widget in self.graph_box.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_box)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def show_work_hours(self):
        try:
            cena = float(self.item_entry.get().replace(",", "."))
            urna_postavka = get_hourly_rate()
            if urna_postavka > 0:
                ure = calculate_work_hours(cena, urna_postavka)
                self.result_label.configure(text=f"Potrebuješ {ure} ur dela.", text_color="white")
            else:
                self.result_label.configure(text="Nastavi postavko!", text_color="#e74c3c")
        except Exception as e:
            self.result_label.configure(text="Vnesi številko!", text_color="#e74c3c")
            print(e)

    def transakcija(self, obstojeca_transakcija=None):
        """Odpre okno za vnos/urejanje transakcije.
        Če je podan obstojeca_transakcija (tuple iz baze), se prikažejo obstoječi podatki.
        """
        self.okno_transakcija = customtkinter.CTkToplevel(self)

        if obstojeca_transakcija:
            # Urejanje obstoječe transakcije
            naslov = "Uredi transakcijo"
            self.tip_transakcije = obstojeca_transakcija[1]
        else:
            naslov = "Prihodki" if self.tip_transakcije == 'prihodek' else "Odhodki"

        self.okno_transakcija.title(naslov)
        sirina_okna = self.winfo_screenwidth()
        visina_okna = self.winfo_screenheight()
        x = (sirina_okna // 2) - (175)
        y = (visina_okna // 2) - (175)
        self.okno_transakcija.geometry(f"350x380+{x}+{y}")
        self.okno_transakcija.attributes("-topmost", True)

        naslov_okna = customtkinter.CTkLabel(self.okno_transakcija, text=naslov, font=("Arial", 18, "bold"))
        naslov_okna.pack(fill="x", pady=10)

        # Izbirnik tipa (samo pri urejanju)
        if obstojeca_transakcija:
            tip_frame = customtkinter.CTkFrame(self.okno_transakcija, fg_color="transparent")
            tip_frame.pack(fill="x", padx=20, pady=5)
            self.tip_var_urejanje = customtkinter.StringVar(value=self.tip_transakcije)
            customtkinter.CTkRadioButton(tip_frame, text="Prihodek", variable=self.tip_var_urejanje,
                                          value="prihodek", command=self.osvezi_predznak_znesek).pack(side="left", padx=10)
            customtkinter.CTkRadioButton(tip_frame, text="Odhodek", variable=self.tip_var_urejanje,
                                          value="odhodek", command=self.osvezi_predznak_znesek).pack(side="left", padx=10)

        self.znesek = customtkinter.CTkEntry(self.okno_transakcija, placeholder_text="Vnesi znesek (€)")
        self.znesek.pack(fill="x", padx=20, pady=5)
        self.datum = customtkinter.CTkEntry(self.okno_transakcija, placeholder_text="Vnesi datum (llll-mm-dd)")
        self.datum.pack(fill="x", padx=20, pady=5)
        self.opis = customtkinter.CTkEntry(self.okno_transakcija, placeholder_text='Opis')
        self.opis.pack(fill="x", padx=20, pady=5)

        # Predizpolnimo, če je podan obstoječa transakcija
        if obstojeca_transakcija:
            # Znesek prikažemo kot absolutno vrednost (predznak določa tip)
            abs_znesek = abs(obstojeca_transakcija[2])
            self.znesek.insert(0, f"{abs_znesek:.2f}")
            self.datum.insert(0, obstojeca_transakcija[3])
            self.opis.insert(0, obstojeca_transakcija[4] or "")

        # Gumbi v eni vrstici
        btn_frame = customtkinter.CTkFrame(self.okno_transakcija, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)

        customtkinter.CTkButton(
            btn_frame, text="Shrani", font=("Arial", 16, "bold"),
            fg_color="#5ed77a", text_color="black", hover_color="#429656",
            command=lambda: self.vzemi_shrani(
                transakcija_id=obstojeca_transakcija[0] if obstojeca_transakcija else None
            )
        ).pack(side="left", expand=True, padx=(0, 5))

        # Gumb "Izbriši" samo pri urejanju
        if obstojeca_transakcija:
            customtkinter.CTkButton(
                btn_frame, text="Izbriši", font=("Arial", 16, "bold"),
                fg_color="#e74c3c", hover_color="#9c3025",
                command=lambda: self.izbrisi_transakcijo(obstojeca_transakcija[0])
            ).pack(side="left", expand=True, padx=(5, 0))
        else:
            customtkinter.CTkButton(
                btn_frame, text="Prekliči", font=("Arial", 16, "bold"),
                fg_color="gray",
                command=self.okno_transakcija.destroy
            ).pack(side="left", expand=True, padx=(5, 0))

    def osvezi_predznak_znesek(self):
        """Pri urejanju - če spremenimo tip, posodobi label."""
        self.tip_transakcije = self.tip_var_urejanje.get()

    def izbrisi_transakcijo(self, transakcija_id):
        """Izbriše transakcijo s potrditvenim oknom."""
        potrditev = customtkinter.CTkToplevel(self)
        potrditev.title("Potrditev brisanja")
        potrditev.geometry("350x150")
        potrditev.attributes("-topmost", True)
        potrditev.grab_set()
        x = (self.winfo_screenwidth() // 2) - 175
        y = (self.winfo_screenheight() // 2) - 75
        potrditev.geometry(f"350x150+{x}+{y}")

        customtkinter.CTkLabel(
            potrditev, text="Izbrišem to transakcijo?",
            font=("Arial", 14, "bold"), text_color="#e74c3c"
        ).pack(pady=(30, 10))

        def potrdi():
            try:
                with get_db_connection() as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM transakcije WHERE id=?", (transakcija_id,))
                    conn.commit()
            except Exception as e:
                print(f"Napaka pri brisanju transakcije: {e}")
            potrditev.destroy()
            self.okno_transakcija.destroy()
            self.create_graph()
            self.osvezi_seznam()

        btn_frame = customtkinter.CTkFrame(potrditev, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkButton(btn_frame, text="Prekliči", fg_color="gray",
                                 command=potrditev.destroy).pack(side="left", expand=True, padx=5)
        customtkinter.CTkButton(btn_frame, text="Izbriši", fg_color="#e74c3c", hover_color="#9c3025",
                                 command=potrdi).pack(side="left", expand=True, padx=5)

    def vzemi_shrani(self, transakcija_id=None):
        datum = self.datum.get().strip()
        try:
            # Preverjanje datuma
            pravilni_datum = datetime.datetime.strptime(datum, "%Y-%m-%d")
            datum_str = pravilni_datum.strftime("%Y-%m-%d")
        except ValueError:
            print("Napaka: napačen format datuma")
            return

        # PRAVILNA PRETVORBA ZNESKA
        znesek_raw = self.znesek.get().replace(',', '.')
        try:
            znesek = float(znesek_raw)
        except ValueError:
            # USTVARIMO NAPAKO, KI JO UPORABNIK VIDI
            napaka_label = customtkinter.CTkLabel(
                self.okno_transakcija,
                text="Napaka: Vpiši samo številke!",
                text_color="#e74c3c",
                font=("Arial", 12, "bold")
            )
            napaka_label.pack(pady=5)
            return

        # Uporabimo tip iz radio gumbov, če smo v načinu urejanja
        if transakcija_id and hasattr(self, 'tip_var_urejanje'):
            self.tip_transakcije = self.tip_var_urejanje.get()

        if self.tip_transakcije == "odhodek" and znesek > 0:
            znesek *= -1

        values = (self.tip_transakcije, znesek, datum_str, self.opis.get())

        try:
            with get_db_connection() as conn:
                vnos_v_bazo = conn.cursor()
                if transakcija_id:
                    vnos_v_bazo.execute("UPDATE transakcije SET tip=?, znesek=?, datum=?, opis=? WHERE id=?",
                                        (*values, transakcija_id))
                else:
                    vnos_v_bazo.execute("INSERT INTO transakcije (tip, znesek, datum, opis) VALUES (?,?,?,?)", values)
                conn.commit()

            self.okno_transakcija.destroy()
            self.create_graph()
            self.osvezi_seznam()
        except Exception as e:
            print(f"Splošna napaka: {e}")

    def odpri_vnos(self, tip):
        self.tip_transakcije = tip
        self.transakcija()

    def odpri_urejanje_transakcije(self, transakcija):
        """Odpre okno za urejanje obstoječe transakcije (klicano ob kliku na vrstico)."""
        # Najprej počistimo morebitne ostanke od prejšnjega radio gumba
        if hasattr(self, 'tip_var_urejanje'):
            try:
                del self.tip_var_urejanje
            except AttributeError:
                pass
        self.transakcija(obstojeca_transakcija=transakcija)

    def osvezi_seznam(self):
        with get_db_connection() as povezava:
            vnos_v_bazo = povezava.cursor()
            for widget in self.seznam_transakcij_okvir.winfo_children():
                widget.destroy()
            podatki_v_bazi = vnos_v_bazo.execute("SELECT * FROM transakcije ORDER BY id DESC")
            for vrstica_podatkov in podatki_v_bazi.fetchall():
                if vrstica_podatkov[1] == 'prihodek':
                    predznak, barva = '+', '#38d15c'
                else:
                    predznak, barva = '-', '#bd1e31'
                vrstica = customtkinter.CTkFrame(self.seznam_transakcij_okvir, fg_color='transparent')
                znesek_label = customtkinter.CTkLabel(vrstica, text_color=barva,
                                                      text=f'{predznak}{abs(vrstica_podatkov[2])}€',
                                                      font=("Arial", 18, "bold"))
                znesek_label.pack(side="left", padx=10)
                datum_label = customtkinter.CTkLabel(vrstica, text_color='white', text=f'Datum:{vrstica_podatkov[3]}',
                                                     font=("Arial", 18, "bold"))
                datum_label.pack(side="left", padx=10)
                opis_label = customtkinter.CTkLabel(vrstica, text_color='white', text=f'{vrstica_podatkov[4]}',
                                                    font=("Arial", 18, "bold"))
                opis_label.pack(side="left", padx=10)
                vrstica.pack(fill="x", pady=10)

                # Klik na vrstico odpre urejanje te transakcije
                vrstica.bind("<Button-1>",
                             lambda e, t=vrstica_podatkov: self.odpri_urejanje_transakcije(t))
                for child in (znesek_label, datum_label, opis_label):
                    child.bind("<Button-1>",
                                lambda e, t=vrstica_podatkov: self.odpri_urejanje_transakcije(t))

    def calculate(self):
        try:
            p = float(self.kredit_znesek.get().replace(",", "."))
            obresti_raw = float(self.kredit_obresti.get().replace(",", "."))
            leta_raw = float(self.kredit_doba.get().replace(",", "."))

            if leta_raw <= 0:
                self.res_label.configure(text="Doba mora biti > 0!", text_color="#e74c3c")
                return

            r = obresti_raw / 100 / 12
            n = leta_raw * 12

            if r == 0:
                monthly = p / n
            else:
                # Formula: [P * r * (1+r)^n] / [(1+r)^n – 1]
                monthly = (p * r * (1 + r) ** n) / ((1 + r) ** n - 1)

            self.res_label.configure(text=f"Mesečni obrok: {round(monthly, 2)} €", text_color="#5ed77a")
        except (ValueError, ZeroDivisionError):
            self.res_label.configure(text="Vnesi pravilne podatke!", text_color="#e74c3c")

    @staticmethod
    def open_net():
        webbrowser.open_new("https://chatgpt.com")

    def ai(self):
        try:
            with get_db_connection() as povezava:
                vnos = povezava.cursor()
                vnos.execute("SELECT value FROM settings WHERE key = 'premium' LIMIT 1")
                rezultat = vnos.fetchone()  # fetchone() vrne samo eno vrstico (npr. ('on',))

            if rezultat:
                premium_val = str(rezultat[0])  # Vzamemo prvo vrednost iz norke

                # Preverimo vse možne oblike pozitivnega premium statusa
                if premium_val.lower() in ['on', '1', 'true']:
                    link_label = customtkinter.CTkLabel(
                        self.right_panel,
                        text="✨ Klepetaj z AI o varčevanju",
                        text_color="#73b6f2",
                        font=("Arial", 13, "underline"),
                        cursor="hand2"
                    )
                    link_label.pack(side='bottom', pady=20)
                    # Pomembno: uporabi self.open_net
                    link_label.bind("<Button-1>", self.open_net)
        except Exception as e:
            print(f"Napaka pri nalaganju AI povezave: {e}")

    def prikazi_savings_plan(self):
        try:
            cilj = float(self.goal_entry.get().replace(",", "."))
            privarcevano = float(self.current_savings_entry.get().replace(",", "."))

            # Pokličemo tvojo funkcijo
            potrebne_ure = savings_plan(cilj, privarcevano)

            if potrebne_ure == float('inf'):
                self.savings_res_label.configure(text="Nastavi urno postavko v nastavitvah!", text_color="#e74c3c")
            elif potrebne_ure == 0:
                self.savings_res_label.configure(text="Cilj je že dosežen! 🥳", text_color="#5ed77a")
            else:
                self.savings_res_label.configure(text=f"Delati moraš še {potrebne_ure} ur.", text_color="white")

        except ValueError:
            self.savings_res_label.configure(text="Vnesi veljavne zneske!", text_color="#e74c3c")
