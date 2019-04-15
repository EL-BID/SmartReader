from _google_ import search
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import logging


def get_text_from_url(response):
    try:
        soup = BeautifulSoup(response, "html.parser")
        text = " "
        all_paras = soup.findAll('p')
        if all_paras is not None:
            text = ''.join(p.text.strip() for p in all_paras)
    except Exception as e:
        pass
    return text


def google_search_query(query):
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


def generate_search_query(topic_names, keywords):
    query = "("
    for i in range(len(keywords)-1):
        #concatenating the keywords with 'or'
        query = query + keywords[i].lower() + " or "
    query = query + keywords[len(keywords)-1].lower() + ") and ("
    '''Starts new code'''
    logging.basicConfig(filename='./log/query.txt', filemode='w', level=logging.DEBUG)
    logging.debug("Query:")
    logging.debug(query)
    '''Ends new code'''

    for i in range(len(topic_names)-1):
        query = query + topic_names[i].lower() + " or "

    query = query + topic_names[len(topic_names)-1].lower() + ")"
    print("Query: ", query)
    return query#concatenating the keywords with the topic, e.g.: keywords = [racing, homing]; topic = [birds] i.e. query = '(racing or homing) and (birds)'


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
