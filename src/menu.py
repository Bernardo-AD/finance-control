from src.month import Month
from src.card import Card
from src.report import generate_report, generate_comparison
from src import storage

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Digite um número válido!")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Digite um número inteiro válido!")

def setup_month(all_months):
    print("\n========================================")
    print("  💰 Finance Control")
    print("========================================")
    name = input("\nQual o mês de referência? (ex: Abril/2026): ")

    if name in all_months:
        print(f"✅ Mês '{name}' carregado!")
        return storage.dict_to_month(all_months[name])

    income = get_float("💰 Qual o salário desse mês? R$")
    limit_input = input("⚠️  Deseja definir um limite de gastos? (s/n): ").lower()
    month = Month(name)
    month.set_income(income)
    if limit_input == "s":
        limit = get_float("Limite de gastos: R$")
        month.set_limit(limit)
    print(f"\n✅ Mês '{name}' criado!")
    return month

def menu_subscriptions(month):
    while True:
        print("\n--- 📱 Mensalidades ---")
        print("1. Adicionar mensalidade")
        print("2. Remover mensalidade")
        print("3. Ver mensalidades")
        print("0. Voltar")
        op = input("Opção: ")

        if op == "1":
            desc = input("Descrição (ex: Gympass): ")
            amount = get_float("Valor mensal: R$")
            month.add_subscription(desc, amount)
            print(f"✅ Mensalidade '{desc}' adicionada!")

        elif op == "2":
            if not month.subscriptions:
                print("❌ Nenhuma mensalidade cadastrada!")
                continue
            for i, s in enumerate(month.subscriptions):
                print(f"{i+1}. {s['description']}: R${s['amount']:.2f}")
            idx = get_int("Número para remover: ") - 1
            if 0 <= idx < len(month.subscriptions):
                removed = month.subscriptions.pop(idx)
                print(f"✅ '{removed['description']}' removida!")
            else:
                print("❌ Número inválido!")

        elif op == "3":
            if not month.subscriptions:
                print("Nenhuma mensalidade cadastrada.")
            else:
                for s in month.subscriptions:
                    print(f"  - {s['description']}: R${s['amount']:.2f}")
                print(f"  Total: R${month.get_total_subscriptions():.2f}")

        elif op == "0":
            break

def menu_reserves(month):
    while True:
        print("\n--- 🏦 Reservas ---")
        print("1. Adicionar reserva")
        print("2. Remover reserva")
        print("3. Ver reservas")
        print("0. Voltar")
        op = input("Opção: ")

        if op == "1":
            desc = input("Descrição (ex: Investimento): ")
            amount = get_float("Valor: R$")
            month.add_reserve(desc, amount)
            print(f"✅ Reserva '{desc}' adicionada!")

        elif op == "2":
            if not month.reserves:
                print("❌ Nenhuma reserva cadastrada!")
                continue
            for i, r in enumerate(month.reserves):
                print(f"{i+1}. {r['description']}: R${r['amount']:.2f}")
            idx = get_int("Número para remover: ") - 1
            if 0 <= idx < len(month.reserves):
                removed = month.reserves.pop(idx)
                print(f"✅ '{removed['description']}' removida!")
            else:
                print("❌ Número inválido!")

        elif op == "3":
            if not month.reserves:
                print("Nenhuma reserva cadastrada.")
            else:
                for r in month.reserves:
                    print(f"  - {r['description']}: R${r['amount']:.2f}")
                print(f"  Total: R${month.get_total_reserves():.2f}")

        elif op == "0":
            break

def menu_card_expenses(card):
    while True:
        print(f"\n--- 💳 {card.name} ---")
        print("1. Adicionar gasto")
        print("2. Editar gasto")
        print("3. Remover gasto")
        print("4. Ver gastos")
        print("0. Voltar")
        op = input("Opção: ")

        if op == "1":
            desc = input("Descrição: ")
            parcelado = input("É parcelado? (s/n): ").lower()
            if parcelado == "s":
                total = get_float("Valor total: R$")
                installments = get_int("Em quantas parcelas? ")
                current = get_int("Parcela atual: ")
                amount = round(total / installments, 2)
                card.add_expense(desc, amount, total=total, installments=installments, current=current)
            else:
                amount = get_float("Valor: R$")
                card.add_expense(desc, amount)
            print(f"✅ '{desc}' adicionado!")

        elif op == "2":
            expenses = card.list_expenses()
            if not expenses:
                print("❌ Nenhum gasto cadastrado!")
                continue
            for i, e in enumerate(expenses):
                print(f"{i+1}. {e['description']}: R${e['amount']:.2f}")
            idx = get_int("Número para editar: ") - 1
            if 0 <= idx < len(expenses):
                desc = input(f"Nova descrição ({expenses[idx]['description']}): ") or expenses[idx]['description']
                amount = get_float(f"Novo valor: R$")
                expenses[idx]['description'] = desc
                expenses[idx]['amount'] = amount
                print("✅ Gasto atualizado!")
            else:
                print("❌ Número inválido!")

        elif op == "3":
            expenses = card.list_expenses()
            if not expenses:
                print("❌ Nenhum gasto cadastrado!")
                continue
            for i, e in enumerate(expenses):
                print(f"{i+1}. {e['description']}: R${e['amount']:.2f}")
            idx = get_int("Número para remover: ") - 1
            if 0 <= idx < len(expenses):
                removed = expenses.pop(idx)
                print(f"✅ '{removed['description']}' removido!")
            else:
                print("❌ Número inválido!")

        elif op == "4":
            if not card.list_expenses():
                print("Nenhum gasto cadastrado.")
            else:
                for e in card.list_expenses():
                    if e["installments"]:
                        print(f"  - {e['description']} (R${e['total']:.2f} — {e['current']}/{e['installments']}): R${e['amount']:.2f}")
                    else:
                        print(f"  - {e['description']}: R${e['amount']:.2f}")
                print(f"  Total: R${card.get_total():.2f}")

        elif op == "0":
            break

