"""Demostración del sistema de nómina."""
from nomina import (
    EmpleadoAsalariado,
    EmpleadoPorComision,
    EmpleadoPorHoras,
    EmpleadoTemporal,
    ServicioNomina,
)
from nomina.reporte import formato_cop, formatear_desprendible


def main() -> None:
    empleados = [
        EmpleadoAsalariado("Ana Pérez", salario_mensual=5_000_000, anios_antiguedad=6),
        EmpleadoPorHoras(
            "Luis Gómez", tarifa_hora=10_000, horas_trabajadas=45,
            anios_antiguedad=2, acepta_fondo_ahorro=True,
        ),
        EmpleadoPorComision(
            "Marta Ruiz", salario_base=2_000_000, porcentaje_comision=0.05,
            ventas=25_000_000, anios_antiguedad=3,
        ),
        EmpleadoTemporal("Carlos Díaz", salario_mensual=1_500_000, meses_contrato=6),
    ]

    servicio = ServicioNomina()
    resultados = servicio.procesar(empleados)

    for resultado in resultados:
        print(formatear_desprendible(resultado))
        print()
    print(f"Total neto a pagar: {formato_cop(servicio.total_neto(resultados))}")


if __name__ == "__main__":
    main()