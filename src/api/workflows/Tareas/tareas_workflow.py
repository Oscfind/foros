import requests
from IPython.display import display
from IPython.core.display import HTML
from src.api.common.services.openai_service import OpenAIService
from src.api.common.services.prompt_service import PromptService
from src.api.workflows.Foros.gpt_content import GptContent
import numpy as np
import time
import re
import json
from src.api.workflows.Foros.data_base_connection import DataBaseConnection
from src.api.workflows.Foros.moodle_flow import MoodleWorkflow
# from src.api.workflows.Foros.sandbox_flow import MoodleWorkflow

class TareasWorkflow:
    _openai_service: GptContent


    def __init__(self, openai_service: OpenAIService, prompt_service: PromptService) -> None:
        """
        Esta función se conecta a la api de OpenAI y también recibe el token de Moodle 
        """
        self._openai_service = GptContent(openai_service, prompt_service)

    def ejecutar_modelo(self, contexto, preguntas, lista_respuestas):
        """
        Esta función toma la lista de los posts de los estudiantes, los filtra para obtener solo los mensajes de los posts.
        También ejecuta el modelo según la pregunta, el diccionario que tiene cada usuario con su post y el texto (contexto vectorizado).
        """
        if type(lista_respuestas) == dict:
            request = {
            'Contexto': contexto,
            'Pregunta': preguntas,
            'Usuario_respuesta': f"{lista_respuestas['author']['fullname']}: {lista_respuestas['message']}",
            # 'Texto': contexto_pdf_vectorizado,
            }
            response = self._openai_service.get_foros_content(str(request))
            return response
        
        elif type(lista_respuestas) == list:
            posts = []
            for estudiante_respuesta in lista_respuestas:
                posts.append({estudiante_respuesta['author']['fullname']: estudiante_respuesta['message']})
            request = {
                'Contexto': contexto,
                'Pregunta': preguntas,
                'Usuarios_respuestas': posts,
                # 'Texto': contexto_pdf_vectorizado,
            }
            response = self._openai_service.get_foros_content(str(request))
            return response
        
    # Función para extraer contenido de la lista de diccionarios que contiene "Contexto", "Caso"
    def extract_content(self, intro, section_name):
        pattern = rf'<strong>{section_name}</strong></h3>\s*<p>(.*?)</p>'
        match = re.search(pattern, intro, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    # Función para extraer las preguntas de la sección TAREA
    def extract_tarea_questions(self, intro):
        pattern = r'<h3><strong>TAREA:</strong></h3>\s*<p>.*?</p>\s*<ul>(.*?)</ul>'
        match = re.search(pattern, intro, re.DOTALL)
        if match:
            ul_content = match.group(1).strip()
            # Extraer las preguntas dentro de <li>
            questions = re.findall(r'<li><em>(.*?)</em></li>', ul_content, re.DOTALL)
            return questions
        return None

    def execute(self) -> dict:
            """
            Función que ejecuta el proceso de obtención de los cursos, foros, discusiones y posts, luego ejecuta el modelo para generar la
            retroalimentación por posts de cada estudiante. Lo anterior se hace usando las funciones anteriores.
            """
            courses = MoodleWorkflow.get_courses()
            # display(courses)
            current_time = int(time.time())
            available_courses = [course for course in courses if course['enddate'] == 0 or course['enddate'] > current_time]
            # display(courses)
            # display(len(courses))
            display(available_courses)
            # display(len(available_courses))

            # este diccionario almacena las retroalimentaciones por curso y por discusión
            feedback_by_course_discussion = {}

            for course in available_courses:
                assignments = MoodleWorkflow.get_assignments_by_course(course['id'])
                display(assignments)

                for assignment in assignments:
                    display(assignment[0]['assignments'][0]['id'])
                    # envios_tareas = MoodleWorkflow.get_submissions_by_assignment(assignment[0]['assignments'][0]['id'])
                    # display(envios_tareas)

                
                # # obtener la fecha actual
                # current_time = int(time.time())
                
                # # filtrar los foros disponibles
                # available_forums = [forum for forum in forums if forum['cutoffdate'] == 0 or forum['cutoffdate'] > current_time]
                # foro_1 = available_forums[0]
                # display(foro_1)