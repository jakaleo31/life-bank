import customtkinter
import calendar
from datetime import datetime


# -------------------------
#   SHRANJEVANJE DOGODKOV (v RAM-u)
# -------------------------
events = {}   # primer: {"2025-03-26": ["Dogodek 1", "Dogodek 2"]}


# -------------------------
#   POPUP ZA DOGODKE
# -------------------------
class EventWindow(customtkinter.CTkToplevel):
    def __init__(self, master, date_str):
        super().__init__(master)
        self.title(f"Events for {date_str}")
        self.geometry("350x400")
        self.date_str = date_str

        customtkinter.CTkLabel(self, text=f"Events on {date_str}", font=("Arial", 18, "bold")).pack(pady=10)

        # List of events
        self.event_list = customtkinter.CTkTextbox(self, width=300, height=200)
        self.event_list.pack(pady=10)

        if date_str in events:
            for e in events[date_str]:
                self.event_list.insert("end", f"- {e}\n")

        # Input
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Add new event...")
        self.entry.pack(pady=10)

        # Button
        add_btn = customtkinter.CTkButton(self, text="Add Event", command=self.add_event)
        add_btn.pack(pady=5)

    def add_event(self):
        text = self.entry.get().strip()
        if not text:
            return

        if self.date_str not in events:
            events[self.date_str] = []

        events[self.date_str].append(text)

        self.event_list.insert("end", f"- {text}\n")
        self.entry.delete(0, "end")


# -------------------------
#   GOOGLE CALENDAR STYLE
# -------------------------
class GoogleCalendar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#1f1f1f")

        self.year = datetime.now().year
        self.month = datetime.now().month

        # Header
        header = customtkinter.CTkFrame(self, fg_color="transparent")
        header.pack(pady=10)

        customtkinter.CTkButton(header, text="<", width=40, command=self.prev_month).grid(row=0, column=0)
        self.month_label = customtkinter.CTkLabel(header, text="", font=("Arial", 22, "bold"))
        self.month_label.grid(row=0, column=1, padx=20)
        customtkinter.CTkButton(header, text=">", width=40, command=self.next_month).grid(row=0, column=2)

        # Calendar grid
        self.grid_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack()

        self.draw_calendar()

    # -------------------------
    #   DRAW CALENDAR
    # -------------------------
    def draw_calendar(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        self.month_label.configure(text=f"{calendar.month_name[self.month]} {self.year}")

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, d in enumerate(days):
            customtkinter.CTkLabel(self.grid_frame, text=d, font=("Arial", 14, "bold")).grid(row=0, column=i, padx=5, pady=5)

        month_days = calendar.monthcalendar(self.year, self.month)

        today = datetime.now().day
        is_current_month = (self.month == datetime.now().month and self.year == datetime.now().year)

        for r, week in enumerate(month_days, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    customtkinter.CTkLabel(self.grid_frame, text="").grid(row=r, column=c)
                else:
                    date_str = f"{self.year}-{self.month:02d}-{day:02d}"

                    # highlight today
                    if is_current_month and day == today:
                        color = "#5ed77a"
                    else:
                        color = "#ffffff"

                    # mark days with events
                    if date_str in events:
                        color = "#73b6f2"

                    btn = customtkinter.CTkButton(
                        self.grid_frame,
                        text=str(day),
                        width=60,
                        height=40,
                        fg_color="transparent",
                        hover_color="#333333",
                        text_color=color,
                        command=lambda d=date_str: self.open_event_window(d)
                    )
                    btn.grid(row=r, column=c, padx=3, pady=3)

    # -------------------------
    #   EVENT POPUP
    # -------------------------
    def open_event_window(self, date_str):
        EventWindow(self, date_str)

    # -------------------------
    #   MONTH SWITCHING
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
#   TEST APP
# -------------------------
if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("600x600")

    cal = GoogleCalendar(app)
    cal.pack(pady=20)

    app.mainloop()

