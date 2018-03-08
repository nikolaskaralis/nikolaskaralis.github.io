#    Presto Extractor
#
#    Copyright (C) 2007, 2008, 2009, 2010, 2011, 2012, 2013 Nikolas Karalis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    http://www.nikolaskaralis.gr
#    email : nikolaskaralis@gmail.com
#

import sys
import os
from shutil import move
from string import find
from reportlab.pdfgen.canvas import Canvas
import Image

def write(name,data):
	temp=file(name,'wb')
	temp.write(data)
	temp.close()
	
def read(name):
	temp=file(name,'rb')
	out=temp.read()
	temp.close()
	return out

# Recursive Deletion of a directory	
def recdel(file):
	os.chdir(file)
	for i in os.listdir('.'):
		os.remove(i)
	os.chdir('..')
	os.rmdir(file)

def pdfize(name):
	pdf = Canvas(name[:-4]+'.pdf',pageCompression=1)
	pdf.setAuthor('PrestoExtractor')
	pdf.setTitle(name[:-4])
	for i in range(pages):
		img=Image.open('page'+str(i+1)+'.jpg')
		s=img.size
		print 'Printing page '+str(i+1)
		pdf.setPageSize(s)
		pdf.drawImage('page'+str(i+1)+'.jpg', 0, 0)
		pdf.showPage()
	pdf.save()
	
if len(sys.argv) < 2:
	print "\nUsage: prestoextract filename [jpg]\n"
	print "If jpg is 1, the program will also give you a copy of the jpgs that produce the pdf."
	print "Created by : Nikolas"
	sys.exit()
else:
	name=sys.argv[1]
	try :
		keep=sys.argv[2]
	except :
		keep=0
	exe=read(name)
	try :
		os.listdir('.').index('temp')
		recdel('temp')
		os.mkdir('temp')
	except :
		os.mkdir('temp')
	os.chdir('temp')
	ind=find(exe,'docu')
	pages=int(exe[ind+4:ind+8])
	exe=exe[ind:]
	for i in range(pages):
		ind=find(exe,'docu')
		ind1=find(exe,'docu',ind+1)
		ind2=find(exe,'docu',ind1+1)
		temp=exe[ind+12:ind1]
		page=str(i+1)
		write('page'+page+'.jpg',temp)
		exe=exe[ind2:]
	pdfize(name)
	if keep==0:
		move(name[:-4]+'.pdf','..')
		os.chdir('..')
		recdel('temp')
	else:
		move(name[:-4]+'.pdf','..')
		os.chdir('..')