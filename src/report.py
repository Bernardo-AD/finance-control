from src.transaction import Transaction

def generate_report(transaction: Transaction):
    print("==== RELATÓRIO FINANCEIRO ====")

    total_receitas = 0
    total_despesas = 0

    for t in transaction.list_all():
        if t["type"] == "receita":
            total_receitas += t["amount"]
            print(f"+ {t['description']}: R${t['amount']:.2f}")
        else:
            total_despesas += t["amount"]
            print(f"- {t['description']}: R${t['amount']:.2f}")

    print ("--------------------------")
    print(f"Total de receitas: R${total_receitas:.2f}")
    print(f"Total de despesas: R${total_despesas:.2f}")
    print(f"Saldo final: R${transaction.get_balance():.2f}")