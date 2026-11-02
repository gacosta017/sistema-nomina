"""Presentación del desprendible de nómina (separada del cálculo: SRP)."""
from decimal import Decimal

from nomina.resultado import ResultadoNomina


def formato_cop(valor: Decimal) -> str:
    """Formatea un valor como pesos colombianos: $1.234.567,50"""
    texto = f"{valor:,.2f}"  # 1,234,567.50
    return "$" + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatear_desprendible(r: ResultadoNomina) -> str:
    lineas = [
        f"=== {r.nombre} ({r.tipo}) ===",
        f"  Devengado:          {formato_cop(r.devengado)}",
        f"  Bonos:              {formato_cop(r.bonos)}",
        f"  Salario bruto:      {formato_cop(r.salario_bruto)}",
    ]
    for nombre, valor in r.deducciones.items():
        lineas.append(f"  (-) {nombre}: {formato_cop(valor)}")
    lineas.append(f"  SALARIO NETO:       {formato_cop(r.salario_neto)}")
    for nombre, valor in r.beneficios.items():
        lineas.append(f"  (+) Beneficio empresa - {nombre}: {formato_cop(valor)}")
    return "\n".join(lineas)