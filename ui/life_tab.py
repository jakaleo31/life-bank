import customtkinter
import calendar
from datetime import datetime, timedelta


class LifeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        self.year = datetime.now().year
        self.month = datetime.now().month
        self.izbrana_barva = "#039be5"

        self.slo_months = ["Januar", "Februar", "Marec", "April", "Maj", "Junij", "Julij", "Avgust", "September",
                           "Oktober", "November", "December"]

        self.header = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=10)

        self.prev_btn = customtkinter.CTkButton(self.header, text="<", width=30, fg_color=('#8c8c8c', '#4c4c4c'),
                                                command=self.prev_month)
        self.prev_btn.pack(side="left", padx=5)

        self.month_label = customtkinter.CTkLabel(self.header, text="",
                                                  font=customtkinter.CTkFont(size=22, weight="bold"))
        self.month_label.pack(side="left", padx=10)

        self.next_btn = customtkinter.CTkButton(self.header, text=">", width=30, fg_color=('#8c8c8c', '#4c4c4c'),
                                                command=self.next_month)
        self.next_btn.pack(side="left", padx=5)

        self.calendar_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.calendar_container.pack(fill="both", expand=True)
        # Tam, kjer definiraš mrežo za celotno aplikacijo
        self.grid_rowconfigure(0, weight=1)  # Vrstica, kjer je vsebina
        self.grid_columnconfigure(0, weight=1)

        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.calendar_container.winfo_children():
            widget.destroy()

        self.month_label.configure(text=f"{self.slo_months[self.month - 1]} {self.year}")

        for i in range(7):
            self.calendar_container.grid_columnconfigure(i, weight=1, uniform="equal_cols")
        for j in range(1, 7):
            self.calendar_container.grid_rowconfigure(j, weight=1, uniform="equal_rows")

        days = ["PONEDELJEK", "TOREK", "SREDA", "ČETRTEK", "PETEK", "SOBOTA", "NEDELJA"]
        for i, day in enumerate(days):
            lbl = customtkinter.CTkLabel(self.calendar_container, text=day, font=("Arial", 11, "bold"),
                                         text_color="gray")
            lbl.grid(row=0, column=i, sticky="nsew", pady=(0, 10))

        cal = calendar.monthcalendar(self.year, self.month)
        coords = {}
        danes = datetime.now()
        je_trenutni_mesec = (self.year == danes.year and self.month == danes.month)

        # 1. DEL: Izris praznih dni
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    coords[day] = (r + 1, c)
                    day_box = customtkinter.CTkFrame(self.calendar_container, fg_color=('#8c8c8c', '#4d4d4d'),
                                                     corner_radius=8, border_width=1,
                                                     border_color=("#dbdbdb", "#333333"))
                    day_box.grid(row=r + 1, column=c, padx=4, pady=4, sticky="nsew")

                    if je_trenutni_mesec and day == danes.day:
                        lbl = customtkinter.CTkLabel(day_box, text=str(day), font=("Arial", 12, "bold"),
                                                     text_color="white", fg_color="#039be5", corner_radius=12,
                                                     width=26, height=26)
                    else:
                        lbl = customtkinter.CTkLabel(day_box, text=str(day), font=("Arial", 12, "bold"))

                    lbl.pack(anchor="nw", padx=10, pady=10)
                    day_box.bind("<Button-1>", lambda k, d=day: self.odpri_urejanje_dogodka(d))

        # 2. DEL: Izris dogodkov z avtomatskim zlaganjem
        try:
            from logika.database import get_db_connection
            with get_db_connection() as conn:
                cursor = conn.cursor()
                zadnji_dan = calendar.monthrange(self.year, self.month)[1]
                start_str = f"{self.year}-{self.month:02d}-01"
                end_str = f"{self.year}-{self.month:02d}-{zadnji_dan}"
                cursor.execute(
                    "SELECT * FROM dogodki WHERE datum_zacetek <= ? AND datum_konec >= ?",
                    (end_str, start_str))
                vsi_dogodki = cursor.fetchall()

            uporabljena_visina = {}  # Ključ bo "vrstica-dan"

            for dog in vsi_dogodki:
                zac_dan = int(dog[2].split("-")[2])
                kon_dan = int(dog[3].split("-")[2])
                trenutni_dan = zac_dan

                while trenutni_dan <= kon_dan:
                    if trenutni_dan in coords:
                        r_koledar, c_koledar = coords[trenutni_dan]
                        span = min(kon_dan - trenutni_dan + 1, 7 - c_koledar)

                        # Iskanje najvišjega prostega nivoja v tem razponu
                        nivo = 0
                        for d_check in range(c_koledar, c_koledar + span):
                            kljuc = f"{r_koledar}-{d_check}"
                            nivo = max(nivo, uporabljena_visina.get(kljuc, 0))

                        # Zamik: 45px pod številko dneva + nivo * višina gumba (30px)
                        y_offset = 45 + (nivo * 30)

                        btn = customtkinter.CTkButton(
                            self.calendar_container,
                            text=f"{dog[1]}" if trenutni_dan == zac_dan or c_koledar == 0 else "",
                            fg_color=dog[6],
                            height=24,
                            corner_radius=4,
                            font=("Arial", 10, "bold"),
                            anchor="w",
                            command=lambda d=dog: self.odpri_urejanje_dogodka(None, d)
                        )
                        btn.grid(row=r_koledar, column=c_koledar, columnspan=span,
                                 padx=6, pady=(y_offset, 0), sticky="new")

                        # Označimo zasedenost za vse stolpce pod tem dogodkom
                        for d_check in range(c_koledar, c_koledar + span):
                            uporabljena_visina[f"{r_koledar}-{d_check}"] = nivo + 1

                        trenutni_dan += span
                    else:
                        trenutni_dan += 1
        except Exception as e:
            print(f"Napaka: {e}")

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.draw_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.draw_calendar()

    def odpri_urejanje_dogodka(self, dan, obstojec_dogodek=None):

        izbran_datum = obstojec_dogodek[2] if obstojec_dogodek else f"{self.year}-{self.month:02d}-{dan:02d}"

        edit_window = customtkinter.CTkToplevel(self)
        edit_window.title("Urejanje" if obstojec_dogodek else "Dodajanje")
        edit_window.geometry("550x650")
        edit_window.attributes("-topmost", True)

        naslov_entry = customtkinter.CTkEntry(edit_window, placeholder_text="Dodajanje naslova", font=("Arial", 22),
                                              fg_color="transparent", border_width=0)
        naslov_entry.pack(fill="x", pady=(20, 0), padx=20)
        if obstojec_dogodek: naslov_entry.insert(0, obstojec_dogodek[1])
        customtkinter.CTkFrame(edit_window, height=2, fg_color="#73b6f2").pack(fill="x", padx=20, pady=(5, 15))
        time_frame = customtkinter.CTkFrame(edit_window, fg_color="transparent")
        time_frame.pack(fill="x", padx=20, pady=10)

        predlogi = [f"{h:02d}:00" for h in range(7, 23)]
        ura_od = customtkinter.CTkComboBox(time_frame, values=predlogi, width=110)
        ura_od.pack(side="left", padx=5)
        ura_do = customtkinter.CTkComboBox(time_frame, values=predlogi, width=110)
        ura_do.pack(side="left", padx=5)

        def toggle_all_day():
            if ves_dan_var.get():
                ura_od.set("00:00")
                ura_do.set("23:59")
                ura_od.configure(state="disabled")  # Da uporabnik ne spreminja ročno
                ura_do.configure(state="disabled")
            else:
                ura_od.configure(state="normal")
                ura_do.configure(state="normal")

            # In v CTkCheckBox dodaj:

        ves_dan_var = customtkinter.BooleanVar(value=True)
        customtkinter.CTkCheckBox(edit_window, text="Ves dan", variable=ves_dan_var, command=toggle_all_day).pack(
            pady=10, padx=20, anchor="w")
        toggle_all_day()

        if obstojec_dogodek:
            ura_od.set(obstojec_dogodek[4])
            ura_do.set(obstojec_dogodek[5])
        else:
            start = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            end = start + timedelta(minutes=45)
            ura_od.set(start.strftime("%H:%M"))
            ura_do.set(end.strftime("%H:%M"))

        date_frame = customtkinter.CTkFrame(edit_window, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=10)
        start_ent = customtkinter.CTkEntry(date_frame, width=140)
        start_ent.insert(0, izbran_datum)
        start_ent.pack(side="left", padx=5)
        end_ent = customtkinter.CTkEntry(date_frame, width=140)
        end_ent.insert(0, obstojec_dogodek[3] if obstojec_dogodek else izbran_datum)
        end_ent.pack(side="left", padx=5)

        customtkinter.CTkLabel(edit_window, text="Izberi barvo:").pack(anchor="w", padx=20)
        colors_frame = customtkinter.CTkFrame(edit_window, fg_color="transparent")
        colors_frame.pack(fill="x", padx=20, pady=5)
        barve = ["#d50000", "#e67c73", "#f4511e", "#f6bf26", "#33b679", "#0b8043", "#039be5", "#3f51b5", "#7986cb",
                 "#8e24aa"]
        self.izbrana_barva = obstojec_dogodek[6] if obstojec_dogodek else barve[6]

        color_preview = customtkinter.CTkFrame(edit_window, height=4, width=100, fg_color=self.izbrana_barva)

        for b in barve:
            btn = customtkinter.CTkButton(colors_frame, text="", fg_color=b, width=28, height=28, corner_radius=14,
                                          command=lambda col=b: self.posodobi_barvo(col, color_preview))
            btn.pack(side="left", padx=2)

        color_preview.pack(fill="x", padx=20, pady=5)

        opis_text = customtkinter.CTkTextbox(edit_window, height=150)
        opis_text.pack(fill="both", pady=10, padx=20)
        if obstojec_dogodek: opis_text.insert("0.0", obstojec_dogodek[7])

        def shrani():
            try:
                from logika.database import get_db_connection
                with get_db_connection() as conn:
                    cur = conn.cursor()
                    vals = (naslov_entry.get(), start_ent.get(), end_ent.get(), ura_od.get(), ura_do.get(),
                            self.izbrana_barva, opis_text.get("0.0", "end").strip())
                    if obstojec_dogodek:
                        cur.execute(
                            "UPDATE dogodki SET naslov=?, datum_zacetek=?, datum_konec=?, ura_od=?, ura_do=?, barva=?, opis=? WHERE id=?",
                            (*vals, obstojec_dogodek[0]))
                    else:
                        cur.execute(
                            "INSERT INTO dogodki (naslov, datum_zacetek, datum_konec, ura_od, ura_do, barva, opis) VALUES (?,?,?,?,?,?,?)",
                            vals)
                    conn.commit()
            except Exception as e:
                print(f"Napaka pri shranjevanju: {e}")
            edit_window.destroy()
            self.draw_calendar()

        btn_container = customtkinter.CTkFrame(edit_window, fg_color="transparent")
        btn_container.pack(fill="x", side="bottom", padx=20, pady=20)

        if obstojec_dogodek:
            def izbrisi():
                from logika.database import get_db_connection
                with get_db_connection() as conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM dogodki WHERE id=?", (obstojec_dogodek[0],))
                    conn.commit()
                edit_window.destroy()
                self.draw_calendar()

            customtkinter.CTkButton(btn_container, text="Izbriši", fg_color="#d50000", command=izbrisi).pack(
                side="left")

        customtkinter.CTkButton(btn_container, text="Shrani dogodek", fg_color="#73b6f2", text_color="black",
                                font=("Arial", 14, "bold"), height=40, command=shrani).pack(side="right")

    def posodobi_barvo(self, col, preview_widget):
        self.izbrana_barva = col
        preview_widget.configure(fg_color=col)
