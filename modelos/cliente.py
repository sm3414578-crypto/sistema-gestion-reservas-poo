# Módulo que define la clase Cliente con encapsulación y validaciones estrictas.
import re
from excepciones.errores_sistema import ErrorValidacionDatos, ErrorClienteInvalido
from modelos.entidad_base import EntidadSistema


class Cliente(EntidadSistema):
    """Representa a un cliente registrado en Software F."""

    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        # Se inicializa la clase base con el identificador del cliente.
        super().__init__(identificador)
        # Se asignan los atributos mediante setters para validar los datos.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        # Se comprueba que el cliente cumpla con todos los datos requeridos.
        self.validar_integridad()

    @property
    def nombre(self) -> str:
        """Retorna el nombre completo encapsulado del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida que el nombre tenga al menos 3 caracteres."""
        # Se verifica que sea texto y no quede vacío al quitar espacios.
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorValidacionDatos("El nombre del cliente debe tener al menos 3 caracteres.")
        # Se guarda el nombre limpio en el atributo privado.
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico encapsulado del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida que el correo tenga un formato válido."""
        # Se define una expresión regular básica para validar correos.
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        # Se comprueba que el texto cumpla con el formato de correo.
        if not isinstance(valor, str) or not re.match(patron, valor.strip()):
            raise ErrorValidacionDatos(f"El correo electrónico '{valor}' no tiene un formato válido.")
        # Se guarda el correo en minúsculas y sin espacios extra.
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Retorna el número de teléfono encapsulado del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono tenga entre 7 y 15 dígitos numéricos."""
        # Se verifica que todos los caracteres sean dígitos y tengan longitud válida.
        if not isinstance(valor, str) or not valor.isdigit() or not (7 <= len(valor) <= 15):
            raise ErrorValidacionDatos("El teléfono debe contener únicamente entre 7 y 15 dígitos.")
        # Se almacena el teléfono validado.
        self.__telefono = valor

    def validar_integridad(self) -> bool:
        """Verifica que los datos personales del cliente estén completos."""
        # Se comprueba que ningún dato obligatorio esté vacío.
        if not self.__nombre or not self.__correo or not self.__telefono:
            raise ErrorClienteInvalido("Los datos personales del cliente están incompletos.")
        return True

    def obtener_resumen(self) -> str:
        """Retorna una descripción legible del cliente."""
        return (
            f"Cliente [{self.identificador}] - {self.nombre} | "
            f"Correo: {self.correo} | Tel: {self.telefono}"
        )
