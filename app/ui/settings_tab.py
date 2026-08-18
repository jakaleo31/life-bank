import customtkinter
from logika.database import get_db_connection
import os
import webbrowser


class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        # NASLOV
        lbl = customtkinter.CTkLabel(self, text="Nastavitve", font=("Arial", 22, "bold"))
        lbl.pack(pady=20)
        # --- TVOJ

        # --- TVOJ PREMIUM OKVIR --
        self.premium_frame = customtkinter.CTkFrame(
            self,
            border_width=1,
            border_color="#ffd700")

        self.premium_frame.pack(fill="x", padx=20, pady=20)
        # --- OKVIR ZA PODATKE (to je tvoj narisani pravokotnik) ---
        podatki_frame = customtkinter.CTkFrame(self, border_width=1)
        podatki_frame.pack(fill="x", padx=20, pady=1)
        # 1. Gumb POSODOBI (na tvoji skici "PONASTAVI")
        vnos_btn = customtkinter.CTkButton(
            podatki_frame,
            text="Posodobi postavko",
            command=self.posodobi_postavko

        )
        vnos_btn.pack(pady=(15, 5), padx=2)

        # 2. Vnosno polje (z placeholder besedilom)
        self.rate_entry = customtkinter.CTkEntry(
            podatki_frame,
            placeholder_text="Tvoja urna postavka")
        self.rate_entry.pack(pady=5, padx=20)

        # 3. Gumb RESET UR. POS.
        reset_btn = customtkinter.CTkButton(
            podatki_frame,
            text="Reset ur. postavke",
            command=self.ponastavi_postavko,
        )
        reset_btn.pack(pady=5, padx=20)

        # 4. Gumb POBRIŠI PODATKE (rdeč, ker je nevarno dejanje)
        izbrisi_btn = customtkinter.CTkButton(
            podatki_frame,
            text="Pobriši podatke",
            fg_color="red",
            hover_color="#E06666",
            command=self.izbrisi_vse_transakcije  # To funkcijo še dodaš spodaj
        )
        izbrisi_btn.pack(pady=(5, 15), padx=20)
        p_title = customtkinter.CTkLabel(
            self.premium_frame,
            text="Aplikacija Premium",
            font=("Arial", 14, "bold"),
            text_color="#ffd700")

        p_title.pack(pady=(10, 0))
        p_desc = customtkinter.CTkLabel(
            self.premium_frame,
            text="Odkleni napedne grafikone in različne teme.",

            font=("Arial", 12))
        p_desc.pack(pady=5)
        p_btn = customtkinter.CTkButton(
            self.premium_frame,
            text="Nadgradi zdaj ✨",
            fg_color="#ffd700",
            text_color="black",
            hover_color="#ccac00",
            font=("Arial", 12, "bold"),
            command=self.buy_premium  # Dodal sem funkcijo za klik
        )
        p_btn.pack(pady=10, padx=10)
        self.teme()

    def buy_premium(self):
        self.premium_window = customtkinter.CTkToplevel(self)
        self.premium_window.title('Premium')
        self.premium_window.geometry("550x650")
        self.premium_window.attributes("-topmost", True)  # NASLOV
        naslov_okna = customtkinter.CTkLabel(
            self.premium_window,
            text='PREMIUM:',
            font=("Arial", 22, "bold"),
            text_color="#ffd700"
        )
        naslov_okna.pack(pady=(20, 10))
        # BESEDILO - Dodan wraplength za samodejno prilagajanje oknu
        besedilo = (
            "POZDRAVLJENI!\n\n"
            "Upam, da se vaša pot začne tukaj v premium opciji, ki omogoča:\n"
            " • različne teme\n"
            " • različne grafikone\n"
            " • pogovor z AI glede varčevanja\n"
            " • in še veliko več...\n\n"
            "Za uporabo teh opcij se morate strinjati z uporabniškimi pravicami na spodnji povezavi."
        )
        vsebina_okna = customtkinter.CTkLabel(
            self.premium_window,
            text=besedilo,
            font=("Arial", 16),
            justify="left",
            wraplength=480  # To bo prelomilo besedilo, da ne gre izven okna (550px - padding)
        )
        vsebina_okna.pack(padx=30, pady=10)
        # POVEZAVA (LINK)
        link_label = customtkinter.CTkLabel(
            self.premium_window,
            text="Klikni tukaj za navodila in pravice (Google)",
            text_color="#1f538d",
            font=("Arial", 13, "underline"),
            cursor="hand2"
        )
        link_label.pack(pady=10)
        # Povežemo na novo funkcijo, ki odpira Google
        link_label.bind("<Button-1>", lambda e: self.open_google())
        # CHECKBOX
        self.check_var = customtkinter.StringVar(value="off")
        checkbox = customtkinter.CTkCheckBox(
            self.premium_window,
            text="Strinjam se s pogoji",
            command=self.checkbox_event,
            variable=self.check_var,
            onvalue="on",
            offvalue="off"
        )
        checkbox.pack(pady=20, padx=50, anchor="w")
        # GUMB SPODAJ
        btn_container = customtkinter.CTkFrame(self.premium_window, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom", padx=20, pady=20)
        customtkinter.CTkButton(
            btn_container,
            text="Potrdi Premium",
            fg_color="#73b6f2",
            text_color="black",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.premium_window.destroy  # Zapre okno po potrditvi
        ).pack(side="right")

        # DODAJ TO METODO V SVOJ RAZRED SettingsFrame

    @staticmethod
    def open_google():
        webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def checkbox_event(self):
        novo_stanje = self.check_var.get()
        try:
            with get_db_connection() as povezava:
                vnos = povezava.cursor()
                vnos.execute('UPDATE settings SET value = ? WHERE key = "premium"', (novo_stanje,))
                povezava.commit()
            print(f'Premium status posodobljen: {novo_stanje}')
        except Exception as e:
            print(f'Napaka pri posodabljanju baze: {e}')

    def posodobi_postavko(self):
        nova_vrednost = self.rate_entry.get().replace(',','.')
        if nova_vrednost:
            try:
                znesek = float(nova_vrednost)
                with get_db_connection() as conn:
                    cursor = conn.cursor()  # Posodobimo vrednost, kjer je ključ 'hourly_rate'
                    cursor.execute("UPDATE settings SET value = ? WHERE key = 'hourly_rate'", (znesek,))
                    conn.commit()
                self.rate_entry.delete(0, 'end')
                print(f"Urna postavka posodobljena na: {znesek} €")
            except ValueError:
                print("Napaka: Vnesi veljavno številko")

    @staticmethod
    def ponastavi_postavko():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE settings SET value = ? WHERE key = 'hourly_rate'", (7.73,))
            conn.commit()
        print("Postavka ponastavljena na 7.73")

    def izbrisi_vse_transakcije(self):
        """Pobriše vse podatke, a najprej zahteva potrditev uporabnika."""
        potrditev = customtkinter.CTkToplevel(self)
        potrditev.title("Potrditev brisanja")
        potrditev.geometry("400x200")
        potrditev.attributes("-topmost", True)
        potrditev.grab_set()  # Modalno okno - uporabnik ne more klikati zunaj

        # Centriranje
        sirina = self.winfo_screenwidth()
        visina = self.winfo_screenheight()
        x = (sirina // 2) - 200
        y = (visina // 2) - 100
        potrditev.geometry(f"400x200+{x}+{y}")

        customtkinter.CTkLabel(
            potrditev,
            text="Ali res želiš izbrisati VSE podatke?",
            font=("Arial", 14, "bold"),
            text_color="#e74c3c"
        ).pack(pady=(30, 10))

        customtkinter.CTkLabel(
            potrditev,
            text="Transakcije, dogodki in nastavitve bodo\nizgubljeni. Tega ni mogoče razveljaviti!",
            font=("Arial", 12),
            justify="center"
        ).pack(pady=(0, 20))

        def potrdi_in_izbrisi():
            try:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM transakcije")
                    cursor.execute("DELETE FROM dogodki")
                    cursor.execute("UPDATE settings SET value = ? WHERE key = 'hourly_rate'", (7.73,))
                    cursor.execute("UPDATE settings SET value = ? WHERE key = 'premium'", ("off",))
                    conn.commit()
                print("Vsi podatki o delu so izbrisani.")
            except Exception as e:
                print(f"Napaka pri brisanju: {e}")
            potrditev.destroy()

        btn_frame = customtkinter.CTkFrame(potrditev, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        customtkinter.CTkButton(
            btn_frame, text="Prekliči", fg_color="gray",
            command=potrditev.destroy
        ).pack(side="left", expand=True, padx=5)

        customtkinter.CTkButton(
            btn_frame, text="Izbriši vse", fg_color="#e74c3c", hover_color="#9c3025",
            command=potrdi_in_izbrisi
        ).pack(side="left", expand=True, padx=5)

    def teme(self):
        try:
            with get_db_connection() as povezava:
                vnos = povezava.cursor()
                vnos.execute("SELECT value FROM settings WHERE key = 'premium' LIMIT 1")
                rezultat = vnos.fetchone()

            premium_val = str(rezultat[0]) if rezultat else "0"

            # Preverimo, če je uporabnik premium
            if premium_val.lower() in ['on', '1', 'true']:
                # 1. NAJPREJ ustvarimo glavni okvir za teme
                glavni_okvir_tem = customtkinter.CTkFrame(self, border_width=1)
                glavni_okvir_tem.pack(fill="x", padx=20, pady=10)

                # 2. Naslov
                title = customtkinter.CTkLabel(
                    glavni_okvir_tem,
                    text="Premium Teme ✨",
                    font=("Arial", 14, "bold"),
                    text_color="#ffd700")
                title.pack(pady=(10, 5))

                subtitle = customtkinter.CTkLabel(
                    glavni_okvir_tem,
                    text="*Sprememba bo vidna ob naslednjem zagonu",
                    font=("Arial", 10, "italic"))
                subtitle.pack(pady=(0, 10))

                # 3. Okvir, kjer bodo krogci (vrstica)
                okvir_krogcev = customtkinter.CTkFrame(glavni_okvir_tem, fg_color="transparent")
                okvir_krogcev.pack(pady=10)

                # 4. Dinamično iskanje datotek v mapi assets/teme
                # Uporabimo relativno pot, da deluje povsod
                base_path = os.path.dirname(os.path.abspath(__file__))
                pot_do_tem = os.path.join(base_path, "..", "assets", "teme")

                # Mapiranje barv za krogce (da vemo, katero barvo dati gumbu)
                barve_mapa = {
                    "modra": "#3b8ed0",
                    "temno_modra": "#1f538d",
                    "zelena": "#2fa572"
                }

                if os.path.exists(pot_do_tem):
                    for datoteka in os.listdir(pot_do_tem):
                        if datoteka.endswith(".json"):
                            # Ugotovimo barvo krogca glede na ime datoteke
                            kljuc = datoteka.replace(".json", "").replace("_teme", "")
                            barva_gumba = barve_mapa.get(kljuc, "#73b6f2")  # privzeta modra, če ne najde

                            # Ustvarimo krogec (gumb)
                            gumb = customtkinter.CTkButton(
                                okvir_krogcev,
                                text="",
                                width=30,
                                height=30,
                                corner_radius=15,  # To naredi krog
                                fg_color=barva_gumba,
                                hover_color=barva_gumba,
                                command=lambda d=datoteka: self.nastavi_temo(d)
                            )
                            gumb.pack(side="left", padx=10, pady=5)
                else:
                    print(f"Mapa s temami ne obstaja na: {pot_do_tem}")

        except Exception as e:
            print(f'Napaka pri nalaganju tem: {e}')

    def nastavi_temo(self, ime_datoteke):
        try:
            pot_do_teme = os.path.join('assets', 'teme', ime_datoteke)
            with get_db_connection() as povezava:
                vnos = povezava.cursor()
                # V bazo shraniš pot do JSON datoteke, da jo main.py ob zagonu prebere
                vnos.execute('UPDATE settings SET value = ? WHERE key = "theme_path"', (pot_do_teme,))
                povezava.commit()
            print(f"Tema nastavljena na: {ime_datoteke}")
        except Exception as e:
            print(f"Napaka pri shranjevanju teme: {e}")
