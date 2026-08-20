# 💰 Life & Money Manager

A desktop application in Python that combines a personal calendar, a financial overview, and statistics into a single clean interface. Built with **CustomTkinter** (modern dark/light GUI), and stores data in **[...]**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f538d)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## ✨ Features

The application is divided into **four main tabs**, accessible via the bottom taskbar:

### 💵 Money
- **Track incomes and expenses** – add, edit and delete transactions with custom descriptions and dates.
- **Balance graph** – a running chart of current balance (premium version extends the Y-axis downward).
- **Transaction list** – clicking a row opens editing.
- **Three calculators** in the same window:
  - 🛒 *How much do I need to work?* – tells you how many work hours are needed for a given purchase.
  - 🏦 *Loan calculator* – monthly installment using an annuity formula.
  - 🐷 *Savings goal* – how many work hours left to reach a set goal.
- **AI integration** (premium) – shortcut to ChatGPT for saving advice.

### 📅 Life
- **Monthly calendar** in the style of Google Calendar (Slovenian weekdays).
- Create, edit and delete **events** with title, time, multi-day range, color and description.
- Multiple events on the same day are **automatically stacked** vertically.
- Quick add by clicking any day.

### 📊 Stats
- **🔥 Streak** – shows whether you were active today (transaction or event).
- **🥧 Pie chart** – current month’s spending broken down by descriptions (Top 5 categories).
- **Progress bar** to the savings goal with percentage progress.

### ⚙️ Settings
- Change the **hourly rate** (in €) that the app uses in all calculators.
- **Reset hourly rate** to the default value (7.73 €).
- **Delete all data** – transactions, events, settings (with a safety confirmation).
- **Premium upgrade** – unlock different color themes (blue, dark blue, green) and AI integration.
- **Choose themes** (theme circles in settings) – change is applied on next app start.

### 🔔 Notifications
- On application start you get a system notification (`plyer`).
- The `checker.py` file enables occasional checking – it notifies you about today’s events and if daily spending is exceeded (default €50).

---

## 📸 Screen layout

```
┌─────────────────────────────────────────────────┐
│                                                 │
│           ( Active tab )                        │
│                                                 │
├─────────────────────────────────────────────────┤
│  📊 Stats │  💵 Money/Life │  ⚙️ Settings      │
└─────────────────────────────────────────────────┘
```

The center button toggles between **Money** (blue) and **Life** (green) — hence the app name.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<user>/life-money-manager.git
cd life-money-manager/app
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

---

## 📦 Packaging to .exe (Windows)

A **PyInstaller** specification (`main.spec`) is already included in the project:

```bash
pyinstaller main.spec
```

The built application will be in the `dist/main/` folder.

> Icons and themes are included in the build automatically via `datas=[('assets', 'assets')]`.

---

## 📂 Project structure

```
app/
├── main.py                # Main App class + taskbar
├── checker.py             # Script for OS-level notifications
├── requirements.txt
├── main.spec              # PyInstaller configuration
│
├── ui/                    # Graphical interface (CustomTkinter)
│   ├── money_tab.py       #   – Money tab (chart, calculators, transactions)
│   ├── life_tab.py        #   – Life tab (calendar, events)
│   ├── settings_tab.py    #   – Settings tab (rate, premium, themes)
│   └── stats_tab.py       #   – Stats tab (pie, progress, streak)
│
├── logika/                # Business logic
│   ├── database.py        #   – SQLite connection + schema (context manager)
│   └── finance.py         #   – calculators (work, loan, savings)
│
├── database/
│   └── manager.db         # SQLite database (created on first run)
│
└── assets/
    ├── icons/             # PNG icons for the taskbar
    │   ├── money_icon.png
    │   ├── life_icon.png
    │   ├── stats.png
    │   └── settings.png
    └── themes/            # Premium color themes (JSON for CustomTkinter)
        ├── modra.json
        ├── temno_modra.json
        └── zelena.json
```

---

## 🗄️ Data model

The SQLite database (`database/manager.db`) has three tables:

| Table         | Fields                                                                                 |
|---------------|----------------------------------------------------------------------------------------|
| `settings`    | `key` (PK), `value` — stores `hourly_rate`, `premium`, `theme_path`, `savings_goal`    |
| `transakcije` | `id`, `tip`, `znesek`, `datum`, `opis`, `kategorija`                                   |
| `dogodki`     | `id`, `naslov`, `datum_zacetek`, `datum_konec`, `ura_od`, `ura_do`, `barva`, `opis`    |

(Notes: the table and column names are shown as they are in the project; translations of the column names are: `transakcije` = transactions (`tip`=type, `znesek`=amount, `datum`=date, `opis`=description, `kategorija`=category), `dogodki` = events (`naslov`=title, `datum_zacetek`=start_date, `datum_konec`=end_date, `ura_od`=time_from, `ura_do`=time_to, `barva`=color, `opis`=description).)

Default settings are inserted on first run (`hourly_rate=7.73`, `savings_goal=1000`, `premium=off`).

---

## 🛠️ Technologies

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** – modern Material-style design for tkinter.
- **[Pillow](https://python-pillow.org/)** – loading PNG icons.
- **[Matplotlib](https://matplotlib.org/)** – balance line chart and spending pie chart.
- **[plyer](https://plyer.readthedocs.io/)** – native system notifications (Windows, Linux, macOS).
- **SQLite3** – built into Python, no separate server required.

---

## 📝 Notes

- **Premium** in this school project is just a demo toggle — a checkbox in settings that stores `on`/`off` in the database. No real paid flow is implemented.
- The link in the Premium window (*"Click here for instructions and rights"*) is a joke (Rickroll) and serves only as a demonstration of a link.
- Changing the **theme** in settings requires **restarting** the application.
- The `checker.py` file is a standalone script — suitable for `cron` (Linux/macOS) or Task Scheduler (Windows).

---

## 📜 License

This project is intended for educational use. Use, copy and modify are permitted under the **MIT** license.

---

Author: **Jaka Selak** · School year 2024/25 · Project for the course **OSPR**
