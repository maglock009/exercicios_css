from flask import render_template
from controllers.base_controller import BaseController

class HTMLBasicoController(BaseController):
    
    def __init__ (self, app):
        self.rotas = [
            ('/', 'home', self.pagina_inicial),
            ('/exercicio_1','exercicio 1',self.exercicio_1),
            ('/exercicio_2','exercicio 2',self.exercicio_2),
            ('/exercicio_3','exercicio 3',self.exercicio_3),
            ('/exercicio_4',"exercicio 4",self.exercicio_4),
        ]

        super().__init__ (app)
    

    def pagina_inicial (self):
        return render_template ("pagina_inicial.html")
    
    def exercicio_1 (self):
        return render_template ("exercicio_1_html.html")
    
    def exercicio_2(self):
        return render_template ("exercicio_2_html.html")
    
    def exercicio_3(self):
        return render_template ("exercicio_3_html.html")
    
    def exercicio_4(self):
        return render_template ("exercicio_4_html.html")
    