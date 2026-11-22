# Módulo que define la clase Reserva integrando Cliente, Servicio, duración y estado.
from excepciones.errores_sistema import (
    ErrorReservaInvalida,
    ErrorServicioNoDisponible,
    ErrorValidacionDatos,
)
from modelos.cliente import Cliente
from modelos.entidad_base import EntidadSistema
from modelos.servicio import Servicio


class Reserva(EntidadSistema):
    """Gestiona el ciclo de vida de una reserva dentro de Software F."""

    # Estados permitidos para una reserva en el sistema.
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        # Se inicializa la clase base con el identificador de la reserva.
        super().__init__(identificador)
        # Se valida que el parámetro cliente sea una instancia válida de Cliente.
        if not isinstance(cliente, Cliente):
            raise ErrorValidacionDatos("La reserva requiere un objeto Cliente válido.")
        # Se valida que el parámetro servicio sea una instancia válida de Servicio.
        if not isinstance(servicio, Servicio):
            raise ErrorValidacionDatos("La reserva requiere un objeto Servicio válido.")
        # Se valida que la duración sea un número entero positivo.
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ErrorValidacionDatos("La duración de la reserva debe ser un entero mayor que cero.")

        # Se encapsulan los atributos principales de la reserva.
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = duracion_horas
        # Toda reserva inicia en estado PENDIENTE.
        self.__estado = "PENDIENTE"
        # Se inicializa el costo total calculado en cero.
        self.__costo_total = 0.0

    @property
    def cliente(self) -> Cliente:
        """Retorna el cliente asociado a la reserva."""
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        """Retorna el servicio asociado a la reserva."""
        return self.__servicio

    @property
    def duracion_horas(self) -> int:
        """Retorna la duración en horas de la reserva."""
        return self.__duracion_horas

    @property
    def estado(self) -> str:
        """Retorna el estado actual de la reserva."""
        return self.__estado

    @property
    def costo_total(self) -> float:
        """Retorna el costo total calculado de la reserva."""
        return self.__costo_total

    def validar_integridad(self) -> bool:
        """Valida que el cliente sea íntegro y que el servicio esté disponible."""
        # Se verifica la integridad de los datos del cliente.
        self.__cliente.validar_integridad()
        # Se comprueba que el servicio siga disponible antes de operar.
        if not self.__servicio.disponible:
            raise ErrorServicioNoDisponible(
                f"La reserva {self.identificador} no puede continuar: "
                f"el servicio '{self.__servicio.nombre_servicio}' no está disponible."
            )
        return True

    def calcular_costo_reserva(self, *args, **kwargs) -> float:
        """
        Método sobrecargado para calcular el costo de la reserva según parámetros opcionales
        (porcentaje_descuento y aplicar_iva) delegando en el servicio asociado.
        """
        # Se calcula y almacena el costo total usando el método polimórfico del servicio.
        self.__costo_total = self.__servicio.calcular_costo(self.__duracion_horas, *args, **kwargs)
        return self.__costo_total

    def confirmar_reserva(self, porcentaje_descuento: float = 0.0, aplicar_iva: bool = True) -> None:
        """Confirma la reserva si está PENDIENTE, valida disponibilidad y calcula su costo."""
        # Se verifica que la reserva se encuentre en estado PENDIENTE.
        if self.__estado != "PENDIENTE":
            raise ErrorReservaInvalida(
                f"Solo se pueden confirmar reservas en estado PENDIENTE. Estado actual: {self.__estado}."
            )
        # Se valida disponibilidad e integridad antes de confirmar.
        self.validar_integridad()
        # Se calcula el costo final aplicando descuento e IVA según corresponda.
        self.calcular_costo_reserva(porcentaje_descuento=porcentaje_descuento, aplicar_iva=aplicar_iva)
        # Se actualiza el estado a CONFIRMADA.
        self.__estado = "CONFIRMADA"

    def procesar_reserva(self) -> None:
        """Procesa una reserva previamente CONFIRMADA."""
        # Se exige que la reserva esté confirmada antes de procesarla.
        if self.__estado != "CONFIRMADA":
            raise ErrorReservaInvalida(
                f"No se puede procesar la reserva {self.identificador} en estado '{self.__estado}'."
            )
        # Se marca la reserva como PROCESADA.
        self.__estado = "PROCESADA"

    def cancelar_reserva(self, motivo: str = "Cancelación solicitada por el usuario") -> None:
        """Cancela una reserva válida siempre que no haya sido PROCESADA."""
        # Se exige que se proporcione un motivo de cancelación no vacío.
        if not isinstance(motivo, str) or not motivo.strip():
            raise ErrorValidacionDatos("Debe indicar un motivo válido para cancelar la reserva.")
        # No se permite cancelar una reserva ya procesada.
        if self.__estado == "PROCESADA":
            raise ErrorReservaInvalida(
                f"No se puede cancelar la reserva {self.identificador} porque ya fue PROCESADA."
            )
        # Se evita cancelar dos veces la misma reserva.
        if self.__estado == "CANCELADA":
            raise ErrorReservaInvalida(f"La reserva {self.identificador} ya está CANCELADA.")
        # Se actualiza el estado a CANCELADA.
        self.__estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        """Retorna una descripción completa del estado y costo de la reserva."""
        return (
            f"Reserva [{self.identificador}] | Estado: {self.estado} | "
            f"Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre_servicio} | "
            f"Duración: {self.duracion_horas}h | Total: ${self.costo_total:,.2f}"
        )
