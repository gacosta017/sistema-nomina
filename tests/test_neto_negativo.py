from decimal import Decimal

import pytest

from nomina.conceptos import ConceptoFijo, ConceptoPorcentual, deducciones_obligatorias
from nomina.empleados import EmpleadoTemporal
from nomina.excepciones import NetoNegativoError

D = Decimal


def test_neto_negativo_lanza_excepcion():
    deducciones = deducciones_obligatorias() + [ConceptoFijo("Préstamo", 2_000_000)]
    empleado = EmpleadoTemporal("Carlos", 1_500_000, 6, deducciones=deducciones)
    with pytest.raises(NetoNegativoError):
        empleado.calcular_nomina()


def test_se_pueden_agregar_deducciones_sin_modificar_la_clase():
    deducciones = deducciones_obligatorias() + [ConceptoPorcentual("Sindicato", 0.01)]
    r = EmpleadoTemporal("Carlos", 1_000_000, 6, deducciones=deducciones).calcular_nomina()
    assert r.deducciones["Sindicato"] == D("10000.00")