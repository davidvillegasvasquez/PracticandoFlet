from models.perfilusuario_model import PerfilusuarioModel

class PerfilusuarioController:
    """
    Controller for perfilusuario page
    """

    def __init__(self, model=None):
        self.model = model or PerfilusuarioModel

    def get_title(self):
        return "Perfilusuario"
