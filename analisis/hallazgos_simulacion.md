# Hallazgos de la simulación de poder: Poisson contra regresión lineal

Notas del 30 de octubre de 2026. La tabla completa está en `resumen_simulaciones.md`, que se regenera con `python analisis/04_resumen_simulaciones.py`. Todas las simulaciones asignan temas al azar; ninguna usa resultados reales.

## Qué cambió en el código

1. **El efecto verdadero de la lineal ahora se mide igual que el del Poisson** (`03_simulacion_poder.py`). Antes, el "verdadero" de las variantes `lineal` y `lineal_pesos` era `tau`. Pero la triple diferencia resta el cambio de los temas de control, y en la simulación esos temas bajan un poco cuando la oposición se mueve hacia los tocados. El Poisson ya lo tomaba en cuenta y la lineal no, así que su sesgo se medía contra un objetivo equivocado. Con `tau = 0.5`, el verdadero de la lineal es 0.56, no 0.50.
2. **Todas las variantes simulan los mismos efectos**: 0, 25%, 50% y 100%. Antes, las variantes solo corrían 0, 50% y 100%, así que no había forma de saber el poder con un efecto de 25% para el modelo de la metodología.
3. **Nuevo script `04_resumen_simulaciones.py`**, que junta todas las corridas en una tabla con falsos positivos, poder y sesgo de cada modelo, más el error estándar de simulación de cada cifra.

## Hallazgos

Con 500 simulaciones por efecto para las dos lineales y 60 para el Poisson con α por periodo:

| Modelo | Simulaciones | Falsos positivos | Poder con +25% | Poder con +50% | Sesgo con +50% |
|---|---|---|---|---|---|
| Poisson, α por periodo | 60 | 13% (±4%) | no se corrió | 78% (±5%) | +45% (±8%) |
| Lineal sin pesos | 500 | 7% (±1%) | 23% (±2%) | 69% (±2%) | −3% (±2%) |
| Lineal con pesos | 500 | 7% (±1%) | 30% (±2%) | 78% (±2%) | −5% (±2%) |

1. **El Poisson con α por periodo exagera el efecto en ~45%; las lineales casi no tienen sesgo.** Calcular α por periodo en lugar de por emisión reduce el sesgo del Poisson (era +100%), pero no lo elimina. Las dos lineales quedan a menos de 5% de su verdadero.
2. **La lineal con pesos tiene más poder que la sin pesos** (78% contra 69% con un efecto de 50%), con los mismos falsos positivos. Entre las dos, la pesada es mejor.
3. **Con 500 simulaciones, las lineales rechazan 7% de las veces sin efecto**, cerca del 5% ideal. La cifra de 13% del Poisson viene de solo 60 simulaciones y tiene mucho margen de error, así que todavía no se puede decir si el Poisson rechaza de más o no.
4. **Un efecto de 25% es difícil de detectar**: la lineal con pesos lo detecta en 30% de los casos. Si β sale cercano a cero, no podremos decir que no hay efecto, solo que no hay uno grande.

## Qué falta

- **Correr el Poisson con α por periodo con 500 simulaciones** para compararlo en igualdad de condiciones (tarda alrededor de una hora):

  ```bash
  python analisis/03_simulacion_poder.py 500 fe_periodo
  python analisis/04_resumen_simulaciones.py
  ```

- **Decidir el modelo principal.** Si el Poisson de 500 simulaciones confirma el sesgo, la lineal con pesos es mejor candidata a modelo principal y el Poisson quedaría como robustez. Eso cambia la ecuación, la explicación de β y varias citas de la metodología.

## Lo que hay que corregir en la metodología v4

- El "38% de poder con un efecto de 25%" no viene de estas simulaciones. Con la lineal pesada es 30%; con el Poisson con α por periodo todavía no se ha corrido.
- La frase sobre Weidner y Zylkin debe decir que el sesgo baja con α por periodo, pero no desaparece.
- Los falsos positivos de 13% vienen de 60 simulaciones del Poisson; con 500 simulaciones de las lineales son 7%.

## Advertencia

En la variante `fe_simple` (α para toda la legislatura), el Poisson sale con menos sesgo y más poder que con α por periodo. Pero la simulación lo favorece por construcción, porque los temas simulados no cambian de popularidad con el tiempo. No es un argumento para elegirlo.
