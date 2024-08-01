import requests
from IPython.display import display
from IPython.core.display import HTML
from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.Tareas.gpt_content import GptContent
import numpy as np
import time
import re
import json
from src.api.workflows.Foros.data_base_connection import DataBaseConnection
from src.api.workflows.Foros.moodle_flow import MoodleWorkflow
# from src.api.workflows.Foros.sandbox_flow import MoodleWorkflow
from bs4 import BeautifulSoup

class TareasWorkflow:
    _openai_service: GptContent


    def __init__(self, openai_service: OpenAIService, prompt_service: PromptService) -> None:
        """
        Esta función se conecta a la api de OpenAI y también recibe el token de Moodle 
        """
        self._openai_service = GptContent(openai_service, prompt_service)

    def ejecutar_modelo(self, preguntas, lista_respuestas):
        """
        Esta función toma la lista de los posts de los estudiantes, los filtra para obtener solo los mensajes de los posts.
        También ejecuta el modelo según la pregunta, el diccionario que tiene cada usuario con su post y el texto (contexto vectorizado).
        """
        request = {
            'Pregunta': preguntas,
            'Usuario_respuesta': lista_respuestas
            }
        response = self._openai_service.get_tareas_content(str(request))
        return response

    
    # Función para extraer el texto de cada entrega y devolverlo en una lista de diccionarios
    def extract_text_from_submissions(self, data):
        submissions_list = []
        for assignment in data['assignments']:
            for submission in assignment['submissions']:
                userid = submission['userid']
                # Accede a `editorfields` dentro de `plugins`
                for plugin in submission['plugins']:
                    if plugin['type'] == 'onlinetext':
                        for editorfield in plugin['editorfields']:
                            if editorfield['name'] == 'onlinetext':
                                # Crea un diccionario con `id_usuario` y `texto`
                                submissions_list.append({'id_usuario': userid, 'texto': editorfield['text']})
        return submissions_list
    
    # Función para filtrar los diccionarios con texto no vacío
    def filter_non_empty_texts(self, submissions_list):
        return [entry for entry in submissions_list if entry['texto'].strip() != '']
    
    def html_to_text(self, html_content):
        """
        Convierte el contenido HTML a un formato de texto legible.
        Preserva la numeración de las listas ordenadas.
        
        Args:
        html_content (str): El contenido HTML a convertir.
        
        Returns:
        str: El contenido convertido a texto legible.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        text_content = []

        # Extraer el texto de los párrafos
        for p in soup.find_all('p'):
            text_content.append(p.get_text(strip=True))

        # Extraer el texto de las listas ordenadas
        for ol in soup.find_all('ol'):
            for index, li in enumerate(ol.find_all('li'), start=1):
                text_content.append(f"{index}. {li.get_text(strip=True)}")

        # Convertir a una cadena de texto con saltos de línea
        return '\n'.join(text_content)

    def execute(self) -> dict:
            """
            Función que ejecuta el proceso de obtención de los cursos, foros, discusiones y posts, luego ejecuta el modelo para generar la
            retroalimentación por posts de cada estudiante. Lo anterior se hace usando las funciones anteriores.
            """
            courses = MoodleWorkflow.get_courses()
            current_time = int(time.time())
            available_courses = [course for course in courses if course['enddate'] == 0 or course['enddate'] > current_time]
            display(available_courses)

            for course in available_courses:
                assignments = MoodleWorkflow.get_assignments_by_course(course['id'])
                preguntas = assignments[0]['assignments'][0]['intro']
                formatted_preguntas = self.html_to_text(preguntas)

                for assignment in assignments:
                    envios_tareas = MoodleWorkflow.get_submissions_by_assignment(assignment['assignments'][0]['id'])
                    lista_usuarios_textos = self.extract_text_from_submissions(envios_tareas)
                    
                    # se filtra la lista para obtener solo los textos con contenido
                    lista_usuarios_textos_sin_textos_vacios = self.filter_non_empty_texts(lista_usuarios_textos)
                    display(formatted_preguntas)
                    display(lista_usuarios_textos_sin_textos_vacios)
                    
                    lista_respuestas_modelo = []
                    for usuario in lista_usuarios_textos_sin_textos_vacios:
                        
                        respuesta = self.ejecutar_modelo(formatted_preguntas, usuario)
                        MoodleWorkflow.save_feedback_and_grade(assignment['assignments'][0]['id'], respuesta)
                        display(respuesta)
                        lista_respuestas_modelo.append(respuesta)
                    display(lista_respuestas_modelo)