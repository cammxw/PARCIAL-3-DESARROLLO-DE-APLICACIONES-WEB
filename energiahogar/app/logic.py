from dataclasses import dataclass

DIAS_MES = 30


class EntradaInvalida(ValueError):
    pass


@dataclass
class Equipo:
    nombre: str
    potencia_w: float
    horas_dia: float


def convertir_numero(texto, campo):
    try:
        return float(str(texto).replace(",", ".").strip())
    except ValueError:
        raise EntradaInvalida(f"El valor de {campo} debe ser un numero")


def convertir_equipos(nombres, potencias, horas):
    equipos = []
    for nombre, potencia, hora in zip(nombres, potencias, horas):
        if not (nombre.strip() or potencia.strip() or hora.strip()):
            continue
        if not nombre.strip():
            raise EntradaInvalida("Todos los equipos deben tener nombre")
        w = convertir_numero(potencia, f"potencia de {nombre.strip()}")
        h = convertir_numero(hora, f"horas de {nombre.strip()}")
        if w <= 0:
            raise EntradaInvalida(f"La potencia de {nombre.strip()} debe ser mayor que cero")
        if not 0 <= h <= 24:
            raise EntradaInvalida(f"Las horas de {nombre.strip()} deben estar entre 0 y 24")
        equipos.append(Equipo(nombre.strip(), w, h))
    if not equipos:
        raise EntradaInvalida("Agrega al menos un equipo")
    return equipos


def consumo_mensual_kwh(potencia_w, horas_dia, dias=DIAS_MES):
    return potencia_w * horas_dia * dias / 1000


def analizar(equipos, tarifa, reduccion=0):
    if tarifa <= 0:
        raise EntradaInvalida("La tarifa debe ser mayor que cero")
    if not 0 <= reduccion <= 100:
        raise EntradaInvalida("La reduccion debe estar entre 0 y 100")
    detalle = [
        {"nombre": e.nombre, "kwh": consumo_mensual_kwh(e.potencia_w, e.horas_dia)}
        for e in equipos
    ]
    total = sum(d["kwh"] for d in detalle)
    for d in detalle:
        d["costo"] = d["kwh"] * tarifa
        d["porcentaje"] = d["kwh"] / total * 100 if total else 0
    detalle.sort(key=lambda d: d["kwh"], reverse=True)
    kwh_escenario = total * (1 - reduccion / 100)
    return {
        "detalle": detalle,
        "total_kwh": total,
        "total_costo": total * tarifa,
        "mayor": detalle[0]["nombre"],
        "reduccion": reduccion,
        "escenario_kwh": kwh_escenario,
        "escenario_costo": kwh_escenario * tarifa,
        "ahorro": (total - kwh_escenario) * tarifa,
    }
