# Generador de Investigadores — La Llamada de Cthulhu (7ª edición)

Generador rápido de personajes para el juego de rol *La Llamada de Cthulhu*
(7ª edición). Incluye dos versiones que hacen exactamente lo mismo:

- **`generador_personaje_cthulhu.html`** — versión web. Se abre directo en
  el navegador de cualquier dispositivo (celular, tablet o PC), sin instalar
  nada.
- **`generador_personaje_cthulhu.py`** — versión de consola en Python.

## ⚠️ Qué NO calcula este generador

A propósito, y de forma intencional, este generador **no calcula**:

- **Edad** (ni sus modificadores a características/EDU)
- **Movimiento**
- **Corpulencia**

Si tu mesa de juego los usa, deberás anotarlos y calcularlos aparte según
el manual.

## Qué SÍ calcula

- Las 9 características (FUE, CON, DES, APA, POD, SUERTE, TAM, INT, EDU)
- Atributos derivados: Puntos de Vida, Puntos de Magia, Cordura inicial y
  Bonificación de Daño
- Una ocupación (elegida o al azar) de una lista de 27, con sus habilidades
  (máximo 8) y los puntos para repartir entre ellas
- Puntos de interés personal (libres, sin límite de habilidades)
- Crédito, clase social, dinero y bienes iniciales, según la Tabla II del
  manual (para "Años 20" o "Actual")

## Uso

### Versión web
Abre `generador_personaje_cthulhu.html` en cualquier navegador (o publícalo
con GitHub Pages, ver más abajo).

### Versión Python
```bash
python3 generador_personaje_cthulhu.py
```

## Publicar la versión web con GitHub Pages (opcional)

Si quieres un link para compartir sin tener que enviar el archivo:

1. Ve a la configuración del repositorio → **Pages**.
2. En "Source", elige la rama `main` y la carpeta `/ (root)`.
3. Guarda. GitHub te dará una URL tipo
   `https://tu-usuario.github.io/tu-repo/generador_personaje_cthulhu.html`.

## Créditos

Basado en las reglas de *La Llamada de Cthulhu* 7ª edición (Chaosium / Edge
Entertainment). Este generador es un proyecto de fans, sin fines de lucro.
