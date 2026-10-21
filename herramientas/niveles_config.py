"""
Configuracion de los 15 fondos: como es cada barrio de Buenos Aires.

Cada nivel define el cielo (hora del dia), el skyline lejano, que tipos de
edificios hay (y cuantos), los arboles, los objetos de la calle, el piso y
donde va cada monumento (x en pixeles de dibujo; el nivel mide 3200).

Los colores van en hexadecimal.
"""

# ----------------------------------------------------------
# Paletas (fachada, borde, extra) por tipo de edificio
# ----------------------------------------------------------

PALETAS = {
    "frances": [
        ("#e3d2ab", "#c8b385"), ("#d9c8b8", "#f0e6d6"), ("#cfd6d0", "#f2ede0"),
        ("#e8dcc0", "#b89a68"), ("#d8c0a8", "#f0e0c8"), ("#ddd0c0", "#a89880"),
    ],
    "italianizante": [
        ("#d9a870", "#f0e0c0"), ("#c8d4c0", "#f0f0e0"), ("#e6c8a0", "#a8744a"),
        ("#d8c0c0", "#f4ecdc"), ("#e0d0a0", "#9a8a5a"), ("#c8d0e0", "#f0ece0"),
    ],
    "casa_baja": [
        ("#e8b868", "#7a3a2a", "#2f6a4a"), ("#d8e0c8", "#6a8a5a", "#8a3a2a"),
        ("#d8a0a0", "#f4ecdc", "#3a5a7a"), ("#c8d8e0", "#3a5a7a", "#7a3a2a"),
        ("#e8d8a0", "#9a5a3a", "#2f6a4a"), ("#e0c0a0", "#8a4a3a", "#3a6a5a"),
    ],
    "conventillo": [
        ("#d8362f", "#f4f1e8"), ("#2f6fd0", "#f5c60c"), ("#f5c60c", "#1b3f9f"),
        ("#2f8f5a", "#f4f1e8"), ("#f08a2e", "#1b3f9f"), ("#e88fb0", "#2f6fd0"),
        ("#47b0d8", "#d8362f"),
    ],
    "torre_vidrio": [
        ("#4a8aa8",), ("#5a7aa0",), ("#3a6a8a",), ("#6a9a9a",), ("#8aa8c0",),
    ],
    "torre_hormigon": [
        ("#b8b4a8",), ("#c8c0b0",), ("#a8aab0",), ("#c4b8a4",),
    ],
    "art_deco": [
        ("#d0c4a8", "#f0e8d0"), ("#c8c0b8", "#e8e0d8"), ("#d8c8a0", "#f4ecd0"),
    ],
    "galpon": [
        ("#a9472f", "#e8dcc4"), ("#9a4030", "#e0d4b8"), ("#b0553a", "#ece0c8"),
    ],
    "fabrica": [
        ("#9a4a35",), ("#a05540",), ("#8a4030",),
    ],
    "departamentos": [
        ("#c8a888", "#f0e8d8"), ("#d8d0bc", "#a89878"), ("#c0b0a0", "#f0e6d0"),
        ("#d0b8a0", "#e8e0d0"), ("#b8c0b0", "#f0eadc"),
    ],
    "mural": [
        ("#d8d0c0",), ("#cfc8b8",),
    ],
    "local": [
        ("#d9cbb0", "#b09870"), ("#d8c0b0", "#a08068"), ("#cfd0c0", "#8a9078"),
    ],
}


# ----------------------------------------------------------
# Los 15 niveles
# ----------------------------------------------------------
#
# cielo        (arriba, medio, abajo)
# noche        0 = dia ... 1 = noche cerrada (oscurece y enciende luces)
# tinte        color con el que se tine toda la ciudad (opcional)
# skyline      siluetas lejanas (se dibujan en este orden)
# estilos      peso de cada tipo de edificio
# arboles      tipos de arbol de la vereda
# props        objetos de la calle y su peso
# suelo        (vereda, calle)
# plaza        probabilidad de que un tramo sea plaza / parque
# esquina      probabilidad de que sea una calle que cruza
# monumentos   (id, centro x)
# ----------------------------------------------------------

