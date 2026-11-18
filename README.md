# super-compu-bros
# Integrantes:
#   Benjamin Aguilar
#   Santino Suarez
#   Bautista Dieguez
---

## Acceso directo (Windows)

Doble click en **`CREAR ACCESO DIRECTO.vbs`**: crea "SUPER COMPU BROS" (con
el icono del juego) en la carpeta del juego y en el Escritorio. El acceso
abre `Super Compu Bros.pyw`, que arranca el juego sin la ventana negra de la
consola. Si moves la carpeta, volve a hacerle doble click.

## Partidas

Al tocar JUGAR aparecen **NUEVA PARTIDA** y **CARGAR PARTIDA**. Hay 6
casillas; cada partida tiene nombre y contrasena (se pide para entrar) y en
la casilla se ve el nivel en el que esta. Cada partida se guarda en
`partidas/partida_N/`. Las cinematicas se ven una vez por partida: si perdes
todas las vidas (o empezas una partida nueva) se vuelven a ver en su momento.
El progreso de antes de las partidas pasa solo a la casilla 1 ("MI PARTIDA",
sin contrasena).

---

## Que trae esta version (fusion de tres versiones)

* **Tres pisos apilados en cada nivel**: la **calle** (donde empezas, con los
  enemigos mas flojos), los **techos** y balcones (el recorrido de siempre) y
  el **cielo** con nubes aleatorias, opcional y con premios. Se sube con
  escaleras y con saltos, y cuanto mas arriba, mas negro el cielo (ver
  "Tres pisos: calle, techos y cielo").
* **30 niveles en dos mapas**: del 1 al 15 por Buenos Aires (el nivel 1 es
  **todo adentro del Instituto Luis A. Huergo**, mas corto y sin enemigos) y del 16 al 30 por el conurbano sur, de
  **Moron a Burzaco**. Los niveles **15 y 30 son peleas contra jefe** (por ahora
  arenas vacias). Ver "30 niveles, dos mapas y jefes".
* **Fondos pixel art** de los 30 niveles, con niveles del triple de largo y
  en capas: a lo lejos se ven los monumentos del barrio de cada nivel (ver
  mas abajo).
* **Niveles de dia y de noche**: dieciocho niveles son de dia, con el **reflejo
  del sol** (rayos, brillo en los vidrios, destellos que titilan), y doce de
  noche, con **luces de edificios, postes de luz, carteles de neon y luna**
  (ver "De dia y de noche").
* **Mision de San Telmo** en el mapa 1 (cara del chico, gris hasta el nivel 3;
  ENTER para entrar, ESC para volver). Por ahora solo muestra
  "MISION EN PROGRESO". Se guarda en `mision.txt`.
* **Hinchas lanzadores** (desde el nivel 5): patrullan y tiran botellas de
  Quilmes. Pisarlos desde arriba los aplasta; tocarlos o que te peguen una
  botella saca una vida. Como los niveles miden 9600 px, hay hinchas en cada
  uno de los 3 tercios: 2 por tercio en el nivel 5, uno mas por tercio en
  cada nivel siguiente, hasta 4 por tercio.
* **Gagambas solo hasta el nivel 7**: del 8 en adelante ya no aparecen
  (`NIVEL_ULTIMO_GAGAMBA` en `juego.py`).
* **Pelotas mas lentas**: las pelotas de Benedetto y Belran (del nivel 8 en
  adelante) van a 1.25 veces la velocidad del personaje
  (`VELOCIDAD_PELOTA = VELOCIDAD_MOV * 1.25` en `juego.py`).
* **Fantasma** (niveles 10 a 29, no en los jefes): vuela hacia vos a la altura del cuerpo, un
  poco levantado del piso, asi que agacharse no sirve y hay que saltar. Si te
  toca no te saca vida, pero por 2 segundos desaparece todo menos el mapa y
  los bordes de la pantalla quedan grises (ver mas abajo). En el cielo
  aparece el doble de seguido.
* **Musica del menu**: ahora suena "Yoshi's Island - Athletic"
  (`assets/musica/menu_athletic.mp3`; la anterior, `menu.mp3`, sigue en la
  carpeta). Se cambia en `MUSICA_MENU` de `musica.py`.
* **Nivel tutorial**: el boton INSTRUCCIONES del menu (ver mas abajo).
* **Aspecto historico** de cada personaje: al elegir un personaje se elige
  si se juega con el aspecto NORMAL o el HISTORICO (ver mas abajo).
* **Ajustes** (el engranaje arriba a la derecha del menu): volumen de la
  musica y de los efectos (ver mas abajo).
* **Efectos de sonido**: agarrar una cerveza, saltar, pisar enemigos, perder
  una vida, romper una botella y llegar a la meta.
