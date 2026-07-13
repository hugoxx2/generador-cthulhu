"""
Generador de Personajes - La Llamada de Cthulhu (7a edicion)
--------------------------------------------------------------
NO calcula: Edad, Movimiento ni Corpulencia (a peticion del usuario).
SI calcula:
  - Caracteristicas (FUE, CON, DES, APA, POD, SUERTE, TAM, INT, EDU)
  - Atributos derivados: Puntos de Vida, Puntos de Magia, Cordura inicial,
    Bonificacion de Dano
  - Ocupacion elegida o al azar, con sus habilidades (maximo 8) y los
    puntos para repartir entre ellas
  - Puntos de interes personal (libres, sin limite de numero de habilidades)
  - Credito, clase social, dinero y bienes segun la Tabla II del manual

Uso:
    python3 generador_personaje_cthulhu.py
"""

import random

# =====================================================================
# 1. CARACTERISTICAS
# =====================================================================

def d6():
    return random.randint(1, 6)


def tirar_3d6():
    return d6() + d6() + d6()


def tirar_2d6():
    return d6() + d6()


def generar_caracteristicas():
    return {
        "FUE": tirar_3d6() * 5,
        "CON": tirar_3d6() * 5,
        "DES": tirar_3d6() * 5,
        "APA": tirar_3d6() * 5,
        "POD": tirar_3d6() * 5,
        "SUERTE": tirar_3d6() * 5,
        "TAM": (tirar_2d6() + 6) * 5,
        "INT": (tirar_2d6() + 6) * 5,
        "EDU": (tirar_3d6() + 3) * 5,
    }


# =====================================================================
# 2. ATRIBUTOS DERIVADOS (sin Movimiento ni Corpulencia)
# =====================================================================

def calcular_bonif_dano(fue, tam):
    suma = fue + tam
    tabla = [
        (64, "-2"), (84, "-1"), (124, "0"), (164, "+1D4"), (204, "+1D6"),
        (284, "+2D6"), (364, "+3D6"), (444, "+4D6"), (524, "+5D6"),
    ]
    for limite, bono in tabla:
        if suma <= limite:
            return bono
    extra = (suma - 524) // 80 + 1
    return f"+{5 + extra}D6"


def generar_atributos_derivados(c):
    return {
        "Puntos de Vida": (c["CON"] + c["TAM"]) // 10,
        "Puntos de Magia": c["POD"] // 5,
        "Cordura inicial": c["POD"],
        "Bonificacion de Dano": calcular_bonif_dano(c["FUE"], c["TAM"]),
    }


# =====================================================================
# 3. OCUPACIONES DE EJEMPLO (max. 8 habilidades cada una)
# =====================================================================

def _max2(c, op1, op2):
    """Puntos usando la mejor de dos caracteristicas x2."""
    return max(c[op1], c[op2]) * 2


