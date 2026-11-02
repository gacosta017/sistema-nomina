from decimal import Decimal

from nomina.dinero import a_decimal, redondear


def test_a_decimal_no_arrastra_error_binario():
    assert a_decimal(0.1) == Decimal("0.1")


def test_a_decimal_conserva_un_decimal():
    valor = Decimal("5.5")
    assert a_decimal(valor) is valor


def test_redondear_usa_mitad_hacia_arriba():
    assert redondear(Decimal("2.675")) == Decimal("2.68")