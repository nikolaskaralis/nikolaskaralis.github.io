import urllib2
from time import strftime

upd=strftime('%d-%m-%Y %H:%M')
htmltemplate='''
<html>
<head>
<head>
<body>
<div align="center">
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.1 Transitional//EN">
<html>
<head>
<title>Greek Seismological Database</title>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-7">
<meta content="Greek Seismological Database" name="Description">
<meta content="Nikolas Karalis" name="Author">
<meta content="Nikolas Karalis, earthquakes, seismological, database, NTUA, semfe" name="Keywords">
<STYLE>
<!--
a {text-decoration: none}
a:hover
{
  background-color: rgb(255, 255, 0);
}
//-->
</STYLE>
</head>
<body vlink="black" link="black" bgcolor="#F5F5F5">
<div align="center">
<table cellspacing="30" bgcolor="Silver">
<tr>
<td><a href="seismotectonic_map.jpg"><img src="seismotectonic_map_small.jpg"></a><br></td>
<td align="center"><h1>Greek Seismological Database</h1>
created by : <b><a href="http://users.ntua.gr/ge04042">Nikolas Karalis</a></b><br><br><br>
In the following you can view a list of the earthquakes in the wider area of Greece during the last few years.<br>
Time is LOCAL (UTC +2).<br>
Data are fetched from <a href="http://www.emsc-csem.org">European-Mediterranean Seismological Centre</a>.<br><br>
Database currently holds data since August 2004 and is automatically updated every hour.<br>
You can find a seismotectonic map of Greece <a href="seismotectonic_map.jpg">here</a>.<br><br>
<b>Last update : %s </b>
<br></td>
</tr></table>
<br><br>
<table border='1' cellpadding=8>
<tr align="center"><td><b>Date</b></td><td><b>Time</b></td><td><b>Coordinates</b></td><td><b>Magnitude</b></td><td><b>Depth</b></td><td><b>Region</b></td></tr>
''' % (upd,)
#f=open('export_EMSC.csv','r')

def getdata(stardate, stopdate):
    url='http://www.emsc-csem.org/export_csv.php?page=current&sub=filter&start_date=%s&end_date=%s&min_lat=33&max_lat=42&min_long=18&max_long=28&min_depth=&max_depth=&min_mag=&max_mag=' %(startdate, stopdate)
    f=urllib2.urlopen(url)
    s=f.read()
    s=s.split('\n')
    print len(s)
    f.close()
    print url
    return s

startdate = '2004-10-01'
stopdate=strftime('%Y-%d-%m')
print 

f=open('index-deprecated.html','w')
f.write(htmltemplate)
exist=True
while 1:
    if stopdate>startdate:
        s=getdata(startdate,stopdate)
        for i in s[1:-1]:
            k=i.split(';')
            date=k[0].split('  ')[0]
            time=k[0].split('  ')[1]
            coord=k[1]+' '+k[2]
            depth=k[3]+' '+k[4]
            if depth=='':
                depth='N/A'
            magnitude=k[6]+' '+k[5]
            region=k[7]
            c='<tr align="center"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (date, time, coord,magnitude, depth, region)
            f.write(c+'\n')
        stopdate=date
    else:
        break
htmlend='''
</table></div></body></html>
'''
f.write(htmlend)
f.close()
print 'Succefully created the file.'