* **Sombras en el piso** para los gagambas y los hinchas lanzadores (y mas
  finita cuando los pisas). Se dibujan con `dibujar_sombra_suelo` en
  `juego.py`; la fuerza y la altura se cambian con `ALFA_SOMBRA_ENEMIGO` y
  `BAJADA_SOMBRA_ENEMIGO`.

---

## 30 niveles, dos mapas y jefes

* **Mapa 1, Buenos Aires (niveles 1 a 15)**: el nivel 1 transcurre **adentro del
  Instituto Luis A. Huergo**, el 2 arranca en su puerta de entrada y sigue por San Telmo, Puerto Madero, Plaza de Mayo... hasta La
  Bombonera (jefe). Usa `assets/fondos/mapa_buenos_aires.png`. La tienda y la
  mision de San Telmo estan solo en este mapa.
* **Mapa 2, conurbano sur (niveles 16 a 30)**: arranca en **Moron** y baja por
  Ramos Mejia, Liniers, Villa Lugano, Avellaneda, Lanus, Wilde, Bernal, Quilmes,
  Berazategui, Florencio Varela, San Francisco Solano, Claypole y Adrogue hasta
  **Burzaco** (jefe final). Usa `assets/fondos/mapa_conurbano.png`.
* **Cambio de mapa**: al ganarle al jefe del 15 el punto parpadea, salen los
  puntitos, la pantalla se cierra con el circulo y se abre el mapa del conurbano
  con el personaje parado en Moron. Al ganar el nivel 30 aparece
  "¡FELICITACIONES!" y con ENTER se vuelve al menu con el mapa y las bebidas
  borrados (se empieza de nuevo desde el Huergo; puntos y personaje se
  conservan).
* **Los jefes** (nivel 15 en La Bombonera y nivel 30 en Burzaco) se marcan en
  el mapa con un punto distinto y el globo dice "NIVEL 15 / JEFE" y "NIVEL 30 /
  JEFE FINAL". **Por ahora son arenas vacias**: el nivel mide 1600 px (en vez
  de 9600), sin enemigos, sin fantasma, sin bebidas, y la bandera esta al final
  (a 100 px del borde derecho). Para armar la pelea de verdad hay que sacar
  esas condiciones: `es_jefe(nivel)` en `archivos.py` (`NIVELES_JEFE = (15,
  30)`) se usa en `juego.py` para dejar todo vacio, y el largo sale de
  `ANCHO_ARENA` en `terreno.py` (el `_terreno.json` de un jefe tiene
  `"ancho": 1600`; la bandera esta en `terreno.meta_x`).
* **Nivel 1: Instituto Huergo, todo por dentro (nivel corto, plano y sin
  enemigos)**. Es **mas chico que los demas**: mide 4800 px (la mitad de un
  nivel normal) y tiene **un solo piso**: como estas adentro del colegio no hay
  techos ni escaleras ni nubes a donde subir (las paredes llegan hasta el
  cielorraso) y **no hay enemigos** (ni gagambas, ni hinchas, ni pelotas, ni
  fantasmas); solo bebidas en el piso. Se camina por la planta baja: arranca en
  el **taller mecanico** y sigue por pasillos con **aulas, el taller electrico,
  casilleros, el laboratorio, ventanales altos, la biblioteca, la escalera,
  preceptoria, un mural, otro taller y el salon de actos**; despues el
  **vestibulo** (el nombre del colegio grabado en granito negro, "FUNDADO EN
  1934", la bandera, la puerta de porteria y los tachos de colores de Escuelas
  Verdes) y, justo antes de la bandera de meta, la **puerta de calle**: el
  porton de rombos abierto y la calle de San Telmo a la vista. El piso es de
  granito reconstituido (se vuelve de baldosas ocres en el umbral), el
  cielorraso tiene su cornisa y tubos fluorescentes, y arriba de las puertas
  hay ventanas altas y caños (con valvulas rojas). Los modulos estan en
  `herramientas/interior_huergo.py`, el vestibulo, la salida, el piso y el
  cielorraso en `herramientas/huergo_real.py` (`RUTA` es el recorrido; tiene que
  sumar `ANCHO_INTERIOR`). En el juego: `es_interior(nivel)` en `archivos.py`
  (`NIVELES_INTERIOR = (1,)`) apaga los enemigos en `juego.py`, y el
  `_terreno.json` trae `"interior": true` y `"ancho": 4800` (`Terreno.interior`,
  `Terreno.tiene_calle`; la bandera esta en `terreno.meta_x`). El colegio se
  dibujo con lo que se sabe (el nombre, el 1934, los talleres y laboratorios, el
  lema) y de memoria: el interior real es **aproximado**.
