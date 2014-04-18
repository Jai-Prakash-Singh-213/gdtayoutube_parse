import random
import  urllib2
import urllib2, feedparser
import logging 
from bs4 import BeautifulSoup
from lxml import html
import json
import time 
import os 

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')




def main(url):
    f = open("/home/desktop/proxy_http_auth.txt")
    file_pass_ip = f.read().strip().split('\n')
    f.close()

    while True:
        try:
            pass_ip = random.choice(file_pass_ip).strip()
            logging.debug(pass_ip)
            proxy = urllib2.ProxyHandler({'http': 'http://'+pass_ip})
            auth = urllib2.HTTPBasicAuthHandler()
            opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            return proxy
        except:
            pass



def supermain(tvs, url):
    proxy = main(url)

    d = feedparser.parse(url,   handlers = [proxy])
    
    gdatajson = []    
   
    gdatajson2 = {}

    for post in d.entries:
        summary_detail = str(post.summary_detail["value"])
        soup = BeautifulSoup(summary_detail, "html.parser")
        img_link = soup.find("img").get("src")

        P_big_title = str(post.title.encode("ascii","ignore"))
        p_title = P_big_title[:P_big_title.find("-")]
        p_link = str(post.link)[:str(post.link).find("&")]
        p_update = str(post.updated)
        p_img = str(img_link)

        gdatajson.append({"title":p_title, 
                          "link": p_link, 
                          "data_updated":p_update, 
                          "img_link":p_img})

        if gdatajson2.get(p_title) is None:
            gdatajson2[p_title] = [{"big_title":P_big_title, 
                                    "link": p_link, 
                                    "img_link": p_img, 
                                    "data_updated": p_update}]
        else:
            gdatajson2[p_title].append({"big_title": P_big_title, 
                                        "link": p_link, 
                                        "img_link": p_img, 
                                        "data_updated": p_update})

        

    if  len(gdatajson) == 0:
        supermain(tvs, url)

    else:
        filename = "/home/desktop/gdtayoutube/gdtayoutube/%s.json" %(tvs)
        filename2 = "/home/desktop/gdtayoutube/gdtayoutube/%s2.json" %(tvs)

        valu_dict = {"value":gdatajson}
        valu_dict2 = {"value": gdatajson2}
 
        f = open(filename, "w+")
        json_encoded = json.dumps(valu_dict)
        f.write(str(json_encoded))
        f.close()      

        f = open(filename2, "w+")
        json_encoded2 = json.dumps(valu_dict2)
        f.write(str(json_encoded2))
        f.close()


        print valu_dict
        print valu_dict2


def sub_supermain():
    tvs_lnk = {
       "strpls":"http://gdata.youtube.com/feeds/base/users/starplus/uploads?v=2&orderby=updated&alt=rss&client=ytapi-youtube-rss-redirect",        "lifeok":"http://gdata.youtube.com/feeds/base/users/lifeok/uploads?client=ytapi-youtube-rss-redirect&alt=rss&orderby=updated&v=2", 
       "channlv":"http://gdata.youtube.com/feeds/base/users/channelvindia/uploads?orderby=updated&alt=rss&client=ytapi-youtube-rss-redirect&v=2",       
       "sony":"http://gdata.youtube.com/feeds/base/users/setindia/uploads?v=2&orderby=updated&client=ytapi-youtube-rss-redirect&alt=rss",
       "zeetv":"http://gdata.youtube.com/feeds/base/users/zeetv/uploads?v=2&alt=rss&orderby=updated&client=ytapi-youtube-rss-redirect",
       "clrs": "http://gdata.youtube.com/feeds/base/users/colorstv/uploads?orderby=updated&client=ytapi-youtube-rss-redirect&alt=rss&v=2"}

    for tvs, link in tvs_lnk.items():
        supermain(tvs, link)
    

if __name__=="__main__":
    sub_supermain()
