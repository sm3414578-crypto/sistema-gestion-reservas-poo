# Módulo que define la clase abstracta Servicio y tres servicios especializados.
from abc import abstractmethod
from excepciones.errores_sistema import (
    ErrorCalculoFinanciero,
    ErrorServicioNoDisponible,
    ErrorValidacionDatos,
)
from modelos.entidad_base import EntidadSistema


class Servicio(EntidadSistema):
    """Clase abstracta base para los servicios ofrecidos por Software F."""

    def __init__(self, identificador: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        # Se inicializa la clase base con el identificador del servicio.
        super().__init__(identificador)
        # Se asignan propiedades mediante setters para validar su contenido.
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @property
    def nombre_servicio(self) -> str:
        """Retorna el nombre encapsulado del servicio."""
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor: str) -> None:
        """Valida que el nombre del servicio no esté vacío."""
        # Se comprueba que sea una cadena con caracteres útiles.
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorValidacionDatos("El nombre del servicio es obligatorio.")
        # Se guarda el nombre limpio.
        self.__nombre_servicio = valor.strip()

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por hora o sesión."""
        return self.__tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        """Valida que la tarifa base sea numérica y mayor que cero."""
        # Se rechazan valores no numéricos o menores/iguales a cero.
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ErrorValidacionDatos("La tarifa base del servicio debe ser mayor que cero.")
        # Se convierte a flotante para cálculos financieros.
        self.__tarifa_base = float(valor)

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para reservar."""
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Valida que la disponibilidad sea un valor booleano."""
        # Se verifica que el estado sea True o False.
        if not isinstance(estado, bool):
            raise ErrorValidacionDatos("La disponibilidad debe ser un booleano (True/False).")
        # Se guarda el estado de disponibilidad.
        self.__disponible = estado

    def validar_integridad(self) -> bool:
        """Verifica que el servicio esté disponible y sus parámetros sean válidos."""
        # Se lanza error si el servicio está marcado como no disponible.
        if not self.disponible:
            raise ErrorServicioNoDisponible(f"El servicio '{self.nombre_servicio}' no está disponible.")
        # Se delega la validación específica a cada subclase.
        return self.validar_parametros()

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Método abstracto para validar los parámetros propios de cada servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas: int, porcentaje_descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Método abstracto polimórfico para calcular el costo con opciones."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto que retorna la descripción del servicio."""
        pass

    def calcular_costo_sobrecargado(self, *args, **kwargs) -> float:
        """
        Simula sobrecarga de métodos para calcular costos con variantes de parámetros:
        - 1 argumento (duracion_horas): costo estándar con IVA y sin descuento.
        - 2 argumentos (duracion_horas, porcentaje_descuento): aplica descuento e IVA.
        - 3 argumentos o kwargs (duracion_horas, porcentaje_descuento, aplicar_iva): control total.
        """
        # Si se pasa duracion_horas en args o kwargs, se extrae; si no, se lanza error.
        if args:
            duracion = args[0]
            descuento = args[1] if len(args) > 1 else kwargs.get("porcentaje_descuento", 0.0)
            iva = args[2] if len(args) > 2 else kwargs.get("aplicar_iva", True)
        elif "duracion_horas" in kwargs:
            duracion = kwargs["duracion_horas"]
            descuento = kwargs.get("porcentaje_descuento", 0.0)
            iva = kwargs.get("aplicar_iva", True)
        else:
            raise ErrorValidacionDatos("Debe indicar 'duracion_horas' para calcular el costo.")
        # Se invoca la implementación polimórfica de calcular_costo.
        return self.calcular_costo(duracion, descuento, iva)

    def _aplicar_ajustes_financieros(self, subtotal: float, porcentaje_descuento: float, aplicar_iva: bool) -> float:
        """Calcula el total aplicando descuento e impuesto IVA de forma validada."""
        # Se verifica que el subtotal sea positivo.
        if subtotal <= 0:
            raise ErrorCalculoFinanciero("El subtotal debe ser mayor que cero.")
        # Se valida que el descuento esté entre 0% y 50%.
        if not isinstance(porcentaje_descuento, (int, float)) or not (0.0 <= porcentaje_descuento <= 50.0):
            raise ErrorCalculoFinanciero("El descuento debe estar entre 0% y 50%.")
        # Se calcula el monto de descuento.
        descuento_aplicado = subtotal * (porcentaje_descuento / 100.0)
        # Se resta el descuento al subtotal.
        total = subtotal - descuento_aplicado
        # Si aplicar_iva es True, se suma el 19% de IVA.
        if aplicar_iva:
            total *= 1.19
        # Se redondea a dos decimales.
        return round(total, 2)

    def obtener_resumen(self) -> str:
        """Retorna el resumen del servicio usando describir_servicio."""
        return self.describir_servicio()


