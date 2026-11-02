from decimal import Decimal

import pytest

from nomina.empleados import EmpleadoTemporal
from nomina.excepciones import ValidacionError

D = Decimal


def test_salario_fijo_sin_bonos_ni_beneficios():
    r = EmpleadoTemporal("Carlos", 1_500_000, meses_contrato=6).calcular_nomina()
    assert r.bonos == D("0")
    assert r.beneficios == {}
    assert r.salario_neto == D("1432170.00")


def test_contrato_debe_tener_duracion_positiva():
    with pytest.raises(ValidacionError):
        EmpleadoTemporal("Carlos", 1_500_000, meses_contrato=0)