* **Nivel 2: San Telmo, desde la puerta del Huergo**. El nivel arranca **parado
  en la puerta de entrada del Instituto Huergo** (`"inicio_x"` en el
  `_terreno.json`; `puerta="huergo"` en la configuracion), con la fachada de la
  **entrada real (Peru 759)**, solo la estructura: la vidriera con un afiche
  azul, el panel de **granito negro con "INSTITUTO INDUSTRIAL"** grabado, el
  **porton de hierro de rombos** con su plaquita blanca y el escalon amarillo,
  el panel con "LUIS A. HUERGO 759", la vidriera con estantes, la cornisa de
  hormigon gris, la piedra beige con ventanitas con rejas y dos postes finitos
  (uno blanco y otro negro). Adelante, la **vereda de baldosas ocres** con la
  banda amarilla junto al cordon y baldosas grises con puntitos (termina donde
  termina el lote). De ahi sigue por las calles de San Telmo. A lo lejos
  estan los edificios de la zona (Facultad de Ingenieria, Otto Krause, el Museo
  Historico Nacional, el Mercado, San Pedro Telmo y la Iglesia Rusa). La entrada
  esta en `herramientas/huergo_real.py` (`fachada_entrada`, `vereda_entrada`).
* Para agregar o mover un punto del mapa: `NIVELES_BUENOS_AIRES` y
  `NIVELES_CONURBANO` en `mapa.py` (nombre y posicion sobre la imagen original),
  y `TRAMOS_BUENOS_AIRES` / `TRAMOS_CONURBANO` (los puntos intermedios del
  camino entre un nivel y el siguiente). `TOTAL_NIVELES = 30` y
  `NIVELES_POR_MAPA = 15` estan en `archivos.py`.

---

## Fantasma (niveles 10 a 29)

* **Cuando aparece**: del nivel 10 al 30 (`NIVEL_FANTASMA_DESDE` y
  `NIVEL_FANTASMA_HASTA` en `juego.py`), menos en las arenas de jefe (15 y 30). Entra por la derecha cada 3 a 6
  segundos (`ESPERA_FANTASMA_MIN` / `ESPERA_FANTASMA_MAX`) y cruza la pantalla
  hacia la izquierda (`VELOCIDAD_FANTASMA`).
* **Altura**: el borde de abajo vuela entre 14 y 24 px sobre el piso y ademas
  flota subiendo y bajando 8 px (`FANTASMA_ALTURA_MIN`, `FANTASMA_ALTURA_MAX`,
  `FANTASMA_FLOTE`). El codigo (`crear_fantasma`) lo limita para que siempre
  quede mas abajo que la cabeza del personaje agachado: agacharse **no** lo
  esquiva y hay que saltar (el de arriba queda muy por debajo de lo mas alto
  del salto, asi que saltando se esquiva sin problema).
* **Sombra**: tiene sombra en el piso que se achica y se aclara cuanto mas alto
  esta, y crece y se oscurece cuando baja (`dibujar_sombra_fantasma`;
  `FANTASMA_SOMBRA_MAX`, `FANTASMA_SOMBRA_MIN`, `FANTASMA_SOMBRA_ALTURA_MIN`).
* **Si te toca**: no saca vida ni se puede pisar. Durante
  `DURACION_EFECTO_FANTASMA` (2 segundos) no se dibuja nada mas que el mapa (el
  fondo y la meta): ni el personaje, ni items, ni enemigos, ni botellas, ni
  pelotas, ni fantasmas, ni el HUD. El juego sigue corriendo por detras (un
  enemigo te puede pegar igual). Los 4 bordes de la pantalla se ponen grises
  (`dibujar_bordes_grises`; color y grosor en `GRIS_BORDE_FANTASMA`,
  `GROSOR_BORDE_FANTASMA` y `DEGRADE_BORDE_FANTASMA`). Un fantasma toca una
  sola vez, y si perdes una vida el efecto se cancela.
* **Dibujo**: los 3 cuadros de la animacion estan en
  `assets/enemigos/fantasma/fantasma_1.png` a `fantasma_3.png` (32 x 32).

---

## Ajustes: volumen de la musica y de los efectos

El engranaje de arriba a la derecha del menu abre AJUSTES, con dos barras de
0 a 100 %:

* **MUSICA**: la cancion de fondo (se oye subir y bajar en el momento).
* **EFECTOS**: los sonidos del juego (agarrar una Heineken o una Guinness,
  saltar, pisar enemigos, perder una vida, romper una botella, la meta). Al
  soltar la barra suena una Guinness de muestra.

Mouse: click o arrastrar la barra, VOLVER para salir. Teclado: ARRIBA / ABAJO
eligen la barra, IZQUIERDA / DERECHA cambian de a 5, ESC o ENTER vuelven.

Lo elegido se guarda en `ajustes.txt` (`musica efectos`, por ejemplo `40 80`)
y **no se borra** aunque pierdas todas las vidas. Si no existe, los dos
arrancan en 100 (como sonaba antes).

