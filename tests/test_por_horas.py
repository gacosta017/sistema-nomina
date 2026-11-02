from decimal import Decimal

import pytest

from nomina.empleados import EmpleadoPorHoras
from nomina.excepciones import ValidacionError

D = Decimal


def test_sin_horas_extras():
    r = EmpleadoPorHoras("Luis", 10_000, 30).calcular_nomina()
    assert r.devengado == D("300000.00")


def test_horas_extras_se_pagan_a_1_5():
    # 40 * 10.000 + 5 * 15.000 = 475.000
    r = EmpleadoPorHoras("Luis", 10_000, 45).calcular_nomina()
    assert r.devengado == D("475000.00")
    assert r.salario_neto == D("453520.50")


def test_exactamente_40_horas_no_hay_extras():
    r = EmpleadoPorHoras("Luis", 10_000, 40).calcular_nomina()
    assert r.devengado == D("400000.00")


def test_no_recibe_bonos():
    r = EmpleadoPorHoras("Luis", 10_000, 50).calcular_nomina()
    assert r.bonos == D("0")


def test_horas_negativas_son_invalidas():
    with pytest.raises(ValidacionError):
        EmpleadoPorHoras("Luis", 10_000, -1)


def test_fondo_de_ahorro_con_mas_de_1_anio_y_aceptando():
    r = EmpleadoPorHoras(
        "Luis", 10_000, 45, anios_antiguedad=2, acepta_fondo_ahorro=True
    ).calcular_nomina()
    assert r.beneficios["Fondo de ahorro"] == D("9500.00")


def test_sin_fondo_si_no_acepta():
    r = EmpleadoPorHoras(
        "Luis", 10_000, 45, anios_antiguedad=2, acepta_fondo_ahorro=False
    ).calcular_nomina()
    assert r.beneficios == {}


def test_sin_fondo_con_1_anio_o_menos():
    r = EmpleadoPorHoras(
        "Luis", 10_000, 45, anios_antiguedad=1, acepta_fondo_ahorro=True
    ).calcular_nomina()
    assert r.beneficios == {}


def test_no_recibe_bono_de_alimentacion():
    r = EmpleadoPorHoras("Luis", 10_000, 45, anios_antiguedad=3).calcular_nomina()
    assert "Bono de alimentación" not in r.beneficios