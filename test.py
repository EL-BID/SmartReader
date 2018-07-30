import os
import nltk
from nltk.tokenize import sent_tokenize

full_text = "The scope of AI is disputed: as machines become increasingly capable, tasks considered as requiring intelligence are often removed from the definition, a phenomenon known as the AI effect, leading to the quip, AI is whatever hasn't been done yet.[3] For instance, optical character recognition is frequently excluded from artificial intelligence, having become a routine technology.[4] Capabilities generally classified as AI as of 2017 include successfully understanding human speech,[5] competing at the highest level in strategic game systems (such as chess and Go),[6] autonomous cars, intelligent routing in content delivery network and military simulations."
sentences = sent_tokenize(full_text)