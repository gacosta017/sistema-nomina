from decimal import Decimal

from nomina.conceptos import (
    ConceptoFijo,
    ConceptoPorcentual,
    deducciones_obligatorias,
)

D = Decimal


def test_concepto_porcentual_calcula_sobre_el_bruto():
    assert ConceptoPorcentual("Prueba", 0.10).calcular(D("1000")) == D("100.00")


def test_concepto_fijo_ignora_el_salario():
    assert ConceptoFijo("Bono", 1_000_000).calcular(D("5")) == D("1000000.00")


def test_deducciones_obligatorias_son_pension_y_arl():
    valores = {
        d.nombre: d.calcular(D("1000000")) for d in deducciones_obligatorias()
    }
    assert valores == {
        "Seguro social y pensión": D("40000.00"),
        "ARL": D("5220.00"),
    }