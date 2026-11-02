"""Servicio de aplicación: procesa la nómina de un conjunto de empleados."""
from decimal import Decimal
from typing import Iterable, List

from nomina.empleados import Empleado
from nomina.resultado import ResultadoNomina


class ServicioNomina:
    """Orquesta el cálculo; depende de la abstracción ``Empleado`` (DIP)."""

    def procesar(self, empleados: Iterable[Empleado]) -> List[ResultadoNomina]:
        return [empleado.calcular_nomina() for empleado in empleados]

    @staticmethod
    def total_neto(resultados: Iterable[ResultadoNomina]) -> Decimal:
        return sum((r.salario_neto for r in resultados), Decimal("0"))