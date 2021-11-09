from fpdf import FPDF

class PDF(FPDF):
    pass

    def logo(self, name, x, y, w, h):
        self.image(name, x, y, w, h)

    def text(self, sociedad):
        self.set_xy(10.0,60.0)
        self.set_text_color(0.0, 0.0, 0.0)
        self.set_font('Arial', '', 15)
        msj = "La Sociedad Anonima con denominacion '" + sociedad.nombre + "', fue creada el dia " + str(sociedad.fecha_creacion) + " y su correo para poder comunicarte es " + sociedad.correo + ". Para acceder a la informacion publica de la misma, escanear el codigo QR." 
        
        self.multi_cell(0, 10, msj)

    def titles(self, title="TITULO DE PRUEBA DE PDF"):
        self.set_xy(00.0,20.0)
        self.set_text_color(220, 50, 50)
        self.set_font('Arial', 'B', 20)
        self.cell(w=210.0, h=40.0, align='C', txt="Expediente digital '" + title + "'", border=0)