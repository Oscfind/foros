import requests

def add_rating_to_post(contextid, itemid, rateduserid, rating):
    endpoint = "https://aula.becat.online/webservice/rest/server.php"
    
    data = {
        'wstoken': "f210b48f757dd01ff29b15965f984190",
        'wsfunction': "core_rating_add_rating",
        'moodlewsrestformat': 'json',
        'contextid': contextid,
        'component': 'mod_forum',
        'ratingarea': 'post',
        'itemid': itemid,
        'scaleid': 10,  # escala de 10
        'rating': rating,
        'rateduserid': rateduserid,
        'contextlevel': 'user',
        'instanceid': 137166
    }   
    
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     response.raise_for_status()


    response = requests.post(endpoint, data=data)  

    return response.json()

 



contextid = 223716
itemid = 137166
rateduserid = 42466
rating = 10

response = add_rating_to_post(contextid, itemid, rateduserid, rating)
print(response)


# import requests  
# def get_moodle_version():  
#     endpoint = "https://aula.becat.online/webservice/rest/server.php"
  
#     data = {  
#         'wstoken': "f210b48f757dd01ff29b15965f984190",  
#         'wsfunction': 'core_webservice_get_site_info',  
#         'moodlewsrestformat': 'json'  
#     }  
#     response = requests.post(endpoint, data=data)  
#     return response.json()  

# version_info = get_moodle_version()  
# print(version_info)  