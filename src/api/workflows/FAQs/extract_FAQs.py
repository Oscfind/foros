import requests  
from bs4 import BeautifulSoup, Tag  
  
  
def obtener_faqs():
    faqs = ''
    # Obtener y analizar el contenido HTML  
    soup = BeautifulSoup(requests.get('https://becat.online/FAQ/').content, 'html.parser') 
    # Procesar y mostrar el contenido de cada acordeón  
    for accordion in soup.select('#accordion h3'):  
        title = accordion.get_text(strip=True)  
        content_div = accordion.find_next_sibling('div')  
        content = ""  
        # Función para asegurar que todas las URLs sean absolutas  
        def ensure_absolute_url(url):  
            return url if url.startswith('http') else f"https://becat.online/FAQ/{url}"  
        # Procesar todos los elementos dentro del div de contenido  
        for element in content_div.children:  
            if isinstance(element, Tag):  # Asegura que el elemento es un Tag antes de usar find_all  
                imgs = element.find_all('img')  
                for img in imgs:  
                    img['src'] = ensure_absolute_url(img['src'])  
    
                links = element.find_all('a')  
                for link in links:  
                    if 'href' in link.attrs:  
                        link['href'] = ensure_absolute_url(link['href'])  
                content += str(element)  
        faqs += f"<h2>{title}</h2><div>{content}</div>"
    return faqs

def obtener_faqs_unir():
    faqs_unir = ''
    # Obtener y analizar el contenido HTML  
    url = 'https://becat.online/faq-sobre-los-titulos-propios-de-la-unir/'  
    response = requests.get(url)  
    soup = BeautifulSoup(response.content, 'html.parser')  
    # Procesar y mostrar el contenido de cada acordeón  
    for accordion in soup.find_all('div', class_='et_pb_toggle'):  # Asegurarse de seleccionar el div correcto del acordeón  
        title = accordion.find('h3', class_='et_pb_toggle_title').get_text(strip=True)  # Extraer el título  
        content_div = accordion.find('div', class_='et_pb_toggle_content')  # Extraer el div que contiene el contenido  
        if content_div:  
            # Extracción del contenido textual, manteniendo etiquetas internas para formato  
            content = str(content_div)  
        else:  
            content = "No content available"  
        faqs_unir += f"<h2>{title}</h2><div>{content}</div>"
    return faqs_unir