OCUPACIONES = {
    "Abogado": {
        "habilidades": ["Buscar libros", "Contabilidad", "Derecho", "Psicologia",
                         "Habilidad interpersonal", "Habilidad interpersonal",
                         "Habilidad libre", "Habilidad libre"],
        "credito": (30, 80), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Agente de policia": {
        "habilidades": ["Armas de fuego", "Combatir (Pelea)", "Derecho", "Descubrir",
                         "Primeros auxilios", "Psicologia", "Habilidad interpersonal",
                         "Conducir automovil o Equitacion"],
        "credito": (9, 30), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Anticuario": {
        "habilidades": ["Arte/Artesania", "Descubrir", "Historia", "Otras lenguas",
                         "Tasacion", "Habilidad libre"],
        "credito": (30, 70), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Artista": {
        "habilidades": ["Arte/Artesania", "Descubrir", "Historia o Naturaleza",
                         "Otras lenguas", "Psicologia", "Habilidad interpersonal",
                         "Habilidad libre", "Habilidad libre"],
        "credito": (9, 50), "formula_txt": "EDU x2 + max(POD,DES) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "POD", "DES"),
    },
    "Atleta profesional": {
        "habilidades": ["Combatir (Pelea)", "Equitacion", "Lanzar", "Nadar",
                         "Saltar", "Trepar", "Habilidad interpersonal", "Habilidad libre"],
        "credito": (9, 70), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Bibliotecario": {
        "habilidades": ["Buscar libros", "Contabilidad", "Lengua propia", "Otras lenguas",
                         "Especialidad libre", "Especialidad libre",
                         "Especialidad libre", "Especialidad libre"],
        "credito": (9, 35), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Clerigo": {
        "habilidades": ["Buscar libros", "Contabilidad", "Escuchar", "Historia",
                         "Otras lenguas", "Psicologia", "Habilidad interpersonal",
                         "Habilidad libre"],
        "credito": (9, 60), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Criminal": {
        "habilidades": ["Descubrir", "Psicologia", "Sigilo", "Habilidad interpersonal",
                         "Armas de fuego/Cerrajeria/Combatir/Disfrazarse/"
                         "Juego de manos/Mecanica/Tasacion (elige 4)"],
        "credito": (5, 65), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Diletante": {
        "habilidades": ["Armas de fuego", "Arte/Artesania", "Equitacion",
                         "Habilidad interpersonal", "Habilidad libre",
                         "Habilidad libre", "Habilidad libre"],
        "credito": (50, 99), "formula_txt": "EDU x2 + APA x2",
        "puntos": lambda c: c["EDU"] * 2 + c["APA"] * 2,
    },
    "Escritor": {
        "habilidades": ["Arte (Literatura)", "Buscar libros", "Historia", "Lengua propia",
                         "Naturaleza o Ciencias ocultas", "Habilidad libre"],
        "credito": (9, 30), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Fanatico": {
        "habilidades": ["Historia", "Psicologia", "Sigilo", "Habilidad interpersonal",
                         "Habilidad interpersonal", "Habilidad libre",
                         "Habilidad libre", "Habilidad libre"],
        "credito": (0, 30), "formula_txt": "EDU x2 + max(APA,POD) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "APA", "POD"),
    },
    "Granjero": {
        "habilidades": ["Arte/Artesania (Agricultura)", "Conducir automovil", "Mecanica",
                         "Naturaleza", "Seguir rastros", "Habilidad interpersonal",
                         "Habilidad libre"],
        "credito": (9, 30), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Ingeniero": {
        "habilidades": ["Arte/Artesania (Dibujo tecnico)", "Buscar libros",
                         "Ciencia (Ingenieria)", "Ciencia (Fisica)", "Conducir maquinaria",
                         "Electricidad", "Mecanica", "Habilidad libre"],
        "credito": (30, 60), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Inspector de policia": {
        "habilidades": ["Armas de fuego", "Arte/Artesania o Disfrazarse", "Derecho",
                         "Descubrir", "Escuchar", "Psicologia", "Habilidad interpersonal",
                         "Habilidad libre"],
        "credito": (20, 50), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Interprete": {
        "habilidades": ["Arte/Artesania (Interpretacion)", "Disfrazarse", "Escuchar",
                         "Psicologia", "Habilidad interpersonal", "Habilidad interpersonal",
                         "Habilidad libre", "Habilidad libre"],
        "credito": (9, 70), "formula_txt": "EDU x2 + APA x2",
        "puntos": lambda c: c["EDU"] * 2 + c["APA"] * 2,
    },
    "Investigador privado": {
        "habilidades": ["Arte/Artesania (Fotografia)", "Buscar libros", "Derecho",
                         "Descubrir", "Disfrazarse", "Psicologia", "Habilidad interpersonal",
                         "Habilidad libre"],
        "credito": (9, 30), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Medico": {
        "habilidades": ["Ciencia (Biologia)", "Ciencia (Farmacologia)", "Medicina",
                         "Otras lenguas (latin)", "Primeros auxilios", "Psicologia",
                         "Especialidad libre", "Especialidad libre"],
        "credito": (30, 80), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Miembro de una tribu": {
        "habilidades": ["Ciencias ocultas", "Combatir o Lanzar", "Descubrir", "Escuchar",
                         "Naturaleza", "Supervivencia", "Trepar"],
        "credito": (0, 15), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Misionero": {
        "habilidades": ["Arte/Artesania", "Medicina", "Mecanica", "Naturaleza",
                         "Habilidad interpersonal", "Habilidad libre", "Habilidad libre"],
        "credito": (0, 30), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Musico": {
        "habilidades": ["Arte/Artesania (Instrumento)", "Escuchar", "Psicologia",
                         "Habilidad interpersonal", "Habilidad libre", "Habilidad libre",
                         "Habilidad libre", "Habilidad libre"],
        "credito": (9, 30), "formula_txt": "EDU x2 + max(DES,POD) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "POD"),
    },
    "Oficial militar": {
        "habilidades": ["Armas de fuego", "Contabilidad", "Psicologia", "Orientarse",
                         "Supervivencia", "Habilidad interpersonal", "Habilidad interpersonal",
                         "Habilidad libre"],
        "credito": (20, 70), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Parapsicologo": {
        "habilidades": ["Antropologia", "Arte/Artesania (Fotografia)", "Buscar libros",
                         "Ciencias ocultas", "Historia", "Otras lenguas", "Psicologia",
                         "Habilidad libre"],
        "credito": (9, 30), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Periodista": {
        "habilidades": ["Arte/Artesania (Fotografia)", "Buscar libros", "Historia",
                         "Lengua propia", "Psicologia", "Habilidad interpersonal",
                         "Habilidad libre", "Habilidad libre"],
        "credito": (9, 30), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Piloto": {
        "habilidades": ["Ciencia (Astronomia)", "Conducir maquinaria", "Electricidad",
                         "Mecanica", "Orientarse", "Pilotar (aeronave)", "Habilidad libre",
                         "Habilidad libre"],
        "credito": (20, 70), "formula_txt": "EDU x2 + DES x2",
        "puntos": lambda c: c["EDU"] * 2 + c["DES"] * 2,
    },
    "Pirata informatico": {
        "habilidades": ["Buscar libros", "Descubrir", "Electricidad", "Electronica",
                         "Informatica", "Habilidad interpersonal", "Habilidad libre",
                         "Habilidad libre"],
        "credito": (10, 70), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Profesor de universidad": {
        "habilidades": ["Buscar libros", "Lengua propia", "Otras lenguas", "Psicologia",
                         "Especialidad libre", "Especialidad libre", "Especialidad libre",
                         "Especialidad libre"],
        "credito": (20, 70), "formula_txt": "EDU x4",
        "puntos": lambda c: c["EDU"] * 4,
    },
    "Soldado": {
        "habilidades": ["Armas de fuego", "Combatir", "Esquivar", "Sigilo",
                         "Supervivencia", "Trepar o Nadar", "Habilidad libre",
                         "Habilidad libre"],
        "credito": (9, 30), "formula_txt": "EDU x2 + max(DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + _max2(c, "DES", "FUE"),
    },
    "Vagabundo": {
        "habilidades": ["Escuchar", "Orientarse", "Saltar", "Sigilo", "Trepar",
                         "Habilidad interpersonal", "Habilidad libre", "Habilidad libre"],
        "credito": (0, 5), "formula_txt": "EDU x2 + max(APA,DES,FUE) x2",
        "puntos": lambda c: c["EDU"] * 2 + max(c["APA"], c["DES"], c["FUE"]) * 2,
    },
}


