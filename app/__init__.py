#app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Cargar variables del entorno
load_dotenv()

# Crear instancias globales
bd = SQLAlchemy()
migraciones = Migrate()

def crear_aplicacion():
    aplicacion = Flask(__name__)
    aplicacion.config.from_object('app.config.ConfiguracionBase')

    # Inicializar las extensiones con la app
    bd.init_app(aplicacion)
    migraciones.init_app(aplicacion, bd)

    return aplicacion
