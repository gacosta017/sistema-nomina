"""Jerarquía de empleados.

Patrón Template Method: ``Empleado.calcular_nomina`` define el algoritmo común
y cada subclase aporta solo lo que cambia (devengado, bonos y beneficios).
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional, Sequence

from nomina.conceptos import (
    Concepto,
    beneficio_bono_alimentacion,
    deducciones_obligatorias,
)
from nomina.dinero import a_decimal, redondear
from nomina.excepciones import NetoNegativoError, ValidacionError
from nomina.resultado import ResultadoNomina

# Reglas de negocio del enunciado.
ANIOS_PARA_BONO_ASALARIADO = 5
PORCENTAJE_BONO_ASALARIADO = Decimal("0.10")


def _validar_no_negativo(valor: Decimal, campo: str) -> Decimal:
    """Valida que un valor numérico no sea negativo y lo devuelve como Decimal."""
    valor = a_decimal(valor)
    if valor < 0:
        raise ValidacionError(f"{campo} no puede ser negativo(a): {valor}")
    return valor


class Empleado(ABC):
    """Clase base abstracta de todos los tipos de empleado."""

    def __init__(
        self,
        nombre: str,
        anios_antiguedad=0,
        deducciones: Optional[Sequence[Concepto]] = None,
    ):
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del empleado es obligatorio")
        self.nombre = nombre.strip()
        self.anios_antiguedad = _validar_no_negativo(anios_antiguedad, "Los años de antigüedad")
        # Inyección de dependencias: por defecto, las deducciones obligatorias.
        self._deducciones = (
            list(deducciones) if deducciones is not None else deducciones_obligatorias()
        )

    # --- Puntos de extensión para las subclases -----------------------------

    @property
    def tipo(self) -> str:
        return type(self).__name__

    @abstractmethod
    def calcular_devengado(self) -> Decimal:
        """Salario base devengado en el mes (sin bonos)."""

    def calcular_bonos(self) -> Decimal:
        """Bonos que se suman al salario bruto. Por defecto, ninguno."""
        return Decimal("0")

    def beneficios(self) -> list:
        """Beneficios adicionales a cargo de la empresa. Por defecto, ninguno."""
        return []

    # --- Algoritmo común -----------------------------------------------------

    def calcular_nomina(self) -> ResultadoNomina:
        devengado = redondear(self.calcular_devengado())
        bonos = redondear(self.calcular_bonos())
        bruto = devengado + bonos

        deducciones = {c.nombre: c.calcular(bruto) for c in self._deducciones}
        beneficios = {c.nombre: c.calcular(bruto) for c in self.beneficios()}
        neto = bruto - sum(deducciones.values(), Decimal("0"))

        if neto < 0:
            raise NetoNegativoError(
                f"El salario neto de {self.nombre} es negativo: {neto}"
            )

        return ResultadoNomina(
            nombre=self.nombre,
            tipo=self.tipo,
            devengado=devengado,
            bonos=bonos,
            salario_bruto=bruto,
            deducciones=deducciones,
            beneficios=beneficios,
            salario_neto=neto,
        )


class EmpleadoAsalariado(Empleado):
    """Salario fijo mensual; bono del 10 % con más de 5 años en la empresa."""

    def __init__(self, nombre: str, salario_mensual, anios_antiguedad=0, deducciones=None):
        super().__init__(nombre, anios_antiguedad, deducciones)
        self.salario_mensual = _validar_no_negativo(salario_mensual, "El salario mensual")

    def calcular_devengado(self) -> Decimal:
        return self.salario_mensual

    def calcular_bonos(self) -> Decimal:
        if self.anios_antiguedad > ANIOS_PARA_BONO_ASALARIADO:
            return self.salario_mensual * PORCENTAJE_BONO_ASALARIADO
        return Decimal("0")

    def beneficios(self) -> list:
        return [beneficio_bono_alimentacion()]  # empleado permanente