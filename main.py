from src.transaction import Transaction
from src.report import generate_report

# Criando o sistema
t = Transaction()

# Adicionando transações
t.add("Salário", 3000, "receita")
t.add("Freelance", 1500, "receita")
t.add("Aluguel", 1000, "despesa")
t.add("Supermercado", 500, "despesa")
t.add("Internet", 100, "despesa")

# Gerando relatório
generate_report(t)