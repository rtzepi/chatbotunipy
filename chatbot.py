from difflib import get_close_matches

class Chatbot:
    def __init__(self):
        # Base de datos de universidades
        self.universidades = [
            {"nombre": "usac", "costo": "bajo", "ubicacion": "centrica"},
            {"nombre": "umg", "costo": "medio", "ubicacion": "periferica"},
            {"nombre": "del_valle", "costo": "alto", "ubicacion": "centrica"},
            {"nombre": "fmarroquin", "costo": "muy_alto", "ubicacion": "exclusiva"}
        ]

        # Base de datos de facultades y carreras
        self.facultades = {
            "medicina": ["medicina_general", "odontologia", "enfermeria", "nutricion"],
            "ingenieria": ["sistemas", "civil", "electronica", "industrial"],
            "ciencias_economicas": ["administracion", "contaduria", "economia", "mercadotecnia"],
            "administracion": ["liderar_equipos", "planificacion_estrategica", "recursos_humanos", "finanzas"]
        }

        # Jornadas disponibles
        self.jornadas = ["matutina", "vespertina", "nocturna"]

        # Variables globales para almacenar el estado de la conversación
        self.universidad_recomendada = None
        self.facultad_recomendada = None
        self.carrera_recomendada = None
        self.jornada_recomendada = None

    # Función para corregir errores ortográficos
    def corregir_entrada(self, entrada, opciones):
        entrada = entrada.lower().strip()  # Normalizar la entrada
        coincidencias = get_close_matches(entrada, opciones, n=1, cutoff=0.5)  # Reducir el cutoff para mayor flexibilidad
        if coincidencias:
            return coincidencias[0]  # Devuelve la coincidencia más cercana
        return None  # No se encontró una coincidencia válida

    # Función para recomendar una universidad
    def recomendar_universidad(self, costo, ubicacion):
        recomendaciones = [
            uni for uni in self.universidades
            if uni["costo"] == costo and uni["ubicacion"] == ubicacion
        ]
        return recomendaciones

    # Función para procesar la respuesta del chatbot
    def procesar_respuesta(self, mensaje):
        palabras = mensaje.lower().split()

        # Listas de palabras clave para costo y ubicación
        palabras_costo_bajo = {"barato", "económico", "bajo", "barata", "económica"}
        palabras_costo_medio = {"medio", "moderado", "regular"}
        palabras_costo_alto = {"caro", "alto", "costoso", "cara"}
        palabras_costo_muy_alto = {"muy alto", "exclusivo", "lujoso"}

        palabras_ubicacion_centrica = {"centro", "céntrica", "céntrico", "central"}
        palabras_ubicacion_periferica = {"periferia", "periférico", "periferico", "afueras", "exterior"}
        palabras_ubicacion_exclusiva = {"exclusiva", "exclusivo", "privada", "élite"}

        # Detectar costo
        costo = None
        if any(p in palabras_costo_bajo for p in palabras):
            costo = "bajo"
        elif any(p in palabras_costo_medio for p in palabras):
            costo = "medio"
        elif any(p in palabras_costo_alto for p in palabras):
            costo = "alto"
        elif any(p in palabras_costo_muy_alto for p in palabras):
            costo = "muy_alto"

        # Detectar ubicación
        ubicacion = None
        if any(p in palabras_ubicacion_centrica for p in palabras):
            ubicacion = "centrica"
        elif any(p in palabras_ubicacion_periferica for p in palabras):
            ubicacion = "periferica"
        elif any(p in palabras_ubicacion_exclusiva for p in palabras):
            ubicacion = "exclusiva"

        # Si no se ha recomendado una universidad, buscar una
        if self.universidad_recomendada is None:
            if costo is None or ubicacion is None:
                return "Por favor, dime si buscas una universidad barata, cara o en qué ubicación."

            recomendaciones = self.recomendar_universidad(costo, ubicacion)
            if recomendaciones:
                self.universidad_recomendada = recomendaciones[0]["nombre"]
                return f"Te recomiendo la universidad: {self.universidad_recomendada}. ¿En qué área te gustaría estudiar? (Medicina, Ingeniería, Ciencias Económicas, Administración)"
            else:
                return "No encontré una universidad con esas características."

        # Si ya se recomendó una universidad, preguntar por la facultad
        elif self.facultad_recomendada is None:
            opciones_facultad = ["medicina", "ingenieria", "ciencias_economicas", "administracion"]
            facultad_corregida = self.corregir_entrada(mensaje.lower(), opciones_facultad)

            if facultad_corregida:
                self.facultad_recomendada = facultad_corregida
                if self.facultad_recomendada == "ingenieria":
                    return f"Has seleccionado {self.facultad_recomendada}. ¿Qué te gustaría hacer? (Desarrollar software, Diseñar circuitos, Construir infraestructura, Optimizar procesos)"
                elif self.facultad_recomendada == "medicina":
                    return f"Has seleccionado {self.facultad_recomendada}. ¿Qué te gustaría hacer? (Trabajar con pacientes, Investigación médica, Cirugía, Pediatría)"
                elif self.facultad_recomendada == "ciencias_economicas":
                    return f"Has seleccionado {self.facultad_recomendada}. ¿Qué te gustaría hacer? (Analizar datos financieros, Gestionar empresas, Contabilidad, Mercadeo)"
                elif self.facultad_recomendada == "administracion":
                    return f"Has seleccionado {self.facultad_recomendada}. ¿Qué te gustaría hacer? (Liderar equipos, Planificación estratégica, Recursos humanos, Finanzas)"
            else:
                return "Por favor, selecciona una facultad válida: Medicina, Ingeniería, Ciencias Económicas, Administración."

        # Si ya se recomendó una facultad, preguntar por la carrera
        elif self.carrera_recomendada is None:
            if self.facultad_recomendada == "ingenieria":
                opciones_carrera = ["desarrollar software", "diseñar circuitos", "construir infraestructura", "optimizar procesos"]
                carrera_corregida = self.corregir_entrada(mensaje.lower(), opciones_carrera)

                if carrera_corregida:
                    if carrera_corregida == "desarrollar software":
                        self.carrera_recomendada = "Ingeniería en Sistemas"
                    elif carrera_corregida == "diseñar circuitos":
                        self.carrera_recomendada = "Ingeniería Electrónica"
                    elif carrera_corregida == "construir infraestructura":
                        self.carrera_recomendada = "Ingeniería Civil"
                    elif carrera_corregida == "optimizar procesos":
                        self.carrera_recomendada = "Ingeniería Industrial"
                    return f"Has seleccionado {self.carrera_recomendada}. ¿Cuántas horas al día puedes dedicar a estudiar? (Mañana, Tarde, Noche)"
                else:
                    return "Por favor, selecciona una opción válida: Desarrollar software, Diseñar circuitos, Construir infraestructura, Optimizar procesos."

            elif self.facultad_recomendada == "medicina":
                opciones_carrera = ["trabajar con pacientes", "investigación médica", "cirugía", "pediatría"]
                carrera_corregida = self.corregir_entrada(mensaje.lower(), opciones_carrera)

                if carrera_corregida:
                    if carrera_corregida == "trabajar con pacientes":
                        self.carrera_recomendada = "Medicina General"
                    elif carrera_corregida == "investigación médica":
                        self.carrera_recomendada = "Investigación Biomédica"
                    elif carrera_corregida == "cirugía":
                        self.carrera_recomendada = "Cirugía"
                    elif carrera_corregida == "pediatría":
                        self.carrera_recomendada = "Pediatría"
                    return f"Has seleccionado {self.carrera_recomendada}. ¿Cuántas horas al día puedes dedicar a estudiar? (Mañana, Tarde, Noche)"
                else:
                    return "Por favor, selecciona una opción válida: Trabajar con pacientes, Investigación médica, Cirugía, Pediatría."

            elif self.facultad_recomendada == "ciencias_economicas":
                opciones_carrera = ["analizar datos financieros", "gestionar empresas", "contabilidad", "mercadeo"]
                carrera_corregida = self.corregir_entrada(mensaje.lower(), opciones_carrera)

                if carrera_corregida:
                    if carrera_corregida == "analizar datos financieros":
                        self.carrera_recomendada = "Economía"
                    elif carrera_corregida == "gestionar empresas":
                        self.carrera_recomendada = "Administración de Empresas"
                    elif carrera_corregida == "contabilidad":
                        self.carrera_recomendada = "Contaduría Pública"
                    elif carrera_corregida == "mercadeo":
                        self.carrera_recomendada = "Mercadeo"
                    return f"Has seleccionado {self.carrera_recomendada}. ¿Cuántas horas al día puedes dedicar a estudiar? (Mañana, Tarde, Noche)"
                else:
                    return "Por favor, selecciona una opción válida: Analizar datos financieros, Gestionar empresas, Contabilidad, Mercadeo."

            elif self.facultad_recomendada == "administracion":
                opciones_carrera = ["liderar equipos", "planificación estratégica", "recursos humanos", "finanzas"]
                carrera_corregida = self.corregir_entrada(mensaje.lower(), opciones_carrera)

                if carrera_corregida:
                    if carrera_corregida == "liderar equipos":
                        self.carrera_recomendada = "Administración de Empresas"
                    elif carrera_corregida == "planificación estratégica":
                        self.carrera_recomendada = "Planificación Estratégica"
                    elif carrera_corregida == "recursos humanos":
                        self.carrera_recomendada = "Recursos Humanos"
                    elif carrera_corregida == "finanzas":
                        self.carrera_recomendada = "Finanzas"
                    return f"Has seleccionado {self.carrera_recomendada}. ¿Cuántas horas al día puedes dedicar a estudiar? (Mañana, Tarde, Noche)"
                else:
                    return "Por favor, selecciona una opción válida: Liderar equipos, Planificación estratégica, Recursos humanos, Finanzas."

        # Si ya se recomendó una carrera, preguntar por la jornada
        elif self.jornada_recomendada is None:
            opciones_jornada = ["mañana", "tarde", "noche"]
            jornada_corregida = self.corregir_entrada(mensaje.lower(), opciones_jornada)

            if jornada_corregida:
                self.jornada_recomendada = jornada_corregida
                return f"¡Perfecto! Te recomiendo la universidad {self.universidad_recomendada}, en la facultad de {self.facultad_recomendada}, carrera de {self.carrera_recomendada}, en jornada {self.jornada_recomendada}."
            else:
                return "Por favor, selecciona una jornada válida: Mañana, Tarde, Noche."

        # Reiniciar el estado para una nueva consulta
        else:
            self.universidad_recomendada = None
            self.facultad_recomendada = None
            self.carrera_recomendada = None
            self.jornada_recomendada = None
            return "¿En qué más puedo ayudarte?"