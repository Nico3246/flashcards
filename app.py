from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

# Ruta para guardar las tarjetas
CARDS_FILE = "cards.json"

# Verificar si el archivo de tarjetas ya existe
if os.path.exists(CARDS_FILE):
    with open(CARDS_FILE, "r") as file:
        cards = json.load(file)
else:
    cards = []

# Ruta para guardar tarjetas
@app.route('/save_card', methods=['POST'])
def save_card():
    front = request.form['front']
    back = request.form['back']
    
    if front and back:
        cards.append({"front": front, "back": back})
        # Guardar en el archivo
        with open(CARDS_FILE, "w") as file:
            json.dump(cards, file)
        return jsonify({"message": "Tarjeta guardada exitosamente"}), 200
    else:
        return jsonify({"message": "Por favor ingresa ambos lados de la tarjeta"}), 400

# Ruta para obtener tarjetas aleatorias
@app.route('/get_random_card', methods=['GET'])
def get_random_card():
    if not cards:
        return jsonify({"message": "No hay tarjetas creadas."}), 404
    
    card = random.choice(cards)
    return jsonify(card)

# Ruta para ver todas las tarjetas
@app.route('/get_all_cards', methods=['GET'])
def get_all_cards():
    return jsonify(cards)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
