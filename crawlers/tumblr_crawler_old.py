#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import urllib
import urllib.request
import urllib.parse
import re
from pathlib import Path
import html
import time
import os
import csv
import pandas as pd



global Localpath 
Localpath= '/media/larkaa/storage/Pictures/tumblr'
global filename 
filename= '/media/larkaa/storage/Pictures/tumblr/blog_list.txt'

#with open(filename, 'r') as f:
#    reader = csv.reader(f)
#    sites = [list(line) for line in csv.reader(f)]
#sites = sites[1:]
    


def get_links3(soup,site,tags = '',only_tags=False):
    img_list = []
    tag_list = []
    caption_list = []
    res = []
            
    temp = []
    text = ''
    d = dict()
    #search all posts
    for a in soup.find_all('post'):
        photos = [x for x in re.findall(r'(https:[A-Za-z0-9./_]*?(?:\.jpg|\.png|\.gif))',html.unescape(str(a))) if 'avatar' not in x and ('1280' in x or '540' in x or '500' in x) and ' ' not in x]        
        if photos:
            
            
            unique = [x.split('_')[-2] for x in photos]
            unique = list(set(unique))

            for i in unique:
                photo_temp = [x for x in photos if i in x]
                
                photo = photo_temp[0]
                temp.append(photo)
                
                # find photos with tags
                for x in a.find_all('tag'):
                    text = re.sub("<[^>]*>", "",x.text)
                    d[photo] = d.get(photo,'') + ';' + text.lower().rstrip('. ')
            
                # find photos with captions
                for x in a.find_all('photo-caption'):
                    
                    text = re.sub("<[^>]*>", "",x.text)
                    d[photo] = d.get(photo,'') + ';' + text.lower().rstrip('. ')
  
        img_list.extend(set(temp))
        
    #convert caption results to dictionary    
    temp =[]
    for key, value in d.items():
        temp = [key,value]
        res.append(temp)
    

    res = pd.DataFrame(res,columns = ['link','tags'])
    tag_list = res
    tag_list['tags'] = res.iloc[:,1].apply(lambda x: re.sub(r"\n", " ",re.sub('http\S*','',x))[1:].rstrip('. '))
    
                
    return(tag_list)

## using tor
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}

    return session

def dl_link(addy,path):
    RETRY = 3
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    
    #change path
    if not os.path.exists('{}/{}'.format(Localpath,path)):
        os.makedirs("{}/{}".format(Localpath,path))
        print('Creating new directory')

    dl_name = os.path.join("{}/{}".format(Localpath,path),addy.split('/')[-1]) 
    #print(dl_name, addy)

    my_file = Path(str(dl_name))
    if not my_file.is_file():
        #print('new media found ',dl_name)
        retry_times = 0
        while retry_times < RETRY:
            try:
                with urllib.request.urlopen(addy) as response, open(dl_name, 'wb') as out_file:
                    data = response.read() # a `bytes` object
                    out_file.write(data)

                break;
            except:
                pass
            retry_times+=1           

#get vidoes 
def get_vids2(soup,site):
    vid_list = []
    d = dict()
    a=''
    #search all posts
    for b in soup.find_all('post'):
        #find vid links
        temp = re.findall('source src=\"(https:.*?)\"'  , str(b))
        if temp:
            temp = temp[0]
            if '480' not in temp:
                a='https://vt.tumblr.com/'+(temp.split('/')[-1]) + '.mp4'
            else:
                a='https://vt.tumblr.com/'+(temp.split('/')[-2]+"_480")+'.mp4'
            
            #add photo first, then include tags
            d[a] = d.get(a,'')       
            # find photos with tags
            for x in b.find_all('tag'):
                text = re.sub("<[^>]*>", "",x.text)
                d[a] = d.get(a,'') + ';' + text.lower().rstrip('. ')
             
            # find photos with captions
            for x in b.find_all('photo-caption'):
                text = re.sub("<[^>]*>", "",x.text)
                d[a] = d.get(a,'') + ';' + text.lower().rstrip('. ')
            
            
    res =[]
    for key, value in d.items():
        temp = [key,value[1:]]
        res.append(temp)

    return(res)
