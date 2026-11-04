# Laboratorio de Unidad 5 — Componentes de Lógica de Negocios

**Proyecto académico de ejemplo de pedidos.** No es la aplicación del PIA de la empresa; los datos CSV y SQLite externos son demostrativos y no se importan automáticamente.

## Requisitos e instalación

- Python 3.11 o superior; Git para publicar el proyecto; una cuenta de GitHub para ejecutar CI.
- Abre la terminal **dentro de `Proyecto_Python_Base_U5`** (donde está `requirements.txt`).

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

Si la activación de PowerShell está bloqueada, usa `.\.venv\Scripts\python.exe -m pytest -v`.

## Arquitectura y función de archivos

- `src/domain.py`: `Order` y reglas del negocio: total positivo, deuda, descuento VIP del 15 % y no confirmar dos veces.
- `src/application.py`: `OrderService.checkout()`, que calcula el cargo y llama al puerto `gateway.charge(amount)`.
- `src/repository.py`: `OrderRow`, `SqlOrderRepository` y `make_engine()` para SQLite mediante SQLAlchemy.
- `src/security.py`: política `can_cancel()`: no cancelar pedidos enviados, administradores en otros estados y dueño antes de 24 horas.
- `tests/test_order.py`: pruebas de dominio y TDD (integrante 1).
- `tests/test_security.py`: autorización (integrante 1).
- `tests/test_repository.py` y `tests/test_service.py`: pruebas originales.
- `tests/test_integracion_e4.py`: E4, integración con SQLite (integrante 2).
- `tests/test_integracion_e5.py`: E5, pagos mediante mocks (integrante 2).
- `.github/workflows/ci.yml`: validación continua (integrante 3).
- `docs/bitacora_ia.md`: documentación del uso y revisión de IA.
- `docs/evidencias_calidad.md`: instrucciones de evidencia E7/E8 y limitaciones de verificación.
- `../casos_de_prueba.csv`: matriz CSV de casos del laboratorio, fuera del proyecto para preservar el paquete original.

Flujo: consumidor → `OrderService` → `Order.confirm()` → `gateway.charge()`; el repositorio es un adaptador independiente de persistencia. El proyecto **no** tiene API HTTP ni interfaz E2E.

## Ejecutar verificaciones de calidad

```bash
python -m pytest -v
python -m ruff check src tests
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
python -m compileall -q src
```

Abre `htmlcov/index.html` después de ejecutar las pruebas de cobertura. El umbral es **80 % de líneas del directorio completo `src/`**, no porcentaje de tests correctos. Cubrir una línea no prueba por sí solo que la lógica sea correcta.

## CI con GitHub Actions

1. Crea un repositorio GitHub vacío. Sube **el contenido de esta carpeta de proyecto** a la raíz (es decir, `requirements.txt`, `src/`, `tests/`, `.github/`).
2. Publica con `git init`, `git add .`, `git commit -m "Unidad 5: pruebas y CI"`, `git branch -M main`, `git remote add origin <URL_DEL_REPOSITORIO>` y `git push -u origin main`.
3. En **Actions → CI Business Logic**, comprueba el primer resultado verde. La cobertura HTML se adjunta como artifact.
4. Para demostrar el bloqueo, cambia temporalmente una aserción del test en **una rama de prueba**, envía el cambio y captura el resultado rojo. Revierte la aserción, vuelve a ejecutar y captura el verde recuperado. No dejes el test defectuoso en la entrega.
5. Si deseas que fallos bloqueen merges, configura en GitHub **Settings → Rules → Rulesets** una regla que exija el check de CI. El archivo YAML por sí mismo no impone protección.

No se ha ejecutado GitHub Actions ni se puede afirmar que exista una URL del repositorio sin publicarlo.

## Riesgos y alcance

- `OrderService.checkout()` **confirma el pedido antes del resultado de la pasarela**. Un rechazo o timeout puede dejarlo en estado `CONFIRMED`. E5 lo evidencia, pero la implementación no se modifica por ser responsabilidad del dominio/servicio a acordar con el equipo.
- El gateway base devuelve `True/False`, por lo que un `False` no distingue formalmente fondos insuficientes de otras causas de rechazo.
- SQLite en memoria prueba el adaptador, pero no garantiza comportamiento idéntico a una base de producción.
- Los archivos `.venv`, cachés, `htmlcov` y `.coverage` no deben versionarse. Para la entrega separada se incluye un reporte HTML generado localmente.
- La adaptación E9 a tres reglas de la empresa del PIA requiere reglas y código del PIA, que no están incluidos en este proyecto de ejemplo.
