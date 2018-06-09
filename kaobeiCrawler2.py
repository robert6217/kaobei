from __future__ import with_statement
import contextlib
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import re
import multiprocessing
import facebook
import requests
import json,time
from dbmodel import *
platform = 10

KAOBEILIST = ['862391723791057', '740862172781897', 'CowBeiPCCU', '1513369348921394', 'CowBeiTSVS', 'cowbayfit', 'KaobeiGirlfriend', 'KaobeiBoyfriend', 'kaobeitku', 'kobeengineer', 'cowbeifju', 'cowbeiNTHU', 'NTPUhate', 'CowBeiNCTU', 'kobeshida', '903473626385697']

HOST  = 'https://graph.facebook.com/v3.0/'

def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    result = file.text.split("=")[1]
    return result

def shortUrl(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')

def getPicture(kaobei):
    token = get_fb_token(app_id, app_secret)
    graph = facebook.GraphAPI(access_token = token)
    page_info = graph.get_object(kaobei, field = 'id')
    fanspageid = page_info['id']
    kaobeiname = page_info['name']
    #print(fanspageid)
    #print(kaobeiname)
    picture = graph.get_connections(id = kaobei, connection_name = 'picture', type='large')
    pictureurl = picture['url']
    pictureshorturl = shortUrl(pictureurl)
    #print(pictureshorturl)
    if selectdata_ID(fanspageid) == 0:
        insertdata_ID(fanspageid, kaobeiname, pictureshorturl)
        print('insert: ', fanspageid, kaobeiname, pictureshorturl)
    else:
        updatedata_ID(fanspageid, kaobeiname, pictureshorturl)
        print('update: ', fanspageid, kaobeiname, pictureshorturl)

def getID(kaobei):
    token = get_fb_token(app_id, app_secret)
    getPicture(kaobei)
    postid_list = []
    res_posts = requests.get(HOST+kaobei+'/posts?limit=100&access_token='+token)
    posts = json.loads(res_posts.text)
    for post in posts['data']:
        #print(post['id'])
        postid_list.append(post['id'])
    return postid_list

def getPostInfo(postid):
    token = get_fb_token(app_id, app_secret)
    dataList = []
    res_post_info = requests.get(HOST+postid+'/?fields=created_time,message,link,likes.limit(0).summary(True),comments.limit(0).summary(True),shares&access_token='+token)
    post_info = json.loads(res_post_info.text)
    #print(post_info)
    if 'created_time' in post_info:
        posttime = post_info['created_time']
    else:
        posttime = ''
    if 'message' in post_info:
        postmessage = post_info['message']
    else:
        postmessage = ''
    if 'link' in post_info:
        postlink = post_info['link']
        postlink = shortUrl(postlink)
    else:
        postlink = ''
    if 'likes' in post_info:
        postlike = post_info['likes']['summary'].get('total_count')
    else:
        postlike = 0
    if 'comments' in post_info:
        postcomment = post_info['comments']['summary'].get('total_count')
    else:
        postcomment = 0
    if 'shares' in post_info:
        postshare = post_info['shares'].get('count')
    else:
        postshare = 0

    dataList.append([postid, posttime, postmessage, postlink, postlike, postcomment, postshare])
    #print(postid, postlike, postcomment, postshare)
    return dataList

def kaobeiList(kaobei_list):
    info = []
    for postid in getID(kaobei_list):
        info.append(getPostInfo(postid))
    return info

def kaobei(kaobeilist):
    pool = multiprocessing.Pool(processes=platform)
    print('cpu_count:',multiprocessing.cpu_count())
    result = []
    for web in kaobeilist:
        result.append(pool.apply_async(kaobeiList,(web,)))
        accessKaobeiData_data(result)
    pool.close()
    pool.join()

def selectdata_ID(fanspageid):
    return len(KaobeiID.query.filter_by(FansPageID = fanspageid).all())

def updatedata_ID(fanspageid, kaobeiname, pictureshorturl):
    update_data = KaobeiID.query.filter_by(FansPageID=fanspageid).update({ KaobeiID.KaobeiName: kaobeiname, KaobeiID.KaobeiPicture: pictureshorturl })
    db.session.commit()fanspageid

def insertdata_ID(fanspageid, kaobeiname, pictureshorturl):
    insert_data = KaobeiID(FansPageID=fanspageid, KaobeiName=kaobeiname, KaobeiPicture=pictureshorturl)
    db.session.add(insert_data)
    db.session.commit()

def accessKaobeiData_data(result):
    for i in result:
        for j in i.get():
            for k in j:
                print(k)
                pageid = re.sub(r'_[0-9]+', "", k[0])
                selectdata = KaobeiData.query.filter_by(PostID = postid_short)
                postid_short = postid.replace(pageid+'_', "")
                insert_data = KaobeiData(PageID=pageid
                                        , PostID=postid_short
                                        , PostTime=k[1]
                                        , PostMessage=k[2]
                                        , PostLink=k[3]
                                        , PostLike=k[4]
                                        , PostComment=k[5]
                                        , PostShare=k[6])
                if selectdata.first() is None:
                    db.session.add(insert_data)
                    db.session.commit()
                    print('insert: ', postid_short)
                else:
                    update_data = selectdata.update({ KaobeiData.PostLike: k[4], KaobeiData.PostComment: k[5], KaobeiData.PostShare: k[6]})
                    db.session.commit()
                    print('update: ', postid_short)

if __name__ == '__main__':
    start = time.time()
    kaobei(KAOBEILIST)
    print('All cost',time.time()-start)