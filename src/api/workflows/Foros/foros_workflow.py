# # último código funcional (con moodle)
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

class ForosWorkflow:
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
            current_time = int(time.time())
            available_courses = [course for course in courses if course['enddate'] == 0 or course['enddate'] > current_time]
            # display(courses)
            # display(len(courses))
            # display(available_courses)
            # display(len(available_courses))

            # este diccionario almacena las retroalimentaciones por curso y por discusión
            feedback_by_course_discussion = {}

            for course in available_courses:
                forums = MoodleWorkflow.get_forums_by_course(course['id'])
                
                # obtener la fecha actual
                current_time = int(time.time())
                
                # filtrar los foros disponibles
                available_forums = [forum for forum in forums if forum['cutoffdate'] == 0 or forum['cutoffdate'] > current_time]
                foro_1 = available_forums[0]
                display(foro_1)


                if 'intro' in foro_1:
                    intro = foro_1['intro']
                    contexto_foro = self.extract_content(intro, "CONTEXTO")
                    caso = self.extract_content(intro, "CASO")
                    lista_preguntas_tarea = self.extract_tarea_questions(intro)
                    preguntas_unificadas_tarea = " ".join(lista_preguntas_tarea)

                display(contexto_foro)
                display(caso)
                display(preguntas_unificadas_tarea)
                
                ## Creando una lista de un solo elemento (foro_1)
                lista_foro_1 = []
                lista_foro_1.append(foro_1)

                for forum in lista_foro_1:
                    discussions = MoodleWorkflow.get_discussions_by_forum(forum['id'])
                    # display(discussions)
                    
                    for discussion in discussions:
                        posts = MoodleWorkflow.get_posts_by_discussion(discussion['discussion'])
                        # display(posts)
                        # posts_sin_pregunta_inicial = posts[:len(posts)-1]
                        # display(posts_sin_pregunta_inicial)


                        
                        if posts[0]["subject"] == "Re: Retroalimentaciones":
                            break
                        else:
                            contador = 0
                            for post in posts:
                                if post["subject"] != "Re: Retroalimentaciones":
                                    contador += 1
                                else:
                                    break

                            question_embedding = DataBaseConnection.encode_text(preguntas_unificadas_tarea)
                            question_embedding_array = np.array(question_embedding)
                            # search_result = DataBaseConnection.seach_context(DataBaseConnection.qdrant_client, course['fullname'], question_embedding_array)
                            search_result = DataBaseConnection.seach_context(DataBaseConnection.qdrant_client, "test IA Col", question_embedding_array)
                            contexto = DataBaseConnection.create_context(search_result)
                            # display(contexto)

                            if contador == 1:
                                feedback_message = self.ejecutar_modelo(caso, preguntas_unificadas_tarea, posts[0])
                            elif contador == 2:
                                feedback_message = self.ejecutar_modelo(caso, preguntas_unificadas_tarea, posts[:2])
                            else:
                                feedback_message = self.ejecutar_modelo(caso, preguntas_unificadas_tarea, posts[:contador])
                            
                            usuario_list = list(feedback_message.keys())
                            html_list = list(feedback_message.values())

                            if course['fullname'] not in feedback_by_course_discussion:
                                feedback_by_course_discussion[course['fullname']] = {}

                            if discussion['id'] not in feedback_by_course_discussion[course['fullname']]:
                                feedback_by_course_discussion[course['fullname']][discussion['id']] = []

                            for i in range(len(feedback_message)):    
                                feedback_by_course_discussion[course['fullname']][discussion['id']].append({
                                    'discussionid': discussion['id'],
                                    'usuario': usuario_list[i].split('_')[0],
                                    'html': html_list[i][0],
                                    'calificacion': html_list[i][1]
                                })

                                # contextid = int(posts[0]['html']['rating'].split('name="contextid" value="')[1].split('"')[0])
                                # display(contextid)
                                # itemid = int(posts[0]['html']['rating'].split('name="itemid" value="')[1].split('"')[0])
                                # display(itemid)
                                # rateduserid = int(posts[0]['html']['rating'].split('name="rateduserid" value="')[1].split('"')[0])
                                # display(rateduserid)
                                # rating = int(html_list[i][1][-1])
                                # display(rating)

                                # # función para calificar el post
                                # MoodleWorkflow.calificar_post(contextid, itemid, rateduserid, rating)
                            

                            


            # se ordenan las retroalimentaciones de los usuarios
            for course in feedback_by_course_discussion:
                for discussion in feedback_by_course_discussion[course]:
                    feedback_by_course_discussion[course][discussion] = feedback_by_course_discussion[course][discussion][::-1]
            display(feedback_by_course_discussion)
            MoodleWorkflow.subir_feedback(feedback_by_course_discussion)
            # return True
