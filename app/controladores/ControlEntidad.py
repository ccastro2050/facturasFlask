# Importar componentes de SQLAlchemy necesarios para trabajar con bases de datos relacionales
from sqlalchemy import create_engine, MetaData, Table, select, insert, update, delete

# Importar utilidades de SQLAlchemy para manejo de conexiones y excepciones
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

# Importar módulo estándar para acceder a variables de entorno
import os

# Importar utilidad para cargar automáticamente las variables desde un archivo .env
from dotenv import load_dotenv

# Cargar todas las variables definidas en el archivo .env
load_dotenv()

# Obtener la cadena de conexión desde la variable de entorno DATABASE_URL
cadena_conexion = os.getenv("DATABASE_URL")

# Crear el motor de conexión utilizando la cadena obtenida
motor = create_engine(cadena_conexion)

# Crear un objeto de tipo MetaData que se usará para cargar la estructura de las tablas
metadata = MetaData(bind=motor)

# Reflejar (cargar) automáticamente todas las tablas existentes en la base de datos conectada
metadata.reflect()

# Definir clase ControlEntidad para agrupar métodos estáticos de acceso a cualquier tabla
class ControlEntidad:

    @staticmethod
    def obtener_todos(nombre_tabla):
        """
        Consultar todos los registros de una tabla existente en la base de datos.
        """
        try:
            # Obtener la tabla desde el metadata usando su nombre
            tabla = metadata.tables.get(nombre_tabla)

            # Si la tabla no existe, retornar una lista vacía
            if tabla is None:
                return []

            # Construir la instrucción SELECT * sobre la tabla
            consulta = select(tabla)

            # Establecer una conexión, ejecutar la consulta y retornar los resultados como diccionarios
            with motor.connect() as conexion:
                resultado = conexion.execute(consulta)
                return [dict(fila._mapping) for fila in resultado.fetchall()]
        except SQLAlchemyError as error:
            # En caso de error, imprimir el mensaje y retornar una lista vacía
            print(f"Error al obtener todos los registros: {error}")
            return []

    @staticmethod
    def insertar(nombre_tabla, datos):
        """
        Insertar un nuevo registro en la tabla especificada.
        'datos' debe ser un diccionario con nombres de columnas y sus valores.
        """
        try:
            # Obtener la tabla desde el metadata
            tabla = metadata.tables.get(nombre_tabla)

            # Si la tabla no existe, retornar None
            if tabla is None:
                return None

            # Construir la instrucción INSERT con los datos proporcionados
            instruccion = insert(tabla).values(**datos)

            # Ejecutar la inserción y confirmar la transacción
            with motor.connect() as conexion:
                resultado = conexion.execute(instruccion)
                conexion.commit()
                return resultado.inserted_primary_key
        except SQLAlchemyError as error:
            # En caso de error, imprimir el mensaje y retornar None
            print(f"Error al insertar: {error}")
            return None

    @staticmethod
    def buscar_por_id(nombre_tabla, columna_id, valor_id):
        """
        Consultar un registro por el valor de una columna clave (como una clave primaria).
        """
        try:
            # Obtener la tabla desde el metadata
            tabla = metadata.tables.get(nombre_tabla)

            # Si la tabla no existe, retornar None
            if tabla is None:
                return None

            # Construir la condición: columna == valor
            condicion = tabla.c[columna_id] == valor_id

            # Construir la consulta con filtro WHERE
            consulta = select(tabla).where(condicion)

            # Ejecutar la consulta y retornar el primer resultado como diccionario
            with motor.connect() as conexion:
                resultado = conexion.execute(consulta).first()
                if resultado:
                    return dict(resultado._mapping)
                return None
        except SQLAlchemyError as error:
            # En caso de error, imprimir el mensaje y retornar None
            print(f"Error al buscar: {error}")
            return None

    @staticmethod
    def actualizar(nombre_tabla, columna_id, valor_id, nuevos_datos):
        """
        Actualizar un registro existente según su identificador.
        'nuevos_datos' debe ser un diccionario con los campos a modificar.
        """
        try:
            # Obtener la tabla desde el metadata
            tabla = metadata.tables.get(nombre_tabla)

            # Si la tabla no existe, retornar False
            if tabla is None:
                return False

            # Construir la condición de búsqueda y la instrucción UPDATE
            condicion = tabla.c[columna_id] == valor_id
            instruccion = update(tabla).where(condicion).values(**nuevos_datos)

            # Ejecutar la instrucción y confirmar la transacción
            with motor.connect() as conexion:
                conexion.execute(instruccion)
                conexion.commit()
                return True
        except SQLAlchemyError as error:
            # En caso de error, imprimir el mensaje y retornar False
            print(f"Error al actualizar: {error}")
            return False

    @staticmethod
    def eliminar(nombre_tabla, columna_id, valor_id):
        """
        Eliminar un registro de la tabla según el valor de su identificador.
        """
        try:
            # Obtener la tabla desde el metadata
            tabla = metadata.tables.get(nombre_tabla)

            # Si la tabla no existe, retornar False
            if tabla is None:
                return False

            # Construir la condición de búsqueda y la instrucción DELETE
            condicion = tabla.c[columna_id] == valor_id
            instruccion = delete(tabla).where(condicion)

            # Ejecutar la instrucción y confirmar la transacción
            with motor.connect() as conexion:
                conexion.execute(instruccion)
                conexion.commit()
                return True
        except SQLAlchemyError as error:
            # En caso de error, imprimir el mensaje y retornar False
            print(f"Error al eliminar: {error}")
            return False