def crawl2(site, only_tags=False,tags='', start=0, stop = 9000,verbose=False):
    
    if not os.path.exists('{}/{}/'.format(Localpath,site)) :
        print('Directory does not exist')
        os.makedirs("{}/{}".format(Localpath,site))   
    
    if only_tags:
        crawl(site, only_tags,tags, start, stop, verbose)
    else:
        folderpath = '{}/{}/'.format(Localpath,site)
        my_file = Path(folderpath, str(site+'_tags.csv.gz'))
        my_file2 = Path(folderpath, str(site+'_vids.csv.gz'))
        if not my_file.is_file():
            crawl(site, only_tags,tags, start, stop, verbose)
            
        tag_count = pd.read_csv(my_file, compression='gzip')
        vids = pd.read_csv(my_file2, compression='gzip')
        
        if tags == '' or tags == []:
            temp = tag_count['link'] 
            temp = temp[:stop]
            for x in temp:
                    dl_link(x, site)
            temp = vids['link'] 
            temp = temp[:stop]
            for x in temp:
                    dl_link(x, site)        
                    
        elif tags:
            for tag in tags:
                print(tag)
                
                temp = tag_count.loc[[True if tag in str(x) else False for x in tag_count['tags'] ],'link']           
                temp = temp[:stop]
                for x in temp:
                    dl_link(x, site +'/'+tag)
                    
                temp = vids.loc[[True if tag in str(x) else False for x in vids['tags'] ],'link']
                temp = temp[:stop]
                for x in temp:
                    dl_link(x, site+'/'+tag)

    return 


def crawl(site, only_tags=False,tags='', start=0, stop = 9000,verbose=False):
    
    base_url = "https://{0}.tumblr.com/api/read?type={1}&num={2}&start={3}"
    MEDIA_NUM = 50
    f=True
    tag_count = pd.DataFrame({},columns=['link','tags'])
    vid_list = []
    vid_check = True
    

    while f:      
        media_url = base_url.format(site, 'photo', MEDIA_NUM, start)
        if verbose:
            print(start,media_url)
        try:
            r  = urllib.request.urlopen(media_url)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("Site %s does not exist" % site)
                f=False
                break
        
        #stopping conditions
        if r.getcode() == 404:
            print("Site %s does not exist" % site)
            f = False
            break
        if start >= stop:
            f=False
            break
            
        soup = BeautifulSoup(r.read(), from_encoding=r.headers.get_content_charset(),features="lxml")
        if len(str(soup))<700:
            print('Ending at start=',start)
            f = False
            break

  
        words = get_links3(soup,site,tags,only_tags)
        tag_count = tag_count.append(words)
        
        if vid_check:
            media_url = base_url.format(site, 'video', MEDIA_NUM, start)
            r  = urllib.request.urlopen(media_url)        
            soup = BeautifulSoup(r.read(), from_encoding=r.headers.get_content_charset(),features="lxml")
            if len(str(soup))<700 or start>=stop:
                vid_check = False
            
            else:
                temp = get_vids2(soup,site)
                if temp:
                    vid_list.extend(temp)
                    
        start += MEDIA_NUM
        #add sleep to not time out
        time.sleep(1)
        
        
    # treat duplicates
    # extract them, delete from original file
    # treat, then merge
    
    a = tag_count.loc[tag_count['link'].duplicated(keep=False),:]
    tag_count.drop_duplicates(subset='link',keep=False, inplace=True)
        
    b = []
    for i in a.link.unique():
        temp = (a.loc[a['link']==i,'tags'])
        temp2 = temp.iloc[0] + ';'+temp.iloc[1]
        newtags= ";".join(set(temp2.lower().split(';')))
        b.append([i,newtags])
            
    tag_count = tag_count.append(pd.DataFrame(b,columns=['link','tags']))
    vid_list = pd.DataFrame(vid_list,columns = ['link','tags'])

    # check for existing file
    #Localpath = os.path.expanduser("~")
    folderpath = '{}/{}/'.format(Localpath,site)
    my_file = Path(folderpath, str(site+'_tags.csv.gz'))
    my_file2 = Path(folderpath, str(site+'_vids.csv.gz'))
    
    
    if not my_file.is_file():
        #filename = site+"_tags.csv.gz"
        tag_count.to_csv(Path(folderpath,site+"_tags.csv.gz"),index=False,compression='gzip')
        
        vid_list.to_csv(Path(folderpath,site+'_vids.csv.gz'),index=False,compression='gzip')
    elif my_file.is_file():
        a = pd.read_csv(my_file, compression='gzip')
        b = pd.read_csv(my_file2, compression='gzip')
        
        #filename = site+"_tags.csv.gz"
        
        res1 = pd.concat([tag_count, a])
        res1.drop_duplicates(subset=['link'], keep='first', inplace=True)
        
        res2 = pd.concat([vid_list, b])
        res2.drop_duplicates(subset=['link'], keep='first', inplace=True)
        res1.to_csv(Path(folderpath,site+"_tags.csv.gz"),index=False,compression='gzip')
        res2.to_csv(Path(folderpath,site+'_vids.csv.gz'),index=False,compression='gzip')
    else:
        print("Did not save results, exiting crawl.")
    return

