from flask import Flask, session, render_template, request
import google, urllib, re, pickle, sys
from bs4 import BeautifulSoup

app = Flask(__name__)

##isname, stringify, and findnames taken from regex assignment
def isname(lis,d):
    x=0
    for sub in lis:
        if sub in d:
            #print sub
            pass
            x=x+1
            #print x
        if x==2: 
            return False
    return True

def stringify(L):
    s = ""
    for n in L:
        for sub in n:
            s = s+" "+sub
        s=s+","
    return s[:-1]

def findnames(txt,d):
    p = re.compile('(?:[A-Z][a-z].\.)* (?:[A-Z][a-z]+)(?:\s[A-Z][a-z]+)+')
    L=p.findall(txt)
    x=0
    for i in xrange(len(L)):
        L[i] = L[i].replace('\n',' ')
        L[i] = L[i].lower().split(" ")
    #print stringify(L)

    L[:] = [ o for o in L if isname(o,d)]
    return L

##organizes results 
def histogram(L):
    D = {}
    for x in L:
        s = ' '.join(x)
        if s in D.keys():
            D[s]+=1
        else:
            D[s]=1
    s = ''
    for w in sorted(D,key=D.get, reverse=True):
        s+=`w`+' | '+`D[w]`+'\n'
    print s
    return s
    
def switchboard(s,g):
    L=s.lower().split(' ')
    if L[0]=='who':
        return who(g)
    else:
        return 'you search for '+s

def who(g):
    result = ''
    h = open('diction.txt','rb')
    d = pickle.load(h)
    h.close()
    names=[]
    for link in g:
        html = urllib.urlopen(link).read()
        soup = BeautifulSoup(html)
        for script in soup(['script','style']):
            script.extract()
        txt = soup.get_text()
        print link
        names.extend(findnames(txt,d))
    return histogram(names)

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        query = request.form['query']
        n=5 ##the number of results, but the program is really slow
        g = google.search(query, num = n, start = 0, stop = n)
        result = switchboard(query,g)
        return render_template("search.html",result=result,search=True)
    


if __name__ == "__main__":
    app.debug = True
    app.run()
