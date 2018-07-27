from _google_ import search
#from urllib2 import urlopen //python 2.7
from urllib.request import urlopen #update for python 3
from bs4 import BeautifulSoup
import re


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
                # print("Subtopic not pdf: ", subtopic_text)
                subtopic_text = re.sub('[^A-Za-z0-9]+', ' ', subtopic_text)
                # print("Subtopic No punctuation: ", subtopic_text)
        except Exception as e:
            pass
    return subtopic_text


def generate_search_query(topic_names, keywords):
    query = "("
    for i in range(len(keywords)-1):
        query = query + keywords[i].lower() + " or " #this concatanates the keywords with 'or'

    query = query + keywords[len(keywords)-1].lower() + ") and ("

    for i in range(len(topic_names)-1):
        query = query + topic_names[i].lower() + " or "

    query = query + topic_names[len(topic_names)-1].lower() + ")"
    print("Query: ", query)
    return query #concatenate keywords with topic, e.g.: subtopics = [racing, homing], topic = [birds] i.e. query = '(racing or homing) and (birds)'


def get_data(topics):
    topic_names = topics["topic_name"]#list of topics in current job
    subtopics = topics["subtopics"]#list of subtopics in current job
    topic_text = {}#initialize an empty dictionary
    for i in range(len(subtopics)):
        print ("Looking for data")
        subtopic_name = subtopics[i]["subtopic_name"]
        print (subtopic_name)
        subtopic_keywords = subtopics[i]["keywords"]
        search_query = generate_search_query(topic_names, subtopic_keywords)#search query string with the topics and keywords
        subtopic_text = google_search_query(search_query)

        if len(subtopic_text.strip()) == 0:
            subtopic_text = google_search_query(search_query)
        topic_text[subtopic_name.lower()] = subtopic_text

    return topic_text
