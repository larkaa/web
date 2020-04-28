#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
from pathlib import Path
import html
import time
import os
import csv
import pandas as pd
from multiprocessing import Pool
import multiprocessing.dummy


#global filename 
#filename= '/media/larkaa/storage/Pictures/tumblr/blog_list.txt'


def get_links(soup,site,update=False):
    img_list = []
    tag_list = []
    caption_list = []
    res = []    
    temp = []
    text = ''
    d = dict()

    for a in soup.find_all('post'):
        photos = [x for x in re.findall(r'(https:[A-Za-z0-9./_]*?(?:\.jpg|\.png|\.gif))', html.unescape(str(a))) 
        if 'avatar' not in x 
        and ('1280' in x or '540' in x or '500' in x) 
        and ' ' not in x]        
        
        if photos:
                
            unique = [x.split('_')[-2] for x in photos]
            unique = list(set(unique))
            #print('unique',unique)
            #print(photos)
            
            for i in unique:
                #find max res photo
                try:
                    max_res = max([int(x.split('_')[-1].split('.')[0]) for x in photos if i in x and '75sq' not in x])
                except:
                    continue
                photo = [x for x in photos if i in x if str(max_res) in x] [0]
                
                temp.append(photo)
                
                
                # find photos with tags
                for x in a.find_all('tag'):
                    text = re.sub("<[^>]*>", "",x.text)
                    d[photo] = d.get(photo,'') + ';' + text.lower().rstrip('. ')
            
                # find photos with captions
                for x in a.find_all('photo-caption'):
                    
                    text = re.sub("<[^>]*>", "",x.text)
                    d[photo] = d.get(photo,'') + ';' + text.lower().rstrip('. ')

        #print(temp)
        img_list.extend(list(set(temp)))
        
    #convert caption results to dictionary    
    temp =[]
    for key, value in d.items():
        temp = [key,value]
        res.append(temp)
    

    res = pd.DataFrame(res,columns = ['link','tags'])
    tag_list = res
    tag_list['tags'] = res.iloc[:,1].apply(lambda x: re.sub(r"\n", " ",re.sub('http\S*','',x))[1:].rstrip('. '))
    
                
    return(tag_list)

            
def get_tor_session():
    timeout = 5
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                        'https': 'socks5://127.0.0.1:9050'}

    r = session.get("https://httpbin.org/ip", timeout=timeout).text
    print('\ttor ip:', re.findall('origin":."(.+)"',r)[0])
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AAppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    session.headers = headers
    
    return session
    
                
def dl_from_df(infile,path,session,stop=9000,poolnum=10):   

    if not infile.is_file():
        print('{} does not exist'.format(infile))
        return 

    #prepare file
    tags = pd.read_csv(infile, engine='python', compression='gzip')

    temp = tags['link'] 
    addy_list = temp[:stop]
    
    print('{} new images'.format(len(addy_list)))

    #change path
    if not os.path.exists('{}/{}'.format(Localpath,path)):
        os.makedirs("{}/{}".format(Localpath,path))
        print('Creating new directory')

    with Pool(poolnum) as p:
        p.starmap(dl_helper, zip(addy_list, [path]*len(addy_list), [session]*len(addy_list)))
    return
                        
def dl_helper(addy,path, s):
    timeout=3
    RETRY = 3
    dl_name = os.path.join("{}/{}".format(Localpath,path),addy.split('/')[-1]) 
    my_file = Path(str(dl_name))  
    
    if my_file.is_file():
        return
    elif not my_file.is_file():
        retry_times = 0
        while retry_times < RETRY:
            try:
                r =  s.get(addy,timeout=timeout) 
                with open(dl_name, 'wb') as out_file:
                    out_file.write(r.content)

                break;
            except:
                time.sleep(1)
                pass
            retry_times+=1                                 

#get vidoes 
def get_vid_links(soup,site):
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
                #a_temp='https://vt.tumblr.com/'+(temp.split('/')[-1])
                a_temp='https://ve.media.tumblr.com/'+(temp.split('/')[-1])
            else:
                #a_temp='https://vt.tumblr.com/'+(temp.split('/')[-2]+"_480")
                a_temp='https://ve.media.tumblr.com/'+(temp.split('/')[-2]+"_480")
            if a_temp.endswith('.mp4'):
                a = a_temp
            else:
                a = a_temp + '.mp4'
            
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
    


    
    
