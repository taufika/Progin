from xml.dom import minidom
import datetime
import time
import urllib
import sys

if len(sys.argv) > 1:
	xmlurl = sys.argv[1]
	print 'Retrieving RSS feed from ' + xmlurl
	if xmlurl != '':
		testfile = urllib.URLopener()
		testfile.retrieve(xmlurl, "rss.xml")

xmldoc = minidom.parse('rss.xml')

mychannel = xmldoc.getElementsByTagName('channel')[0]
rsstitle = mychannel.getElementsByTagName('title')[0]
rssdesc = mychannel.getElementsByTagName('description')[0]


print rsstitle.childNodes[0].nodeValue + ' | ' + rssdesc.childNodes[0].nodeValue
print '====================================================='
rssupdated = 'Updated on ' + mychannel.getElementsByTagName('lastBuildDate')[0].childNodes[0].nodeValue
print rssupdated
print '====================================================='
print '                 LAST 24 HOUR NEWS                   '
print '====================================================='

itemlist = mychannel.getElementsByTagName('item')
itemlist.sort(key=lambda x: time.strptime(x.getElementsByTagName('pubDate')[0].childNodes[0].nodeValue, '%a, %d %b %Y %H:%M:%S %Z'), reverse=True)

i = 1
for s in itemlist :
	itemtitle = s.getElementsByTagName('title')[0]
	pubDate = s.getElementsByTagName('pubDate')[0]
	pubTime = datetime.datetime.strptime(pubDate.childNodes[0].nodeValue[0:25], '%a, %d %b %Y %H:%M:%S')
	nowTime = datetime.datetime.utcnow()
	diffTime = (nowTime - pubTime)
	diffTime = diffTime.seconds + diffTime.days*24*60*60
	if diffTime <= 86400:
		itemcontent = s.getElementsByTagName('guid')[0]
		print str(i) + '. ' + itemtitle.childNodes[0].nodeValue
		print '    Published on ' + pubDate.childNodes[0].nodeValue
		print '   (' + itemcontent.childNodes[0].nodeValue + ')'
		i = i+1 
