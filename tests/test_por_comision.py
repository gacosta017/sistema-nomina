from decimal import Decimal

import pytest

from nomina.empleados import EmpleadoPorComision
from nomina.excepciones import ValidacionError

D = Decimal


def test_ventas_bajo_el_umbral_solo_comision():
    r = EmpleadoPorComision("Marta", 2_000_000, 0.05, 10_000_000).calcular_nomina()
    assert r.devengado == D("2500000.00")
    assert r.bonos == D("0")


def test_ventas_exactamente_20_millones_no_reciben_bono():
    r = EmpleadoPorComision("Marta", 2_000_000, 0.05, 20_000_000).calcular_nomina()
    assert r.bonos == D("0")


def test_ventas_sobre_el_umbral_reciben_bono_3_por_ciento():
    r = EmpleadoPorComision("Marta", 2_000_000, 0.05, 25_000_000).calcular_nomina()
    assert r.devengado == D("3250000.00")
    assert r.bonos == D("750000.00")
    assert r.salario_bruto == D("4000000.00")


def test_recibe_bono_de_alimentacion():
    r = EmpleadoPorComision("Marta", 2_000_000, 0.05, 0).calcular_nomina()
    assert r.beneficios["Bono de alimentación"] == D("1000000.00")


def test_ventas_negativas_son_invalidas():
    with pytest.raises(ValidacionError):
        EmpleadoPorComision("Marta", 2_000_000, 0.05, -1)