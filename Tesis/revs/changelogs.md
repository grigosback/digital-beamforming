# Propios

## Algoritmos de estimación de dirección de arribo:

- P.28: Se cambió "desvío estándar del error en la separación de elementos con respecto a la distancia nominal $d$." "error relativo en la separación de elementos con respecto a la distancia nominal $d$."

# Damián

## Abstract:

- Se cambió "sistema de procesamiento" por "microprocesador".

- Se agregó el abstract en inglés.

## Introducción

- P.1: Se cambió "una" por "uno"

- P.1: Se cambió "estas órbitas tienen la ventaja" por "estas órbitas presentan la ventaja"

- P.1: Se definió el término "pisada"

## Algoritmos de estimación de dirección de arribo

- P.21: Se cambió "sino" por "de lo contrario"

- P.22: Se cambió "acondicionadas" por "condicionadas"

- P.22: Se cambió "Ss es ortogonal a Ss" por "Ss y Ss no coinciden en general"

## Muestreo Aleatorio

- P.35: Se cambió "en el caso en el que existieran ventanas de tiempo en el que" por "y en el caso en el que existieran ventanas de tiempo en las cuales"

- P.36: Se añadió la referencia requerida.

- P.39: Se cambió "ningún escenario" por "ninguna escala temporal"

## Estimación del número de señales recibidas

- P.43: Se corrigieron errores de nomenclaturas.

- P.43: Se cambió "valore singulares de la SVM de la matriz X" por "valores singulares obtenidos mediante la SVD de la matriz X"

- P.46: Se cambió "entra" por "se enmarca"

- P.48: Se definió y(i) y x(i)

## Integración en GNURadio

- P.66: Se cambió "sobrepasar" por "superar"

## Trabajo a futuro

- P.75: Se definió UDP

- P.76: Se cambió "más alla que" por "si bien"

# Roberto:

## Abstract:

- P.15: Se cambió "En el siguiente trabajo se realiza el análisis de distintas técnicas de conformación de haz" por "En el siguiente trabajo se realiza el análisis de distintas técnicas de conformación digital de haces mediante el empleo de un arreglo de antenas para la recepción"

## Introducción:

- P.1: Se cambió: "En la actualidad, este servicio requiere que el usuario se encuentre dentro del área de cobertura de alguna de las antenas instaladas por el proveedor, sin embargo, en los últimos años" por "En la actualidad, este servicio requiere que el usuario se encuentre dentro del área de cobertura de alguna de las antenas instaladas por los proveedores del servicio. Sin embargo, en los últimos años".

- P.1: Se cambió "en la actualidad estas siguen consideradas" por "en la actualidad estas siguen siendo consideradas"

- P.1: Se cambió "cuyas distancias de enlace se encuentran típicamente entre los 200 km y los 2000 km" por "cuyas distancias de enlace se encuentran por debajo de los 2000 km" y se agregó una cita para validar el dato.

## Conformación de haz:

- P.7: Se cambió "consideremos que tenemos un conjunto de antenas $M$ idénticas" por "consideremos que tenemos un conjunto de $M$ antenas idénticas"

- P.7: Se añadió en la leyenda de la Figura 2.4: "Aunque se utilice la misma letra, en este caso el ángulo $\theta$ no corresponde al ángulo de elevación sino al ángulo medido con respecto a la vertical."

- P.7: Se cambió "a las cuales les llega un frente de onda con un cierto ángulo $theta$ con respecto a la vertical, como se muestra en la Figura 2.4" por "a las cuales les llega un frente de onda con un cierto ángulo $\theta$ con respecto a la vertical proveniente de un emisor ubicado dentro del plano formado por las antenas, como se muestra en la Figura 2.4"

- P.7: Se cambió "y que el frente de onda se lo puede considerar plano" por "y que el frente de onda puede ser considerado plano"

- **P.9 Ver corrección con respecto a ganancias nulas**

- P.9: En el penúltimo párrafo se añadió la siguiente aclaración: "Es conveniente aclarar que el esquema mostrado en la Figura 2.5b es un esquema base del funcionamiento de un conformador digital de haz, ya que entre cada elemento y su respectivo conversor analógico-digital puede existir una etapa de recepción que vuelve más complejo al sistema."

- P.11: Se cambió "escanear" por "direccionar".

- P.12: Se cambió "permite el escaneo" por "permite el direccionamiento de la recepción"

