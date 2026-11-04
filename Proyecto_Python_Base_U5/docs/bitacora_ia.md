# Bitácora de apoyo de IA — Unidad 5

## Alcance y criterio de validación

La IA se utilizó como asistente para revisar la asignación de tareas, proponer casos adicionales de integración, localizar ramas no probadas y redactar documentación. **Las decisiones de aceptación se basan en los contratos reales de `src/` y en la ejecución de pytest**, no en la autoridad de una respuesta automática. No se cargaron datos reales de clientes ni se realizaron pagos.

## Registro verificable

| Etapa | Propuesta o pregunta planteada a la IA | Revisión humana / corrección | Evidencia |
|---|---|---|---|
| Integración E4 | Proponer pruebas de commit, rollback y duplicidad de claves con SQLite en memoria. | Se comprobó que `save()` agrega objetos y que `commit()` y `rollback()` pertenecen a `Session`; se añadieron verificaciones después de cerrar la sesión. | `tests/test_integracion_e4.py` |
| Pasarela E5 | Proponer escenarios aprobado, rechazo, VIP y timeout sin llamadas reales. | Se usó `unittest.mock.Mock`, se validó el importe con `assert_called_once_with`, y se comprobó la excepción real. | `tests/test_integracion_e5.py` |
| Caso de IA **corregido** | Tratar fondos insuficientes como excepción diferenciada `InsufficientFunds`. | **Rechazado**: el contrato actual únicamente devuelve booleano. `False` activa `RuntimeError("payment rejected")`; no existe clase `InsufficientFunds`. Se conservó el comportamiento real y quedó documentada la limitación. | `src/application.py`, `tests/test_integracion_e5.py` |
| Calidad E7 | Medir cobertura y revisar ramas sin ejecutar. | La herramienta mide instrucciones ejecutadas; no se confunde 100 % de cobertura con calidad funcional absoluta. | Reporte local `htmlcov/index.html` |
| Pipeline E8 | Verificar lint, tests, cobertura y compilación en pushes y PR. | Se revisaron rutas relativas, se mantuvo el umbral 80 %, se incluyó el artefacto HTML, pero la ejecución remota **requiere publicar el repositorio**. | `.github/workflows/ci.yml` |

## Responsabilidad del equipo

Las sugerencias de IA no sustituyen la inspección del código, la ejecución real de pruebas ni la captura de evidencia RED–GREEN o GitHub Actions. No se debe afirmar que un workflow ha pasado en GitHub hasta comprobarlo en la pestaña Actions. Cualquier cambio futuro en reglas de negocio obliga a revisar expectativas y volver a ejecutar las pruebas.