# get tag info
def get_tag_info(site,max_value=5):
    
    folderpath = '{}/{}/'.format(Localpath,site)
    tag_file = Path(folderpath, str(site+'_tags.csv.gz'))
    vid_file = Path(folderpath, str(site+'_vids.csv.gz'))
    try:
        tags = pd.read_csv(tag_file, compression='gzip')
    except:
        print("\tNo tag file created")
        return
    
    print("Top Reblogs")
    d = dict()

    for i in tags['tags']:
        if ':' in str(i):
            j = str(i).split(':')[0]
            k = j.split(';')[-1]
            d[k] = d.get(k,0) + 1
    count = {key:val for key, val in d.items() if val>max_value}
    for w in sorted(count, key=count.get, reverse=True):
        print("\t",w, count[w])
    
    import matplotlib.pyplot as plt
    plt.bar(count.keys(), count.values(), color='g')
    plt.xticks(rotation='vertical')
    plt.show() 
        
    print("\nTag stats")
    d = dict()
    
    for i in tags['tags']:
        j = str(i).split(';')
        for k in j:
            if (':') not in str(k): #this is for reblogs
                d[k]=d.get(k,0) + 1
    count2 = {key:val for key, val in d.items() if val>max_value}
    for w in sorted(count2, key=count2.get, reverse=True):
        print("\t",w, count2[w])    
    plt.bar(count2.keys(), count2.values(), color='g')
    plt.xticks(rotation='vertical')
    plt.show()
    time.sleep(10)

class Snapshot(dict):
    def __init__(self, urlkey=None, timestamp=None, original=None, mimetype=None, statuscode=None, digest=None, length=None):
        super(Snapshot, self).__init__()
        self['urlkey'] = urlkey
        self['timestamp'] = timestamp
        self['original'] = original
        self['mimetype'] = mimetype
        self['statuscode'] = statuscode
        self['digest'] = digest
        self['length'] = length
        self['snapshot_url'] = 'http://web.archive.org/web/%s/%s/' % (timestamp, original)
                    
def search_tags(site,search_word):
    
    folderpath = '{}/{}/'.format(Localpath,site)
    tag_file = Path(folderpath, str(site+'_tags.csv.gz'))
    vid_file = Path(folderpath, str(site+'_vids.csv.gz'))
    try:
        tags = pd.read_csv(tag_file, compression='gzip')
    except:
        print("\tNo tag file created")
        return

    res = tags.link[tags.tags.str.contains(search_word)]
    pd.set_option('display.max_colwidth', 400)
    print(res)
    return(res)


