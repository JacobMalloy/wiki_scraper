from bs4 import BeautifulSoup
from collections import deque
import urllib3
import re

r = re.compile("^/+(en.wikipedia.com/){0,1}wiki/(?!Special:)(?!Wikipedia:)(?!Template:)(?!File:)(?!Category:).*");

visited_set=dict()
frontier=deque()

http = urllib3.PoolManager()

def getLinks(url):
    global visited_set
    global frontier
    global http
    if url[0] in visited_set:
        return
    visited_set[url[0]] = url[1]
    html_page = http.request('GET',f"https://en.wikipedia.org/wiki/{url[0]}").data
    soup = BeautifulSoup(html_page,"html.parser")


    for link in soup.find_all("a",href=True):
        s = link["href"]
        #print(s)
        if(r.match(s)):
            frontier.append((s.split("/")[-1].split("#")[0],url[0]))


start = "David_Icove"
end = "Donald_Trump"
frontier.append((start,"start"));
v=""
while True:
    val = frontier.popleft()
    print(val);
    if(val[0]==end):
        visited_set[val[0]] = val[1]
        print("finished")
        v=val[0]
        break
    getLinks(val)
#print(visited_set)
while v!="start":
    print(v)
    v=visited_set[v]