Archivos: `ajustes.py` (los valores), `pantalla_ajustes.py` (la pantalla y el
dibujo del engranaje), `sonidos.py` (hace sonar cada efecto con su volumen) y
`musica.py` (volumen base de la cancion x el ajuste). Los efectos son
`assets/sonidos/*.wav`, hechos con codigo (estilo chiptune):

```
python herramientas/generar_sonidos.py            # los rehace todos
python herramientas/generar_sonidos.py salto      # solo algunos
```

Para usar un sonido propio alcanza con reemplazar el `.wav` con el mismo
nombre; el volumen base de cada uno esta en `VOLUMENES` de `sonidos.py`.

---

## Nivel tutorial (boton INSTRUCCIONES)

Se juega con el personaje elegido, sin vidas ni puntos. ESC vuelve al menu.

1. Al aparecer: "USA D PARA MOVERTE A LA DERECHA, A PARA MOVERTE A LA
   IZQUIERDA".
2. Mas adelante: "USA S PARA AGACHARTE". Llega una pelota a la altura mas baja
   que pasa por arriba de un personaje agachado (de pie te pega; si te pega
   volves al principio de esa parte).
3. Un bloque con "W PARA SALTAR".
4. Un circuito de bloques (valla, escalera, vallas altas).
5. Una bandera gris: al tocarla se vuelve directo al menu.

Todo esta en `tutorial.py`: los textos (`TEXTOS`), la posicion de los bloques
(`TORRES`), la pelota (`X_DISPARO_PELOTA`, `VELOCIDAD_PELOTA_TUTORIAL`) y la
bandera (`X_BANDERA`). Los dibujos estan en `assets/tutorial/` (`bloque.png`,
`piso.png`, `fondo.png`) y la musica en `assets/musica/tutorial.mp3`.
La pantalla vieja de instrucciones (`instrucciones.py`) ya no se usa.

---

## Aspecto historico de los personajes

Cada personaje tiene dos aspectos: el normal y el historico (en blanco y
negro). No son personajes aparte: al elegir uno aparece "ELEGIR ASPECTO" con
el normal y, por ejemplo, "BENJUCHIS HISTORICO". Lo elegido se guarda en
`personajes.txt` (`BENJA` o `BENJA:HISTORICO`) y se ve en la barra de vidas.

* El dibujo de cada historico es `assets/personajes/<NOMBRE>/historico/final.png`
  (16 x 27, la pose quieta).
* El resto de las poses (caminar, saltar, agacharse, cabeza para la barra de
  vidas y pose de seleccion) las genera `herramientas/generar_historicos.py`
  a partir de ese dibujo (hace falta `pip install pillow numpy`). Si se
  quiere redibujar alguna a mano alcanza con reemplazar el PNG: el script no
  pisa los archivos que ya existen (`--forzar` los rehace, `--vista` genera
  una hoja con todas las poses en `herramientas/vistas/`).
* Los nombres que se muestran estan en `NOMBRES_HISTORICOS` de `main.py`.

---

## Tres pisos: calle, techos y cielo

Cada nivel (9600 px de largo) tiene tres pisos apilados, y la camara sube y
baja suave segun el piso donde estas parado (no se mueve cuando saltas). La
excepcion es el nivel 1, adentro del Huergo: solo tiene el piso de abajo (el
pasillo), no hay a donde subir:

| Piso | Donde | Enemigos | Bebidas |
|---|---|---|---|
| **Calle** | abajo, ahi empezas; libre de punta a punta | los mas flojos: 8 gagambas (niveles 2 a 7) o 3 a 5 hinchas lanzadores (del 8 en adelante) | 6 (`ITEMS_CALLE`) |
| **Techos y balcones** | en el medio (lo de siempre) | gagambas (hasta el nivel 7), hinchas, pelotas (del 8 en adelante) y fantasmas (10 a 15) | las de siempre |
| **Cielo** | arriba, solo por nubes | los mas fuertes: pelotas en **todos** los niveles, mas seguido (`ESPERA_PELOTA_CIELO_*`), y fantasmas (10 a 15) el doble de seguido (`ESPERA_FANTASMA_CIELO_*`) | 6 premios (`ITEMS_CIELO`), sobre las nubes |

* **Tres rutas para ganar**: en ninguna parte del nivel hay algo que corte el
  camino, asi que se llega a la meta (el mastil dorado, al final del nivel)
  por cualquiera de los tres pisos:
  * **Calle**: caminando de punta a punta (las escaleras no estorban).
  * **Techos**: subis por una escalera y seguis por los techos y balcones,
    sin bajar, hasta el ultimo edificio.
  * **Cielo**: subis por una escalera, vas por los techos hasta el primer
    edificio grande, saltas a la nube que hay encima y seguis por la
    "autopista" de nubes hasta la meta.
  Se puede cambiar de piso cuando quieras (escaleras, saltos y caidas). Los
  premios (bebidas) del cielo siguen siendo un extra.
