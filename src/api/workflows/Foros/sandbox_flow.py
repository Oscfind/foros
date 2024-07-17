import requests
from IPython.core.display import HTML

class MoodleWorkflow:

    def get_courses():
        """
        Esta función toma la url de Moodle y el token, también toma los cursos (en caso de que hayan otros cursos que no correspondan)
        """
        url = 'https://sandbox.moodledemo.net/webservice/rest/server.php'
        params = {
            'wstoken': '1128713fd4ebe37bad90c073d36f10dd',
            'wsfunction': 'core_course_get_courses',
            'moodlewsrestformat': 'json'
        }
        response = requests.get(url, params=params)
        courses = response.json()
        print("Courses response:", courses)
        if isinstance(courses, list):
            filtered_courses = [course for course in courses if course['fullname'] in ['My first course', 'My second course']]
        else:
            print("Unexpected courses response format")
            filtered_courses = []
        return filtered_courses

    def get_forums_by_course(course_id):
        """
        Esta función toma los foros por cada curso.
        """
        url = 'https://sandbox.moodledemo.net/webservice/rest/server.php'
        params = {
            'wstoken': '1128713fd4ebe37bad90c073d36f10dd',
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
        url = 'https://sandbox.moodledemo.net/webservice/rest/server.php'
        params = {
            'wstoken': '1128713fd4ebe37bad90c073d36f10dd',
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
        url = 'https://sandbox.moodledemo.net/webservice/rest/server.php'
        params = {
            'wstoken': '1128713fd4ebe37bad90c073d36f10dd',
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
        url = 'https://sandbox.moodledemo.net/webservice/rest/server.php'
        
        for course_name, discussions in feedback_by_course_discussion.items():
            for discussion_id, feedback_list in discussions.items():
                feedback_messages = ""
                puntos = ": "
                for feedback in feedback_list:
                    feedback_messages += f"🤖 <strong>{feedback['usuario'].split('_')[0]}{puntos}</strong><span style='background-color: #AEC6CF'>{feedback['html']} <strong>{feedback['calificacion']}</strong></span><br><br>"


                data = {
                    'wstoken': '1128713fd4ebe37bad90c073d36f10dd',
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