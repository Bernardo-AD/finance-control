import pytest
from src.transaction import Transaction

def test_add_receita():
    t = Transaction()
    t.add("Salário", 3000, "receita")
    assert len(t.list_all()) == 1

def test_balance_positivo():
    t = Transaction()
    t.add("Salário", 3000, "receita")
    t.add("Aluguel", 1000, "despesa")
    assert t.get_balance() == 2000

def test_tipo_invalido():
    t = Transaction()
    with pytest.raises(ValueError):
        t.add("Erro", 100, "invalido")