NIVELES = {

    1: dict(
        barrio="LA BOCA",
        cielo=("#4f9ae0", "#8fc8f0", "#f6e6c8"),
        nubes="#ffffff",
        sol=(900, 36, 8, "#fff2b0"),
        skyline=["puerto", "casas"],
        estilos={"conventillo": 8, "casa_baja": 1, "fabrica": 1, "galpon": 1, "mural": 1},
        mural=["boca", "abstracto"],
        arboles=[("platano", 1)],
        prob_arbol=0.25,
        props={"farola": 3, "banderin": 3, "chori": 2, "tango": 2, "banco": 2, "cesto": 2, "kiosco": 1},
        suelo=("adoquin", "adoquin"),
        plaza=0.08, esquina=0.10,
        calles=["BRANDSEN", "SUAREZ", "IBERLUCEA", "MENDOZA", "GARIBALDI", "ALTE BROWN"],
        trafico={"auto": 4, "taxi": 2, "colectivo": 1},
        monumentos=[("bombonera", 620), ("caminito", 1330), ("transbordador", 2030), ("usina_del_arte", 2700)],
        siguiente="SAN TELMO",
    ),

    2: dict(
        barrio="SAN TELMO",
        cielo=("#5aa4e4", "#9ed2f2", "#f8ead0"),
        nubes="#ffffff",
        sol=(260, 40, 8, "#fff4c0"),
        skyline=["casas"],
        estilos={"italianizante": 4, "casa_baja": 5, "frances": 1, "local": 2},
        textos=["ANTIGUEDADES", "TANGO", "CAFE", "LIBROS", "ARTE", "MATE"],
        arboles=[("platano", 1)],
        prob_arbol=0.45,
        props={"farol_colgante": 4, "feria": 4, "tango": 3, "banco": 2, "cesto": 2, "kiosco": 1},
        suelo=("baldosa", "adoquin"),
        plaza=0.12, esquina=0.12,
        calles=["DEFENSA", "BOLIVAR", "HUMBERTO 1", "CHILE", "CARLOS CALVO", "INDEPENDENCIA"],
        trafico={"auto": 3, "taxi": 3, "colectivo": 1},
        monumentos=[("mercado_san_telmo", 540), ("iglesia_rusa", 1500), ("san_pedro_telmo", 2450)],
        siguiente="PUERTO MADERO",
    ),

    3: dict(
        barrio="PUERTO MADERO",
        cielo=("#3f8ee0", "#86c6f0", "#e8f0f4"),
        nubes="#ffffff",
        sol=(1000, 34, 8, "#fffbd0"),
        skyline=["rascacielos", "puerto"],
        fondo_alto=(36, 84),
        estilos={"galpon": 5, "torre_vidrio": 3, "departamentos": 1, "torre_hormigon": 1},
        arboles=[("sauce", 2), ("platano", 1)],
        prob_arbol=0.35,
        props={"grua": 2, "bolardo": 3, "farola": 3, "banco": 2, "cesto": 2},
        suelo=("ladrillo", "vias"),
        plaza=0.16, esquina=0.10,
        calles=["J MANSO", "A VILLAFLOR", "M GUEMES", "O COSSETTINI", "A M DE JUSTO", "M LYNCH"],
        trafico={"auto": 4, "taxi": 2, "colectivo": 1},
        monumentos=[("puente_de_la_mujer", 600), ("fragata_sarmiento", 1560), ("fuente_nereidas", 2500)],
        siguiente="PLAZA DE MAYO",
    ),

    4: dict(
        barrio="PLAZA DE MAYO",
        cielo=("#3a8fe6", "#7ec4f2", "#e6f0f4"),
        nubes="#ffffff",
        sol=(500, 30, 8, "#fffbd0"),
        skyline=["centro"],
        estilos={"italianizante": 4, "frances": 2, "art_deco": 1, "torre_hormigon": 1},
        arboles=[("palmera", 2), ("platano", 1)],
        prob_arbol=0.4,
        props={"farola": 3, "banco": 2, "bandera": 3, "cesto": 2, "kiosco": 1},
        suelo=("plaza", "asfalto"),
        especiales=["panuelos", "palomas"],
        plaza=0.12, esquina=0.10,
        calles=["BALCARCE", "H YRIGOYEN", "RIVADAVIA", "B MITRE", "AV DE MAYO", "DEFENSA"],
        trafico={"auto": 3, "taxi": 3, "colectivo": 2},
        monumentos=[("casa_rosada", 480), ("piramide_de_mayo", 1180), ("cabildo", 1870), ("catedral_metropolitana", 2600)],
        siguiente="RETIRO",
    ),

    5: dict(
        barrio="RETIRO",
        cielo=("#3a86e0", "#78bcf0", "#e4eef4"),
        nubes="#ffffff",
        sol=(1100, 34, 8, "#fffbd0"),
        skyline=["rascacielos", "centro"],
        fondo_alto=(60, 120),
        estilos={"torre_vidrio": 2, "torre_hormigon": 2, "art_deco": 2, "frances": 3, "departamentos": 1},
        arboles=[("ombu", 2), ("ficus", 2), ("platano", 1)],
        prob_arbol=0.5,
        props={"farola": 3, "banco": 2, "kiosco": 1, "subte": 1, "parada": 1, "semaforo": 1, "cesto": 2},
        suelo=("baldosa", "asfalto"),
        plaza=0.14, esquina=0.10,
        calles=["SAN MARTIN", "AV SANTA FE", "ARENALES", "M T DE ALVEAR", "AV LIBERTADOR", "SUIPACHA"],
        trafico={"auto": 3, "taxi": 3, "colectivo": 3},
        monumentos=[("torre_monumental", 560), ("edificio_kavanagh", 1480), ("estacion_retiro", 2480)],
        siguiente="RECOLETA",
    ),

    6: dict(
        barrio="RECOLETA",
        cielo=("#4a90e0", "#8cc8f0", "#f2ece0"),
        nubes="#ffffff",
        sol=(300, 38, 8, "#fff4c0"),
        skyline=["frances", "parque"],
        estilos={"frances": 7, "italianizante": 2, "departamentos": 1},
        arboles=[("ficus", 3), ("palo_borracho", 2), ("jacaranda", 2), ("cipres", 1)],
        prob_arbol=0.6,
        props={"farola": 3, "banco": 2, "feria": 2, "kiosco": 1, "cesto": 2},
        suelo=("baldosa", "asfalto"),
        plaza=0.20, esquina=0.10,
        calles=["JUNIN", "V LOPEZ", "QUINTANA", "AV ALVEAR", "AZCUENAGA", "LAS HERAS"],
        trafico={"auto": 4, "taxi": 3, "colectivo": 1},
        monumentos=[("floralis_generica", 540), ("cementerio_recoleta", 1520), ("basilica_pilar", 2520)],
        siguiente="BARRIO NORTE",
    ),

    7: dict(
        barrio="BARRIO NORTE",
        cielo=("#4a94e4", "#90ccf2", "#f4ecdc"),
        nubes="#ffffff",
        sol=(800, 32, 8, "#fff4c0"),
        skyline=["frances"],
        estilos={"frances": 7, "italianizante": 1, "departamentos": 2, "local": 2},
        textos=["LIBROS", "FARMACIA", "CAFE", "FLORES", "OPTICA"],
        arboles=[("platano", 2), ("jacaranda", 1)],
        prob_arbol=0.55,
        props={"farola": 3, "banco": 2, "kiosco": 1, "parada": 1, "semaforo": 1, "cesto": 2},
        suelo=("baldosa", "asfalto"),
        plaza=0.10, esquina=0.12,
        calles=["AV SANTA FE", "AV CORDOBA", "PUEYRREDON", "AYACUCHO", "CALLAO", "AV ALVEAR"],
        trafico={"auto": 4, "taxi": 3, "colectivo": 2},
        monumentos=[("ateneo_grand_splendid", 520), ("palais_de_glace", 1500), ("facultad_medicina", 2480)],
        siguiente="PALERMO",
    ),

    8: dict(
        barrio="PALERMO",
        cielo=("#52a8ec", "#96d4f4", "#f0f4e8"),
        nubes="#ffffff",
        sol=(1050, 40, 8, "#fffbd0"),
        skyline=["parque", "casas"],
        estilos={"casa_baja": 3, "departamentos": 2, "mural": 3, "local": 1, "italianizante": 1},
        mural=["abstracto"],
        textos=["CAFE", "ARTE", "MODA", "HELADOS"],
        arboles=[("jacaranda", 3), ("palo_borracho", 2), ("platano", 2), ("sauce", 2), ("ombu", 1)],
        prob_arbol=0.75,
        props={"farola": 2, "banco": 3, "cesto": 2, "kiosco": 1, "semaforo": 1, "chori": 1},
        suelo=("sendero", "pasto"),
        especiales=["lagos"],
        plaza=0.45, esquina=0.06,
        calles=["HONDURAS", "SERRANO", "GURRUCHAGA", "THAMES", "CABRERA", "AV SANTA FE"],
        trafico={"auto": 3, "taxi": 1},
        monumentos=[("planetario", 560), ("jardin_japones", 1500), ("rosedal", 2480)],
        siguiente="ABASTO",
    ),

    9: dict(
        barrio="ABASTO",
        cielo=("#4a98e8", "#94cef4", "#f6e8cc"),
        nubes="#ffffff",
        sol=(400, 36, 8, "#fff4c0"),
        skyline=["casas", "centro"],
        estilos={"local": 3, "departamentos": 2, "mural": 3, "casa_baja": 2, "italianizante": 1, "torre_hormigon": 1},
        mural=["tango", "tango", "abstracto"],
        textos=["TANGO", "EMPANADAS", "PIZZA", "CAFE", "VINOS"],
        arboles=[("platano", 1)],
        prob_arbol=0.4,
        props={"farola": 3, "tango": 3, "kiosco": 1, "banco": 1, "cesto": 2, "parada": 1, "semaforo": 1},
        suelo=("baldosa", "asfalto"),
        plaza=0.08, esquina=0.12,
        calles=["CORRIENTES", "ANCHORENA", "AGUERO", "GARDEL", "LAVALLE", "ZELAYA"],
        trafico={"auto": 4, "taxi": 3, "colectivo": 2},
        monumentos=[("abasto_shopping", 560), ("estatua_gardel", 1360), ("casa_museo_gardel", 2300)],
        siguiente="ONCE",
    ),

    10: dict(
        barrio="ONCE",
        cielo=("#5aa0e6", "#9ed0f2", "#f6e4c8"),
        nubes="#fff6e6",
        sol=(1150, 36, 8, "#fff0a0"),
        skyline=["casas", "centro"],
        estilos={"local": 6, "departamentos": 2, "italianizante": 2, "frances": 1},
        textos=["TELAS", "BAZAR", "ROPA", "OFERTA", "BOTONES", "JUGUETES"],
        arboles=[("platano", 1)],
        prob_arbol=0.3,
        props={"feria": 5, "kiosco": 2, "parada": 1, "cabina": 1, "farola": 3, "cesto": 2, "semaforo": 1},
        suelo=("baldosa", "asfalto"),
        plaza=0.07, esquina=0.12,
        calles=["PUEYRREDON", "RIVADAVIA", "LAVALLE", "JUNIN", "LARREA", "PASCO"],
        trafico={"auto": 3, "taxi": 3, "colectivo": 4},
        monumentos=[("aguas_corrientes", 560), ("estacion_once", 1520), ("mausoleo_rivadavia", 2500)],
        siguiente="CONGRESO",
    ),

    11: dict(
        barrio="CONGRESO",
        cielo=("#4a94e6", "#8ecaf2", "#f2e8d6"),
        nubes="#fff6e6",
        sol=(450, 36, 9, "#ffeaa0"),
        skyline=["centro", "frances"],
        estilos={"frances": 4, "italianizante": 3, "art_deco": 1, "local": 1, "departamentos": 1},
        textos=["CAFE", "LIBROS", "BAR"],
        arboles=[("palmera", 2), ("ombu", 1), ("platano", 2), ("palo_borracho", 1)],
        prob_arbol=0.5,
        props={"farola": 3, "banco": 2, "bandera": 2, "kiosco": 1, "cesto": 2, "semaforo": 1},
        suelo=("baldosa", "asfalto"),
        especiales=["palomas"],
        plaza=0.15, esquina=0.10,
        calles=["AV DE MAYO", "CALLAO", "ENTRE RIOS", "RIVADAVIA", "SAENZ PENA", "POZOS"],
        trafico={"auto": 3, "taxi": 3, "colectivo": 3},
        monumentos=[("palacio_congreso", 560), ("confiteria_el_molino", 1360), ("monumento_dos_congresos", 2300)],
        siguiente="OBELISCO",
    ),

    12: dict(
        barrio="OBELISCO",
        cielo=("#2c3f94", "#b8689a", "#f6b078"),
        nubes="#ffd0b8",
        sol=(700, 120, 12, "#ffd890"),
        noche=0.30,
        luces=0.55,
        tinte=("#ff9a70", 0.07),
        skyline=["rascacielos", "centro"],
        fondo_alto=(50, 110),
        estilos={"local": 4, "art_deco": 2, "torre_hormigon": 2, "departamentos": 2, "italianizante": 2},
        textos=["TEATRO", "PIZZA", "LIBROS", "CINE", "CAFE", "BAR", "TANGO"],
        arboles=[("platano", 1)],
        prob_arbol=0.3,
        props={"farola": 3, "kiosco": 1, "semaforo": 2, "cesto": 2, "parada": 1},
        suelo=("baldosa", "asfalto"),
        plaza=0.06, esquina=0.14,
        calles=["CORRIENTES", "9 DE JULIO", "LAVALLE", "PELLEGRINI", "LIBERTAD", "SUIPACHA"],
        trafico={"auto": 5, "taxi": 5, "colectivo": 3},
        monumentos=[("teatro_gran_rex", 560), ("obelisco", 1380), ("teatro_colon", 2380)],
        siguiente="MONSERRAT",
    ),

    13: dict(
        barrio="MONSERRAT",
        cielo=("#3c3a86", "#d8647e", "#ffb860"),
        nubes="#ffb090",
        sol=(850, 126, 14, "#ffe090"),
        noche=0.34,
        luces=0.5,
        tinte=("#ff8a4a", 0.10),
        skyline=["centro", "casas"],
        estilos={"italianizante": 4, "casa_baja": 3, "frances": 2, "local": 1, "departamentos": 1},
        textos=["CAFE", "LIBROS", "ARTE"],
        arboles=[("platano", 1)],
        prob_arbol=0.4,
        props={"farol_colgante": 3, "farola": 2, "banco": 2, "tango": 2, "kiosco": 1, "cesto": 2},
        suelo=("baldosa", "adoquin"),
        plaza=0.10, esquina=0.12,
        calles=["AV DE MAYO", "BOLIVAR", "PERU", "ALSINA", "MORENO", "BELGRANO"],
        trafico={"auto": 3, "taxi": 3, "colectivo": 2},
        monumentos=[("cafe_tortoni", 520), ("palacio_barolo", 1440), ("san_ignacio", 2420)],
        siguiente="CONSTITUCION",
    ),

    14: dict(
        barrio="CONSTITUCION",
        cielo=("#1c2660", "#7a589a", "#e8886a"),
        nubes="#c898b0",
        sol=(1000, 132, 12, "#ffc080"),
        noche=0.52,
        luces=0.6,
        tinte=("#6a4a9a", 0.16),
        skyline=["industrial", "casas"],
        estilos={"galpon": 2, "fabrica": 2, "departamentos": 2, "local": 2, "casa_baja": 2, "torre_hormigon": 1},
        textos=["BAR", "KIOSCO", "PIZZA", "REMIS"],
        arboles=[("platano", 1)],
        prob_arbol=0.3,
        props={"farola": 4, "parada": 2, "kiosco": 1, "semaforo": 1, "cesto": 2},
        suelo=("baldosa", "vias"),
        plaza=0.10, esquina=0.12,
        calles=["AV SAN JUAN", "BRASIL", "LIMA", "SOLIS", "AV GARAY", "SALTA"],
        trafico={"auto": 3, "taxi": 3, "colectivo": 5},
        monumentos=[("estacion_constitucion", 600), ("iglesia_claretiana", 1560), ("autopista_25_de_mayo", 2480)],
        siguiente="LA BOMBONERA",
    ),

    15: dict(
        barrio="LA BOMBONERA",
        cielo=("#0c1236", "#202c68", "#4a4a92"),
        nubes="#5a5a9a",
        luna=(380, 34, 9),
        estrellas=True,
        noche=0.70,
        luces=0.65,
        tinte=("#1c2a70", 0.30),
        skyline=["estadio", "casas"],
        estilos={"conventillo": 6, "mural": 2, "casa_baja": 1, "fabrica": 1, "departamentos": 1},
        mural=["boca", "boca", "abstracto"],
        arboles=[("platano", 1)],
        prob_arbol=0.2,
        props={"banderin": 5, "chori": 3, "farola": 3, "banco": 1, "tango": 1, "cesto": 2},
        suelo=("baldosa", "asfalto"),
        especiales=["boca"],
        plaza=0.08, esquina=0.10,
        calles=["BRANDSEN", "DEL CROTTO", "AUSTRALIA", "ALTE BROWN", "IBERLUCEA"],
        trafico={"auto": 4, "taxi": 2, "colectivo": 3},
        monumentos=[("bombonera", 620), ("puente_avellaneda", 1560), ("tren_roca", 2480)],
        siguiente=None,
    ),
}
