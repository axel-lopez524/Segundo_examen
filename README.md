# Tequila Barullo

Sitio web conceptual de Tequila Barullo para la evaluación parcial de Desarrollo de Aplicaciones Web. Incluye siete páginas con navegación común, tres calculadoras procesadas en el servidor mediante formularios POST, componentes Bootstrap, un carrusel y una explicación del flujo web. No es un canal oficial de venta; la información comercial debe confirmarse con la marca.

## Requisitos

- Python 3.10 o posterior.
- `pip`.
- Conexión a Internet para cargar Bootstrap y las fuentes tipográficas desde sus CDN.

## Crear y activar el entorno virtual

Desde la carpeta del proyecto:

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows CMD**

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

## Ejecutar

```bash
python app.py
```

Abre [http://127.0.0.1:5000](http://127.0.0.1:5000). El sitio ofrece Inicio, Compra, Salario, Temperatura, Empresa, Servicios y Contacto. Las calculadoras validan sus entradas y presentan los datos y resultados en la página. La compra es una estimación académica; no procesa pedidos ni confirma precios oficiales. Solo para mayores de 18 años: disfruta con responsabilidad.

## Estructura

```text
app.py
templates/       base.html, index.html, calculadoras y páginas informativas
static/css/      Estilos
static/img/      Ilustraciones SVG locales
examen/          Explicación técnica y capturas de ejecución
```

La explicación, el diagrama Mermaid y la interpretación de cada cálculo están en [`examen/explicacion.md`](examen/explicacion.md).
Las capturas de ejecución están en [`examen/evidencias/`](examen/evidencias/).
