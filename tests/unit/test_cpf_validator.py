import pytest
from pycpfcnpj import cpfcnpj


@pytest.mark.parametrize("cpf", ["11144477735", "98765432100"])
def test_validate_valid_cpf(cpf):
    """Testa se cpfcnpj.validate retorna True para CPFs válidos."""
    assert cpfcnpj.validate(cpf) is True


@pytest.mark.parametrize("cpf", ["11144477700", "12345678901"])
def test_validate_invalid_cpf(cpf):
    """Testa se cpfcnpj.validate retorna False para CPFs inválidos."""
    assert cpfcnpj.validate(cpf) is False


def test_validate_formatted_cpf():
    """Testa CPFs válidos formatados corretamente."""
    assert cpfcnpj.validate("111.444.777-35") is True
    assert cpfcnpj.validate("987.654.321-00") is True


@pytest.mark.parametrize("cpf", ["11111111111", "22222222222", "99999999999"])
def test_validate_repeated_digits_cpf(cpf):
    """Testa CPFs de dígitos repetidos (todos inválidos)."""
    assert cpfcnpj.validate(cpf) is False


def test_validate_short_cpf():
    """Testa CPFs curtos demais."""
    assert cpfcnpj.validate("1234567890") is False


def test_validate_long_cpf():
    """Testa CPFs longos demais."""
    assert cpfcnpj.validate("123456789012") is False


def test_validate_non_numeric_cpf():
    """Testa CPFs com caracteres não numéricos."""
    assert cpfcnpj.validate("abcdefghijk") is False
