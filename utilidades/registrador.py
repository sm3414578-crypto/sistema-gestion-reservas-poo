# Módulo encargado del registro de eventos y errores en archivo de texto plano.
from datetime import datetime
from pathlib import Path


class RegistradorLogs:
    """Escribe eventos estructurados del sistema en un archivo .log."""

    def __init__(self, ruta_archivo: str = "logs/eventos_sistema.log"):
        # Se normaliza la ruta y se crea el directorio padre si no existe.
        self.ruta_archivo = Path(ruta_archivo)
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        # Se garantiza que el archivo de log exista desde el inicio.
        self.ruta_archivo.touch(exist_ok=True)

    def registrar_evento(self, nivel: str, origen: str, mensaje: str) -> None:
        """Agrega una línea con marca de tiempo, nivel, origen y mensaje al log."""
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel.upper()}] [{origen}] {mensaje}\n"
        with self.ruta_archivo.open("a", encoding="utf-8") as archivo:
            archivo.write(linea)
