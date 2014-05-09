#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  jw_video.py
#  
#  Copyright 2014 Luke Gerhardt <koohiisan>
#  
import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib2,urllib,re
_ADDON_NAME = "jw.org Videos"
addon_handle = int(sys.argv[1])
this_addon = xbmcaddon.Addon()
xbmcplugin.setContent(addon_handle, 'movies')
setting_quality = str(this_addon.getSettings('quality'))
setting_lang = str(setting_quality = this_addon.getSettings('language'))
test_setting_lang_abbr = re.search(r'\((.*?)\)',setting_lang)
if test_setting_lang_abbr:
	setting_lang_abbr = setting_lang_abbr.group()
else:
	setting_lang_abbr = 'en'
setting_lang_urlbase = setting_lang_abbr + '/videos/'

def log(msg, level=0):
        xbmc.log('%s: %s' % (_ADDON_NAME, msg), level)

baseurl = 'http://www.jw.org/'

def addDir(name,url,mode,iconimage,boolfolder):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image',iconimage)
        ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=boolfolder)
        return ok

def deesc(t):

    return (t
        .replace("&quot;", '"')
        .replace("&amp;", '&')
        .replace("&lt;", '<')
        .replace("&gt;", '>')
        .replace("&#39;", '\'')
        .replace("&nbsp;",' ')
        ).strip()

def show_categories():    
		addDir('All Topics', baseurl+setting_lang_urlbase+'?videoFilter=none&sortBy=1',1,'', True)
		addDir('Bible Accounts', baseurl+setting_lang_urlbase+'?videoFilter=bibleAccounts&sortBy=1',1,'',True)
		addDir('For the Family', baseurl+setting_lang_urlbase+'?videoFilter=families&sortBy=1',1,'',True)
		addDir('For Teenagers', baseurl+setting_lang_urlbase+'?videoFilter=teenagers&sortBy=1',1,'',True)
		addDir('For Children', baseurl+setting_lang_urlbase+'?videoFilter=children&sortBy=1',1,'',True)
		addDir('What Your Peers Say', baseurl+setting_lang_urlbase+'?videoFilter=whatPeersSay&sortBy=1',1,'',True)
		addDir('Whiteboard Animations', baseurl+setting_lang_urlbase+'?videoFilter=whiteboardAnimations&sortBy=1',1,'',True)
		addDir('Become Jehovah\'s Friend', baseurl+setting_lang_urlbase+'?videoFilter=jehovahs-friend&sortBy=1',1,'',True)
		addDir('News', baseurl+setting_lang_urlbase+'?videoFilter=news&sortBy=1',1,'',True)
		addDir('Our Activities', baseurl+setting_lang_urlbase+'?videoFilter=activities&sortBy=1',1,'',True)
		addDir('History & Organization', baseurl+setting_lang_urlbase+'?videoFilter=history&sortBy=1',1,'',True)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
def get_videos(urltouse):
	curloop = 0
	loopagain = 1
	while loopagain==1:
		req = urllib2.Request(urltouse + '&start=' + str(curloop))
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		if '&amp;start=' + str(curloop+10) in str(link):
			curloop=curloop+10
			loopagain = 1
			log ("detected more pages, so will loop starting with " + str(curloop))
		else:
			loopagain = 0
			log ("no further pages detected")
		regexp=re.compile('mixDesc">\s*<a href="(.+?)"[\s\S]*?data-onpagetitle="(.+?)"[\s\S]*?data-src="(.+?)"').findall(link)
		log ("regexp value: " + str(regexp))
		for matched1,matched3,matched2 in regexp:
			trythisone = baseurl + str(matched1).replace('(', '').replace(')', '')
			addDir(str(matched3), trythisone,2,str(matched2),False)
		
def play_video(trythisone):					
	req2 = urllib2.Request(trythisone)
	req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
	response2 = urllib2.urlopen(req2)
	link2=response2.read()
	response2.close()
	testurl = re.compile('>(.*?)</h1>[\s\S]*href=\'(.*?)\'>\s*Dow').findall(link2)
	for b,a in testurl:
		if 'mp4' in str(a):
			brackets = str(a).replace('[', '').replace(']', '').replace('&amp;','&')
			pattern = re.sub('<a href="', '', str(brackets))
			realurl = re.sub ('\" target="_blank">Download This Video</a>', '', str(pattern))
			gohere = baseurl + str(realurl).replace('&alllangs=1','&alllangs=0')
			req3 = urllib2.Request(gohere)
			req3.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
			response3 = urllib2.urlopen(req3)
			link3=response3.read()
			response3.close()
			vidurlobj = re.compile('class="aVideoURL"[\s\S]*?r([0-9]*?)P.mp4[\s\S]*?</a>(.*?)</td>([\s\S]*?)\/tr').findall(link3)
			print str(vidurlobj)
			nummatches = len(vidurlobj)
			print "nummatches: " + str(nummatches)
			pl = xbmc.PlayList(1)
			pl.clear()
			if nummatches==1:
				for a,b,c in vidurlobj:
					print "a:" + str(a)
					print "b:" + str(b)
					print "c:" + str(c)
					linklist = re.compile('<a href="(.*?)"').findall(c)
					for linktotest in linklist:
						print ("testing: " + str(linktotest))
						if str(a) in str(linktotest) and str(linktotest).find('Sub_')==-1:
							thetitle = deesc(str(b))
							print (thetitle + " :: " + str(c))
							li = xbmcgui.ListItem(label=thetitle, iconImage='', thumbnailImage='', path=str(linktotest))
							li.setInfo(type='Video', infoLabels={ "Title": thetitle })
							li.setProperty('IsPlayable', 'true')
							xbmc.PlayList(1).add(str(linktotest),li)
							print "done adding...now play"
							xbmc.Player().play(pl)
							break
						
			else:
				for a,b,c in vidurlobj:
					print "a:" + str(a)
					print "b:" + str(b)
					print "c:" + str(c)
					linklist = re.compile('<a href="(.*?)"').findall(c)
					for linktotest in linklist:
						print ("testing: " + str(linktotest))
						if str(a) in str(linktotest) and str(linktotest).find('Sub_')==-1:
							thetitle = deesc(str(b))
							print (thetitle + " :(>1): " + str(c))
							li = xbmcgui.ListItem(label=thetitle, iconImage='', thumbnailImage='', path=str(linktotest))
							li.setInfo(type='Video', infoLabels={ "Title": thetitle })
							li.setProperty('IsPlayable', 'true')
							xbmc.PlayList(1).add(str(linktotest),li)
				print "done adding...now play"
				xbmc.Player().play(pl)

params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if url!=None and len(url)>5 and str(mode)=='1':
    get_videos(url)
elif str(mode)=='2':
	play_video(url)
else:
	show_categories()

xbmcplugin.endOfDirectory(addon_handle)
