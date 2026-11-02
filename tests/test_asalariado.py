from decimal import Decimal

import pytest

from nomina.empleados import EmpleadoAsalariado
from nomina.excepciones import ValidacionError

D = Decimal


def test_con_mas_de_5_anios_recibe_bono_del_10_por_ciento():
    r = EmpleadoAsalariado("Ana", 5_000_000, anios_antiguedad=6).calcular_nomina()
    assert r.bonos == D("500000.00")
    assert r.salario_bruto == D("5500000.00")


def test_con_exactamente_5_anios_no_recibe_bono():
    r = EmpleadoAsalariado("Ana", 5_000_000, anios_antiguedad=5).calcular_nomina()
    assert r.bonos == D("0")


def test_deducciones_pension_y_arl_y_neto():
    r = EmpleadoAsalariado("Ana", 5_000_000, anios_antiguedad=6).calcular_nomina()
    assert r.deducciones["Seguro social y pensión"] == D("220000.00")
    assert r.deducciones["ARL"] == D("28710.00")
    assert r.salario_neto == D("5251290.00")


def test_recibe_bono_de_alimentacion():
    r = EmpleadoAsalariado("Ana", 3_000_000).calcular_nomina()
    assert r.beneficios["Bono de alimentación"] == D("1000000.00")


def test_salario_negativo_es_invalido():
    with pytest.raises(ValidacionError):
        EmpleadoAsalariado("Ana", -1)


def test_nombre_vacio_es_invalido():
    with pytest.raises(ValidacionError):
        EmpleadoAsalariado("   ", 1_000_000)