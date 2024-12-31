import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import sqlite3
import random

kivy.require('2.1.0')  # Requiere la versión de Kivy

# Crear la base de datos si no existe
def init_db():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flashcards
                 (front TEXT, back TEXT)''')
    conn.commit()
    conn.close()

# Guardar una nueva tarjeta en la base de datos
def save_card(front, back):
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute("INSERT INTO flashcards (front, back) VALUES (?, ?)", (front, back))
    conn.commit()
    conn.close()

# Obtener todas las tarjetas
def get_all_cards():
    conn = sqlite3.connect('cards.db')
    c = conn.cursor()
    c.execute("SELECT * FROM flashcards")
    cards = c.fetchall()
    conn.close()
    return cards

# Clase principal de la aplicación
class FlashcardApp(App):

    def build(self):
        self.init_ui()
        self.current_card = None  # Para almacenar la tarjeta actual

    def init_ui(self):
        self.layout = BoxLayout(orientation='vertical')

        self.btn_create = Button(text="Crear Tarjetas", on_press=self.create_card)
        self.btn_practice = Button(text="Practicar", on_press=self.practice_card)
        self.btn_view = Button(text="Ver Tarjetas", on_press=self.view_cards)

        self.layout.add_widget(self.btn_create)
        self.layout.add_widget(self.btn_practice)
        self.layout.add_widget(self.btn_view)

        return self.layout

    # Función para crear una tarjeta
    def create_card(self, instance):
        self.create_popup()

    # Mostrar un popup para crear una tarjeta
    def create_popup(self):
        self.popup_layout = BoxLayout(orientation='vertical')
        
        self.front_input = TextInput(hint_text="Frontal", multiline=False)
        self.back_input = TextInput(hint_text="Trasera", multiline=False)
        self.save_button = Button(text="Guardar", on_press=self.save_new_card)

        self.popup_layout.add_widget(self.front_input)
        self.popup_layout.add_widget(self.back_input)
        self.popup_layout.add_widget(self.save_button)

        self.popup = Popup(title="Crear tarjeta", content=self.popup_layout, size_hint=(0.7, 0.5))
        self.popup.open()

    # Guardar la nueva tarjeta en la base de datos
    def save_new_card(self, instance):
        front = self.front_input.text
        back = self.back_input.text
        if front and back:
            save_card(front, back)
            self.popup.dismiss()

    # Función para practicar con tarjetas
    def practice_card(self, instance):
        cards = get_all_cards()
        if cards:
            self.show_random_card(cards)

    # Mostrar una tarjeta aleatoria
    def show_random_card(self, cards):
        random_card = random.choice(cards)
        front = random_card[0]
        back = random_card[1]

        # Almacenar la tarjeta actual
        self.current_card = (front, back)

        self.card_layout = BoxLayout(orientation='vertical')
        self.card_label = Label(text=front, font_size=40)
        self.card_label.bind(on_touch_down=self.flip_card)

        self.card_layout.add_widget(self.card_label)
        self.layout.clear_widgets()
        self.layout.add_widget(self.card_layout)

    # Voltear la tarjeta para mostrar la parte trasera
    def flip_card(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            if self.current_card:
                front, back = self.current_card
                # Cambiar el texto de la tarjeta
                if instance.text == front:
                    instance.text = back
                else:
                    instance.text = front

    # Función para ver todas las tarjetas
    def view_cards(self, instance):
        cards = get_all_cards()
        self.layout.clear_widgets()

        for front, back in cards:
            self.layout.add_widget(Label(text=f"{front} - {back}"))

if __name__ == '__main__':
    init_db()
    FlashcardApp().run()