* **Subir de la calle a los techos: escaleras de mano.** Parate cerca de una
  escalera y apreta **W o ARRIBA**: te agarras y subis (se agarra a +-22 px).
  Arriba, apretando **S o ABAJO** en el borde de la escalera volves a bajar.
  Agarrado a una escalera, **ESPACIO** te suelta con un salto hacia el lado
  (no se puede soltar dentro de un edificio mas alto). Las escaleras estan en
  los edificios (cualquier altura) y hay 6 por nivel.
* **Subir a las nubes**: desde el techo de cada edificio grande saltas a la
  nube que hay un escalon (108 px) arriba, y de ahi al resto del cielo.
* **La autopista de nubes (el piso de abajo del cielo)**: una fila de nubes a
  la misma altura (y = 156, `NUBE_Y0`) que va **desde el primer edificio grande
  hasta la meta**, con huecos al azar entre 40 y 150 px
  (`NUBE_HUECO_MIN` / `NUBE_HUECO_MAX`) que se cruzan de un salto. Las nubes
  del piso 1 (las de encima, a menos de un salto) nunca tapan la zona donde
  se cae sobre una nube de la autopista (`NUBE_ATERRIZAJE_ANTES` /
  `NUBE_ATERRIZAJE_DESPUES`), asi que de cada una **siempre se puede pasar a
  la siguiente**.
* **Mas arriba**: sobre la autopista se apilan mas nubes (17 pisos, hasta
  y = -1440 mas o menos), repartidas por todo el nivel, no solo en una zona.
  Cada nube de arriba se apoya en una del piso de abajo, a menos de un salto y
  tapandola al menos 64 px. Las nubes se pisan por arriba (las atravesas desde
  abajo).
* **Las nubes son aleatorias** y distintas cada vez que empieza el nivel
  (`Terreno.generar_nubes`), pero **siempre se puede llegar a todas** y hay
  camino hasta la meta. `herramientas/probar_nubes.py` lo comprueba con la
  fisica real (cruce de cada hueco de la autopista, subida a cada nube y un
  buscador de ruta de la primera nube hasta la meta).
* **Si te caes** (de una nube o de un techo) **caes al piso de abajo**: aterrizas
  en la nube, el techo o la calle que haya debajo, y **no perdes una vida**.
* **El cielo se va poniendo negro cuanto mas subis**: arranca un poco
  arriba de las primeras nubes y es casi negro arriba de todo (color `OSCURO_COLOR`,
  entre `OSCURO_DESDE_Y = 60` y `OSCURO_TOTAL_Y = -1500`, tapa como maximo
  `OSCURO_ALFA_MAX` de 255), y salen **estrellas** (`ESTRELLAS`). Las nubes
  siguen brillantes y los fondos lejanos se mueven mas despacio hacia arriba
  (parallax vertical). Todo esta en `fondos_nivel.py`.
* **Camara vertical**: los pies del personaje se ven siempre a la misma altura
  en la calle y en los techos, y en las nubes un poco mas arriba
  (`PIES_CALLE_PANTALLA`, `PIES_NUBE_PANTALLA`, `SUAVIZADO_CAMARA`, en
  `juego.py`). Si caes rapido, la camara se adelanta para que veas donde caes.
* **Datos del nivel**: `nivel_NN_terreno.json` ahora tambien trae `escaleras`
  (la calle esta en y = 804, `CALLE_Y`). Las nubes no se guardan: se generan al
  empezar.

---

## Techos y balcones

Los niveles miden 9600 px y el piso del medio se recorre **por los techos**:
una fila de edificios de tres alturas, pegados uno al lado del otro. Se llega
subiendo por las escaleras de la calle (ver arriba) y se puede volver a bajar.

| Edificio | Techo (y de pantalla) | Se sube con |
|---|---|---|
| Chico | 480 | (es el mas bajo) |
| Mediano | 372 | un salto desde el chico |
| Grande | 264 | un salto desde el mediano, o un **balcon** desde el chico |

* Cada escalon mide 108 px y un salto llega a 160 px. Las paredes son
  solidas: hay que saltar para subir al techo de al lado.
* **Balcones**: los edificios grandes tienen balcones que salen de la pared,
  sobre el edificio mas bajo de al lado. Se pisan por arriba (podes
  atravesarlos desde abajo). Entre un grande y uno chico hay un balcon a
  media altura que sirve de escalon; entre un grande y uno mediano hay otro,
  opcional, que sirve para llegar mas rapido.
* Cada nivel tiene un recorrido distinto (siempre el mismo para cada nivel,
  no es al azar en cada partida). Empieza y termina en un edificio chico.
