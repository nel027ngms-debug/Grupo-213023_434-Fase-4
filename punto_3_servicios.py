"""
====================================================================
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)
Curso: Programación (Código: 213023)
Fase 4 - Prácticas Simuladas: Componente Práctico
Estudiante: Nelson Geovanny Medina Sedano
Grupo: 213023_434
====================================================================
"""
from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. CLASE ABSTRACTA BASE (EntidadGeneral)
# ==========================================
class EntidadGeneral(ABC):
    """
    Clase abstracta base para representar cualquier entidad general 
    dentro del sistema (Clientes, Servicios, Reservas).
    """
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad
        self._fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @property
    def fecha_registro(self) -> str:
        return self._fecha_registro

    @abstractmethod
    def obtener_detalles(self) -> str:
        """
        Método abstracto que obliga a todas las clases derivadas 
        a implementar su propia descripción detallada.
        """
        pass
        # ==========================================
# 2. CLASE CLIENTE (Hereda de EntidadGeneral)
# ==========================================
class Cliente(EntidadGeneral):
    """
    Clase que representa a un cliente en el sistema.
    Aplica encapsulación de datos personales y validaciones estrictas.
    """
    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        
        # Validaciones de datos de entrada
        if not nombre or not isinstance(nombre, str):
            raise ValueError("El nombre del cliente no puede estar vacío y debe ser texto.")
        if "@" not in correo or "." not in correo:
            raise ValueError("El correo electrónico proporcionado no tiene un formato válido.")
        if not telefono.isdigit() or len(telefono) < 7:
            raise ValueError("El teléfono debe contener únicamente dígitos y tener al menos 7 caracteres.")

        # Atributos privados (Encapsulación)
        self._nombre = nombre
        self._correo = correo
        self._telefono = telefono

    # Encapsulación mediante propiedades (Getters)
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def correo(self) -> str:
        return self._correo

    @property
    def telefono(self) -> str:
        return self._telefono

    # Implementación obligatoria del método abstracto de la clase base
    def obtener_detalles(self) -> str:
        return f"Cliente ID: {self.id_entidad} | Nombre: {self._nombre} | Correo: {self._correo} | Teléfono: {self._telefono}"


# ============================================
# 3. CLASE SERVICIO (Hereda de EntidadGeneral)
# ============================================
class Servicio(EntidadGeneral):
    """Clase abstracta para representar servicios del sistema"""
    def __init__(self, id_servicio: str, nombre_servicio:str):
        super().__init__(id_servicio)
        self._nombre_servicio = nombre_servicio

    @property
    def nombre_servicio(self):
        return self._nombre_servicio

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def obtener_detalles(self):
        return self.describir_servicio()


# ============================================
# 3.1. SERVICIO DE HOSPEDAJE (Servicio)
# ============================================
class ServicioHospedaje(Servicio):

    def __init__(self, id_servicio, dias, valor_dia):
        super().__init__(id_servicio, "Hospedaje")

        self._dias = dias
        self._valor_dia = valor_dia

    def validar_parametros(self):
        return self._dias > 0 and self._valor_dia > 0

    def calcular_costo(self):
        if not self.validar_parametros():
            raise ValueError("Datos Inválidos para Hospedaje.")
        return self._dias * self._valor_dia

    def describir_servicio(self):
        return(
            f"Servicio: Hospedaje | "
            f"Días: {self._dias}  | "
            f"Valor por día: ${self._valor_dia}"
        )


# ============================================
# 3.2. SERVICIO DE TRANSPORTE (Servicio)
# ============================================
class ServicioTransporte(Servicio):

    def __init__(self, id_servicio, kilometros, tarifa_km):
        super().__init__(id_servicio, "Transporte")

        self._kilometros = kilometros
        self._tarifa_km = tarifa_km

    def validar_parametros(self):
        return self._kilometros > 0 and self._tarifa_km > 0

    def calcular_costo(self):
        if not self.validar_parametros():
            raise ValueError("Datos invalidos para transporte.")
        return self._kilometros * self._tarifa_km

    def describir_servicio(self):
        return (
            f"Servicio: Transporte | "
            f"Kilometros: {self._kilometros} | "
            f"Tarifa por km: ${self._tarifa_km}"
        )


# ============================================
# 3.3. SERVICIO DE ALIMENTACIÓN (Servicio)
# ============================================
class ServicioAlimentacion(Servicio):

    def __init__(self, id_servicio, personas, costo_persona):
        super().__init__(id_servicio, "Alimentación")

        self._personas = personas
        self._costo_persona = costo_persona

    def validar_parametros(self):
        return self._personas > 0 and self._costo_persona > 0 

    def calcular_costo(self):
        if not self.validar_parametros():
            raise ValueError("Datos inválidos para alimentación.")
        return self._personas * self._costo_persona
    
    def describir_servicio(self):
        return (
            f"Servicio: Alimentación |"
            f"Personas: {self._personas} |"
            f"Costo por persona: ${self._costo_persona}"
        )
        

# ==========================================
# 4. CLASE RESERVA (Hereda de EntidadGeneral)
# ==========================================

import logging

# Configuración del archivo para registrar eventos y errores
logging.basicConfig(
    filename="registro_reservas.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================
# 4.1. EXCEPCIÓN PERSONALIZADA PARA RESERVAS
# ==========================================

class ReservaError(Exception):
    """
    Excepción personalizada para controlar errores
    relacionados con la creación y gestión de reservas.
    """
    pass


# ==========================================
# 4.2. CLASE RESERVA
# ==========================================

class Reserva(EntidadGeneral):
    """
    Clase que representa una reserva dentro del sistema.
    Integra un cliente, un servicio, duración y estado.
    Implementa confirmación, cancelación y procesamiento
    mediante el manejo de excepciones.
    """

    def __init__(self, id_reserva: str, cliente: Cliente,
                 servicio: Servicio, duracion: int):

        # Inicializar los atributos de la clase padre
        super().__init__(id_reserva)

        # Validar la información del cliente
        if not isinstance(cliente, Cliente):
            raise ValueError("Debe proporcionar un cliente válido.")

        # Validar la información del servicio
        if not isinstance(servicio, Servicio):
            raise ValueError("Debe proporcionar un servicio válido.")

        # Validar la duración de la reserva
        if (isinstance(duracion, bool)
                or not isinstance(duracion, int)
                or duracion <= 0):
            raise ValueError("La duración debe ser un número entero positivo.")

        # Atributos encapsulados de la reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"

        logging.info(
            f"Reserva {self.id_entidad} creada correctamente."
        )

    # ==========================================
    # 4.3. ENCAPSULACIÓN MEDIANTE PROPIEDADES
    # ==========================================

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado
