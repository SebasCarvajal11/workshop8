# Workshop — Sistema experto de precios dinámicos (CLIPS)

Implementación del **Workshop 5: Rule Based Systems**: motor de reglas de negocio para fijar precio y descuentos de un SKU según demanda, inventario, márgenes y políticas comerciales.

## Requisitos del enunciado

| Código | Significado |
|--------|-------------|
| DA / DB | Demanda alta / baja |
| OB | Existencias bajas |
| VA / VB | Ventas altas / bajas |
| MA / MB | Margen alto / bajo |
| TL | Lead time largo |
| PF | Financiamiento solicitado |
| EG | Envío gratis |
| DR | Devolución restringida |
| GE | Garantía extendida |

**Acciones:** subir precio (+10% por regla), bajar precio (−10%), cupón 5% (AD), o vetar descuento (¬AD) con prioridad en reglas **4** y **10**.

Las **11 reglas** están en `clips/pricing-rules.clp` y operan sobre la clase COOL **`Producto`** (12 slots: `da`…`ge`). La capa Python convierte métricas o respuestas de entrevista en una instancia `Producto`, ejecuta CLIPS vía [clipspy](https://github.com/noxdafox/clipspy) y consolida señales en una recomendación legible.

### Entrevista sí/no (rúbrica académica)

```powershell
pricing-expert --mode interview
```

Modo alternativo con umbrales numéricos: `pricing-expert --mode metrics`.

En la web: menú **Entrevista** → 12 preguntas → motor CLIPS.

## E-commerce web (El Mercantil)

Tienda en **React + Vite** (`web/`) con API **FastAPI** que ejecuta el mismo motor CLIPS. Cubre el Workshop 5 en interfaz:

| Ruta | Contenido |
|------|-----------|
| `/` | Portada: 4 SKU, simulador completo (métricas + PF/EG/DR/GE + lead time), proposiciones DA–GE, panel experto |
| `/entrevista` | 12 preguntas sí/no → instancia COOL `Producto` → 11 reglas |
| `/canasta` | Cotización por línea con CLIPS y financiamiento por ítem |
| `/product/:sku` | Ficha con simulador completo y enlace desde portada |

- Catálogo con precios dinámicos por SKU
- Simulador con umbrales del PDF y flags comerciales
- Carrito con cotización por reglas y panel de proposiciones/reglas disparadas

### Desarrollo (dos terminales)

```powershell
cd "d:\Workshop 8 Rules Business Engine"
.\.venv\Scripts\Activate.ps1
pip install -e .
pricing-api
```

```powershell
cd "d:\Workshop 8 Rules Business Engine\web"
pnpm install
# Si pnpm avisa de build scripts ignorados: pnpm approve-builds  (elegir esbuild)
pnpm dev
```

Abrir http://localhost:5173 (el proxy de Vite envía `/api` y `/media` al puerto 8000).

**Imágenes de producto:** colóquelas en `product-images/` en la raíz del proyecto (nombre descriptivo: por ejemplo «Audífonos…», «Silla ergonómica»). Formatos admitidos incluyen `.avif`, `.webp`, `.png`, `.jpg`, etc. Al iniciar la API se renombran y copian a `assets/products/` y `web/public/products/` como `sku-aud-02.avif`, etc. Sin API: ejecute `.\scripts\sync-product-images.ps1` (usa Python del `.venv`). La web sirve `/products/…`.

### Producción (una sola URL)

```powershell
cd web
pnpm install
pnpm build
cd ..
.\.venv\Scripts\uvicorn pricing_expert.api.main:app --host 0.0.0.0 --port 8000
```

Sirve API y frontend estático en http://localhost:8000.

## Estructura

```
clips/pricing-rules.clp    # Reglas CLIPS (obligatorio para evaluación)
clips/scenarios/           # Hechos de ejemplo para CLIPS IDE
product-images/            # Fotos de usuario → sincronización automática al catálogo
src/pricing_expert/        # OOP: métricas, evaluador, motor, CLI, API
web/                       # Frontend e-commerce (pnpm)
tests/                     # Casos de reglas representativas
```

## Instalación y uso

```powershell
cd "d:\Workshop 8 Rules Business Engine"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install pytest
python -m pricing_expert.cli
```

O tras instalar el paquete:

```powershell
pricing-expert
```

## CLIPS sin Python

1. Instalar [CLIPS](https://www.julesberg.com/clips/) 6.4+.
2. Abrir `clips/pricing-rules.clp` y cargar un escenario de `clips/scenarios/`.
3. `(reset)` → `(run)` → `(facts)` para ver `price-signal` y `discount-signal`.

## Pruebas

```powershell
pytest
```

## Notas de diseño

- **Salience** 100 y 90 en reglas 4 y 10 para reflejar vetos comerciales.
- Si coexisten subidas y bajas de precio, el resultado es `MIXED` (sin cambio neto automático).
- Los umbrales numéricos siguen el PDF (p. ej. &gt;1000 visitas/día = DA).

## Autoría académica

Desarrollo individual según lineamientos del taller (CLIPS + evaluación escrita + UX/OOP).
"# workshop8" 
