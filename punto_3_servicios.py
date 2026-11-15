"""
====================================================================
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)
Curso: Programación (Código: 213023)
Integrantes:
-Verónica Sánchez Cabrera
-Francisco Javier Lozano Yara
-Nelson Geovanny Medina Sedano
Fase 4 - Prácticas Simuladas: Componente Práctico
Empresa: Software FJ - Sistema Integral de Gestión
Grupo: 213023_434
====================================================================
"""

from abc import ABC, abstractmethod  # Importa herramientas para crear clases y métodos abstractos
from datetime import datetime          # Importa datetime para registrar fechas y horas exactas
import logging                         # Importa el módulo logging para generar el archivo de registro

# Configuración global del archivo de logs para registrar eventos y errores del sistema
logging.basicConfig(
    filename="registro_software_fj.log",                   # Nombre del archivo de salida de logs
    level=logging.INFO,                                    # Nivel mínimo de registro (INFO y superiores)
    format="%(asctime)s - %(levelname)s - %(message)s"     # Formato: Fecha/Hora - Nivel - Mensaje
)


# ==========================================
# 0. EXCEPCIONES PERSONALIZADAS DEL SISTEMA
# ==========================================
class ErrorSistemaFJ(Exception):
    """Excepción base personalizada para errores generales de Software FJ."""
    pass


class DatosInvalidosError(ErrorSistemaFJ):
    """Excepción lanzada cuando los datos de cliente o servicio no cumplen las reglas."""
    pass


class ReservaError(ErrorSistemaFJ):
    """Excepción lanzada ante operaciones no permitidas o fallos en las reservas."""
    pass


