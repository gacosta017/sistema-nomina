"""Resultado inmutable del cálculo de nómina de un empleado."""
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class ResultadoNomina:
    nombre: str
    tipo: str
    devengado: Decimal          # salario base / horas / comisiones
    bonos: Decimal              # bonos que hacen parte del salario bruto
    salario_bruto: Decimal      # devengado + bonos
    deducciones: dict = field(default_factory=dict)   # nombre -> valor
    beneficios: dict = field(default_factory=dict)    # nombre -> valor (a cargo de la empresa)
    salario_neto: Decimal = Decimal("0")

    @property
    def total_deducciones(self) -> Decimal:
        return sum(self.deducciones.values(), Decimal("0"))

    @property
    def total_beneficios(self) -> Decimal:
        return sum(self.beneficios.values(), Decimal("0"))