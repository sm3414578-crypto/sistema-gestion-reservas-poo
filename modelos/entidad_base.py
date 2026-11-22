# Módulo que define la clase abstracta base EntidadSistema para Software F.
from abc import ABC, abstractmethod
from excepciones.errores_sistema import ErrorValidacionDatos


class EntidadSistema(ABC):
    """Clase base abstracta para entidades identificables del sistema."""

    def __init__(self, identificador: str):
        # Se asigna el identificador usando su property con validación.
        self.identificador = identificador

    @property
    def identificador(self) -> str:
        """Retorna el identificador encapsulado de la entidad."""
        return self.__identificador

    @identificador.setter
    def identificador(self, valor: str) -> None:
        """Valida que el identificador sea un texto no vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorValidacionDatos("El identificador de la entidad es obligatorio.")
        self.__identificador = valor.strip()

    @abstractmethod
    def validar_integridad(self) -> bool:
        """Verifica que la entidad cumpla sus reglas de integridad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna una representación resumida y legible de la entidad."""
        pass