# =====================================================================
# 4. TABLA II: DINERO Y PROPIEDADES
# =====================================================================

TABLA_CREDITO = {
    "años20": [
        # (cr_min, cr_max, clase, mult_dinero, mult_bienes, gasto_dia)
        (0, 0, "Indigente", 0, 0, 0.5),
        (1, 9, "Pobre", 1, 10, 2),
        (10, 49, "Clase media", 2, 50, 10),
        (50, 89, "Adinerado", 5, 500, 50),
        (90, 98, "Rico", 20, 2000, 250),
        (99, 99, "Inmensamente rico", None, None, 5000),
    ],
    "actual": [
        (0, 0, "Indigente", 0, 0, 10),
        (1, 9, "Pobre", 20, 200, 40),
        (10, 49, "Clase media", 40, 1000, 200),
        (50, 89, "Adinerado", 100, 10000, 1000),
        (90, 98, "Rico", 400, 40000, 5000),
        (99, 99, "Inmensamente rico", None, None, 100000),
    ],
}


def calcular_dinero(credito, era="años20"):
    for cr_min, cr_max, clase, mult_dinero, mult_bienes, gasto in TABLA_CREDITO[era]:
        if cr_min <= credito <= cr_max:
            if clase == "Indigente":
                dinero = 0.5 if era == "años20" else 10
                bienes = "Ninguna"
            elif clase == "Inmensamente rico":
                dinero = 50000 if era == "años20" else 1_000_000
                bienes = "5.000.000$ o mas" if era == "años20" else "100.000.000$ o mas"
            else:
                dinero = credito * mult_dinero
                bienes = f"{credito * mult_bienes} $"
            return {"clase_social": clase, "dinero": dinero, "bienes": bienes,
                    "nivel_de_gasto": gasto}
    raise ValueError("Credito fuera de rango (0-99)")


