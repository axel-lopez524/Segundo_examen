from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from flask import Flask, render_template, request


app = Flask(__name__)
app.config["SECRET_KEY"] = "portal-servicios-local"

CENTAVO = Decimal("0.01")


def parse_decimal(value: str, label: str) -> Decimal:
    try:
        number = Decimal(value)
    except (InvalidOperation, TypeError):
        raise ValueError(f"Escribe un valor numérico válido para {label}.") from None
    if not number.is_finite():
        raise ValueError(f"Escribe un valor numérico válido para {label}.")
    return number


def money(value: Decimal) -> str:
    return f"{value.quantize(CENTAVO, rounding=ROUND_HALF_UP):,.2f}"


def temperature_value(value: Decimal) -> str:
    return f"{value.quantize(CENTAVO, rounding=ROUND_HALF_UP):f}".rstrip("0").rstrip(".")


@app.get("/")
def inicio():
    return render_template("index.html", title="Inicio")


@app.route("/compra", methods=["GET", "POST"])
def compra():
    result = None
    error = None
    form = {"cantidad": "", "precio": ""}

    if request.method == "POST":
        form = {"cantidad": request.form.get("cantidad", "").strip(),
                "precio": request.form.get("precio", "").strip()}
        try:
            cantidad_decimal = parse_decimal(form["cantidad"], "la cantidad")
            if cantidad_decimal != cantidad_decimal.to_integral_value() or cantidad_decimal <= 0:
                raise ValueError("La cantidad debe ser un número entero mayor que cero.")
            precio = parse_decimal(form["precio"], "el precio unitario")
            if precio < 0:
                raise ValueError("El precio unitario no puede ser negativo.")
            cantidad = int(cantidad_decimal)
            subtotal = precio * cantidad
            descuento = subtotal * Decimal("0.10") if subtotal > Decimal("1000") else Decimal("0")
            result = {
                "cantidad": cantidad,
                "precio": money(precio),
                "subtotal": money(subtotal),
                "descuento": money(descuento),
                "total": money(subtotal - descuento),
                "aplica_descuento": descuento > 0,
            }
        except ValueError as exc:
            error = str(exc)

    return render_template("compra.html", title="Compra", form=form, result=result, error=error)


@app.route("/salario", methods=["GET", "POST"])
def salario():
    result = None
    error = None
    form = {"horas": "", "pago_hora": ""}

    if request.method == "POST":
        form = {"horas": request.form.get("horas", "").strip(),
                "pago_hora": request.form.get("pago_hora", "").strip()}
        try:
            horas = parse_decimal(form["horas"], "las horas trabajadas")
            pago_hora = parse_decimal(form["pago_hora"], "el pago por hora")
            if horas < 0 or pago_hora < 0:
                raise ValueError("Las horas y el pago por hora no pueden ser negativos.")
            horas_normales = min(horas, Decimal("40"))
            horas_extra = max(horas - Decimal("40"), Decimal("0"))
            total = horas_normales * pago_hora + horas_extra * pago_hora * Decimal("2")
            result = {
                "horas": temperature_value(horas),
                "pago_hora": money(pago_hora),
                "horas_normales": temperature_value(horas_normales),
                "horas_extra": temperature_value(horas_extra),
                "total": money(total),
            }
        except ValueError as exc:
            error = str(exc)

    return render_template("salario.html", title="Salario", form=form, result=result, error=error)


@app.route("/temperatura", methods=["GET", "POST"])
def temperatura():
    result = None
    error = None
    form = {"celsius": ""}

    if request.method == "POST":
        form = {"celsius": request.form.get("celsius", "").strip()}
        try:
            celsius = parse_decimal(form["celsius"], "la temperatura en Celsius")
            kelvin = celsius + Decimal("273.15")
            if kelvin < 0:
                raise ValueError("La temperatura no puede ser inferior al cero absoluto (-273.15 °C).")
            fahrenheit = celsius * Decimal("9") / Decimal("5") + Decimal("32")
            result = {
                "celsius": temperature_value(celsius),
                "fahrenheit": temperature_value(fahrenheit),
                "kelvin": temperature_value(kelvin),
            }
        except ValueError as exc:
            error = str(exc)

    return render_template("temperatura.html", title="Temperatura", form=form, result=result, error=error)


@app.get("/empresa")
def empresa():
    return render_template("empresa.html", title="Empresa")


@app.get("/servicios")
def servicios():
    return render_template("servicios.html", title="Servicios")


@app.get("/contacto")
def contacto():
    return render_template("contacto.html", title="Contacto")


if __name__ == "__main__":
    app.run(debug=True)
