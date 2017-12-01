#!/usr/local/bin/python

#standard libs
import operator
from collections import defaultdict
import os
from io import StringIO
import hashlib, uuid

import requests as req
from bs4 import BeautifulSoup
from nltk import download, pos_tag
from nltk.tokenize import RegexpTokenizer
from os import path
from PIL import Image
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from wordcloud import WordCloud
from Crypto.Cipher import AES

#for testing purposes
URL = 'https://en.wikipedia.org/wiki/Octopus'

KEY = hashlib.sha256('hireJ@keLy0ns'.encode('utf-8')).digest()
IV = 16 * '\x00'
MODE = AES.MODE_CBC

def get_salt():
    return uuid.uuid4().hex

def encrypt_word(_word):
    encryptor = AES.new(KEY, MODE, IV=IV)
    return encryptor.encrypt(_word)

def decrypt_word(_word):
    decrytor = AES.new(KEY, MODE, IV=IV)
    return decryptor.decrypt(ciphertext)


class WCTopWords(object):
    """ creates a wordcloud from the top 100 words used in a given website

        USAGE
            example init:
                `wc = LyonsOctopusTopWords('https://en.wikipedia.org/wiki/Octopus')`
            optional init params:
                render: (boolean, default=False) set True to render to screen for testing
                    `wc = LyonsOctopusTopWords('www.yahoo.com',render=True)`
                nv_only: (boolean, deafault=True) parse only nouns and verbs or all words
                    `wc = LyonsOctopusTopWords('www.yahoo.com',nv_only=False)`
    """
    def __init__(self, url=URL):
        self.url = url
        self.words = None
        self.encr_words = None
        self.salt_key = None

    def generate_wc(self, render=False, nv_only=True):
        page_text = self.get_page_text(self.url)
        nouns_and_verbs = self.get_words(page_text, nouns_verbs=nv_only)
        self.words = self.get_top_100_words(nouns_and_verbs)
        self.encr_words = self.encrypt(self.words)
        self.generate_octopus_shaped_word_cloud(self.words, render_to_screen=render)

    def get_page_text(self, _url):
        """ takes in a url --string
            returns lowercase text of the body of that web page --string
        """
        page = req.get(_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        # text = soup.get_text().lower()
        text = soup.body.get_text().lower()

        return text


    def get_words(self, _text, nouns_verbs=True):
        """ takes in web page text --string
            returns only the noun and verb words --list of strings
        """
        # only parse 'word characters', ie no digits, or non alphabectical letters
        tokenizer = RegexpTokenizer(r'\w+')

        # first time script runs, download the ntlk corpus, needed to find nouns and verbs
        try:
            tokens = tokenizer.tokenize(_text)
        except LookupError:
            download('popular') #'wordnet' smaller? and works?   MOVE TO __INIT__ !!!
            tokens = tokenizer.tokenize(_text)
        tags = pos_tag(tokens)

        if nouns_verbs:
            # for tag reference https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/"""
            accetable_tags = ['NN','NNP','NNS','NNPS','VB','VBD','VBG', 'VBN', 'VBP', 'VBZ']
            # yes, technically 'I' should appear, but word clouds are boring with small words ;)
            return [word for word,pos in tags if (pos in accetable_tags and len(word) > 1)]
        else:
            return [word for word,pos in tags if (len(word) > 1)]


    def get_top_100_words(self, _words):
        """ takes in a list of words --list
            returns the top 100 most frequent --dict (key=word,val=freq)
        """
        word_counts = defaultdict(int)
        for word in _words:
            word_counts[word] += 1

        wsort = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
        return dict(wsort[:100])


    def encrypt(self, _words):
        """ takes in words --dict (key=word,val=freq)
            return list of dicts (one dict per word)
                --dict {'salt_hash':string, #salted hash of the word
                        'encr_word':string, #encrypted word
                        'freq':int, #frequency of the word}
        """
        all_encr_words = []
        salt_key = get_salt()
        for word, freq in _words.items():
            encr_words = {}
            # need to convert, so can properly be saved in the db
            # salted_word_hash = hashlib.sha256((word+salt_key).encode('utf-8')).digest()
            salted_word_hash = word+salt_key
            encr_words['salt_hash'] = salted_word_hash
            # encr_word = encrypt_word(word) ##need to implement padding to fix
            encr_word = word
            encr_words['encr_word'] = encr_word
            encr_words['freq'] = freq
            all_encr_words.append(encr_words)
        return all_encr_words


    def generate_octopus_shaped_word_cloud(self, _words, render_to_screen=False):
        """ takes an input of words and their freq --dict (key=word,val=freq)
            saves the world cloud image to ./wcloud.png
        """
        d = path.dirname(__file__)
        # d = os.getcwd()

        # read the mask image
        # taken from http://cliparts.co/cliparts/5cR/yLR/5cRyLRnca.png
        octopus_mask = np.array(Image.open(path.join(d, "octopus_stencil.png")))

        # already parsed for nouns and verbs so this is unnecessary
        # but easy way to add default or additional stopwords
        # from wordcloud import STOPWORDS
        # stopwords = set(STOPWORDS)
        # stopwords.add("insert_custom_word_here")
        stopwords = []

        wc = WordCloud(background_color="white", max_words=2000, mask=octopus_mask,
                       stopwords=stopwords)

        # generate word cloud
        wc.generate_from_frequencies(_words)

        # store to file
        wc.to_file(path.join(d, "templates/wcloud.png"))

        # matplotlib is causing RuntimeError due to python installation issues locally
        if render_to_screen:
            plt.imshow(wc, interpolation='bilinear')
            plt.axis("off")
            plt.show()





if __name__ == '__main__':
    wctw = WCTopWords(URL)
    wctw.generate_wc(render=False)
    # wctw.generate_wc(render=True, nv_only=False)




#for debugging
#exec(open("./generator.py").read())