* **Como se coloca todo**: el dibujo y la colision salen del mismo calculo.
  `terreno.py` lee `assets/niveles/nivel_NN_terreno.json` (donde esta cada
  techo y cada balcon) y decide donde van los enemigos y las bebidas:
  * Los **hinchas lanzadores** y los **gagambas** patrullan sobre un solo
    techo, sin pasar de los bordes, sin ponerse debajo de un balcon, y dejan
    libre el lugar donde aterrizas despues de subir un escalon.
  * Las **bebidas** se acomodan en los techos cerca de su lugar de siempre,
    con la misma altura (las altas siguen obligando a saltar) y separadas
    por lo menos 90 px entre si. Los ids que se guardan en `bebidas.txt` no
    cambiaron.
  * Las **pelotas** pasan por encima de los techos (el codigo elige una
    altura que no choque con los edificios) y desaparecen al pegar contra una
    pared. El **fantasma** acompana la altura del techo en el que estas.
* Si falta `nivel_NN_terreno.json`, el nivel se arma plano como antes (sin escaleras ni calle propia).
* El tutorial no usa techos, calle ni cielo (sigue siendo plano).

---

## Fondos pixel art de los 30 niveles

Cada nivel es un barrio del mapa, dibujado en pixel art (los niveles 1 a 15 son
Buenos Aires y los 16 a 30 el conurbano sur, de Moron a Burzaco). **A lo lejos
se ve lo que hay en cada zona**: los monumentos del barrio aparecen detras de
los edificios y se van acercando a medida que avanzas. **Ningun monumento se
repite** (89 usados en total; el nivel 1 es por dentro del Huergo y no tiene
monumentos de fondo, el 2 muestra la Facultad de Ingenieria, la escuela Otto
Krause y el Museo Historico Nacional ademas de los de San Telmo, y en el nivel
15, ya en La Boca, La Bombonera y Caminito). Los edificios de los barrios del conurbano
estan dibujados de memoria, asi que son aproximados. Los niveles miden **el
triple** de largo (9600 px) y tienen el triple de items y enemigos, salvo los
jefes (1600 px, ver "30 niveles, dos mapas y jefes") y el nivel 1, por dentro
del Huergo (4800 px, sin enemigos). Cada nivel arranca con un
cartel "BIENVENIDOS A <barrio>" (el 1, adentro del Huergo, lleva el nombre del
colegio) y termina con otro que indica el siguiente.

| Nivel | Barrio | Monumentos |
|---|---|---|
| 1 | Instituto Huergo (por dentro) | ninguno: es un colegio por dentro (las paredes llegan hasta el cielorraso) |
| 2 | San Telmo | Facultad de Ingenieria (UBA), Escuela Industrial Otto Krause, Mercado de San Telmo, Iglesia de San Pedro Gonzalez Telmo, Catedral Ortodoxa Rusa, Museo Historico Nacional |
| 3 | Puerto Madero | Puente de la Mujer, Fragata ARA Presidente Sarmiento, Fuente de las Nereidas |
| 4 | Plaza de Mayo | Casa Rosada, Piramide de Mayo, Cabildo de Buenos Aires, Catedral Metropolitana |
| 5 | Retiro | Torre Monumental, Edificio Kavanagh, Estacion Retiro |
| 6 | Recoleta | Floralis Generica, Cementerio de la Recoleta, Basilica Nuestra Senora del Pilar |
| 7 | Barrio Norte | El Ateneo Grand Splendid, Palais de Glace, Facultad de Medicina |
| 8 | Palermo | Planetario Galileo Galilei, Jardin Japones, Rosedal de Palermo |
| 9 | Abasto | Abasto Shopping, Monumento a Carlos Gardel, Casa Museo Carlos Gardel y mural |
| 10 | Once | Palacio de Aguas Corrientes, Estacion Once de Septiembre, Mausoleo de Rivadavia |
| 11 | Congreso | Palacio del Congreso de la Nacion, Confiteria El Molino, Monumento a los Dos Congresos |
| 12 | Obelisco | Teatro Gran Rex, Obelisco, Teatro Colon |
| 13 | Monserrat | Cafe Tortoni, Palacio Barolo, Iglesia de San Ignacio de Loyola |
| 14 | Constitucion | Estacion Constitucion, Iglesia del Inmaculado Corazon de Maria, Autopista 25 de Mayo |
| 15 | La Bombonera | La Bombonera, Caminito |
| 16 | Moron | Catedral de Moron, Palacio Municipal de Moron, Museo Nacional de Aeronautica |
| 17 | Ramos Mejia | Estacion Ramos Mejia, Casa de la Cultura, Plaza Bartolome Mitre |
| 18 | Liniers | Estacion Liniers, Estadio Jose Amalfitani, Santuario de San Cayetano |
| 19 | Villa Lugano | Autodromo Oscar y Juan Galvez, Monobloques de Villa Lugano, Reserva Ecologica Lago Lugano |
| 20 | Avellaneda | Estadio Libertadores de America, El Cilindro de Avellaneda, Puente Nicolas Avellaneda |
| 21 | Lanus | Estadio Ciudad de Lanus, Estacion Lanus, Palacio Municipal de Lanus |
| 22 | Wilde | Estacion Wilde, Parroquia de Wilde, Plaza Wilde |
| 23 | Bernal | Parroquia Maria Auxiliadora, Estacion Bernal, Universidad Nacional de Quilmes |
| 24 | Quilmes | Catedral de Quilmes, Cerveceria Quilmes, Casa de Santa Coloma |
| 25 | Berazategui | Cristalerias Rigolleau, Museo del Vidrio, Estacion Berazategui |
| 26 | Florencio Varela | Hospital El Cruce, Universidad Nacional Arturo Jauretche, Estacion Florencio Varela |
| 27 | San Francisco Solano | Parroquia San Francisco Solano, Estacion Solano, Plaza de Solano |
| 28 | Claypole | Estacion Claypole, Parroquia de Claypole, Tanque de agua del ferrocarril |
| 29 | Adrogue | Casa de Borges, La Cucaracha, Plaza Brown |
| 30 | Burzaco | Primer Monumento a la Bandera, Estacion Burzaco |

