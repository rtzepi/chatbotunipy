from flask import Flask, request, jsonify, render_template, session
from chatbot import Chatbot

app = Flask(__name__)
app.secret_key = "clavesecreta_aqui"  # Clave secreta para las sesiones

@app.route("/", methods=["GET", "POST"])
def chat():
    # Inicializar el estado del chatbot en la sesión si no existe
    if "chatbot_state" not in session:
        session["chatbot_state"] = {
            "universidad_recomendada": None,
            "facultad_recomendada": None,
            "carrera_recomendada": None,
            "jornada_recomendada": None
        }

    # Reiniciar el historial si la página se carga por primera vez
    if request.method == "GET":
        session["historial"] = []

    # Inicializar el historial si no existe
    if "historial" not in session:
        session["historial"] = []

    if request.method == "POST":
        mensaje = request.form["mensaje"]

        # Crear una nueva instancia de Chatbot y pasarle el estado guardado
        chatbot = Chatbot()
        chatbot.universidad_recomendada = session["chatbot_state"]["universidad_recomendada"]
        chatbot.facultad_recomendada = session["chatbot_state"]["facultad_recomendada"]
        chatbot.carrera_recomendada = session["chatbot_state"]["carrera_recomendada"]
        chatbot.jornada_recomendada = session["chatbot_state"]["jornada_recomendada"]

        # Procesar la respuesta del chatbot
        respuesta = chatbot.procesar_respuesta(mensaje)

        # Guardar el estado actualizado en la sesión
        session["chatbot_state"] = {
            "universidad_recomendada": chatbot.universidad_recomendada,
            "facultad_recomendada": chatbot.facultad_recomendada,
            "carrera_recomendada": chatbot.carrera_recomendada,
            "jornada_recomendada": chatbot.jornada_recomendada
        }

        # Guardar el mensaje y la respuesta en el historial
        session["historial"].append(("Tú", mensaje))
        session["historial"].append(("Chatbot", respuesta))
        session.modified = True  # Marcar la sesión como modificada

    return render_template("chat.html", historial=session.get("historial", []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

#if __name__ == "__main__":
#    app.run(debug=True)