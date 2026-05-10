def calculate_work_hours(price, hourly_rate):
    """Izračuna koliko ur moraš delati za določen predmet."""
    if hourly_rate <= 0: return 0
    return round(price / hourly_rate, 1)


def can_afford_credit(monthly_income, monthly_expenses, installment):
    """Preveri, če uporabniku po plačilu obroka ostane vsaj 20% dohodka."""
    disposable_income = monthly_income - monthly_expenses
    return disposable_income > installment * 1.2


def get_hourly_rate():
    """Funkcija, ki jo kličeš v MoneyFrame za izračun."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'hourly_rate'")
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        return 7.73  # Če baze ni, vrne privzeto
    except Exception as e:
        print(f"Napaka pri branju baze: {e}")
        return 0.0


def savings_plan(goal_amount, current_savings):
    """Izračuna koliko UR dela potrebuješ za dosego cilja."""
    # 1. Preberemo urno postavko iz SQL
    moja_urna_postavka = get_hourly_rate()
    # 2. Izračunamo, koliko denarja še manjka
    remaining_money = goal_amount - current_savings
    # 3. Varnostni preverjanje: če je cilj že dosežen
    if remaining_money <= 0:
        return 0
    # 4. Varnostni preverjanje: če je urna postavka 0, ne moremo deliti
    if moja_urna_postavka <= 0:
        return float('inf')
    # 5. Izračun: Manjkajoči denar / zaslužek na uro = potrebne ure
    return round(remaining_money / moja_urna_postavka, 1)
