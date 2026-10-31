# Resumen de las simulaciones de poder

Generado por `analisis/04_resumen_simulaciones.py`. Temas asignados al azar; no usa resultados reales.

- **Falsos positivos**: rechazo con efecto 0. Lo ideal es 5%.
- **Poder**: rechazo con efecto positivo.
- **Sesgo**: diferencia promedio entre el beta estimado y su verdadero, en % del verdadero.
- Entre paréntesis, el error estándar de simulación. Diferencias menores a unos dos errores estándar no son claras.

| Modelo | Simulaciones por efecto | Falsos positivos | Poder con +25% | Poder con +50% | Poder con +100% | Sesgo con +50% |
|---|---|---|---|---|---|---|
| Poisson, α por emisión | 100 | 10% (±3%) | 8% (±3%) | 35% (±5%) | 81% (±4%) | +100% (±12%) |
| Poisson, sesiones sumadas | 100 | 12% (±3%) | no se corrió | 35% (±5%) | 76% (±4%) | +93% (±12%) |
| Poisson, α por periodo | 200 | 8% (±2%) | 33% (±3%) | 78% (±3%) | 100% (±0%) | +44% (±4%) |
| Poisson, α para toda la legislatura | 60 | 13% (±4%) | no se corrió | 85% (±5%) | 100% (±0%) | +26% (±6%) |
| Lineal sin pesos, α por periodo | 500 | 7% (±1%) | 23% (±2%) | 69% (±2%) | 99% (±0%) | -3% (±2%) |
| Lineal con pesos, α por periodo | 500 | 7% (±1%) | 30% (±2%) | 78% (±2%) | 100% (±0%) | -5% (±2%) |