# =====================================================================
# 5. GENERADOR DE PERSONAJE
# =====================================================================

def generar_personaje(nombre="Investigador", ocupacion=None, era="años20"):
    c = generar_caracteristicas()
    derivados = generar_atributos_derivados(c)

    if ocupacion is None:
        ocupacion = random.choice(list(OCUPACIONES.keys()))
    datos_ocup = OCUPACIONES[ocupacion]

    puntos_ocupacion = datos_ocup["puntos"](c)
    puntos_interes = c["INT"] * 2  # libres, sin limite de numero de habilidades

    cr_min, cr_max = datos_ocup["credito"]
    credito = random.randint(cr_min, cr_max)
    dinero_info = calcular_dinero(credito, era)

    return {
        "nombre": nombre,
        "ocupacion": ocupacion,
        "era": era,
        "caracteristicas": c,
        "derivados": derivados,
        "habilidades_ocupacion": datos_ocup["habilidades"],
        "puntos_ocupacion": puntos_ocupacion,
        "formula_ocupacion": datos_ocup["formula_txt"],
        "puntos_interes_personal": puntos_interes,
        "credito": credito,
        **dinero_info,
    }


def mostrar_ficha(f):
    print(f"\n=== {f['nombre']} — {f['ocupacion']} ({f['era']}) ===\n")

    print("--- Caracteristicas ---")
    for k, v in f["caracteristicas"].items():
        print(f"{k:8s}: {v}")

    print("\n--- Atributos derivados ---")
    for k, v in f["derivados"].items():
        print(f"{k}: {v}")

    print("\n--- Habilidades de ocupacion (max. 8) ---")
    for h in f["habilidades_ocupacion"]:
        print(f" - {h}")
    print(f"Puntos para repartir: {f['puntos_ocupacion']} ({f['formula_ocupacion']})")

    print("\n--- Interes personal (habilidades libres, sin limite de numero) ---")
    print(f"Puntos disponibles (INT x2): {f['puntos_interes_personal']}")

    print("\n--- Credito y dinero ---")
    print(f"Credito: {f['credito']} ({f['clase_social']})")
    print(f"Dinero: {f['dinero']} $")
    print(f"Bienes: {f['bienes']}")
    print(f"Nivel de gasto: {f['nivel_de_gasto']} $/dia")


def mostrar_ejemplo():
    """Ejemplo de referencia, similar al Harvey Walters del manual,
       para orientarse si te pierdes."""
    print("""
--- EJEMPLO DE REFERENCIA ---
Harvey Walters, Periodista, años 20.
Caracteristicas: FUE 20  CON 70  TAM 80  DES 55  APA 70  INT 85  POD 80  EDU 84  SUERTE 45
Derivados: PV 15  PM 16  Cordura inicial 80  Bonif. de Dano +0

Ocupacion (Periodista) -> puntos = EDU x4 = 336, para repartir entre:
  Arte/Artesania (Fotografia), Buscar libros, Historia, Lengua propia,
  Psicologia, Encanto (habilidad interpersonal) y dos habilidades libres.

Interes personal -> puntos = INT x2 = 170, para las habilidades que quieras.

Credito inicial: 45 -> Clase media -> Dinero 90 $, Bienes 2.250 $, Gasto 10 $/dia.
------------------------------
""")


if __name__ == "__main__":
    print("Ocupaciones disponibles:", ", ".join(OCUPACIONES.keys()))
    nombre = input("\nNombre del personaje (Enter para 'Investigador'): ").strip() or "Investigador"
    ocupacion = input("Ocupacion (Enter para elegir al azar): ").strip()
    ocupacion = ocupacion if ocupacion in OCUPACIONES else None
    era = input("Era: 'años20' o 'actual' (Enter para años20): ").strip() or "años20"

    mostrar_ejemplo()
    ficha = generar_personaje(nombre, ocupacion, era)
    mostrar_ficha(ficha)