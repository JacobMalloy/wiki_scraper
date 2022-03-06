from bs4 import BeautifulSoup
from collections import deque
import urllib3
import re

r = re.compile("^/+(en.wikipedia.com/){0,1}wiki/(?!Special:)(?!Portal:)(?!Talk:)(?!Help:)(?!Wikipedia:)(?!Template:)(?!File:)(?!Category:).*");

visited_set=set()
frontier=deque()

http = urllib3.PoolManager()

def write_set(name,cur_set):
    s=""
    for i in cur_set:
        s+=i+"\n"
    with open(f"data/{name}","w") as f:
        f.write(s)

def getLinks(url):
    global visited_set
    global frontier
    global http
    cur_set=set()
    if url in visited_set:
        return
    visited_set.add(url)
    html_page = http.request('GET',f"https://en.wikipedia.org/wiki/{url}").data
    soup = BeautifulSoup(html_page,"html.parser")


    for link in soup.find_all("a",href=True):
        s = link["href"]
        #print(s)
        if(r.match(s)):
            frontier.append(s.split("/")[-1].split("#")[0])
            cur_set.add(s.split("/")[-1].split("#")[0])
    write_set(url,cur_set)

start = "Alan_Turing"
frontier.append(start);
v=""
while len(frontier)>0:
    val = frontier.popleft()
    print(val);
    getLinks(val)