def crawl(site, update=False, start=0, stop = 9000,verbose=False,s=None):
    
    base_url = "https://{0}.tumblr.com/api/read?type={1}&num={2}&start={3}"
    MEDIA_NUM = 50
    tag_count = pd.DataFrame({},columns=['link','tags'])
    vid_list = []
    vid_check = True
    a_check = []
    r = ' '
    
    # check for existing file & load
    folderpath = '{}/{}/'.format(Localpath,site)
    my_file = Path(folderpath, str(site+'_tags.csv.gz'))
    my_file2 = Path(folderpath, str(site+'_vids.csv.gz'))
    
    if my_file.is_file():
        a = pd.read_csv(my_file, engine='python', compression='gzip')
        a_check = a['link']
    if my_file2.is_file():
        b = pd.read_csv(my_file2, engine='python', compression='gzip')

    while True:      
        media_url = base_url.format(site, 'photo', MEDIA_NUM, start)
        if verbose:
            print(start,media_url, end = '\r')
        try:
            r = s.get(media_url)
            if r.status_code == 404:
                print("Site %s does not exist" % site)
                return
            
        except Exception as err: 
            print('Error', err)
            print('Ending at ',start)
            break
        
        #stopping conditions
        if start >= stop:
            break
            
        #soup = BeautifulSoup(r.read(), from_encoding=r.headers.get_content_charset(),features="lxml")
        soup = BeautifulSoup(r.text, features="lxml")
        if len(str(soup))<700:
            print('\nEnding at ',start)
            break  
        
        words = get_links(soup,site,update)
        tag_count = tag_count.append(words)
        
        if vid_check:
            media_url = base_url.format(site, 'video', MEDIA_NUM, start)       
            r = s.get(media_url)
            #soup = BeautifulSoup(r.read(), from_encoding=r.headers.get_content_charset(),features="lxml")
            soup = BeautifulSoup(r.text, features="lxml")
            if len(str(soup))<700 or start>=stop:
                vid_check = False
            elif r.status_code == 404:
                #print("Site %s does not exist" % site)
                vid_check = False
                return
            else:
                temp = get_vid_links(soup,site)
                if temp:
                    vid_list.extend(temp)
        

        # check if any image exist in the list already, 
        # if so quit            
        check_dup = set(tag_count['link']) & set(a_check)
        if check_dup:
            print('\tDuplicate links, quitting at {}'.format(start))
            break
                    
        start += MEDIA_NUM
        time.sleep(1) #add sleep to not time out
        
        
    # treat duplicates
    # extract them, delete from original file
    # convert to dataframe, then merge
    
    ta = tag_count.loc[tag_count['link'].duplicated(keep=False),:]
    tag_count.drop_duplicates(subset='link',keep=False, inplace=True)
        
    tb = []
    for i in ta.link.unique():
        temp = (ta.loc[ta['link']==i,'tags'])
        temp2 = temp.iloc[0] + ';'+temp.iloc[1]
        newtags= ";".join(set(temp2.lower().split(';')))
        tb.append([i,newtags])
            
    tag_count = tag_count.append(pd.DataFrame(tb,columns=['link','tags']))
    vid_list = pd.DataFrame(vid_list,columns = ['link','tags'])

    
    if not my_file.is_file():
        tag_count.to_csv(Path(folderpath,site+"_tags.csv.gz"),index=False,compression='gzip')        
        vid_list.to_csv(Path(folderpath,site+'_vids.csv.gz'),index=False,compression='gzip')
        
    elif my_file.is_file():
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
        tags = pd.read_csv(tag_file, engine='python', compression='gzip')
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
        tags = pd.read_csv(tag_file, engine='python', compression='gzip')
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
    
    
def check_archive(ws, session=None):
    url = 'http://web.archive.org/cdx/search/cdx?url='
    site = 'http://'+ws+'.tumblr.com/'
    a_check = []
    
    
    #existing tag file
    folderpath = '{}/{}/'.format(Localpath,ws)
    my_file = Path(folderpath, str(ws+'_tags.csv.gz'))
    #print(my_file)
    if my_file.is_file():
        existing_file = pd.read_csv(my_file, engine='python', compression='gzip')
        existing_tags = existing_file['link']
    
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
    print(url+site, end = '\r')
    snapshots = page.text.split('\n')
    snapshot_list = []
    
    #loop through archived websites
    for snapshot in snapshots:
        snapshot_items = snapshot.split(' ')
        if len(snapshot_items) == 7:
            snap = Snapshot(snapshot_items[0], snapshot_items[1], snapshot_items[2], snapshot_items[3], snapshot_items[4], snapshot_items[5], snapshot_items[6])
            snapshot_list.append(snap)

    img_list = []
    
    
    
    #get photos from each page
    for a in snapshot_list:
        page = requests.get(a['snapshot_url'])
        #print(a['snapshot_url'])
        temp = (re.findall('src="(\S+?(?:\.jpg|\.png|\.gif))',page.text))
        temp2 = [x for x in temp if ('1280' in x or '540' in x or '500' in x) and 'avatar' not in x]
        unique = list(set([x.split('_')[-2] for x in temp2]))
        
        archive_photos = []
        #print(temp2)
        try:
            #find max res photo
            for i in unique:
                try:
                    max_res = max([int(x.split('_')[-1].split('.')[0]) for x in temp2 if i in x and '75sq' not in x])
                except:
                    continue
                photo = [x for x in temp2 if i in x if str(max_res) in x] 
                archive_photos.extend(photo)
        except:
            archive_photos = temp2
        
        
        img_list.extend(archive_photos)

    
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
                s = [x for x in test2 if i in x and ('1280' in x or '540' in x or '500' in x) and 'avatar' not in x and '75sq' not in x]
                if s:
                    s = s[0]
                    temp1 = s[0:s.find('/http')]+'if_'+s[s.find('/http'):]
                    img_list.append(temp1)
                    
        # check if duplicated in existing tag_list
        # quit if true
        #print(img_list)
        #print(a_check)
        check_dup = set(img_list) & set(a_check)
        #print(check_dup)
        if check_dup:
            break
    
    img_list2 = list(set(img_list)) 
    
    tag_count =pd.DataFrame(img_list2,columns=['link'])
    tag_count['tags']= 'webarchive'

    #add to existing tag file
    if my_file.is_file():
        res1 = pd.concat([tag_count, existing_file])
        res1.drop_duplicates(subset=['link'], keep='first', inplace=True) 
        res1.to_csv(Path(folderpath,ws+"_tags.csv.gz"),index=False,compression='gzip')
     
    #download the images
    #for x in img_list2:
    #    dl_link(x,ws)
        
    addy_list = img_list2
    if session == None:
        session = get_tor_session()
    with Pool(10) as p:
        p.starmap(dl_helper, zip(addy_list, [ws]*len(addy_list), [session]*len(addy_list)))
        
    # do this after dl_link function, which will create folder path
    if not my_file.is_file():
        tag_count.to_csv(Path(folderpath,ws+"_tags.csv.gz"),index=False,compression='gzip')
    
    
def scrape(site, update=False, start=0, stop = 9000, verbose=False, session = None):

    global Localpath 
    Localpath= '/media/larkaa/storage/Pictures/tumblr'

    if session == None:    
        session = get_tor_session()
    
    if not os.path.exists('{}/{}/'.format(Localpath,site)) :
        print('Directory does not exist')
        os.makedirs("{}/{}".format(Localpath,site))   
    
    if update:
        crawl(site, update, start, stop, verbose, session)
        #check_archive(site, session)
        
    else:
        folderpath = '{}/{}/'.format(Localpath,site)

        my_file = Path(folderpath, str(site+'_tags.csv.gz'))
        dl_from_df(my_file, site, session, stop)
        
        my_file2 = Path(folderpath, str(site+'_vids.csv.gz'))
        dl_from_df(my_file2, site, session, stop)

    return 
    
    
    
