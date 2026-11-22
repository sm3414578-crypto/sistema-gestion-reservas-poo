# Script principal de ejecución y simulación de Software F sin base de datos.
from excepciones.errores_sistema import ErrorSistemaBase, ErrorValidacionDatos
from modelos.cliente import Cliente
from modelos.servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from servicios.gestor_sistema import GestorSoftwareF


def ejecutar_simulacion() -> None:
    """Ejecuta una simulación de 12 operaciones cubriendo éxitos y fallos."""
    # Se instancia el gestor principal con su archivo de logs en texto plano.
    gestor = GestorSoftwareF(ruta_log="logs/eventos_sistema.log")
    print("=== INICIO DE SIMULACIÓN SOFTWARE F (12 OPERACIONES) ===\n")

    # Operación 1 [ÉXITO]: Crear y registrar un cliente válido.
    try:
        cliente_1 = Cliente("CLI-001", "valentina mendoza", "cvmendoza@correo.com", "3104567890")
        ok_1 = gestor.registrar_cliente(cliente_1)
        print(f"[Op 1 - Éxito] Registro cliente CLI-001: {ok_1} | {cliente_1.obtener_resumen()}")
    except ErrorSistemaBase as err:
        print(f"[Op 1 - Error] {err}")

    # Operación 2 [ÉXITO]: Crear y registrar un segundo cliente válido.
    try:
        cliente_2 = Cliente("CLI-002", "sergio molano", "sm3414578@correo.com", "3159876543")
        ok_2 = gestor.registrar_cliente(cliente_2)
        print(f"[Op 2 - Éxito] Registro cliente CLI-002: {ok_2} | {cliente_2.obtener_resumen()}")
    except ErrorSistemaBase as err:
        print(f"[Op 2 - Error] {err}")

    # Operación 3 [FALLO VALIDACIÓN]: Intentar crear un cliente con correo inválido.
    try:
        cliente_invalido = Cliente("CLI-003", "carlos molano", "correo_sin_arroba", "3001112233")
        gestor.registrar_cliente(cliente_invalido)
    except ErrorValidacionDatos as err:
        gestor._GestorSoftwareF__logger.registrar_evento("ERROR", "SIMULACION", f"Op 3 fallida: {err}")
        print(f"[Op 3 - Fallo esperado] Validación de cliente rechazada: {err}")

    # Operación 4 [ÉXITO]: Registrar tres servicios especializados (Sala, Equipo, Asesoría).
    sala = ReservaSala("SRV-SALA-1", "Sala Ejecutiva A", 50000.0, capacidad_personas=12, tiene_proyector=True)
    equipo = AlquilerEquipo("SRV-EQ-1", "Portátiles Empresariales", 15000.0, "Cómputo", cantidad_unidades=3)
    asesoria = AsesoriaEspecializada("SRV-ASE-1", "Consultoría de Arquitectura", 80000.0, "Software", nivel_senior=True)
    r_sala = gestor.registrar_servicio(sala)
    r_equipo = gestor.registrar_servicio(equipo)
    r_asesoria = gestor.registrar_servicio(asesoria)
    print(f"[Op 4 - Éxito] Servicios registrados -> Sala: {r_sala}, Equipo: {r_equipo}, Asesoría: {r_asesoria}")

    # Operación 5 [FALLO NEGOCIO]: Intentar registrar un cliente con ID duplicado.
    cliente_duplicado = Cliente("CLI-001", "valentina Duplicada", "duplicada@correo.com", "3104567890")
    dup_ok = gestor.registrar_cliente(cliente_duplicado)
    print(f"[Op 5 - Fallo esperado] Registro duplicado CLI-001 rechazado: {dup_ok}")

    # Operación 6 [ÉXITO]: Crear y confirmar una reserva de sala con sobrecarga de costo (10% desc, con IVA).
    res_1 = gestor.crear_y_confirmar_reserva("RES-001", "CLI-001", "SRV-SALA-1", duracion_horas=3, porcentaje_descuento=10.0, aplicar_iva=True)
    print(f"[Op 6 - Éxito] {res_1.obtener_resumen() if res_1 else 'No creada'}")

    # Operación 7 [ÉXITO]: Crear y confirmar una reserva de asesoría sin IVA y sin descuento.
    res_2 = gestor.crear_y_confirmar_reserva("RES-002", "CLI-002", "SRV-ASE-1", duracion_horas=2, porcentaje_descuento=0.0, aplicar_iva=False)
    print(f"[Op 7 - Éxito] {res_2.obtener_resumen() if res_2 else 'No creada'}")

    # Operación 8 [FALLO ENCADENADO]: Reserva con servicio inexistente (encadena ErrorServicioNoDisponible en ErrorReservaInvalida).
    res_3 = gestor.crear_y_confirmar_reserva("RES-003", "CLI-001", "SRV-NO-EXISTE", duracion_horas=2)
    print(f"[Op 8 - Fallo encadenado esperado] Reserva RES-003 rechazada: {res_3 is None}")

    # Operación 9 [FALLO ENCADENADO]: Reserva con cliente inexistente (encadena ErrorClienteInvalido en ErrorReservaInvalida).
    res_4 = gestor.crear_y_confirmar_reserva("RES-004", "CLI-999", "SRV-EQ-1", duracion_horas=1)
    print(f"[Op 9 - Fallo encadenado esperado] Reserva RES-004 rechazada: {res_4 is None}")

    # Operación 10 [ÉXITO]: Procesar la reserva confirmada RES-001.
    proc_ok = gestor.procesar_reserva_por_id("RES-001")
    print(f"[Op 10 - Éxito] Procesar reserva RES-001: {proc_ok}")

    # Operación 11 [FALLO NEGOCIO]: Intentar cancelar RES-001 después de haber sido PROCESADA.
    canc_procesada = gestor.cancelar_reserva_por_id("RES-001", "Cliente cambió de opinión tarde")
    print(f"[Op 11 - Fallo esperado] Cancelar RES-001 ya procesada: {canc_procesada}")

    # Operación 12 [ÉXITO]: Cancelar la reserva confirmada RES-002 antes de procesarla.
    canc_ok = gestor.cancelar_reserva_por_id("RES-002", "Reprogramación solicitada por el cliente")
    print(f"[Op 12 - Éxito] Cancelar reserva RES-002: {canc_ok}")

    print("\n=== RESUMEN FINAL EN MEMORIA ===")
    print(f"Clientes: {len(gestor.clientes)} | Servicios: {len(gestor.servicios)} | Reservas: {len(gestor.reservas)}")
    for r in gestor.reservas:
        print(" -", r.obtener_resumen())


if __name__ == "__main__":
    ejecutar_simulacion()
