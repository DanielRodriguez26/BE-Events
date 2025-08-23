#!/usr/bin/env python3
"""
Test de integración para la API de Mis Eventos
Ejecuta pruebas básicas para verificar que todos los endpoints funcionan correctamente
"""

import json
import time
from datetime import datetime, timedelta

import requests

# Configuración de la API
BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"


class APITester:
    """Clase para realizar pruebas de integración de la API"""

    def __init__(self):
        """Inicializa el tester con una sesión de requests"""
        self.session = requests.Session()
        self.token = None
        self.test_user_id = None
        self.test_event_id = None
        self.test_registration_id = None

    def print_test(self, test_name, success=True):
        """Imprime el resultado de una prueba con formato visual"""
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"{status} {test_name}")

    def test_health_check(self):
        """Prueba el endpoint de verificación de salud"""
        try:
            response = self.session.get(f"{BASE_URL.replace('/api/v1', '')}/health")
            if response.status_code == 200:
                self.print_test("Health Check")
                return True
            else:
                self.print_test("Health Check", False)
                return False
        except Exception as e:
            self.print_test(f"Health Check - Error: {str(e)}", False)
            return False

    def test_register_user(self):
        """Prueba el registro de un nuevo usuario"""
        try:
            data = {
                "email": TEST_EMAIL,
                "username": "testuser",
                "password": TEST_PASSWORD,
                "confirm_password": TEST_PASSWORD,
                "first_name": "Test",
                "last_name": "User",
                "phone": "3001234567",
                "role_id": 1,
            }
            response = self.session.post(f"{BASE_URL}/auth/register", json=data)

            if response.status_code in [200, 201, 409]:  # 409 si el usuario ya existe
                self.print_test("Registro de Usuario")
                return True
            else:
                self.print_test(
                    f"Registro de Usuario - Status: {response.status_code}", False
                )
                return False
        except Exception as e:
            self.print_test(f"Registro de Usuario - Error: {str(e)}", False)
            return False

    def test_login(self):
        """Prueba el inicio de sesión de usuario"""
        try:
            data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
            response = self.session.post(f"{BASE_URL}/auth/login", json=data)

            if response.status_code == 200:
                result = response.json()
                self.token = result.get("access_token")
                if self.token:
                    self.session.headers.update(
                        {"Authorization": f"Bearer {self.token}"}
                    )
                    self.print_test("Login de Usuario")
                    return True
                else:
                    self.print_test("Login de Usuario - Token no encontrado", False)
                    return False
            else:
                self.print_test(
                    f"Login de Usuario - Status: {response.status_code}", False
                )
                return False
        except Exception as e:
            self.print_test(f"Login de Usuario - Error: {str(e)}", False)
            return False

    def test_get_events(self):
        """Prueba obtener la lista de eventos"""
        try:
            response = self.session.get(f"{BASE_URL}/events/")

            if response.status_code == 200:
                result = response.json()
                if "items" in result:
                    self.print_test("Obtener Eventos")
                    return True
                else:
                    self.print_test("Obtener Eventos - Formato incorrecto", False)
                    return False
            else:
                self.print_test(
                    f"Obtener Eventos - Status: {response.status_code}", False
                )
                return False
        except Exception as e:
            self.print_test(f"Obtener Eventos - Error: {str(e)}", False)
            return False

    def test_get_events_with_capacity(self):
        """Prueba obtener eventos con información de capacidad disponible"""
        try:
            response = self.session.get(f"{BASE_URL}/events/with-capacity/")

            if response.status_code == 200:
                result = response.json()
                if "items" in result:
                    self.print_test("Obtener Eventos con Capacidad")
                    return True
                else:
                    self.print_test(
                        "Obtener Eventos con Capacidad - Formato incorrecto", False
                    )
                    return False
            else:
                self.print_test(
                    f"Obtener Eventos con Capacidad - Status: {response.status_code}",
                    False,
                )
                return False
        except Exception as e:
            self.print_test(f"Obtener Eventos con Capacidad - Error: {str(e)}", False)
            return False

    def test_get_upcoming_events(self):
        """Prueba obtener eventos próximos con información de capacidad"""
        try:
            response = self.session.get(f"{BASE_URL}/events/upcoming/with-capacity/")

            if response.status_code == 200:
                result = response.json()
                if "items" in result:
                    self.print_test("Obtener Eventos Próximos")
                    return True
                else:
                    self.print_test(
                        "Obtener Eventos Próximos - Formato incorrecto", False
                    )
                    return False
            else:
                self.print_test(
                    f"Obtener Eventos Próximos - Status: {response.status_code}", False
                )
                return False
        except Exception as e:
            self.print_test(f"Obtener Eventos Próximos - Error: {str(e)}", False)
            return False

    def test_search_events(self):
        """Prueba la búsqueda de eventos por criterios"""
        try:
            params = {"title": "test", "is_active": True}
            response = self.session.get(f"{BASE_URL}/events/search/", params=params)

            if response.status_code == 200:
                result = response.json()
                self.print_test("Búsqueda de Eventos")
                return True
            else:
                self.print_test(
                    f"Búsqueda de Eventos - Status: {response.status_code}", False
                )
                return False
        except Exception as e:
            self.print_test(f"Búsqueda de Eventos - Error: {str(e)}", False)
            return False

    def test_get_user_profile(self):
        """Prueba obtener el perfil del usuario autenticado"""
        try:
            response = self.session.get(f"{BASE_URL}/users/me")

            if response.status_code == 200:
                result = response.json()
                if "id" in result:
                    self.test_user_id = result["id"]
                    self.print_test("Obtener Perfil de Usuario")
                    return True
                else:
                    self.print_test(
                        "Obtener Perfil de Usuario - ID no encontrado", False
                    )
                    return False
            else:
                self.print_test(
                    f"Obtener Perfil de Usuario - Status: {response.status_code}", False
                )
                return False
        except Exception as e:
            self.print_test(f"Obtener Perfil de Usuario - Error: {str(e)}", False)
            return False

    def test_get_my_statistics(self):
        """Prueba obtener estadísticas personales del usuario"""
        try:
            response = self.session.get(f"{BASE_URL}/statistics/my-statistics")

            if response.status_code == 200:
                result = response.json()
                if "user_id" in result:
                    self.print_test("Obtener Estadísticas del Usuario")
                    return True
                else:
                    self.print_test(
                        "Obtener Estadísticas del Usuario - Formato incorrecto", False
                    )
                    return False
            else:
                self.print_test(
                    f"Obtener Estadísticas del Usuario - Status: {response.status_code}",
                    False,
                )
                return False
        except Exception as e:
            self.print_test(
                f"Obtener Estadísticas del Usuario - Error: {str(e)}", False
            )
            return False

    def test_get_event_capacity(self):
        """Prueba obtener información de capacidad disponible de un evento"""
        try:
            # Primero obtener un evento
            response = self.session.get(f"{BASE_URL}/events/")
            if response.status_code == 200:
                events = response.json().get("items", [])
                if events:
                    event_id = events[0]["id"]
                    response = self.session.get(
                        f"{BASE_URL}/event-registrations/event/{event_id}/capacity"
                    )

                    if response.status_code == 200:
                        result = response.json()
                        if "event_id" in result:
                            self.print_test("Obtener Información de Capacidad")
                            return True
                        else:
                            self.print_test(
                                "Obtener Información de Capacidad - Formato incorrecto",
                                False,
                            )
                            return False
                    else:
                        self.print_test(
                            f"Obtener Información de Capacidad - Status: {response.status_code}",
                            False,
                        )
                        return False
                else:
                    self.print_test(
                        "Obtener Información de Capacidad - No hay eventos", False
                    )
                    return False
            else:
                self.print_test(
                    "Obtener Información de Capacidad - No se pudieron obtener eventos",
                    False,
                )
                return False
        except Exception as e:
            self.print_test(
                f"Obtener Información de Capacidad - Error: {str(e)}", False
            )
            return False

    def test_get_my_registrations(self):
        """Prueba obtener los registros de eventos del usuario"""
        try:
            response = self.session.get(
                f"{BASE_URL}/event-registrations/my-registrations/"
            )

            if response.status_code == 200:
                result = response.json()
                if "items" in result:
                    self.print_test("Obtener Mis Registros")
                    return True
                else:
                    self.print_test("Obtener Mis Registros - Formato incorrecto", False)
                    return False
            else:
                self.print_test(
                    f"Obtener Mis Registros - Status: {response.status_code}", False
                )
                return False
        except Exception as e:
            self.print_test(f"Obtener Mis Registros - Error: {str(e)}", False)
            return False

    def run_all_tests(self):
        """Ejecuta todas las pruebas de integración"""
        print("🚀 Iniciando pruebas de integración de la API...")
        print("=" * 60)

        tests = [
            ("Health Check", self.test_health_check),
            ("Registro de Usuario", self.test_register_user),
            ("Login de Usuario", self.test_login),
            ("Obtener Eventos", self.test_get_events),
            ("Obtener Eventos con Capacidad", self.test_get_events_with_capacity),
            ("Obtener Eventos Próximos", self.test_get_upcoming_events),
            ("Búsqueda de Eventos", self.test_search_events),
            ("Obtener Perfil de Usuario", self.test_get_user_profile),
            ("Obtener Estadísticas del Usuario", self.test_get_my_statistics),
            ("Obtener Información de Capacidad", self.test_get_event_capacity),
            ("Obtener Mis Registros", self.test_get_my_registrations),
        ]

        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.print_test(f"{test_name} - Excepción: {str(e)}", False)

        print("=" * 60)
        print(f"📊 Resultados: {passed}/{total} pruebas pasaron")

        if passed == total:
            print(
                "🎉 ¡Todas las pruebas pasaron! La API está funcionando correctamente."
            )
        else:
            print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")

        return passed == total


def main():
    """Función principal del script de pruebas"""
    print("🧪 Test de Integración - API Mis Eventos")
    print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
    print()

    tester = APITester()
    success = tester.run_all_tests()

    if success:
        print("\n✅ El backend está listo para usar!")
        print(
            "📚 Consulta API_DOCUMENTATION.md para más información sobre los endpoints."
        )
    else:
        print("\n❌ Hay problemas que necesitan ser resueltos antes de continuar.")


if __name__ == "__main__":
    main()
