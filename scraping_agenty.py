import requests
from bs4 import BeautifulSoup
import json
import re

#Función para obtener todas las etiquetas <a> con atributos href de la url
def get_all_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        #Filtrar para mantener solo urls absolutas
        links = [link if link.startswith('http') else url + link for link in links]
        return links
    except requests.RequestException as e:
        print(f"Error al obtener {url}: {e}")
        return []

#Función para obtener todas las etiquetas <h1> y <p> de la url
def get_h1_and_p_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        h1_tags = [str(tag) for tag in soup.find_all('h1')]
        p_tags = [str(tag) for tag in soup.find_all('p')]
        return h1_tags + p_tags
    except requests.RequestException as e:
        print(f"Error al obtener {url}: {e}")
        return []

#Función para rastrear el sitio web comenzando desde la url inicial y guardar los datos recopilados en un archivo json
def crawl_website(start_url):
    crawled_data = {}
    links_to_crawl = get_all_links(start_url)
    
    for link in links_to_crawl:
        if re.match(r'^https?://', link):  #Validar el formato de la url
            print(f"Crawling {link}...")
            tags = get_h1_and_p_tags(link)
            crawled_data[link] = tags
    
    with open('crawled_data.json', 'w', encoding='utf-8') as file:
        json.dump(crawled_data, file, ensure_ascii=False, indent=4)  #Especificar el formato con indent=4

if __name__ == "__main__":
    start_url = 'https://agenty.com/' 
    crawl_website(start_url)

