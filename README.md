# Software F — Sistema de Gestión de Clientes, Servicios y Reservas (POO)

Aplicación desarrollada en **Python** aplicando Programación Orientada a Objetos (POO), manejo estructurado de excepciones, encapsulación, herencia, polimorfismo y registro de eventos en archivo plano de logs, **sin utilizar base de datos**.

## Estructura del proyecto

- `excepciones/errores_sistema.py`: Jerarquía de excepciones personalizadas del sistema (`ErrorSistemaBase`, `ErrorValidacionDatos`, `ErrorClienteInvalido`, `ErrorServicioNoDisponible`, `ErrorReservaInvalida`, `ErrorCalculoFinanciero`).
- `utilidades/registrador.py`: Clase `RegistradorLogs` encargada de escribir eventos y trazas de error en un archivo de texto plano (`logs/eventos_sistema.log`).
- `modelos/entidad_base.py`: Clase abstracta base (`EntidadSistema`) con propiedades encapsuladas y métodos abstractos.
- `modelos/cliente.py`: Clase `Cliente` con validación estricta de nombre, correo y teléfono.
- `modelos/servicio.py`: Clase abstracta `Servicio` y servicios especializados (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) con cálculo de costos, descuentos e impuestos.
- `modelos/reserva.py`: Clase `Reserva` que gestiona el ciclo de vida de una reserva (`PENDIENTE`, `CONFIRMADA`, `PROCESADA`, `CANCELADA`).
- `servicios/gestor_sistema.py`: Controlador `GestorSoftwareF` que administra listas internas en memoria, bloques `try/except/else/finally`, encadenamiento de excepciones (`raise ... from ...`) y registro en logs.
- `main.py`: Script principal con la simulación de 12 operaciones (casos exitosos y fallos controlados).

## Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
python main.py
