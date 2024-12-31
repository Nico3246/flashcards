import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class FlashcardsApp(toga.App):
    def startup(self):
        # Crear el layout de la aplicación
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        # Crear una etiqueta para mostrar un mensaje
        self.label = toga.Label('¡Bienvenido a la App de Flashcards!', style=Pack(padding=5))

        # Crear un botón que cambiará el texto de la etiqueta al hacer clic
        self.button = toga.Button('Empezar a crear tarjetas', on_press=self.on_button_press, style=Pack(padding=5))

        # Agregar los widgets al layout
        self.main_box.add(self.label)
        self.main_box.add(self.button)

        # Crear la ventana principal
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def on_button_press(self, widget):
        # Cambiar el texto de la etiqueta cuando se presione el botón
        self.label.text = 'Creando tarjetas...'

if __name__ == '__main__':
    app = FlashcardsApp('Flashcards', 'org.example.flashcards')
    app.main_loop()
