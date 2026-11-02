"""Conceptos de nómina: deducciones y beneficios.

Un *concepto* es cualquier valor que se calcula a partir del salario bruto.
Las deducciones y los beneficios comparten esta abstracción (DRY), y se pueden
agregar nuevos conceptos sin modificar las clases de empleado (Open/Closed).
"""
from abc import ABC, abstractmethod
from decimal import Decimal

from nomina.dinero import a_decimal, redondear

# Valores de las reglas de negocio (un solo lugar para cambiarlos).
PORCENTAJE_PENSION = Decimal("0.04")
# Tasa ARL riesgo I (0,522 %). El enunciado no da el valor: es un supuesto.
TASA_ARL = Decimal("0.00522")
VALOR_BONO_ALIMENTACION = Decimal("1000000")
PORCENTAJE_FONDO_AHORRO = Decimal("0.02")


class Concepto(ABC):
    """Contrato común de un concepto de nómina (deducción o beneficio)."""

    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def calcular(self, salario_bruto: Decimal) -> Decimal:
        """Devuelve el valor del concepto para un salario bruto dado."""


class ConceptoPorcentual(Concepto):
    """Concepto que es un porcentaje del salario bruto."""

    def __init__(self, nombre: str, porcentaje):
        super().__init__(nombre)
        self.porcentaje = a_decimal(porcentaje)

    def calcular(self, salario_bruto: Decimal) -> Decimal:
        return redondear(salario_bruto * self.porcentaje)


class ConceptoFijo(Concepto):
    """Concepto de valor fijo, independiente del salario."""

    def __init__(self, nombre: str, valor):
        super().__init__(nombre)
        self.valor = redondear(a_decimal(valor))

    def calcular(self, salario_bruto: Decimal) -> Decimal:
        return self.valor


# --- Fábricas de los conceptos definidos en el enunciado -------------------

def deduccion_pension() -> Concepto:
    return ConceptoPorcentual("Seguro social y pensión", PORCENTAJE_PENSION)


def deduccion_arl() -> Concepto:
    return ConceptoPorcentual("ARL", TASA_ARL)


def beneficio_bono_alimentacion() -> Concepto:
    return ConceptoFijo("Bono de alimentación", VALOR_BONO_ALIMENTACION)


def beneficio_fondo_ahorro() -> Concepto:
    return ConceptoPorcentual("Fondo de ahorro", PORCENTAJE_FONDO_AHORRO)


def deducciones_obligatorias() -> list:
    """Deducciones que aplican a todos los empleados."""
    return [deduccion_pension(), deduccion_arl()]