def verify_images():
    from os import listdir
    from PIL import Image
    res = []

    for root, dirs, files in os.walk(Localpath): 
        print(root)
        for filename in files:
            if filename.endswith(('.png','.jpg','.gif')):
                try:
                    img = Image.open(os.path.join(root,filename)) # open the image file
                    img.verify() # verify that it is, in fact an image
                except (IOError, SyntaxError) as e:
                    print('Bad file:', filename) # print out the names of corrupt files
                    res.append(os.path.join(root,filename))
                    #os.remove(os.path.join(root, filename))
    return(res)
    
    
def check_archive(ws):
    url = 'http://web.archive.org/cdx/search/cdx?url='
    site = 'http://'+ws+'.tumblr.com/'
    
    #example:
    #web.archive.org/web/20131120112835/http://joeschmoe.tumblr.com/
    
    #request a list of all archived websites
    try:
        page = requests.get(url+site)
        print('Site {} is in archive'.format(site))
    except:
        print('Site {} not in archive'.format(site))
        return
    if page.text == '':
        #print('Site {} not in archive'.format(site))
        print('Page empty {}'.format(site))
        return
    print(url+site)
    snapshots = page.text.split('\n')
    snapshot_list = []
    
    #loop through archived websites
    for snapshot in snapshots:
        snapshot_items = snapshot.split(' ')
        if len(snapshot_items) == 7:
            snap = Snapshot(snapshot_items[0], snapshot_items[1], snapshot_items[2], snapshot_items[3], snapshot_items[4], snapshot_items[5], snapshot_items[6])
            snapshot_list.append(snap)

    img_list = []
     
    #page = requests.get(snapshot_list[0]['snapshot_url'])
    #get photos from each page
    for a in snapshot_list:
        page = requests.get(a['snapshot_url'])
        #print(a['snapshot_url'])
        temp = (re.findall('src="(\S+?(?:\.jpg|\.png|\.gif))',page.text))
        temp2 = [x for x in temp if ('1280' in x or '540' in x or '500' in x) and 'avatar' not in x]
        img_list.extend(temp2)
        #temp = (re.findall('src="(\S+?\.gif)',page.text))
        #mg_list.extend(temp)
    
        # find photosets if they exist
        sets = re.findall('(http\S+?photoset\S+?)\"',page.text)
        for s in sets:
            set_temp = requests.get(s)
            test2 = re.findall('(http\S+?web.archive.org\S+?(?:\.jpg|\.png|\.gif))',html.unescape(set_temp.text))
            test2 = [x for x in test2 if '{' not in x if ' ' not in x]
            unique2 = list(set([x.split('_')[-2] for x in test2]))
            #print(test2)
            #print(s)
            for i in unique2:
                #print(i)
                s = [x for x in test2 if i in x and ('1280' in x or '540' in x or '500' in x) and 'avatar' not in x]
                if s:
                    s = s[0]
                    temp1 = s[0:s.find('/http')]+'if_'+s[s.find('/http'):]
                    img_list.append(temp1)
    
    img_list2 = list(set(img_list)) 
    
    tag_count =pd.DataFrame(img_list2,columns=['link'])
    tag_count['tags']= 'webarchive'

    #add to existing tag file
    folderpath = '{}/{}/'.format(Localpath,ws)
    my_file = Path(folderpath, str(site+'_tags.csv.gz'))
    
    
    if my_file.is_file():
        a = pd.read_csv(my_file, compression='gzip')
        res1 = pd.concat([tag_count, a])
        res1.drop_duplicates(subset=['link'], keep='first', inplace=True) 
        res1.to_csv(Path(folderpath,site+"_tags.csv.gz"),index=False,compression='gzip')
     
    #download the images
    for x in img_list2:
        dl_link(x,ws)
        
    # do this after bc previous function will create folder path
    if not my_file.is_file():
        tag_count.to_csv(Path(folderpath,ws+"_tags.csv.gz"),index=False,compression='gzip')
    
    