# ==========================================
# 1. CLASE ABSTRACTA BASE (EntidadGeneral)
# ==========================================
class EntidadGeneral(ABC):
    """
    Clase abstracta base que representa cualquier entidad general
    dentro del sistema (Clientes, Servicios, Reservas).
    """
    def __init__(self, id_entidad: str):
        # Validación básica del identificador de la entidad
        if not id_entidad or not isinstance(id_entidad, str):
            raise DatosInvalidosError("El ID de la entidad debe ser un texto no vacío.")
        # Atributos encapsulados (protegidos)
        self._id_entidad = id_entidad
        self._fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id_entidad

    @property
    def fecha_registro(self) -> str:
        """Retorna la fecha y hora en que fue creada la entidad."""
        return self._fecha_registro

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Método abstracto que obliga a las clases hijas a describirse."""
        pass


# ==========================================
# 2. CLASE CLIENTE (Hereda de EntidadGeneral)
# ==========================================
class Cliente(EntidadGeneral):
    """
    Representa a un cliente de Software FJ.
    Aplica encapsulación estricta de datos personales y validaciones en el constructor.
    """
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Llamada al constructor de la clase padre EntidadGeneral
        super().__init__(id_cliente)

        # Validaciones estrictas de los datos personales
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise DatosInvalidosError("El nombre del cliente debe ser texto y tener al menos 3 caracteres.")
        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise DatosInvalidosError("El correo electrónico proporcionado no tiene un formato válido.")
        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) < 7:
            raise DatosInvalidosError("El teléfono debe contener solo números y tener mínimo 7 dígitos.")

        # Encapsulación de atributos privados
        self._nombre = nombre.strip()
        self._correo = correo.strip()
        self._telefono = telefono.strip()
        # Registro exitoso en el log
        logging.info(f"Cliente registrado: {self._id_entidad} - {self._nombre}")

    @property
    def nombre(self) -> str:
        """Getter para obtener el nombre del cliente."""
        return self._nombre

    @property
    def correo(self) -> str:
        """Getter para obtener el correo del cliente."""
        return self._correo

    @property
    def telefono(self) -> str:
        """Getter para obtener el teléfono del cliente."""
        return self._telefono

    def obtener_detalles(self) -> str:
        """Implementación polimórfica que devuelve la ficha completa del cliente."""
        return (
            f"Cliente ID: {self.id_entidad} | Nombre: {self._nombre} | "
            f"Correo: {self._correo} | Teléfono: {self._telefono}"
        )


# ============================================
# 3. CLASE ABSTRACTA SERVICIO (Polimorfismo)
# ============================================
class Servicio(EntidadGeneral):
    """
    Clase abstracta para representar los servicios ofrecidos por Software FJ.
    Define la estructura común y los métodos polimórficos obligatorios.
    """
    def __init__(self, id_servicio: str, nombre_servicio: str, tarifa_base: float):
        # Inicializa el ID en la clase padre
        super().__init__(id_servicio)
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = tarifa_base
        self._disponible = True  # Estado de disponibilidad del servicio

    @property
    def nombre_servicio(self) -> str:
        """Retorna el nombre comercial del servicio."""
        return self._nombre_servicio

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para ser reservado."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        """Permite cambiar la disponibilidad del servicio validando que sea booleano."""
        if not isinstance(estado, bool):
            raise DatosInvalidosError("La disponibilidad debe ser True o False.")
        self._disponible = estado

    def _aplicar_ajustes_financieros(self, subtotal: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Método auxiliar para procesar la sobrecarga de cálculo de costos.
        Valida rangos de impuestos y descuentos antes de aplicarlos al subtotal.
        """
        if impuesto < 0 or descuento < 0 or descuento > 100:
            raise DatosInvalidosError("El impuesto debe ser >= 0 y el descuento debe estar entre 0 y 100.")
        monto_descuento = subtotal * (descuento / 100.0)       # Calcula el valor a descontar
        base_gravable = subtotal - monto_descuento             # Resta el descuento al subtotal
        monto_impuesto = base_gravable * (impuesto / 100.0)    # Calcula el impuesto sobre la base
        return round(base_gravable + monto_impuesto, 2)        # Retorna el total redondeado a 2 decimales

    @abstractmethod
    def validar_parametros(self) -> bool:
        """Método abstracto para validar las reglas de negocio de cada servicio."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Método abstracto sobrecargado mediante parámetros opcionales.
        Permite calcular el costo base, o incluir duración, impuestos y descuentos.
        """
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto para retornar la descripción específica del servicio."""
        pass

    def obtener_detalles(self) -> str:
        """Enlaza el método abstracto de EntidadGeneral con describir_servicio."""
        return self.describir_servicio()


# ============================================
# 3.1. SERVICIO 1: RESERVA DE SALAS
# ============================================
class ServicioSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o desarrollo."""
    def __init__(self, id_servicio: str, nombre_sala: str, capacidad: int, tarifa_hora: float):
        super().__init__(id_servicio, f"Sala - {nombre_sala}", tarifa_hora)
        self._capacidad = capacidad
        # Valida inmediatamente al instanciar para evitar objetos corruptos
        if not self.validar_parametros():
            raise DatosInvalidosError("Capacidad de sala o tarifa por hora inválida.")
        logging.info(f"Servicio de Sala creado: {self.id_entidad}")

    def validar_parametros(self) -> bool:
        """Verifica que la capacidad y la tarifa por hora sean mayores a cero."""
        return (
            isinstance(self._capacidad, int) and self._capacidad > 0 and
            isinstance(self._tarifa_base, (int, float)) and self._tarifa_base > 0
        )

    def calcular_costo(self, duracion: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo por horas de la sala aplicando impuestos/descuentos opcionales."""
        if not self.validar_parametros() or duracion <= 0:
            raise DatosInvalidosError("Parámetros o duración inválidos para calcular costo de Sala.")
        subtotal = self._tarifa_base * duracion
        return self._aplicar_ajustes_financieros(subtotal, impuesto, descuento)

    def describir_servicio(self) -> str:
        """Retorna la descripción técnica de la sala."""
        return (
            f"Servicio: {self._nombre_servicio} | Capacidad: {self._capacidad} personas | "
            f"Tarifa/Hora: ${self._tarifa_base}"
        )


# ============================================
# 3.2. SERVICIO 2: ALQUILER DE EQUIPOS
# ============================================
class ServicioEquipo(Servicio):
    """Servicio especializado para el alquiler de hardware y equipos de cómputo."""
    def __init__(self, id_servicio: str, tipo_equipo: str, cantidad: int, tarifa_dia: float):
        super().__init__(id_servicio, f"Equipo - {tipo_equipo}", tarifa_dia)
        self._cantidad = cantidad
        if not self.validar_parametros():
            raise DatosInvalidosError("Cantidad de equipos o tarifa diaria inválida.")
        logging.info(f"Servicio de Equipos creado: {self.id_entidad}")

    def validar_parametros(self) -> bool:
        """Verifica que la cantidad de equipos y la tarifa diaria sean positivas."""
        return (
            isinstance(self._cantidad, int) and self._cantidad > 0 and
            isinstance(self._tarifa_base, (int, float)) and self._tarifa_base > 0
        )

    def calcular_costo(self, duracion: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo total según cantidad de equipos, días y ajustes opcionales."""
        if not self.validar_parametros() or duracion <= 0:
            raise DatosInvalidosError("Parámetros o duración inválidos para calcular costo de Equipos.")
        subtotal = self._tarifa_base * self._cantidad * duracion
        return self._aplicar_ajustes_financieros(subtotal, impuesto, descuento)

    def describir_servicio(self) -> str:
        """Retorna la descripción detallada del alquiler de equipos."""
        return (
            f"Servicio: {self._nombre_servicio} | Cantidad: {self._cantidad} unid. | "
            f"Tarifa/Día: ${self._tarifa_base}"
        )


# ============================================
# 3.3. SERVICIO 3: ASESORÍAS ESPECIALIZADAS
# ============================================
class ServicioAsesoria(Servicio):
    """Servicio especializado para consultoría y asesoría en ingeniería de software."""
    def __init__(self, id_servicio: str, especialidad: str, tarifa_sesion: float, es_remota: bool = True):
        super().__init__(id_servicio, f"Asesoría - {especialidad}", tarifa_sesion)
        self._es_remota = es_remota
        if not self.validar_parametros():
            raise DatosInvalidosError("Tarifa de sesión o modalidad de asesoría inválida.")
        logging.info(f"Servicio de Asesoría creado: {self.id_entidad}")

    def validar_parametros(self) -> bool:
        """Verifica que la tarifa sea positiva y la modalidad sea un valor booleano."""
        return (
            isinstance(self._tarifa_base, (int, float)) and self._tarifa_base > 0 and
            isinstance(self._es_remota, bool)
        )

    def calcular_costo(self, duracion: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Calcula el costo de sesiones; aplica recargo del 10% si la asesoría es presencial."""
        if not self.validar_parametros() or duracion <= 0:
            raise DatosInvalidosError("Parámetros o duración inválidos para calcular costo de Asesoría.")
        recargo_presencial = 1.0 if self._es_remota else 1.10  # 10% adicional por desplazamiento
        subtotal = (self._tarifa_base * duracion) * recargo_presencial
        return self._aplicar_ajustes_financieros(subtotal, impuesto, descuento)

    def describir_servicio(self) -> str:
        """Retorna la descripción de la asesoría y su modalidad."""
        modalidad = "Remota" if self._es_remota else "Presencial (+10%)"
        return (
            f"Servicio: {self._nombre_servicio} | Modalidad: {modalidad} | "
            f"Tarifa/Sesión: ${self._tarifa_base}"
        )


# ==========================================
# 4. CLASE RESERVA (Hereda de EntidadGeneral)
# ==========================================
class Reserva(EntidadGeneral):
    """
    Integra un cliente, un servicio, duración y estado.
    Gestiona el ciclo de vida (Pendiente -> Confirmada -> Procesada / Cancelada)
    y aplica sobrecarga de métodos para calcular totales con impuestos o descuentos.
    """
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        # Inicializa el ID en la clase padre
        super().__init__(id_reserva)

        # Validaciones de integridad referencial y de tipos
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Debe proporcionar una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Debe proporcionar una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ReservaError(f"El servicio '{servicio.nombre_servicio}' no se encuentra disponible.")
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise DatosInvalidosError("La duración de la reserva debe ser un entero positivo.")

        # Asignación de atributos encapsulados
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._costo_final = 0.0

        # Registro de creación en el archivo de log (paréntesis corregido)
        logging.info(f"Reserva {self.id_entidad} creada en estado 'Pendiente' para {cliente.nombre}.")

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> int:
        return self._duracion

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_final(self) -> float:
        return self._costo_final

    def calcular_total(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Método sobrecargado para cotizar o calcular el valor de la reserva:
        - Sin argumentos: calcula el costo neto.
        - Con impuesto y/o descuento: delega el cálculo polimórfico al servicio.
        """
        return self._servicio.calcular_costo(
            duracion=self._duracion,
            impuesto=impuesto,
            descuento=descuento
        )

    def confirmar(self) -> str:
        """Cambia el estado de la reserva de 'Pendiente' a 'Confirmada'."""
        try:
            if self._estado != "Pendiente":
                raise ReservaError(f"No se puede confirmar la reserva {self.id_entidad} en estado '{self._estado}'.")
            self._estado = "Confirmada"
            logging.info(f"Reserva {self.id_entidad} confirmada correctamente.")
            return f"Reserva {self.id_entidad} confirmada exitosamente."
        except ReservaError as error:
            logging.error(f"Error de negocio al confirmar reserva {self.id_entidad}: {error}")
            raise
        except Exception as error:
            logging.exception(f"Error inesperado al confirmar la reserva {self.id_entidad}.")
            raise ReservaError("Fallo técnico al confirmar la reserva.") from error

    def cancelar(self) -> str:
        """Cancela una reserva que esté 'Pendiente' o 'Confirmada'."""
        try:
            if self._estado not in ("Pendiente", "Confirmada"):
                raise ReservaError(f"No se puede cancelar una reserva en estado '{self._estado}'.")
            self._estado = "Cancelada"
            logging.info(f"Reserva {self.id_entidad} cancelada correctamente.")
            return f"Reserva {self.id_entidad} cancelada exitosamente."
        except ReservaError as error:
            logging.error(f"Error de negocio al cancelar reserva {self.id_entidad}: {error}")
            raise
        except Exception as error:
            logging.exception(f"Error inesperado al cancelar la reserva {self.id_entidad}.")
            raise ReservaError("Fallo técnico al cancelar la reserva.") from error

    def procesar(self, impuesto: float = 19.0, descuento: float = 0.0) -> float:
        """
        Procesa una reserva confirmada, valida el servicio y calcula el costo final
        (por defecto aplica IVA del 19%, pero puede invocarse con otros valores).
        """
        try:
            if self._estado != "Confirmada":
                raise ReservaError("La reserva debe estar 'Confirmada' antes de procesarse.")
            if not self._servicio.validar_parametros():
                raise ReservaError("Los parámetros internos del servicio no son válidos.")

            # Invoca el método sobrecargado de cálculo
            self._costo_final = self.calcular_total(impuesto=impuesto, descuento=descuento)
            self._estado = "Procesada"

            logging.info(
                f"Reserva {self.id_entidad} procesada. Total cobrado: ${self._costo_final} "
                f"(Impuesto: {impuesto}%, Descuento: {descuento}%)."
            )
            return self._costo_final

        except (ReservaError, DatosInvalidosError) as error:
            logging.error(f"Error al procesar reserva {self.id_entidad}: {error}")
            raise
        except Exception as error:
            logging.exception(f"Error inesperado durante el procesamiento de {self.id_entidad}.")
            raise ReservaError("No fue posible completar el procesamiento de la reserva.") from error

    def obtener_detalles(self) -> str:
        """Retorna el resumen completo de la reserva."""
        return (
            f"Reserva ID: {self.id_entidad} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre_servicio} | Duración: {self._duracion} | "
            f"Estado: {self._estado} | Total: ${self._costo_final}"
        )