class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas físicas."""

    def __init__(self, identificador: str, nombre_servicio: str, tarifa_base: float, capacidad_personas: int, tiene_proyector: bool = True, disponible: bool = True):
        # Se asignan los atributos propios de la sala.
        self.capacidad_personas = capacidad_personas
        self.tiene_proyector = tiene_proyector
        # Se inicializa la clase abstracta Servicio.
        super().__init__(identificador, nombre_servicio, tarifa_base, disponible)
        # Se validan los parámetros específicos.
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        """Valida que la capacidad de la sala esté entre 2 y 100 personas."""
        # Se comprueba el rango permitido para la capacidad.
        if not isinstance(self.capacidad_personas, int) or not (2 <= self.capacidad_personas <= 100):
            raise ErrorValidacionDatos("La capacidad de la sala debe estar entre 2 y 100 personas.")
        return True

    def calcular_costo(self, duracion_horas: int, porcentaje_descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo de la sala incluyendo recargo por proyector si aplica."""
        # Se valida que la duración sea entera y positiva.
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ErrorValidacionDatos("La duración en horas debe ser un entero mayor que cero.")
        # Se suma un recargo fijo si la sala incluye proyector.
        recargo_proyector = 15000.0 if self.tiene_proyector else 0.0
        # Se calcula el subtotal antes de descuentos e impuestos.
        subtotal = (self.tarifa_base * duracion_horas) + recargo_proyector
        # Se aplican los ajustes financieros y se retorna el total.
        return self._aplicar_ajustes_financieros(subtotal, porcentaje_descuento, aplicar_iva)

    def describir_servicio(self) -> str:
        """Describe las características de la sala reservable."""
        estado_proyector = "con proyector" if self.tiene_proyector else "sin proyector"
        return (
            f"Sala [{self.identificador}] '{self.nombre_servicio}' | "
            f"Capacidad: {self.capacidad_personas} ({estado_proyector}) | Tarifa: ${self.tarifa_base}/h"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de equipos."""

    def __init__(self, identificador: str, nombre_servicio: str, tarifa_base: float, categoria_equipo: str, cantidad_unidades: int, disponible: bool = True):
        # Se asignan los atributos propios del alquiler de equipos.
        self.categoria_equipo = categoria_equipo
        self.cantidad_unidades = cantidad_unidades
        # Se inicializa la clase abstracta Servicio.
        super().__init__(identificador, nombre_servicio, tarifa_base, disponible)
        # Se validan los parámetros específicos.
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        """Valida categoría y cantidad mínima de unidades a alquilar."""
        # Se verifica que la categoría no esté vacía.
        if not isinstance(self.categoria_equipo, str) or not self.categoria_equipo.strip():
            raise ErrorValidacionDatos("La categoría del equipo es obligatoria.")
        # Se verifica que la cantidad de unidades sea al menos 1.
        if not isinstance(self.cantidad_unidades, int) or self.cantidad_unidades < 1:
            raise ErrorValidacionDatos("La cantidad de unidades debe ser al menos 1.")
        return True

    def calcular_costo(self, duracion_horas: int, porcentaje_descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo multiplicando tarifa, horas y cantidad de unidades."""
        # Se valida la duración en horas.
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ErrorValidacionDatos("La duración en horas debe ser un entero mayor que cero.")
        # Se calcula el subtotal según duración y unidades.
        subtotal = self.tarifa_base * duracion_horas * self.cantidad_unidades
        # Se aplican descuentos e IVA.
        return self._aplicar_ajustes_financieros(subtotal, porcentaje_descuento, aplicar_iva)

    def describir_servicio(self) -> str:
        """Describe las características del alquiler de equipos."""
        return (
            f"Equipo [{self.identificador}] '{self.nombre_servicio}' | "
            f"Categoría: {self.categoria_equipo} | Unidades: {self.cantidad_unidades} | "
            f"Tarifa: ${self.tarifa_base}/u/h"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Asesorías especializadas."""

    def __init__(self, identificador: str, nombre_servicio: str, tarifa_base: float, especialidad: str, nivel_senior: bool = False, disponible: bool = True):
        # Se asignan los atributos propios de la asesoría.
        self.especialidad = especialidad
        self.nivel_senior = nivel_senior
        # Se inicializa la clase abstracta Servicio.
        super().__init__(identificador, nombre_servicio, tarifa_base, disponible)
        # Se validan los parámetros específicos.
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        """Valida que la especialidad de la asesoría esté definida."""
        # Se comprueba que la especialidad sea texto no vacío.
        if not isinstance(self.especialidad, str) or not self.especialidad.strip():
            raise ErrorValidacionDatos("La especialidad de la asesoría es obligatoria.")
        return True

    def calcular_costo(self, duracion_horas: int, porcentaje_descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo de la asesoría aplicando recargo si el consultor es Senior."""
        # Se valida la duración en horas.
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise ErrorValidacionDatos("La duración en horas debe ser un entero mayor que cero.")
        # Se aplica un multiplicador de 1.25 si es nivel Senior.
        factor_senior = 1.25 if self.nivel_senior else 1.0
        # Se calcula el subtotal.
        subtotal = self.tarifa_base * duracion_horas * factor_senior
        # Se aplican ajustes financieros y se retorna el resultado.
        return self._aplicar_ajustes_financieros(subtotal, porcentaje_descuento, aplicar_iva)

    def describir_servicio(self) -> str:
        """Describe las características de la asesoría especializada."""
        rango = "Senior" if self.nivel_senior else "Estándar"
        return (
            f"Asesoría [{self.identificador}] '{self.nombre_servicio}' | "
            f"Especialidad: {self.especialidad} ({rango}) | Tarifa: ${self.tarifa_base}/h"
        )
