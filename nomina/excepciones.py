"""Excepciones propias del dominio de nómina."""


class NominaError(Exception):
    """Error base del sistema de nómina."""


class ValidacionError(NominaError):
    """Un dato de entrada viola una regla de negocio (horas, ventas, etc.)."""


class NetoNegativoError(NominaError):
    """El salario neto calculado resultó negativo."""