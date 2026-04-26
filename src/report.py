from src.month import Month

def generate_report(month: Month):
    print(f"\n{'='*40}")
    print(f"  📅 Controle Financeiro — {month.name}")
    print(f"{'='*40}")

    print(f"\n💰 Entrada: R${month.income:.2f}")

    if month.reserves:
        print(f"\n🏦 Reservas:")
        for r in month.reserves:
            print(f"   - {r['description']}: R${r['amount']:.2f}")
        print(f"   Total reservas: R${month.get_total_reserves():.2f}")

    if month.subscriptions:
        print(f"\n📱 Mensalidades:")
        for s in month.subscriptions:
            print(f"   - {s['description']}: R${s['amount']:.2f}")
        print(f"   Total mensalidades: R${month.get_total_subscriptions():.2f}")

    for card in month.cards:
        print(f"\n💳 {card.name}:")
        for e in card.list_expenses():
            if e["installments"]:
                print(f"   - {e['description']} (R${e['total']:.2f} — {e['current']}/{e['installments']}): R${e['amount']:.2f}")
            else:
                print(f"   - {e['description']}: R${e['amount']:.2f}")
        print(f"   Total {card.name}: R${card.get_total():.2f}")

    # Alertas
    alert = month.check_limit()
    if alert:
        status, percent, diff = alert
        print(f"\n{'='*40}")
        if status == "danger":
            print(f"  ❌ LIMITE ULTRAPASSADO em R${diff:.2f}!")
        elif status == "warning":
            print(f"  ⚠️  ATENÇÃO: {percent:.1f}% do limite usado!")
            print(f"  Restam R${diff:.2f} até o limite.")

    print(f"\n{'='*40}")
    print(f"  📊 Saldo final: R${month.get_balance():.2f}")
    print(f"{'='*40}\n")

def generate_comparison(month1: Month, month2: Month):
    print(f"\n{'='*40}")
    print(f"  📊 Comparativo: {month1.name} vs {month2.name}")
    print(f"{'='*40}")

    def diff(a, b):
        d = b - a
        sign = "+" if d > 0 else ""
        return f"{sign}R${d:.2f}"

    print(f"\n💰 Entrada:     R${month1.income:.2f} → R${month2.income:.2f} ({diff(month1.income, month2.income)})")
    print(f"🏦 Reservas:    R${month1.get_total_reserves():.2f} → R${month2.get_total_reserves():.2f} ({diff(month1.get_total_reserves(), month2.get_total_reserves())})")
    print(f"📱 Mensalidds:  R${month1.get_total_subscriptions():.2f} → R${month2.get_total_subscriptions():.2f} ({diff(month1.get_total_subscriptions(), month2.get_total_subscriptions())})")
    print(f"💳 Gastos:      R${month1.get_total_expenses():.2f} → R${month2.get_total_expenses():.2f} ({diff(month1.get_total_expenses(), month2.get_total_expenses())})")
    print(f"📊 Saldo:       R${month1.get_balance():.2f} → R${month2.get_balance():.2f} ({diff(month1.get_balance(), month2.get_balance())})")
    print(f"{'='*40}\n")