Los dibujos del Puente Transbordador, la Usina del Arte y el Tren del Roca
(de La Boca) siguen en `herramientas/monumentos/nivel15.py`, sin usar.

### De dia y de noche

| De dia (sol) | De noche (luna) |
|---|---|
| 1 Instituto Huergo (por dentro, con luz de ventanales), 2 San Telmo, 4 Plaza de Mayo, 5 Retiro, 7 Barrio Norte, 8 Palermo, 10 Once, 11 Congreso, 13 Monserrat, 16 Moron, 17 Ramos Mejia, 19 Villa Lugano, 20 Avellaneda, 22 Wilde, 24 Quilmes, 26 Florencio Varela, 28 Claypole, 29 Adrogue | 3 Puerto Madero, 6 Recoleta, 9 Abasto, 12 Obelisco, 14 Constitucion, 15 La Bombonera, 18 Liniers, 21 Lanus, 23 Bernal, 25 Berazategui, 27 San Francisco Solano, 30 Burzaco |

**De dia, el reflejo del sol**

* El sol del cielo tiene rayos y un resplandor grande, y se ve durante todo el
  nivel (se va corriendo despacio hacia la izquierda con el parallax).
* En el juego, el sol **suma luz por encima de todo el fondo** (le da a los
  edificios y a las nubes) y suelta unos reflejos de lente chiquitos. Se
  apaga cuando subis y el cielo se pone negro.
* Los vidrios de las ventanas reflejan el sol: franjas diagonales de cielo y de
  luz, y algunos ventanales brillan casi blancos. En los edificios de la calle,
  del medio y de lejos. Las paredes tienen una linea de luz del lado del sol y
  las siluetas lejanas un borde claro arriba.
* Hay **destellos que titilan** (cruces de luz) sobre los vidrios que dan al sol,
  y sobre la vereda y el asfalto, que tambien tiene rayitas de brillo.

**De noche, luces en el fondo**

* Las paredes se oscurecen y se prenden ventanas de varios colores (la
  proporcion y los tonos cambian por barrio: calidas, frias, de neon o de
  sodio) con un resplandor de un pixel alrededor.
* **Postes de luz**: en la vereda hay el doble que de dia, y alumbran de
  verdad: halo, cono de luz sobre la pared, charco en la vereda y reflejo largo
  en el asfalto. En el juego suman luz y algunos **fallan a ratos**. Tambien
  hay postes chicos en las azoteas y en las terrazas de los edificios del
  fondo.
* **Carteles de neon** en los edificios del fondo (sobre todo en Abasto y el
  Obelisco), **luces rojas de aviso** en antenas y torres que prenden y apagan,
  ventanitas encendidas en la ciudad lejana y **focos** que iluminan los
  monumentos desde abajo.
* La **luna** cambia de fase segun el barrio (llena, creciente o media), con su
  resplandor, y las nubes se ven a la luz de la luna. El texto de arriba pasa a
  blanco.

`previsualizacion/dia_y_noche.png` muestra los 30 niveles juntos, marcados DIA o
NOCHE (`python herramientas/hoja_dia_noche.py` la vuelve a armar).

Todo esto sale de la configuracion de cada barrio (`herramientas/niveles_config.py`):
con `sol` el nivel es de dia; con `luna` y `noche` es de noche (`luces` =
ventanas prendidas, `paleta_luces`, `farola_luz` y `neon` ajustan el tono). Lo
que se anima en el juego se guarda en `assets/niveles/nivel_NN_efectos.json`
(si falta, el fondo se ve igual pero sin movimiento). Para cambiar un nivel de
dia a noche o al reves alcanza con cambiar esas claves y volver a correr
`python herramientas/generar_techos.py`. El HUD pasa a blanco en los niveles
de `NIVELES_OSCUROS` (`fondos_nivel.py`).

### Como esta hecho

