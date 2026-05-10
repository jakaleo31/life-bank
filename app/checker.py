import sqlite3
import datetime
import os
from plyer import notification

# Pot do tvoje baze (prilagodi, če je drugje)
DB_PATH = os.path.join("database", "manager.db")


def check_and_notify():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        danes = datetime.datetime.now().strftime("%Y-%m-%d")

        # --- 1. PREVERJANJE KOLEDARJA ---
        cursor.execute("SELECT naslov FROM dogodki WHERE datum_zacetek = ?", (danes,))
        dogodki = cursor.fetchall()
        for dogodek in dogodki:
            notification.notify(
                title="Opomnik za dogodek",
                message=f"Danes imaš: {dogodek[0]}",
                app_name="Life & Money Manager",
                timeout=10
            )

        # --- 2. PREVERJANJE FINANC (Primer: če si zapravil preveč) ---
        cursor.execute("SELECT SUM(abs(znesek)) FROM transakcije WHERE tip='odhodek' AND datum = ?", (danes,))
        poraba_danes = cursor.fetchone()[0] or 0

        if poraba_danes > 50:  # Recimo, da je 50€ tvoj limit
            notification.notify(
                title="Finance Opozorilo!",
                message=f"Danes si zapravil že {poraba_danes:.2f}€. Premisli o naslednjem nakupu!",
                app_name="Life & Money Manager",
                timeout=10
            )

        conn.close()
    except Exception as e:
        print(f"Napaka v checkerju: {e}")


if __name__ == "__main__":
    check_and_notify()