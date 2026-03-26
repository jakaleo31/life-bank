import customtkinter
import calendar
from datetime import datetime


class CalendarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#1f1f1f", **kwargs)

        # Trenutni mesec in leto
        self.year = datetime.now().year
        self.month = datetime.now().month

        # Header (mesec + gumbi)
        self.header = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header.pack(pady=10)

        self.prev_btn = customtkinter.CTkButton(
            self.header, text="<", width=40, command=self.prev_month
        )
        self.prev_btn.grid(row=0, column=0, padx=5)

        self.month_label = customtkinter.CTkLabel(
            self.header, text="", font=("Arial", 20, "bold")
        )
        self.month_label.grid(row=0, column=1, padx=10)

        self.next_btn = customtkinter.CTkButton(
            self.header, text=">", width=40, command=self.next_month
        )
        self.next_btn.grid(row=0, column=2, padx=5)

        # Frame za dneve
        self.days_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.days_frame.pack()

        self.draw_calendar()

    # -------------------------
    #   IZRIŠI KOLEDAR
    # -------------------------
    def draw_calendar(self):
        # Počisti star koledar
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        # Posodobi naslov
        self.month_label.configure(text=f"{calendar.month_name[self.month]} {self.year}")

        # Imena dni
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            lbl = customtkinter.CTkLabel(
                self.days_frame, text=day, font=("Arial", 14, "bold")
            )
            lbl.grid(row=0, column=i, padx=5, pady=5)

        # Koledar meseca
        month_days = calendar.monthcalendar(self.year, self.month)

        today = datetime.now().day
        current_month = (self.month == datetime.now().month and self.year == datetime.now().year)

        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0:
                    # prazno polje
                    lbl = customtkinter.CTkLabel(self.days_frame, text="")
                    lbl.grid(row=row, column=col, padx=5, pady=5)
                else:
                    # označi današnji dan
                    if current_month and day == today:
                        fg = "#5ed77a"
                    else:
                        fg = "#ffffff"

                    btn = customtkinter.CTkButton(
                        self.days_frame,
                        text=str(day),
                        width=40,
                        fg_color="transparent",
                        hover_color="#333333",
                        text_color=fg
                    )
                    btn.grid(row=row, column=col, padx=5, pady=5)

    # -------------------------
    #   PREJŠNJI / NASLEDNJI MESEC
    # -------------------------
    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.draw_calendar()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.draw_calendar()


# -------------------------
#   TEST OKNO
# -------------------------
if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("400x400")

    calendar_widget = CalendarFrame(app)
    calendar_widget.pack(pady=20)

    app.mainloop()
