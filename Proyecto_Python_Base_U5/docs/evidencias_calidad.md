# E7 y E8 — Evidencia y procedimiento

## E7. Cobertura (comprobación local)

Comandos:

```bash
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
python -m ruff check src tests
```

En `htmlcov/index.html` se puede consultar línea por línea el código cubierto. El reporte HTML se guarda fuera del repositorio en la carpeta de evidencias de la entrega.

**Pendiente de verificar en un entorno con Ruff:** el linter no estuvo disponible en el entorno local de preparación. GitHub Actions tiene configurada su ejecución; es indispensable revisar el resultado real del job antes de declarar E8 finalizada.

## E8. Pipeline

El flujo está configurado en `.github/workflows/ci.yml` para `push` y `pull_request`: descarga del código, instalación Python 3.11, dependencias, Ruff, pytest con cobertura mínima 80 %, compilación y carga del reporte HTML.

Evidencia de la plataforma aún pendiente: **URL real del repositorio**, captura de workflow verde, captura de workflow rojo mediante fallo controlado en una rama, y recuperación verde tras revertirlo. No se han fabricado capturas.

## Capturas recomendadas

1. Terminal con comando pytest, número de tests y cobertura total.
2. Navegador con `htmlcov/index.html` y detalle de una rama faltante, si existe; si no existen líneas faltantes, señalar honestamente cobertura completa del ejemplo.
3. Pestaña Actions con las tres ejecuciones y el motivo del fallo controlado.

## Riesgos aún abiertos

- Rechazo o timeout de la pasarela dejan un pedido confirmado.
- La suite académica usa SQLite en memoria, no la base real del PIA.
- La actividad colaborativa E9 debe implementarse sobre las reglas aprobadas de la empresa del PIA por el equipo.
