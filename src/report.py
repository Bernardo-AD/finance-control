from src.month import Month

def generate_report(month: Month):
    print(f"\n{'='*40}")
    print(f"   Controle Financeiro — {month.name}")
    print(f"{'='*40}")

    print(f"\n Entrada: R${month.income:.2f}")

    print(f"\n Reservas:")
    for r in month.reserves:
        print(f"   - {r['description']}: R${r['amount']:.2f}")
    print(f"   Total reservas: R${month.get_total_reserves():.2f}")

    for card in month.cards:
        print(f"\n {card.name}:")
        for e in card.list_expenses():
            if e["installments"]:
                print(f"   - {e['description']} (R${e['total']:.2f} — {e['current']}/{e['installments']}): R${e['amount']:.2f}")
            else:
                print(f"   - {e['description']}: R${e['amount']:.2f}")
        print(f"   Total {card.name}: R${card.get_total():.2f}")

    print(f"\n{'='*40}")
    print(f"   Saldo final: R${month.get_balance():.2f}")
    print(f"{'='*40}\n")