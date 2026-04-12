class Transaction:  # classe para gerenciar as transações
    def __init__(self):
        self._transactions = []

        def add(self, description, amount, type): #Função responsavel por adicionar uma transação
            if type not in ["receita", "despesa"]:
                raise ValueError("Tipo deve ser 'receita' ou 'despesa'") #Validação para garantir que o tipo seja válido
            self._transactions.append({
                "description": description,
                "amount": amount,
                "type": type
            })

    def get_balance(self): #Função para calcular o saldo atual com base nas transações registradas
        balance = 0
        for t in self._transactions:
            if t["type"] == "receita":
                balance += t["amount"]
            else:
                balance -= t["amount"]
        return balance
    
    def list_all(self): #Função para listar todas as transações registradas
        return self._transactions