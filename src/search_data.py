#from _google_ import search
from googlesearch import search
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import logging


'''def get_text_from_url(response):
    try:
        soup = BeautifulSoup(response, "html.parser")
        text = " "
        all_paras = soup.findAll('p')
        if all_paras is not None:
            text = ''.join(p.text.strip() for p in all_paras)
    except Exception as e:
        pass
    return text'''

def get_text_from_url(response):
    try:
        # Se por algum motivo vier None, já evita erro
        if response is None:
            return ""

        # Lê o conteúdo da resposta
        html = response.read()
        if not html:
            return ""

        # Garante que estamos passando string/bytes para o BS
        soup = BeautifulSoup(html, "html.parser")
        if soup is None:  # extra segurança
            return ""

        paragraphs = soup.find_all("p")
        if not paragraphs:
            return ""

        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        # normaliza espaços
        text = re.sub(r"\s+", " ", text)
        return text
    except Exception as e:
        # por enquanto loga o erro pra debug
        print("Erro em get_text_from_url:", e, type(response))
        return ""

'''def google_search_query(query):
    subtopic_text = ""
    for url in search(query, stop=20):
        try:
            response = urlopen(url)
            content_type = response.getheader('Content-Type')
            reg_exp = ';.*'
            mime_type = re.sub(reg_exp, '', content_type)

            if 'application/pdf' != mime_type:
                subtopic_text = subtopic_text + get_text_from_url(response).strip()
                subtopic_text = re.sub('[^A-Za-z0-9]+', ' ', subtopic_text)
        except Exception as e:
            pass
    return subtopic_text
'''

def google_search_query(query):
    subtopic_text = ""
    for url in search(query, stop=20):
        try:
            response = urlopen(url)
            content_type = response.getheader("Content-Type") or ""
            mime_type = re.sub(r";.*", "", content_type)

            if mime_type != "application/pdf":
                page_text = get_text_from_url(response).strip()
                if page_text:
                    subtopic_text += " " + page_text
                    subtopic_text = re.sub(r"[^A-Za-z0-9]+", " ", subtopic_text)
        except Exception as e:
            # enquanto você está debugando, é bom ver qual URL quebra
            print("Erro ao processar URL:", url, "->", e)
    return subtopic_text



#def generate_search_query(topic_names, keywords):
#    query = "("
#    for i in range(len(keywords)-1):
#        #concatenating the keywords with 'or'
#        query = query + keywords[i].lower() + " or "
#    query = query + keywords[len(keywords)-1].lower() + ") and ("
#    '''Starts new code'''
#    logging.debug("Query:")
#    logging.debug(query)
#    '''Ends new code'''
#
#    for i in range(len(topic_names)-1):
#        query = query + topic_names[i].lower() + " or "
#
#    query = query + topic_names[len(topic_names)-1].lower() + ")"
#    print("Query: ", query)
#    return query#concatenating the keywords with the topic, e.g.: keywords = [racing, homing]; topic = [birds] i.e. query = '(racing or homing) and (birds)'

def generate_search_query(topic_names, keywords):
    if not keywords:
        # fallback simples: usa só os topics
        base = " or ".join(t.lower() for t in topic_names)
        query = f"({base})"
        print("Query (sem keywords):", query)
        return query

    query = "(" + " or ".join(k.lower() for k in keywords) + ") and ("
    logging.debug("Query:")
    logging.debug(query)

    query += " or ".join(t.lower() for t in topic_names) + ")"
    print("Query: ", query)
    return query


def get_data(topics):
    #storing a list of topics in current job
    topic_names = topics["topic_name"]
    #storing a list of subtopics in current job
    subtopics = topics["subtopics"]
    #initializing an empty dictionary
    topic_text = {}
    for i in range(len(subtopics)):
        print ("Looking for data")
        subtopic_name = subtopics[i]["subtopic_name"]
        print (subtopic_name)
        subtopic_keywords = subtopics[i]["keywords"]
        search_query = generate_search_query(topic_names, subtopic_keywords)#storing the search query string with the topics and keywords
        subtopic_text = google_search_query(search_query)

        if len(subtopic_text.strip()) == 0:
            subtopic_text = google_search_query(search_query)
        topic_text[subtopic_name.lower()] = subtopic_text

    return topic_text
