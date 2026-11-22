# Módulo que define la jerarquía de excepciones personalizadas de Software F.


class ErrorSistemaBase(Exception):
    """Clase base para todas las excepciones controladas del sistema."""

    def __init__(self, mensaje: str):
        # Se almacena el mensaje descriptivo del error.
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ErrorValidacionDatos(ErrorSistemaBase):
    """Se lanza cuando un dato no cumple con las reglas de formato o rango."""


class ErrorClienteInvalido(ErrorSistemaBase):
    """Se lanza cuando hay problemas de integridad o duplicidad en clientes."""


class ErrorServicioNoDisponible(ErrorSistemaBase):
    """Se lanza cuando un servicio no existe o no está disponible para reservar."""


class ErrorReservaInvalida(ErrorSistemaBase):
    """Se lanza cuando una operación o transición de estado de reserva no es válida."""


class ErrorCalculoFinanciero(ErrorSistemaBase):
    """Se lanza cuando ocurre un error en cálculos de tarifas, descuentos o IVA."""
