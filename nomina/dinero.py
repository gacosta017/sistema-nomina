"""Utilidades para manejar valores monetarios con Decimal (evita errores de float)."""
from decimal import ROUND_HALF_UP, Decimal

CENTAVOS = Decimal("0.01")


def a_decimal(valor) -> Decimal:
    """Convierte int, float, str o Decimal a Decimal sin arrastrar error binario."""
    if isinstance(valor, Decimal):
        return valor
    return Decimal(str(valor))


def redondear(valor: Decimal) -> Decimal:
    """Redondea a 2 decimales (mitad hacia arriba)."""
    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)