def menu_cards(month):
    while True:
        print("\n--- 💳 Cartões ---")
        print("1. Adicionar cartão")
        print("2. Gerenciar gastos de um cartão")
        print("3. Remover cartão")
        print("4. Ver cartões")
        print("0. Voltar")
        op = input("Opção: ")

        if op == "1":
            name = input("Nome do cartão (ex: Nubank): ")
            card = Card(name)
            month.add_card(card)
            print(f"✅ Cartão '{name}' adicionado!")

        elif op == "2":
            if not month.cards:
                print("❌ Nenhum cartão cadastrado!")
                continue
            for i, c in enumerate(month.cards):
                print(f"{i+1}. {c.name} — R${c.get_total():.2f}")
            idx = get_int("Número do cartão: ") - 1
            if 0 <= idx < len(month.cards):
                menu_card_expenses(month.cards[idx])
            else:
                print("❌ Número inválido!")

        elif op == "3":
            if not month.cards:
                print("❌ Nenhum cartão cadastrado!")
                continue
            for i, c in enumerate(month.cards):
                print(f"{i+1}. {c.name}")
            idx = get_int("Número para remover: ") - 1
            if 0 <= idx < len(month.cards):
                removed = month.cards.pop(idx)
                print(f"✅ Cartão '{removed.name}' removido!")
            else:
                print("❌ Número inválido!")

        elif op == "4":
            if not month.cards:
                print("Nenhum cartão cadastrado.")
            else:
                for c in month.cards:
                    print(f"  - {c.name}: R${c.get_total():.2f}")

        elif op == "0":
            break

def menu_comparison(all_months, current_month):
    months_list = list(all_months.keys())
    if len(months_list) < 2:
        print("\n❌ Você precisa ter pelo menos 2 meses salvos para comparar!")
        return

    print("\n--- 📊 Comparativo ---")
    print("Meses disponíveis:")
    for i, m in enumerate(months_list):
        print(f"{i+1}. {m}")

    idx = get_int("Escolha o mês para comparar com o atual: ") - 1
    if 0 <= idx < len(months_list):
        other = storage.dict_to_month(all_months[months_list[idx]])
        generate_comparison(other, current_month)
    else:
        print("❌ Número inválido!")

def run():
    all_months = storage.load()
    month = setup_month(all_months)

    while True:
        alert = month.check_limit()
        print(f"\n{'='*40}")
        print(f"  📅 {month.name}")
        print(f"  💰 Entrada:    R${month.income:.2f}")
        print(f"  🏦 Reservas:   R${month.get_total_reserves():.2f}")
        print(f"  📱 Mensalidds: R${month.get_total_subscriptions():.2f}")
        print(f"  💳 Gastos:     R${month.get_total_expenses():.2f}")
        print(f"  📊 Saldo:      R${month.get_balance():.2f}")
        if alert:
            status, percent, diff = alert
            if status == "danger":
                print(f"  ❌ LIMITE ULTRAPASSADO em R${diff:.2f}!")
            elif status == "warning":
                print(f"  ⚠️  {percent:.1f}% do limite usado!")
        print(f"{'='*40}")
        print("\n1. Gerenciar reservas")
        print("2. Gerenciar mensalidades")
        print("3. Gerenciar cartões")
        print("4. Ver relatório completo")
        print("5. Comparar com outro mês")
        print("6. Salvar e sair")
        print("0. Sair sem salvar")

        op = input("\nOpção: ")

        if op == "1":
            menu_reserves(month)
        elif op == "2":
            menu_subscriptions(month)
        elif op == "3":
            menu_cards(month)
        elif op == "4":
            generate_report(month)
        elif op == "5":
            menu_comparison(all_months, month)
        elif op == "6":
            all_months[month.name] = storage.month_to_dict(month)
            storage.save(all_months)
            print("\n✅ Dados salvos! Até logo! 👋")
            break
        elif op == "0":
            print("\n👋 Saindo sem salvar!")
            break
        else:
            print("❌ Opção inválida!")