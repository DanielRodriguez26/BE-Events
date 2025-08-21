#!/usr/bin/env python
"""
Script para diagnosticar problemas de conexión con PostgreSQL
"""
import locale
import os
import sys


def test_postgresql_connection():
    print("=== DIAGNÓSTICO DE CONEXIÓN A POSTGRESQL ===\n")

    # 1. Verificar encoding del sistema
    print("1. Configuración del sistema:")
    print(f"   - Encoding por defecto: {sys.getdefaultencoding()}")
    print(f"   - Locale: {locale.getlocale()}")
    print(f"   - Filesystem encoding: {sys.getfilesystemencoding()}")

    # 2. Verificar variables de entorno
    print("\n2. Variables de entorno relevantes:")
    env_vars = ["LANG", "LC_ALL", "LC_CTYPE", "PGCLIENTENCODING"]
    for var in env_vars:
        value = os.getenv(var, "No definida")
        print(f"   - {var}: {value}")

    # 3. Probar conexión directa con psycopg2
    print("\n3. Prueba de conexión directa:")
    try:
        import psycopg2

        print(f"   - psycopg2 version: {psycopg2.__version__}")

        # Configurar encoding explícitamente
        os.environ["PGCLIENTENCODING"] = "utf8"

        conn_params = {
            "host": "localhost",
            "port": "5432",
            "database": "events_db",
            "user": "postgres",
            "password": "1234",
            "client_encoding": "utf8",
        }

        print("   - Intentando conexión...")
        conn = psycopg2.connect(**conn_params)
        print("   ✅ Conexión exitosa!")

        # Verificar encoding
        cursor = conn.cursor()
        cursor.execute("SHOW client_encoding;")
        encoding = cursor.fetchone()[0]
        print(f"   - Client encoding: {encoding}")

        cursor.execute("SHOW server_encoding;")
        encoding = cursor.fetchone()[0]
        print(f"   - Server encoding: {encoding}")

        conn.close()

    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        print(f"   Tipo de error: {type(e).__name__}")

    # 4. Probar con SQLAlchemy
    print("\n4. Prueba con SQLAlchemy:")
    try:
        from sqlalchemy import create_engine

        # URL simple sin parámetros especiales
        url = "postgresql://postgres:1234@localhost:5432/events_db"

        # Configurar encoding en variables de entorno
        os.environ["PGCLIENTENCODING"] = "utf8"

        engine = create_engine(url, connect_args={"client_encoding": "utf8"})

        print("   - Intentando conexión con SQLAlchemy...")
        conn = engine.connect()
        print("   ✅ Conexión con SQLAlchemy exitosa!")
        conn.close()

    except Exception as e:
        print(f"   ❌ Error con SQLAlchemy: {e}")
        print(f"   Tipo de error: {type(e).__name__}")


if __name__ == "__main__":
    test_postgresql_connection()
