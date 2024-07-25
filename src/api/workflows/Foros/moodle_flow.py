import requests
from IPython.core.display import HTML
from dotenv import load_dotenv
import os

class MoodleWorkflow:
    

    def get_courses():
        """
        Esta función toma la url de Moodle y el token, también toma los cursos (en caso de que hayan otros cursos que no correspondan)
        """
        url = os.getenv('URL_BECAT')
        params = {
            'wstoken': os.getenv('WS_TOKEN'),
            'wsfunction': 'core_course_get_courses',
            'moodlewsrestformat': 'json'
        }
        response = requests.get(url, params=params)
        courses = response.json()
        # return courses
        print("Courses response:", courses)
        if isinstance(courses, list):
            # filtered_courses = [course for course in courses if course['fullname'] in ['test IA Col']]
            filtered_courses = [course for course in courses if course['fullname'] in ['Teología fundamental']]
                
        else:
            print("Unexpected courses response format")
            filtered_courses = []
        return filtered_courses

    def get_forums_by_course(course_id):
        """
        Esta función toma los foros por cada curso.
        """
        url = os.getenv('URL_BECAT')
        params = {
            'wstoken': os.getenv('WS_TOKEN'),
            'wsfunction': 'mod_forum_get_forums_by_courses',
            'moodlewsrestformat': 'json',
            'courseids[0]': course_id
        }
        response = requests.get(url, params=params)
        forums = response.json()
        print(f"Foros del curso {course_id}:", forums)
        if isinstance(forums, list):
            return forums
        else:
            print(f"Unexpected forums response format for course {course_id}")
            return []

    def get_discussions_by_forum(forum_id):
        """
        Esta función toma las discusiones por curso.
        """
        url = os.getenv('URL_BECAT')
        params = {
            'wstoken': os.getenv('WS_TOKEN'),
            'wsfunction': 'mod_forum_get_forum_discussions',
            'moodlewsrestformat': 'json',
            'forumid': forum_id
        }
        response = requests.get(url, params=params)
        discussions = response.json()
        print(f"Discusiones del foro {forum_id}:", discussions)
        if isinstance(discussions, dict) and 'discussions' in discussions:
            return discussions['discussions']
        else:
            print(f"Formato de respuesta de discusiones inesperadas para el foro {forum_id}")
            return []

    def get_posts_by_discussion(discussion_id):
        """
        Esta función toma los posts por discusión.
        """
        url = os.getenv('URL_BECAT')
        params = {
            'wstoken': os.getenv('WS_TOKEN'),
            'wsfunction': 'mod_forum_get_discussion_posts',
            'moodlewsrestformat': 'json',
            'discussionid': discussion_id
        }
        response = requests.get(url, params=params)
        posts = response.json()
        print(f"Posts de la discusión {discussion_id}:", posts)
        if isinstance(posts, dict) and 'posts' in posts:
            return posts['posts']
        else:
            print(f"Formato de respuesta de discusiones inesperadas para el foro {discussion_id}")
            return []

    def subir_feedback(feedback_by_course_discussion):
        """
        Esta función se encarga de diseñar el formato de la retroalimentación para cada usuario, y luego subirlo a Moodle.
        """
        url = os.getenv('URL_BECAT')
        
        for course_name, discussions in feedback_by_course_discussion.items():
            for discussion_id, feedback_list in discussions.items():
                feedback_messages = ""
                puntos = ": "
                for feedback in feedback_list:
                    # feedback_messages += f"🤖 <strong>{feedback['usuario'].split('_')[0]}{puntos}</strong><span style='background-color: #AEC6CF'>{feedback['html']}</span><br><br> {feedback['calificacion']}"
                    # feedback_messages += f"🤖 <strong>{feedback['usuario'].split('_')[0]}{puntos}</strong><span style='background-color: #AEC6CF; display: inline;'>{feedback['html']}</span><span style='display: inline;'><strong>Calificación sugerida:</strong> {feedback['calificacion'].split(': ')[1]}</span><br><br>"
                    feedback_messages += (
                    f"🤖 <strong>{feedback['usuario'].split('_')[0]}{puntos}</strong>"
                    f"<span style='background-color: #AEC6CF; display: inline;'>{feedback['html']}</span><br>"
                    f"<div style='display: inline;'><strong>Calificación sugerida:</strong> {feedback['calificacion'].split(': ')[1]}</div><br><br>")



                data = {
                    'wstoken': os.getenv('WS_TOKEN'),
                    'wsfunction': 'mod_forum_add_discussion_post',
                    'moodlewsrestformat': 'json',
                    'postid': discussion_id,
                    'subject': 'Re: Retroalimentaciones',
                    'message': feedback_messages
                }
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    print(f"Retroalimentación subida correctamente para la discusión {discussion_id} del curso {course_name}")
                else:
                    print(f"Error al subir la retroalimentación para la discusión {discussion_id} del curso {course_name}: {response.text}")



    def calificar_post(contextid, itemid, rateduserid, rating):
        """
        Subir una calificación a un post en Moodle.

        Args:
            base_url (str): La URL base de tu instancia de Moodle (ej. "https://aula.becat.online")
            token (str): El token de acceso a la API de Moodle.
            contextid (int): ID del contexto.
            itemid (int): ID del ítem (el post a calificar).
            rateduserid (int): ID del usuario a calificar.
            rating (int): La calificación a asignar.

        Returns:
            dict: La respuesta de la API de Moodle.
        """
        url = os.getenv('URL_BECAT')
        os.getenv('URL_BECAT')
        params = {
            'wstoken': os.getenv('WS_TOKEN'),
            'wsfunction': 'core_rating_add_rating',
            'moodlewsrestformat': 'json',
            'contextid': contextid,
            'component': 'mod_forum',
            'ratingarea': 'post',
            'itemid': itemid,
            'scaleid': 10,  # Escala
            'rating': rating,
            'rateduserid': rateduserid,
        }

        response = requests.post(url, data=params)
        response_json = response.json()
        print(f"Response JSON: {response_json}")

        if response.status_code == 200:
            print("Calificación subida correctamente")
        else:
            print(f"Error al subir la retroalimentación: {response_json}")
        return response_json