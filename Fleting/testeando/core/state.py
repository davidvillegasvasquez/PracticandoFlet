
class AppState:
    device = None  # mobile | tablet | desktop
    initial_device = "mobile"
    language = "es"
    initialized = False
    current_route = "/"
    auth_state = {
        "access_token": None,
        "refresh_token": None,
        "expires_at": 0, # Timestamp de expiración
    }
    usuario = None
