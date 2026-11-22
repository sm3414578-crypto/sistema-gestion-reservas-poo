# Módulo controlador que gestiona listas internas, excepciones encadenadas y logs.
from typing import List, Optional
from excepciones.errores_sistema import (
    ErrorClienteInvalido,
    ErrorReservaInvalida,
    ErrorServicioNoDisponible,
    ErrorSistemaBase,
)
from modelos.cliente import Cliente
from modelos.reserva import Reserva
from modelos.servicio import Servicio
from utilidades.registrador import RegistradorLogs


class GestorSoftwareF:
    """Coordina clientes, servicios, reservas en memoria y registro en logs."""

    def __init__(self, ruta_log: str = "logs/eventos_sistema.log"):
        # Listas internas en memoria que reemplazan cualquier base de datos.
        self.__clientes: List[Cliente] = []
        self.__servicios: List[Servicio] = []
        self.__reservas: List[Reserva] = []
        # Instancia encargada de escribir eventos y errores en el archivo de logs.
        self.__logger = RegistradorLogs(ruta_log)
        # Se registra el inicio del sistema en el archivo de logs.
        self.__logger.registrar_evento("INFO", "SISTEMA", "Software F iniciado sin base de datos.")

    @property
    def clientes(self) -> List[Cliente]:
        """Retorna una copia de la lista interna de clientes."""
        return list(self.__clientes)

    @property
    def servicios(self) -> List[Servicio]:
        """Retorna una copia de la lista interna de servicios."""
        return list(self.__servicios)

    @property
    def reservas(self) -> List[Reserva]:
        """Retorna una copia de la lista interna de reservas."""
        return list(self.__reservas)

    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Registra un cliente válido en la lista interna evitando duplicados."""
        try:
            # Se verifica que el objeto sea de tipo Cliente.
            if not isinstance(cliente, Cliente):
                raise ErrorClienteInvalido("El objeto proporcionado no es un Cliente válido.")
            # Se comprueba que no exista otro cliente con el mismo identificador.
            if any(c.identificador == cliente.identificador for c in self.__clientes):
                raise ErrorClienteInvalido(f"Ya existe un cliente con el ID '{cliente.identificador}'.")
        except ErrorSistemaBase as error_negocio:
            # Se registra el fallo en el archivo de logs sin detener la ejecución.
            self.__logger.registrar_evento("ERROR", "CLIENTES", str(error_negocio))
            return False
        else:
            # Si no hubo errores, se agrega el cliente a la lista interna.
            self.__clientes.append(cliente)
            self.__logger.registrar_evento("INFO", "CLIENTES", f"Cliente registrado: {cliente.obtener_resumen()}")
            return True
        finally:
            # Bloque de auditoría que siempre registra el tamaño actual de la lista.
            self.__logger.registrar_evento("DEBUG", "CLIENTES", f"Total de clientes en memoria: {len(self.__clientes)}")

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Registra un servicio especializado en la lista interna del catálogo."""
        try:
            # Se verifica que el objeto herede de Servicio.
            if not isinstance(servicio, Servicio):
                raise ErrorServicioNoDisponible("El objeto proporcionado no es un Servicio válido.")
            # Se evita registrar dos servicios con el mismo identificador.
            if any(s.identificador == servicio.identificador for s in self.__servicios):
                raise ErrorServicioNoDisponible(f"Ya existe un servicio con el ID '{servicio.identificador}'.")
        except ErrorSistemaBase as error_negocio:
            # Se registra el error en el log y se indica que la operación falló.
            self.__logger.registrar_evento("ERROR", "SERVICIOS", str(error_negocio))
            return False
        else:
            # Si es válido, se añade el servicio a la lista interna.
            self.__servicios.append(servicio)
            self.__logger.registrar_evento("INFO", "SERVICIOS", f"Servicio registrado: {servicio.obtener_resumen()}")
            return True
        finally:
            # Se registra el estado actual de la lista de servicios.
            self.__logger.registrar_evento("DEBUG", "SERVICIOS", f"Total de servicios en memoria: {len(self.__servicios)}")

    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        """Busca un cliente por ID dentro de la lista interna."""
        for cliente in self.__clientes:
            if cliente.identificador == id_cliente:
                return cliente
        return None

    def buscar_servicio(self, id_servicio: str) -> Optional[Servicio]:
        """Busca un servicio por ID dentro de la lista interna."""
        for servicio in self.__servicios:
            if servicio.identificador == id_servicio:
                return servicio
        return None

    def crear_y_confirmar_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion_horas: int,
        porcentaje_descuento: float = 0.0,
        aplicar_iva: bool = True,
    ) -> Optional[Reserva]:
        """Crea y confirma una reserva usando encadenamiento de excepciones."""
        try:
            # Se verifica que no exista otra reserva con el mismo ID.
            if any(r.identificador == id_reserva for r in self.__reservas):
                raise ErrorReservaInvalida(f"Ya existe una reserva con el ID '{id_reserva}'.")

            # Se busca el cliente en la lista interna.
            cliente = self.buscar_cliente(id_cliente)
            if cliente is None:
                raise ErrorClienteInvalido(f"Cliente con ID '{id_cliente}' no encontrado.")

            # Se busca el servicio en la lista interna.
            servicio = self.buscar_servicio(id_servicio)
            if servicio is None:
                raise ErrorServicioNoDisponible(f"Servicio con ID '{id_servicio}' no encontrado.")

            # Se crea la reserva y se intenta confirmar.
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion_horas)
            nueva_reserva.confirmar_reserva(porcentaje_descuento=porcentaje_descuento, aplicar_iva=aplicar_iva)

        except ErrorSistemaBase as error_origen:
            # Se encadena la excepción original dentro de ErrorReservaInvalida (raise ... from ...).
            try:
                raise ErrorReservaInvalida(
                    f"Error al procesar la reserva '{id_reserva}': {error_origen.mensaje}"
                ) from error_origen
            except ErrorReservaInvalida as error_encadenado:
                causa_raiz = type(error_encadenado.__cause__).__name__
                self.__logger.registrar_evento(
                    "ERROR",
                    "RESERVAS",
                    f"{error_encadenado} | Causa encadenada ({causa_raiz}): {error_origen}",
                )
                return None
        else:
            # Se guarda la reserva confirmada en la lista interna.
            self.__reservas.append(nueva_reserva)
            self.__logger.registrar_evento("INFO", "RESERVAS", f"Reserva confirmada: {nueva_reserva.obtener_resumen()}")
            return nueva_reserva
        finally:
            # Se registra la cantidad total de reservas en memoria.
            self.__logger.registrar_evento("DEBUG", "RESERVAS", f"Total de reservas en memoria: {len(self.__reservas)}")

    def procesar_reserva_por_id(self, id_reserva: str) -> bool:
        """Marca como PROCESADA una reserva confirmada existente."""
        try:
            # Se busca la reserva por su identificador.
            reserva = next((r for r in self.__reservas if r.identificador == id_reserva), None)
            if reserva is None:
                raise ErrorReservaInvalida(f"No se encontró la reserva '{id_reserva}' para procesar.")
            # Se ejecuta la transición de estado a PROCESADA.
            reserva.procesar_reserva()
        except ErrorSistemaBase as error:
            self.__logger.registrar_evento("ERROR", "RESERVAS", str(error))
            return False
        else:
            self.__logger.registrar_evento("INFO", "RESERVAS", f"Reserva procesada: {id_reserva}")
            return True

    def cancelar_reserva_por_id(self, id_reserva: str, motivo: str) -> bool:
        """Cancela de forma controlada una reserva si su estado lo permite."""
        try:
            # Se busca la reserva por su identificador.
            reserva = next((r for r in self.__reservas if r.identificador == id_reserva), None)
            if reserva is None:
                raise ErrorReservaInvalida(f"No se encontró la reserva '{id_reserva}' para cancelar.")
            # Se ejecuta la cancelación con validación de estado y motivo.
            reserva.cancelar_reserva(motivo)
        except ErrorSistemaBase as error:
            self.__logger.registrar_evento("ERROR", "RESERVAS", str(error))
            return False
        else:
            self.__logger.registrar_evento("INFO", "RESERVAS", f"Reserva cancelada ({id_reserva}): {motivo}")
            return True
