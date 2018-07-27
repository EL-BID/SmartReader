from __future__ import absolute_import
from __future__ import division #print_function, unicode_literals
from unidecode import unidecode
import sys, traceback
import unicodedata
import codecs

import requests
import unicodedata
import spacy
from spacy.lang.en import English #update for python 3
nlp = spacy.load('en')
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import nltk, re, pprint
from nltk import word_tokenize
from nltk import sent_tokenize



from gensim.summarization import keywords
from gensim.summarization import summarize

sentencess=[]
compare=[]


LANGUAGE = "english"


def get_summary(textss , truereq, numofsent):
    output_sentences = []
    hold=''

    truecount=0



    #print('\n\n\n\n\n\n' )

    store=''
    store=keywords(textss,ratio=0.05)
    store1=str(store)
    holdfirst=nltk.word_tokenize(store1)
    ##print(holdfirst)



    #INCLUDE TEXT FILE AGAIN HERE!!

    parser=PlaintextParser.from_string(textss,Tokenizer(LANGUAGE)) # IF READING FROM A TEXT FILE



    stemmer = Stemmer(LANGUAGE)

    #summarizer = LexRankSummarizer(stemmer)

    summarizer = Summarizer(stemmer)

    summarizer.stop_words = get_stop_words(LANGUAGE)


    sentencess=[]

    compare=[]

    for sentence in summarizer(parser.document,numofsent):



        #print(sentence)

        print('\n')



        hold=str(sentence)

        ttt=nltk.word_tokenize(hold)



        count=0

        for i in range(0, len(ttt)):


            for j in range(0,len(holdfirst)):

                if ttt[i]==holdfirst[j]:

                    count+=1

        compare.append(count)

        sentencess.append(str(sentence))###################0000000000000000000000000000000000000000000000000000000000


    ########################################################################
    ##############################################
    #####################################
    #####################


    from gensim import corpora, models, similarities
    from nltk.tokenize import sent_tokenize



    #texty=a.text ######################################369\\0000000000000000000000000000000000

    import os
    import tempfile
    TEMP_FOLDER = tempfile.gettempdir()
    #print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))


    documents=sent_tokenize(textss)

    summalen=len(documents)


    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
              for document in documents]

    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
              for text in texts]

    from pprint import pprint  # pretty-#printer
    #pprint(texts)


    dictionary = corpora.Dictionary(texts)

    dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))  # store the dictionary, for future reference

    #print(dictionary)

    #print(dictionary.token2id)###################################



    new_doc = str(textss.encode('utf-8'))
    new_vec = dictionary.doc2bow(new_doc.lower().split())

    corpus = [dictionary.doc2bow(text) for text in texts]

    corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'deerwester.mm'), corpus)  # store to disk, for later use


    dictionary = corpora.Dictionary.load( os.path.join(TEMP_FOLDER,  'deerwester.dict') )
    corpus = corpora.MmCorpus( os.path.join(TEMP_FOLDER,  'deerwester.mm') ) # comes from the first tutorial, "From strings to vectors"
    ##print(corpus)

    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)



    doc = str(textss.encode('utf-8'))
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow] # convert the query to LSI space
    ##print(vec_lsi)

    index = similarities.MatrixSimilarity(lsi[corpus])

    index.save( os.path.join(TEMP_FOLDER,  'deerwester.index') )
    index = similarities.MatrixSimilarity.load( os.path.join(TEMP_FOLDER,  'deerwester.index') )


    sims = index[vec_lsi]
    ##print(list(enumerate(sims)))
    sims = sorted(enumerate(sims), key=lambda item: -item[1])


    newlist=[]


    for i in range(0,summalen):
        newlist.append(documents[sims[i][0]])
        if i==4:
            break



    for sentencez in newlist:


        #print('\nThese are NEW SET OF SENTS\n')

        #print(sentencez)

        #print('\n')



        hold=str(sentencez)

        ttt=nltk.word_tokenize(hold)



        count=0

        for i in range(0, len(ttt)):


            for j in range(0,len(holdfirst)):

                if ttt[i]==holdfirst[j]:

                    count+=1

        compare.append(count)

        sentencess.append(str(sentencez))############
        # print(sentencess)












    ######################
    ####################################
    ##############################################
    #########################################################################

    ##print(sentencess)
    ##print('\n\n')
    ##print(compare)
    ##print('\n\n')

    #print('\n\nSUMMARY \n\n')





    i=0

    while i<truereq:

        holdsubs=[]




        indexes=compare.index(max(compare))






        doc1=nlp( u'%s' %  str(sentencess[indexes]))
        parse=doc1



        for word in parse:


            if word.dep_ == 'nsubj':
                holdsubs.append(word.text.lower())



                ################################

        if holdsubs:

            if holdsubs[0]!='they' and holdsubs[0]!='their' and holdsubs[0]!='both' and holdsubs[0]!='these' and holdsubs[0]!='this':
                countcomma=str(sentencess[indexes]).count(',')
                if countcomma<7:
                    #print(sentencess[indexes]) # THESE ARE THE SUMMARIZED SENTENCES
                    output_sentences.append(sentencess[indexes])
                    #print('\n')
                    #print(compare[indexes])

                    i+=1








        del sentencess[indexes]
        del compare[indexes]





    return output_sentences





# if __name__ == "__main__":


# text = """Definitions of mobile financial services. Uses the mobile phone to transfer money and make payments to the underserved. The GSMA Mobile Money team tracks mobile money services which meet the following criteria. The service must offer at least one of the following products domestic or international transfer mobile payments including bill payment bulk disbursement and merchant payment. The service must rely heavily on a network of transactional points outside bank branches and ATMs which make the service accessible to unbanked and underbanked people. Customers must be able to use the service without having been previously banked. Mobile banking services which offer the mobile phone as just another channel to access a traditional banking product and payment services linked to a current bank account or credit card such as Apple Pay and Google Wallet are not included. The service must offer an interface for initiating transactions for agents and or customers which is available on basic mobile devices. Uses the mobile phone to provide savings services to the underserved. The GSMA Mobile Money team tracks mobile savings services which meet the following criteria. The service allows subscribers to save money in an account which provides principal security and in some cases an interest rate. The service must allow underserved people to save money using a mobile device. Services which offer the mobile phone as just another channel to access a traditional savings account are not included. The service must be available on basic mobile devices. Uses the mobile phone to provide credit services to the underserved. The GSMA Mobile Money team tracks mobile credit services which meet the following criteria. The service allows subscribers to borrow a certain amount of money which they agree to repay within a specified period of time. The service must allow underserved people to apply for credit and repay it more easily using a mobile device. Airtime credit products or services which offer the mobile phone as just another channel to access a traditional credit product are not included. The service must be available on basic mobile devices. Uses the mobile phone to provide insurance services to the underserved. The GSMA Mobile Money team tracks mobile insurance services which meet the following criteria. The service must allow subscribers to manage risks by providing a guarantee of compensation for specified loss damage illness or death. The service must allow underserved people to access insurance services easily using a mobile device.Services which offer the mobile phone as just another channel for the clients of an insurance company to access a traditional insurance product are not included. The service must be available on basic mobile devices."""
# output = get_summary( text, 1, 4 )






#FILE TO BE SUMMARIZED TO BE INCLUDED BELOW, AND ONCE IN THE test_func function.



# text=''
# filea = 'sub-topics/Taxation'
# x = open(filea)
# text = unidecode(x.read().decode("utf-8") )



# #TEXT FOR TEXT FILES


# # truereq holds number of sentences you want in summary.

# truereq=2


# numofsent=truereq*3







# status = get_summary(text, truereq, numofsent)
