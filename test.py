from gensim.corpora import MmCorpus
from gensim.test.utils import get_tmpfile
corpus = [[(0, 1), (1, 1)], [(0, 1), (1, 1), (2, 2)]]
output_fname = get_tmpfile("test.mm")

MmCorpus.serialize(output_fname, corpus)
mm = MmCorpus(output_fname) # `mm` document stream now has random access
# print(mm[1]) # retrieve document no. 42, etc.
# print(mm[0])




# paragraphs = ["value1","value2","value3","value4","value5","value6","value7","value8","value9",]

# for p in range(len(paragraphs)):
# 	print('good')
# 	print(str(p))


# for p in paragraphs[0:50]:
# 	print('over')
# 	print(str(p))


# for p in paragraphs[0:4]:
# 	print('below')
# 	print(str(p))

'''
texts = [['survey', 'data', 'survey', 'data', 'is', 'by'], ['data', 'is', 'is', 'is', 'as', 'as', 'is', 'by'], ['data', 'is', 'data']]
dictionary = <gensim.corpora.dictionary.Dictionary object at 0x7f4db803dba8> (just as a reference)

import tempfile
import os
from gensim import corpora, models, similarities

TEMP_FOLDER = tempfile.gettempdir()
dictionary = corpora.Dictionary([['survey', 'data', 'survey', 'data', 'is', 'by'], ['data', 'is', 'is', 'is', 'as', 'as', 'is', 'by'], ['data', 'is', 'data']])
dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))

-------
import tempfile
import os
from gensim import corpora, models, similarities
TEMP_FOLDER = tempfile.gettempdir()
corups =[[(0, 1), (1, 1)], [(0, 1), (1, 1), (2, 2)]]
corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'deerwester.mm'), corpus)

'''