* Cada nivel tiene **cuatro capas** que se mueven a distinta velocidad
  (parallax): `cielo` (casi quieto), `lejos` (siluetas de la ciudad y los
  monumentos, lenta), `medio` (edificios y arboles, media) y `ciudad` (la
  calle, los edificios y los techos por donde se camina, a la velocidad del
  juego). La velocidad de cada capa sale sola del ancho de su imagen. Cuando la
  camara sube, las capas lejanas suben mas despacio (cielo 0.08, lejos 0.30,
  medio 0.60, ciudad 1.0) y la oscuridad del cielo se dibuja encima.
* `fondos_nivel.py` carga las imagenes de `assets/niveles/` y las dibuja en
  `juego.py`. Tambien anima las luces (destellos del sol, luz de los postes,
  luces rojas, brillo del sol y de la luna) con `nivel_NN_efectos.json`. Si faltan `lejos` y `medio`, se dibujan igual el cielo y la
  ciudad; si falta alguna de las dos obligatorias, el juego usa un fondo
  simple con bloques grises para los edificios.
* `assets/niveles/nivel_NN_cielo.png`, `_lejos.png`, `_medio.png`,
  `_ciudad.png`, `_terreno.json` y `_efectos.json`: capas y datos de cada nivel.
  `assets/monumentos/*.png`: cada monumento suelto (los 92 que hay dibujados;
  el juego no los lee, son para mirarlos).
* `previsualizacion/niveles/nivel_NN_techos.png` y `nivel_NN_calle.png`: vista
  previa de cada nivel (principio, medio y final) a la altura de los techos y
  de la calle. `previsualizacion/galeria_monumentos.png`:
  todos los monumentos.

### Regenerar o cambiar las imagenes

Las imagenes se dibujan con codigo (no hay archivos fuente aparte). Hace
falta `pip install pillow numpy`.

```
python herramientas/generar_techos.py            # los 30 niveles (techos)
python herramientas/generar_techos.py 4 12 30    # solo algunos
python herramientas/generar_techos.py --vista    # + vistas previas en herramientas/vistas/
python herramientas/galeria_monumentos.py        # hoja con todos los monumentos
python herramientas/probar_nubes.py              # comprueba que todas las nubes se alcanzan
python herramientas/probar_nubes.py 3 8 -s 10    # solo esos niveles, 10 semillas
```

* `herramientas/generar_techos.py`: arma el recorrido de edificios de cada
  nivel (alturas, balcones, fachadas, cartel de entrada y de salida), dibuja
  las cuatro capas (con la calle, las escaleras y los faroles, de dia con sol o
  de noche con luces) y escribe el `_terreno.json` (con `escaleras`) y el
  `_efectos.json`. Verifica que cada
  nivel tenga las escaleras bien repartidas. Cada nivel usa una semilla
  fija, asi que siempre sale el mismo resultado.
  Con `ESTILOS_EN_TIER`, `TRANSICIONES` y `PROPS_BARRIO` se cambia que
  fachadas van en cada altura, como se suceden los edificios y los objetos
  de las azoteas.
* `herramientas/interior_huergo.py`: los modulos de pasillo del nivel 1
  (`ESTILOS`: aula, taller mecanico y electrico, casilleros, biblioteca,
  laboratorio, oficina, ventanal, escalera, salon de actos y mural), las luces
  y las tres capas de atras (`capa_cielo`, `capa_lejos`, `capa_medio`, que casi no
  se ven porque las paredes llegan hasta el cielorraso).
* `herramientas/huergo_real.py`: el Huergo de verdad. La **entrada** del nivel 2
  (`fachada_entrada`, `vereda_entrada`, hecha a partir de la foto: granito negro
  con letras chicas grabadas, porton de rombos, vidrieras, cornisa, piedra
  beige) y las piezas del **interior** del nivel 1: el recorrido (`RUTA`), el
  vestibulo, la salida con el porton abierto, el piso de granito, el umbral, el
  cielorraso y los tubos fluorescentes.
* `herramientas/generar_niveles.py`: es la herramienta de antes (la calle
  con vereda). Sigue en la carpeta porque `generar_techos.py` usa sus
  funciones; si la corres, **pisa** las imagenes `_cielo` y `_ciudad` con la
  version de la calle (y los niveles dejan de coincidir con el
  `_terreno.json`), asi que despues hay que volver a correr
  `generar_techos.py`.
* `herramientas/monumentos/nivelNN.py`: el dibujo de cada monumento.
* `herramientas/niveles_config.py`: como es cada barrio (cielo, colores,
  donde va cada monumento).
* `herramientas/efectos_luz.py`: el reflejo del sol y las luces de la noche
  (vidrios, ventanas prendidas, postes, neon, balizas).
* `herramientas/edificios.py` y `herramientas/pixelart.py`: fachadas de
  relleno y las herramientas de dibujo.
