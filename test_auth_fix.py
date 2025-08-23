import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000/api/v1"

def test_auth():
    """Prueba el flujo completo de autenticación"""
    
    # 1. Intentar hacer login
    print("1. Probando login...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            
            if access_token:
                print(f"Token obtenido: {access_token[:50]}...")
                
                # 2. Probar el endpoint /me con el token
                print("\n2. Probando endpoint /me...")
                headers = {"Authorization": f"Bearer {access_token}"}
                
                me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
                print(f"Status Code: {me_response.status_code}")
                print(f"Response: {me_response.text}")
                
                # 3. Probar un endpoint protegido
                print("\n3. Probando endpoint protegido de eventos...")
                events_response = requests.get(f"{BASE_URL}/events/", headers=headers)
                print(f"Status Code: {events_response.status_code}")
                print(f"Response: {events_response.text[:200]}...")
                
            else:
                print("No se pudo obtener el token de acceso")
        else:
            print("Login falló")
            
    except Exception as e:
        print(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    test_auth()
