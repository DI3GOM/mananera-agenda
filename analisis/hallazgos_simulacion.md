# Hallazgos de la simulación de poder: Poisson contra regresión lineal

Notas actualizadas el 30 de octubre de 2026. La tabla completa está en `resumen_simulaciones.md`, que se regenera con `python analisis/04_resumen_simulaciones.py`. Todas las simulaciones asignan temas al azar a los discursos reales. Ninguna usa resultados reales del proyecto.

## Resultado principal

| Modelo | Simulaciones | Falsos positivos | Poder con +25% | Poder con +50% | Sesgo con +50% |
|---|---|---|---|---|---|
| Poisson, α por periodo | 200 | 8% (±2%) | 33% (±3%) | 78% (±3%) | +44% (±4%) |
| Lineal sin pesos | 500 | 7% (±1%) | 23% (±2%) | 69% (±2%) | −3% (±2%) |
| Lineal con pesos | 500 | 7% (±1%) | 30% (±2%) | 78% (±2%) | −5% (±2%) |

1. **El Poisson y la lineal con pesos detectan lo mismo**: los dos encuentran un efecto de +50% en 78% de los casos y rechazan sin efecto en 7–8% de los casos.
2. **La diferencia está en el tamaño del efecto.** El Poisson lo exagera en ~44%, y no es ruido: el margen es de ±4%. Calcular α por periodo en vez de por emisión bajó el sesgo del Poisson de +100% a +44%, pero no lo eliminó. La lineal con pesos se queda a 5% del valor verdadero.
3. **Decisión:** la regresión lineal con pesos es el modelo principal y el Poisson queda como prueba de robustez. La lineal sin pesos tiene menos poder (69% contra 78%), así que la descartamos.
4. **Un efecto de +25% es difícil de detectar** con cualquier modelo (30% de las veces con la lineal con pesos). Si β sale cercano a cero, solo podremos decir que no hay un efecto grande.
5. **Los dos modelos rechazan un poco más que el 5% ideal.** Por eso la permutación sigue como prueba de confirmación. El 13% que reportábamos antes para el Poisson venía de solo 60 simulaciones y era ruido.

## Qué cambió en el código

- **`03_simulacion_poder.py`:**
  - El "verdadero" de la lineal ahora toma en cuenta que los temas de control bajan un poco cuando la oposición se mueve hacia los tocados, igual que el del Poisson. Antes era `tau`, que daba un objetivo equivocado (con `tau = 0.5`, el verdadero de la lineal es 0.56).
  - Todas las variantes simulan efectos de 0, 25%, 50% y 100%.
  - Ya no salen los avisos de pyfixest, y el script imprime su avance cada 50 simulaciones.
- **`04_resumen_simulaciones.py`** (nuevo): junta todas las corridas en una tabla con el error estándar de simulación de cada cifra.

## Advertencias

- **En la variante `fe_simple`** (α para toda la legislatura), el Poisson sale con menos sesgo que con α por periodo. Pero la simulación lo favorece por construcción, porque los temas simulados no cambian de popularidad con el tiempo. No es un argumento para elegirlo.
- **La simulación no coincide del todo con lo que dice la metodología.** Usa 66 emisiones, porque cuenta la sesión de la tarde del mismo miércoles como posterior, y solo los turnos de 150 palabras o más. La metodología dice 64 emisiones y todas las palabras de las secciones libres. Hay que alinear las dos cosas antes del análisis real.
