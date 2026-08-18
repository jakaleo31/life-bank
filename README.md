# 💰 Life & Money Manager

Namizna aplikacija v Pythonu, ki združuje osebni koledar, finančni pregled in statistiko v en sam pregleden vmesnik. Zgrajena je s **CustomTkinter** (moderen temni/svetli GUI), podatke pa hrani v **SQLite** bazi.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1f538d)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## ✨ Funkcionalnosti

Aplikacija je razdeljena na **štiri glavne zavihke**, do katerih dostopaš preko spodnje opravilne vrstice (taskbar):

### 💵 Money
- **Vodenje prihodkov in odhodkov** – vnos, urejanje in brisanje transakcij s poljubnimi opisi in datumi.
- **Graf stanja** – tekoči graf trenutnega stanja (premium različica razširi os Y navzdol).
- **Seznam transakcij** – klik na vrstico odpre urejanje.
- **Trije kalkulatorji** v istem oknu:
  - 🛒 *Koliko moram delati?* – pove, koliko ur dela potrebuješ za določen nakup.
  - 🏦 *Kreditni kalkulator* – mesečni obrok po anuitetni formuli.
  - 🐷 *Varčevalni cilj* – koliko ur dela še potrebuješ do zastavljenega cilja.
- **AI povezava** (premium) – bližnjica do ChatGPT za nasvete o varčevanju.

### 📅 Life
- **Mesečni koledar** v stilu Google Calendar (slovenski dnevi).
- Ustvarjanje, urejanje in brisanje **dogodkov** z naslovom, časom, večdnevnim razponom, barvo in opisom.
- Več dogodkov na isti dan se **avtomatsko zloži** po višini.
- Hitro dodajanje s klikom na poljuben dan.

### 📊 Stats
- **🔥 Ogenj** (streak) – prikaže, ali si bil danes aktiven (transakcija ali dogodek).
- **🥧 Pie chart** – poraba tekočega meseca razdeljena po opisih (Top 5 kategorij).
- **Progress bar** do varčevalnega cilja s procentom napredka.

### ⚙️ Nastavitve
- Spreminjanje **urne postavke** (v €), ki jo aplikacija uporabi v vseh kalkulatorjih.
- **Reset urne postavke** na privzeto vrednost (7,73 €).
- **Pobriši vse podatke** – transakcije, dogodki, nastavitve (z varnostno potrditvijo).
- **Premium nadgradnja** – odkleni različne barvne teme (modra, temno modra, zelena) in AI povezavo.
- **Izbira tem** (krogi v nastavitvah) – sprememba je vidna ob naslednjem zagonu.

### 🔔 Obvestila
- Ob zagonu aplikacije te pozdravi sistemsko obvestilo (`plyer`).
- Datoteka `checker.py` omogoča občasno preverjanje – opozori te na današnje dogodke in prekoračitev dnevne porabe (privzeto 50 €).

---

## 📸 Zgradba zaslona

```
┌─────────────────────────────────────────────────┐
│                                                 │
│           ( Aktiven zavihek )                   │
│                                                 │
├─────────────────────────────────────────────────┤
│  📊 Stats │  💵 Money/Life │  ⚙️ Nastavitve    │
└─────────────────────────────────────────────────┘
```

Sredinski gumb preklaplja med **Money** (modra) in **Life** (zelena) — od tod ime aplikacije.

---

## 🚀 Namestitev

### 1. Kloniraj repozitorij

```bash
git clone https://github.com/<uporabnik>/life-money-manager.git
cd life-money-manager/app
```

### 2. (Priporočeno) Ustvari virtualno okolje

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Namesti odvisnosti

```bash
pip install -r requirements.txt
```

### 4. Poženi aplikacijo

```bash
python main.py
```

---

## 📦 Pakiranje v .exe (Windows)

V projektu je že pripravljena **PyInstaller** specifikacija (`main.spec`):

```bash
pyinstaller main.spec
```

Izpilana aplikacija bo v mapi `dist/main/`.

> Ikone in teme se preko `datas=[('assets', 'assets')]` vključijo v build samodejno.

---

## 📂 Struktura projekta

```
app/
├── main.py                # Glavni razred App + taskbar
├── checker.py             # Skripta za obvestila na OS nivoju
├── requirements.txt
├── main.spec              # PyInstaller konfiguracija
│
├── ui/                    # Grafični vmesnik (CustomTkinter)
│   ├── money_tab.py       #   – zavihek Money (graf, kalkulatorji, transakcije)
│   ├── life_tab.py        #   – zavihek Life (koledar, dogodki)
│   ├── settings_tab.py    #   – zavihek Nastavitve (postavka, premium, teme)
│   └── stats_tab.py       #   – zavihek Stats (pie, progress, ogenj)
│
├── logika/                # Poslovna logika
│   ├── database.py        #   – SQLite povezava + shema (context manager)
│   └── finance.py         #   – kalkulatorji (delo, kredit, varčevanje)
│
├── database/
│   └── manager.db         # SQLite baza (ustvarjena ob prvem zagonu)
│
└── assets/
    ├── icons/             # PNG ikone za taskbar
    │   ├── money_icon.png
    │   ├── life_icon.png
    │   ├── stats.png
    │   └── settings.png
    └── teme/              # Premium barvne teme (JSON za CustomTkinter)
        ├── modra.json
        ├── temno_modra.json
        └── zelena.json
```

---

## 🗄️ Podatkovni model

SQLite baza (`database/manager.db`) ima tri tabele:

| Tabela        | Polja                                                                              |
|---------------|------------------------------------------------------------------------------------|
| `settings`    | `key` (PK), `value` — hrani `hourly_rate`, `premium`, `theme_path`, `savings_goal` |
| `transakcije` | `id`, `tip`, `znesek`, `datum`, `opis`, `kategorija`                              |
| `dogodki`     | `id`, `naslov`, `datum_zacetek`, `datum_konec`, `ura_od`, `ura_do`, `barva`, `opis` |

Privzete vrednosti nastavitev se vstavijo ob prvem zagonu (`hourly_rate=7.73`, `savings_goal=1000`, `premium=off`).

---

## 🛠️ Tehnologije

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** – moderen Material dizajn za tkinter.
- **[Pillow](https://python-pillow.org/)** – nalaganje PNG ikon.
- **[Matplotlib](https://matplotlib.org/)** – linijski graf stanja in pie chart porabe.
- **[plyer](https://plyer.readthedocs.io/)** – izvorna sistemska obvestila (Windows, Linux, macOS).
- **SQLite3** – vgrajena v Python, brez dodatnega strežnika.

---

## 📝 Opombe

- **Premium** je v tej šolski izvedbi zgolj demo preklopnik — checkbox v nastavitvah v bazo shrani `on`/`off`. Pravi plačljivi tok ni implementiran.
- Link v Premium oknu (*"Klikni tukaj za navodila in pravice"*) je šaljiv (Rickroll) in služi le kot demonstracija povezave.
- Sprememba **teme** iz nastavitev zahteva **vnovični zagon** aplikacije.
- Datoteka `checker.py` je samostojna skripta — primerna je za `cron` (Linux/macOS) ali Task Scheduler (Windows).

---

## 📜 Licenca

Projekt je namenjen izobraževanju. Uporaba, kopiranje in spreminjanje je dovoljeno v skladu z licenco **MIT**.

---

Avtor: **Jaka Selak** · Šolsko leto 2024/25 · Projekt pri predmetu **OSPR**
