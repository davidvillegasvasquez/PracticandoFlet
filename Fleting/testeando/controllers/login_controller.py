from models.login_model import LoginModel

class LoginController:
    """
    Controller for login page
    """
    def __init__(self, model=None):
        self.model = model or LoginModel

    def get_title(self):
        return "Login"

    def get_email(self):
        return self.model.email

    def get_pass(self):
        return self.model.password

    def set_email(self, email):
        self.model.email = email

    def set_pass(self, password):
        self.model.password = password



