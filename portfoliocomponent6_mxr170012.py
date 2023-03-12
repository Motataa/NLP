# Motalib Rahim
# mxr170012
# Dr. Karen Mazidi

import requests # send https req
from bs4 import BeautifulSoup # parsing data, formatting
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
from nltk.probability import FreqDist  # distribution


def webcrawl(url: str):
    page = requests.get(url) # stores response once requests are sent
    soup = BeautifulSoup(page.content, 'html.parser') # object created from html to info
    output = list() # lists contains 15 relevant url
    counter = 0 # counts no. of links
    for link in soup.find_all('a'):  # iterate through specific html tag
        output.append(link['href'])
        counter += 1
        if counter == 15: # 15 urls according to its relevancy
            break
    return output

def scrape(url):

    web_url = webcrawl(url)
    # iterate and write urls to a file
    for x in web_url:
        f_name = x.split(".")[1] + ".txt"
        html = requests.get(url).content
        f = open(f_name, 'w+')
        f.write(str(html))
        f.close()

def clean(url: str):

    # retrieve url
    web_url = webcrawl(url)

    for x in web_url:
        # retrieve html
        get_text = str(requests.get(x).content)

        # delete newlines and tabs
        get_text = get_text.replace("\n", " ")
        get_text = get_text.replace("\t", " ")

        # tokenize sentence
        token = sent_tokenize(get_text)

        sent = token
        # store token in file
        z = ""
        f_name = url.split(".")[1] + "_word.txt"
        file = open(f_name, 'w+')

        for sents in sent:
            z += sents + "\n"
            file.write(z)

        file.close()

def imp_terms(url: str):

    # retrieve
    get_text = str(requests.get(url).content)

    # clean
    get_text = get_text.replace("\n", " ")
    get_text = get_text.replace("\t", " ")

    token = word_tokenize(get_text)

    # retrieve text; remove stopwords and punctuation
    term = (t for t in token if t.isalpha() and len(t) > 4 and t.lower)

    term_in = nltk.Text(term) # nltk conversion

   # frequency calculation
    calc = dict(FreqDist(term_in))
    calc = dict(sorted(calc.items(), key=lambda v: v[1], reverse=True))

    # store in file
    z = ""
    f_name = url.split(".")[1] + "imp_terms.txt"
    file = open(f_name, "w+")
    for key in list(calc.items())[:40]:
        z += "(" + key[0] + "," + str(key[1]) + ")\n"
        file.write(z)
    file.close()

    return list(calc.items())[:40]


def search(url):

    first = dict() # first word
    check = list() # if word exists
    inline = list() # next in line

    get_text = str(requests.get(url).content)

    # delete newlines and tabs
    get_text = get_text.replace("\n", " ")
    get_text = get_text.replace("\t", " ")

    # tokenize sentence
    token = sent_tokenize(get_text)

    sent = token
    # take token and store
    facts = [v[0] for v in imp_terms(url)[:10]]
    inline = facts.copy()

    while len(inline) > 0:
        t = inline.pop()
        if not t in first and len(t)  > 0 and t.isalpha():
            first[t] = list()

        for l in sent:
            if t in l:
                term = l.split(" ")
                for t2 in term:
                    if t2 != t and len(t2) > 0 and t2.isalpha():
                        inline.append(t2)
                        first[t].append(t2)

    return first


if __name__ == '__main__':
    # sports site
    url = "https://www.skysports.com/"  # chosen url to scrape
    print(webcrawl(url))

    term = imp_terms(url)
    print(f"Top 10 terms of the website {url}: ") # output top 10 terms
    for g in range(len(term)):
        key = term[g]
        print(key[0], end = "")
        if g < len(term)-1:
            print(", ", end ="")
        else:
            print("")
    print(search(url))

