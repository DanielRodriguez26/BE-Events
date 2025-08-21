#!/usr/bin/env python3
"""
Script simple para probar la conexión a la base de datos
"""

print("=== INICIANDO PRUEBA SIMPLE ===")

try:
    print("1. Importando módulos...")
    from app.db.base import SessionLocal
    from app.db.models import Event

    print("   ✅ Módulos importados correctamente")

    print("\n2. Creando sesión de base de datos...")
    db = SessionLocal()
    print("   ✅ Sesión creada")

    print("\n3. Probando consulta simple...")
    count = db.query(Event).count()
    print(f"   ✅ Total de eventos en la base de datos: {count}")

    print("\n4. Cerrando sesión...")
    db.close()
    print("   ✅ Sesión cerrada")

    print("\n✅ PRUEBA EXITOSA - La base de datos está funcionando correctamente")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback

    traceback.print_exc()