- P.12: Se realizó la siguiente aclaración con respecto al sentido del ángulo de azimut: Es conveniente aclarar que en este ejemplo se muestra que el ángulo de azimut tiene sentido antihorario, opuesto a como se define en el sistema de coordenadas horizontales que se mostró en la Figura \ref{fig:beamforming*lookangles}. La razón por la cual se muestra de esta manera es para utilizar un sistema de coordenadas cartesianos que permita definir la ubicación de los elementos del arreglo de antenas y así utilizar coordenadas polares para definir la dirección de arribo de la señal, en las cuales el ángulo de azimut se mide desde el eje $x$ hacia el eje $y$ y, por ende, tiene sentido antihorario. Esta manera de definir los ángulos de arribo vuelve más intuitiva la interpretación de los cálculos y no conlleva ninguna pérdida de generalidad ya que se puede pasar de una convención a otra haciendo:
  \begin{equation}
  \varphi*{\textrm{C. Horizontales}} = -\varphi\*{\textrm{C. Polares}},
  \end{equation}
  donde $\varphi_{\textrm{Hor}}$ es el ángulo de azimut en coordenadas horizontales y $-\varphi_{\textrm{Pol}}$ es el ángulo de azimut en coordenadas polares. Para todos los análisis y simulaciones que siguen se utilizará la definición del ángulo de azimut en coordenadas polares.

- P.15: Se aclaró el sentido de los ángulos de elevación y azimut en la Figura 2.9

## Algoritmos de estimación de dirección de arribo:

- P.18: Se cambió "las cuales conforman la base" por "las cuales conforman una base"

- **P.20: ver corrección con respecto a Rxx**

- P.21: Se cambió "ya que sino el subespacio de las muestras" por "ya que, de lo contrario, el subespacio de las muestras"

- P.21: Se cambió "la matriz de autocorrelación muestral" por "la matriz de autocorrelación".

- P.21: Se cambió "Antes de comenzar el análisis de los algoritmos de estimación de arribo" por "Antes de comenzar el análisis de los algoritmos de estimación de dirección arribo"

- P.28: Se añadió la definición de SNR utilizada en las simulaciones antes de 3.4.1

- P.28: Se añadió las especificaciones de la plataforma de cómputo utilizada en las simulaciones antes de 3.4.1

- P.28: Se añadió el signo faltante ° después de \varphi=30

- P.29: Se cambió la definición de RMSE quitando el 2 del denominador y se rehicieron las gráficas.

- P.33: Se añadió la siguiente información: "También puede verse que la complejidad de esta operación es $O(MN^2)$, como sugiere la teoría" añadiendo la cita correspondiente.

## Muestreo Aleatorio

- P.36: Se cambió en la leyenda de la Figura 4.1 "100 kHz" por "7 kHz"

- **P.37: ver corrección ecuación 4.3**

- P.38: Se corrigió la Ecuación 4.8 **preguntar**

- P.41: Se añadió la siguiente aclaración "Para el caso de $p=0,01$ el error sube un orden de magnitud con respecto al muestreo secuencial, lo cual tiene sentido ya que se espera que la varianza sea proporcional a la inversa del número de muestras independientes."

- P.41: Se añadió el eje graduado en T de la figura 4.4.

## Estimación de la cantidad de señales recibidas

- P.46: Se cambió "una variable $y$, la cual se sabe" por "una variable ``$y$'', de la cual se sabe".

- P.51: Se cambió "la implementación de estos algoritmos puedan realizarse de forma muy rápida" por "la implementación de estos algoritmos pueda realizarse de forma muy rápida".

- P.52: Se corrigió todo lo que se refería a valores singulares de X y en realidad eran autovalores de Rxx. Se explicó la relación que existen entre los valores singulares de X y los autovalores de Rxx, referenciando el resultado.

- **P.55: Analizar Figura 5.12**

## Diseño del sistema

- P.57: Se cambió "chip FPGA" por "dispositivo FPGA"

- P.60: "¿No es más bien la descomposición en V.S. de la matriz de autocovarianza muestral de la entrada Xrs?": No, se aplica la SVD sobre la matriz de muestras para evitar calcular la Rxx.

## Integración en GNURadio

- P.71: Se puso en mayúsculas "ESPRIT"

- P.71: Se puso apaisada la figura 7.7 y 7.8

- P.72: Se cambió "bloque con peor rendimiento" por "bloque que insume la mayor parte de la carga de cómputo en el sistema"

- P.72: Se cambió "incrementar el rendimiento" por "incrementar la eficiencia".

- P.73: Se corrigió la Figura 7.9 tomando la EB/N0 en el receptor, y se agregó la curva de BPSK con recepción óptima teórica para comparar.

## Apéndice

- P.79: Se cambió "desfasajes" por "fasores".

- P.79: Se corrigieron todos los errores de nomenclaturas.

- P.79: Se cambió arctan por arctan2

## Bibliografía

- Se cambió el título por "Referencias"

- Se agregaron fechas de acceso a los links

- Se acomodó el diseño como fue requerido

# Ambos

## Algoritmos de estimación de dirección de arribo:

- P.22: Se cambió $\mathfrak{a}$ por $\mathfrak{A}$.

## Muestreo aleatorio

- P.38: Se cambió f0 por fc.
