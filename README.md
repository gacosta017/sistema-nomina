# Sistema de Nómina (POO) — Actividad Unidad Tres

Sistema de nómina en **Python** con programación orientada a objetos para una empresa con cuatro tipos de empleado (asalariado, por horas, por comisión y temporal), cada uno con su propia forma de calcular salario, beneficios y deducciones.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python main.py          # demostración con los 4 tipos de empleado
python -m pytest -v     # pruebas unitarias
```

## Estructura

```
nomina/
  conceptos.py     # Concepto (abstracto), ConceptoPorcentual, ConceptoFijo y fábricas de las reglas
  empleados.py     # Empleado (abstracto) + 4 tipos concretos
  resultado.py     # ResultadoNomina (dataclass inmutable)
  servicio.py      # ServicioNomina: procesa una lista de empleados
  reporte.py       # Formato del desprendible (separado del cálculo)
  dinero.py        # Decimal y redondeo
  excepciones.py   # ValidacionError, NetoNegativoError
tests/test_empleados.py
main.py
```

## Reglas de negocio y dónde se implementan

| Regla | Clase / método |
|---|---|
| Asalariado: bono 10 % si > 5 años | `EmpleadoAsalariado.calcular_bonos` |
| Por horas: extras > 40 h a 1,5 x; sin bonos | `EmpleadoPorHoras.calcular_devengado` |
| Comisión: base + % ventas; bono 3 % si ventas > $20.000.000 | `EmpleadoPorComision` |
| Temporal: fijo, sin bonos ni beneficios | `EmpleadoTemporal` |
| Pensión 4 % y ARL | `deducciones_obligatorias()` |
| Bono alimentación $1.000.000 (Asalariado, Comisión) | `beneficios()` de cada clase |
| Fondo de ahorro 2 % (por horas > 1 año y acepta) | `EmpleadoPorHoras.beneficios` |
| Validaciones (neto, horas, ventas) | `ValidacionError`, `NetoNegativoError` |

## Supuestos (confirmar con el docente)

1. **ARL**: el enunciado no da el porcentaje. Se usa 0,522 % (riesgo I) en `TASA_ARL`, fácil de cambiar.
2. **Salario bruto** = devengado + bonos. Las deducciones (4 % y ARL) se calculan sobre el bruto.
3. **Beneficios** (bono de alimentación, fondo de ahorro) son a cargo de la empresa: se muestran en el desprendible pero **no** cambian el neto del empleado.
4. "Más de 5 años" y "más de 1 año" son estrictos (5 años exactos no recibe el bono).
5. "Ventas superan $20.000.000" es estricto (exactamente 20 M no recibe bono).
6. El bono de 3 % se **suma** a la comisión normal.

## Principios SOLID aplicados

- **S — Responsabilidad única:** cada módulo hace una cosa: calcular (`empleados`), representar el resultado (`resultado`), orquestar (`servicio`), presentar (`reporte`).
- **O — Abierto/Cerrado:** para un nuevo tipo de empleado se crea una subclase; para una nueva deducción o beneficio, un nuevo `Concepto`. No se modifica código existente.
- **L — Sustitución de Liskov:** cualquier subclase de `Empleado` funciona donde se espera un `Empleado` (`ServicioNomina.procesar` los trata igual).
- **I — Segregación de interfaces:** `Concepto` tiene un único método (`calcular`); las subclases solo sobrescriben `calcular_bonos` o `beneficios` si lo necesitan.
- **D — Inversión de dependencias:** `ServicioNomina` depende de la abstracción `Empleado`, y los empleados reciben sus deducciones por inyección (parámetro `deducciones`).

Otros patrones y buenas prácticas: **Template Method** (`calcular_nomina`), **Decimal** para dinero, constantes con nombre en lugar de números mágicos, excepciones propias, docstrings y nombres expresivos.

## Metodología de desarrollo

Se trabajó con un enfoque **iterativo e incremental con TDD ligero** (Kanban personal):

1. **Análisis:** lectura del enunciado y listado de reglas de negocio y supuestos.
2. **Diseño:** clase base abstracta + subclases; conceptos de deducción/beneficio como objetos.
3. **Iteraciones cortas:** un tipo de empleado por iteración → pruebas → commit.
4. **Refactorización:** eliminar duplicación (ej. validaciones y conceptos porcentuales) tras tener las pruebas en verde.
5. **Control de versiones:** GitHub con ramas `main` y `develop`, y *commits* siguiendo *Conventional Commits*.

## Plan de commits sugerido (evidencia de control de versiones)

```bash
git init && git branch -M main
git add .gitignore requirements.txt README.md && git commit -m "chore: estructura inicial del proyecto"
git checkout -b develop
git add nomina/excepciones.py nomina/dinero.py nomina/conceptos.py && git commit -m "feat: conceptos de deducciones y beneficios"
git add nomina/resultado.py nomina/empleados.py nomina/__init__.py && git commit -m "feat: jerarquía de empleados y cálculo de nómina"
git add nomina/servicio.py nomina/reporte.py main.py && git commit -m "feat: servicio de nómina, reporte y demo"
git add tests && git commit -m "test: pruebas unitarias de reglas y validaciones"
git checkout main && git merge develop && git remote add origin <URL_DE_TU_REPO> && git push -u origin main develop
```

Idealmente haz los commits a medida que avanzas (y no todos el mismo día) para que el historial sea creíble.

## Guion sugerido para el video de YouTube (5–8 min)

1. **Presentación (30 s):** nombre, asignatura y qué problema resuelve el sistema.
2. **Reglas de negocio (1 min):** los 4 tipos de empleado y las deducciones.
3. **Diseño (2 min):** mostrar `Empleado` abstracta, las subclases y `Concepto`; explicar Template Method y SOLID con ejemplos del código.
4. **Demostración (1–2 min):** ejecutar `python main.py` y explicar un desprendible.
5. **Pruebas (1 min):** ejecutar `pytest -v` y mostrar casos borde (5 años exactos, 20 M exactos, neto negativo).
6. **Metodología y GitHub (1 min):** historial de commits y ramas.
7. **Cierre (15 s):** conclusiones y supuestos.
