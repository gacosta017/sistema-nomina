from decimal import Decimal

from nomina import (
    EmpleadoAsalariado,
    EmpleadoPorHoras,
    EmpleadoTemporal,
    ServicioNomina,
)
from nomina.reporte import formato_cop, formatear_desprendible

D = Decimal


def test_procesa_varios_tipos_de_empleado_polimorficamente():
    empleados = [
        EmpleadoAsalariado("Ana", 5_000_000, 6),
        EmpleadoPorHoras("Luis", 10_000, 45),
        EmpleadoTemporal("Carlos", 1_500_000, 6),
    ]
    resultados = ServicioNomina().procesar(empleados)
    assert [r.nombre for r in resultados] == ["Ana", "Luis", "Carlos"]


def test_total_neto_suma_los_netos():
    empleados = [
        EmpleadoAsalariado("Ana", 5_000_000, 6),
        EmpleadoTemporal("Carlos", 1_500_000, 6),
    ]
    servicio = ServicioNomina()
    resultados = servicio.procesar(empleados)
    assert servicio.total_neto(resultados) == D("6683460.00")


def test_formato_cop():
    assert formato_cop(D("1234567.50")) == "$1.234.567,50"


def test_desprendible_incluye_nombre_y_neto():
    r = EmpleadoAsalariado("Ana", 5_000_000, 6).calcular_nomina()
    texto = formatear_desprendible(r)
    assert "Ana" in texto
    assert "$5.251.290,00" in texto