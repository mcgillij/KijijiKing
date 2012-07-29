from bs4 import BeautifulSoup
import httplib, re
from pprint import pprint
from collections import defaultdict

def remove_control_chars(s):
    return (''.join([x for x in s if ord(x) < 128]))
    
def is_want(product):
    return (re.search(r'Wanted', product))    
            
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_result(soup, num):
    match = "resultRow"+str(num)
    
    if (soup.find(id=match)):       
        mylist = soup.find(id=match).findAll("td")
        mylink =  soup.find(id=match).a
        desc = mylist[2]
        desc = remove_html_tags(str(desc))    
        return (str(mylink) + desc)
    else:
        return
    
def process_first_page(results, search):
    pagenum = 1;
    
    if pagenum == 1:
        pagestr = "isSearchFormZtrue"
    else:
        pagestr = "PageZ"+pagenum

    city = "halifax.kijiji.ca"
    httpconn = httplib.HTTPConnection(city)
    if (type(search) is list or type(search) is tuple):
        searchstr1 = "-".join(search)
        searchstr2 = "Q20".join(search)
    else:
        searchstr1 = search
        searchstr2 = search

    querystr = "/f-"+searchstr1+"-Classifieds-W0QQKeywordZ"+searchstr2+"QQ"+pagestr
    httpconn.request("GET", querystr)

    r1 = httpconn.getresponse()
    print r1.status, r1.reason
    data1 = r1.read()
    soup = BeautifulSoup(data1)
    
    
    items = 20
    for i in reversed(range(items)):        
        product = get_result(soup, i)        
        if (product and not is_want(product)):
            results[search].append( product)



if __name__ == '__main__':
    results = defaultdict(list)
    search_list = ['bass', 'pants', 'joystick']
    for e in search_list:
        print "searching for:  "+ e
        process_first_page(results, e)
    pprint(results['bass'])