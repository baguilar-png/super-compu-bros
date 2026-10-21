# super-compu-bros
# Integrantes:
#   Benjamin Aguilar
#   Santino Suarez
#   Bautista Dieguez
---

## Que trae esta version (fusion de tres versiones)

* **Tres pisos apilados en cada nivel**: la **calle** (donde empezas, con los
  enemigos mas flojos), los **techos** y balcones (el recorrido de siempre) y
  el **cielo** con nubes aleatorias, opcional y con premios. Se sube con
  escaleras y con saltos, y cuanto mas arriba, mas negro el cielo (ver
  "Tres pisos: calle, techos y cielo").
* **Fondos pixel art** de los 15 niveles, con niveles del triple de largo y
  en capas: a lo lejos se ven los monumentos del barrio de cada nivel (ver
  mas abajo).
* **Mision de San Telmo** en el mapa (cara del chico, gris hasta el nivel 3;
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
* **Fantasma** (niveles 10 a 15): vuela hacia vos a la altura del cuerpo, un
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

## Fantasma (niveles 10 a 15)

* **Cuando aparece**: solo del nivel 10 al 15 (`NIVEL_FANTASMA_DESDE` y
  `NIVEL_FANTASMA_HASTA` en `juego.py`). Entra por la derecha cada 3 a 6
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
baja suave segun el piso donde estas parado (no se mueve cuando saltas):

| Piso | Donde | Enemigos | Bebidas |
|---|---|---|---|
| **Calle** | abajo, ahi empezas; libre de punta a punta | los mas flojos: 8 gagambas (niveles 1 a 7) o 3 a 5 hinchas lanzadores (del 8 en adelante) | 6 (`ITEMS_CALLE`) |
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

## Fondos pixel art de los 15 niveles (Buenos Aires)

Cada nivel es un barrio del mapa, dibujado en pixel art. **A lo lejos se ve
lo que hay en cada zona**: los monumentos del barrio aparecen detras de los
edificios (en el nivel 1, La Bombonera, Caminito y el Puente Transbordador)
y se van acercando a medida que avanzas. **Ningun monumento se repite**
(46 en total), salvo La Bombonera, que esta en La Boca (nivel 1) y en su
propio nivel (el 15). Los niveles miden **el triple** de largo (9600 px) y
tienen el triple de items y enemigos. Cada nivel arranca con un cartel
"BIENVENIDOS A <barrio>" y termina con otro que indica el siguiente.

| Nivel | Barrio | Monumentos |
|---|---|---|
| 1 | La Boca | La Bombonera, Caminito, Puente Transbordador Nicolas Avellaneda, Usina del Arte |
| 2 | San Telmo | Mercado de San Telmo, Catedral Ortodoxa Rusa, Iglesia de San Pedro Gonzalez Telmo |
| 3 | Puerto Madero | Puente de la Mujer, Fragata Sarmiento, Fuente de las Nereidas |
| 4 | Plaza de Mayo | Casa Rosada, Piramide de Mayo, Cabildo, Catedral Metropolitana |
| 5 | Retiro | Torre Monumental, Edificio Kavanagh, Estacion Retiro |
| 6 | Recoleta | Floralis Generica, Cementerio de la Recoleta, Basilica del Pilar |
| 7 | Barrio Norte | El Ateneo Grand Splendid, Palais de Glace, Facultad de Medicina |
| 8 | Palermo | Planetario, Jardin Japones, Rosedal |
| 9 | Abasto | Abasto Shopping, Monumento a Gardel, Casa Museo Gardel |
| 10 | Once | Palacio de Aguas Corrientes, Estacion Once, Mausoleo de Rivadavia |
| 11 | Congreso | Palacio del Congreso, Confiteria El Molino, Monumento a los Dos Congresos |
| 12 | Obelisco | Obelisco, Teatro Colon, Teatro Gran Rex |
| 13 | Monserrat | Palacio Barolo, Cafe Tortoni, Iglesia de San Ignacio |
| 14 | Constitucion | Estacion Constitucion, Iglesia Claretiana, Autopista 25 de Mayo |
| 15 | La Bombonera | La Bombonera, Puente Nicolas Avellaneda, Tren del Roca |

Los niveles van de la manana a la noche: del 12 en adelante atardece y en
La Bombonera es de noche (con luces prendidas en las ventanas).

### Como esta hecho

* Cada nivel tiene **cuatro capas** que se mueven a distinta velocidad
  (parallax): `cielo` (casi quieto), `lejos` (siluetas de la ciudad y los
  monumentos, lenta), `medio` (edificios y arboles, media) y `ciudad` (la
  calle, los edificios y los techos por donde se camina, a la velocidad del
  juego). La velocidad de cada capa sale sola del ancho de su imagen. Cuando la
  camara sube, las capas lejanas suben mas despacio (cielo 0.08, lejos 0.30,
  medio 0.60, ciudad 1.0) y la oscuridad del cielo se dibuja encima.
* `fondos_nivel.py` carga las imagenes de `assets/niveles/` y las dibuja en
  `juego.py`. Si faltan `lejos` y `medio`, se dibujan igual el cielo y la
  ciudad; si falta alguna de las dos obligatorias, el juego usa un fondo
  simple con bloques grises para los edificios.
* `assets/niveles/nivel_NN_cielo.png`, `_lejos.png`, `_medio.png`,
  `_ciudad.png` y `_terreno.json`: capas y datos de cada nivel.
  `assets/monumentos/*.png`: cada monumento suelto.
* `previsualizacion/niveles/nivel_NN_techos.png` y `nivel_NN_calle.png`: vista
  previa de cada nivel (principio, medio y final) a la altura de los techos y
  de la calle. `previsualizacion/galeria_monumentos.png`:
  todos los monumentos.

### Regenerar o cambiar las imagenes

Las imagenes se dibujan con codigo (no hay archivos fuente aparte). Hace
falta `pip install pillow numpy`.

```
python herramientas/generar_techos.py            # los 15 niveles (techos)
python herramientas/generar_techos.py 4 12       # solo algunos
python herramientas/generar_techos.py --vista    # + vistas previas en herramientas/vistas/
python herramientas/galeria_monumentos.py        # hoja con todos los monumentos
python herramientas/probar_nubes.py              # comprueba que todas las nubes se alcanzan
python herramientas/probar_nubes.py 3 8 -s 10    # solo esos niveles, 10 semillas
```

* `herramientas/generar_techos.py`: arma el recorrido de edificios de cada
  nivel (alturas, balcones, fachadas, cartel de entrada y de salida), dibuja
  las cuatro capas (con la calle, las escaleras y los faroles) y
  escribe el `_terreno.json` (con `escaleras`). Verifica que cada
  nivel tenga las escaleras bien repartidas. Cada nivel usa una semilla
  fija, asi que siempre sale el mismo resultado.
  Con `ESTILOS_EN_TIER`, `TRANSICIONES` y `PROPS_BARRIO` se cambia que
  fachadas van en cada altura, como se suceden los edificios y los objetos
  de las azoteas.
* `herramientas/generar_niveles.py`: es la herramienta de antes (la calle
  con vereda). Sigue en la carpeta porque `generar_techos.py` usa sus
  funciones; si la corres, **pisa** las imagenes `_cielo` y `_ciudad` con la
  version de la calle (y los niveles dejan de coincidir con el
  `_terreno.json`), asi que despues hay que volver a correr
  `generar_techos.py`.
* `herramientas/monumentos/nivelNN.py`: el dibujo de cada monumento.
* `herramientas/niveles_config.py`: como es cada barrio (cielo, colores,
  donde va cada monumento).
* `herramientas/edificios.py` y `herramientas/pixelart.py`: fachadas de
  relleno y las herramientas de dibujo.
