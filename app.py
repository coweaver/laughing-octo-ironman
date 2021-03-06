from flask import Flask, session, render_template, request
import google, urllib, re, pickle, sys
from bs4 import BeautifulSoup

app = Flask(__name__)

##findnames taken from regex assignment
def isname(word,dic):
    for sub in dic:
        if sub in word:
            return False
    return True


def findnames(txt):
    reg = "((([DMS][ris]{1,3}\.? )?([A-Z]([a-z]*|\.)){1}((([\s-][A-Z][a-z]*){0,1})|(([\s-][A-Z]\.){0,2}))([\s-][A-Z][a-z]+){1}((,?[\s-][JjSs]r.)|([\s-][XIV]+)){0,1})|([DMS][ris]{1,3}\.?[\s-][A-Z][a-z]*))"
    L = []
    ret = re.findall(reg, txt)
    for x in ret:
        if x[0][:3] != "The":
            L.append(x[0])
    return L

def finddates(txt):
    reg = '(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{1,4}'
    L=[]
    ret = re.findall(reg,txt)
    for x in ret:
        L.append(x)
    return L

##organizes results
def histogram(st,L,names):
    D = {}
    for x in L:
        s = ''.join(x)
        if s in D.keys():
            D[s]+=1
        else:
            D[s]=1
    print s
    results = {}
    if names :
        h = open('diction2.txt','rb')
        d = pickle.load(h)
        h.close()
        print d
        numresults = 10
        for w in sorted(D,key=D.get, reverse=True):
            if not w.lower() in st and isname(w,d):
                print D[w]
                print w
                results[D[w]] = w
                numresults-=1
                if numresults == 0:
                    break
    else:
        for w in sorted(D,key=D.get, reverse=True)[:10]:
            print D[w]
            print w
            results[D[w]] = w
    print results
    return results

def switchboard(s,g):
    s=s.lower()
    if s[:3]=='who':
        return who(s,g)
    elif s[:4]=='when':
        return when(s,g)
    else:
        return 'you search for '+s

def who(s,g):
    result = ''
    names=[]
    for link in g:
        html = urllib.urlopen(link).read()
        soup = BeautifulSoup(html)
        for script in soup(['script','style']):
            script.extract()
        txt = soup.get_text().replace('\n',' ')
        print link
        names.extend(findnames(txt))
    return histogram(s,names,True)

def when(s,g):
    dates=[]
    for link in g:
        html = urllib.urlopen(link).read()
        soup = BeautifulSoup(html)
        for script in soup(['script','style']):
            script.extract()
        txt = soup.get_text().replace('\n',' ')
        print link
        dates.extend(finddates(txt))
    return histogram('',dates,False)


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        query = request.form['query']
        n=5 ##the number of results, but the program is really slow
        g = google.search(query, num = n, start = 0, stop = n)
        result = switchboard(query,g)
        if isinstance(result, dict):
            sortedKeys = sorted(result.keys(), reverse = True)
            return render_template("search.html",result=result,isDict=True,
                                   sortedKeys=sortedKeys,search=True)
        else:
            return render_template("search.html",result=result,isDict=False,
                                   search=True)


if __name__ == "__main__":
    app.debug = True
    app.run()

