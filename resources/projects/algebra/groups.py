#!/usr/bin/env python

import cgi
import sys
def parse():
	print "Content-type: text/html\n"
	try:
		form = cgi.FieldStorage() #parse query
		if form.has_key("order") and form["order"].value != "":
			order=int(form["order"].value)
		if form.has_key("elements") and form["elements"].value != "":
			elements=form["elements"].value
		if form.has_key("matrix") and form["matrix"].value != "":
			matrix=form["matrix"].value
		if form.has_key("colors") and form["colors"].value != "":
			col=form["colors"].value
		if form.has_key("letters") and form["letters"].value != "":
			letters=int(form["letters"].value)
		else : letters=0
		matrix=matrix.split('\r\n')
		elements=elements.split(' ')
		col=col.split(' ')
		if len(elements) != len(col):
			print "The number of elements must be the same as the number of colors."
		colors={}
		for i in range(len(elements)):
			colors[elements[i]]=col[i]
	except:
		print "There is a problem with the data you provided."
		sys.exit()
	try:
		group(order,elements,matrix,colors,letters)
	except:
		print "A problem occured. Make sure you filled the form correctly"
		sys.exit()

def group(order,elements,matrix,colors,letters):
	tb='<html> \n <head> \n </head>\n <body>\n <div align="center">\n <h1>Group Color Representation</h1> \n <table border="1" cellpadding="15">\n'
	tb='''
	<html>
	<head>
	<meta http-equiv="content-type" content="text/html; charset=iso-8859-7">
	<!--<link rel="shortcut icon" type="image/x-icon" href="photos/xyz.gif">-->
	<meta content="Groups Color Representation" name="Description">
	<meta content="Nikolas Karalis" name="Author">
	<meta content="Nikolas Karalis, groups, colors, NTUA, semfe, mathematics" name="Keywords">
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
	<h1>Group Color Representation</h1>
	<table border="1" cellpadding="15">
	'''
	#first line with elements (bold)
	tb+='<tr><td>&nbsp;</td>'
	for i in range(order):
		tb+='<td><b>%s</b></td>' %(elements[i])
	tb+='</tr>\n'
	#The rest of the lines
	if letters==1:
		for r in range(order):
			tb+='<tr><td><b> %s </b></td>' %('&nbsp;'+elements[r]+'&nbsp;') #The first column, with the elements (bold)
			raw=matrix[r].split(' ')
			for c in range(order):
				tb+='<td bgcolor=%s>&nbsp;%s&nbsp;</td>' %(colors[raw[c]],raw[c]+'&nbsp;')
			tb+='</tr>\n'
	else :
		for r in range(order):
			tb+='<tr><td><b> %s </b></td>' %(elements[r]) #The first column, with the elements (bold)
			raw=matrix[r].split(' ')
			for c in range(order):
				tb+='<td bgcolor=%s>&nbsp;%s&nbsp;</td>' %(colors[raw[c]],'&nbsp;&nbsp;&nbsp;')
			tb+='</tr>\n'
	tb+='''</table>
	<br><br><br>
	<a href="javascript: history.go(-1)"><h3>Back</h3></a>
	</body>
	</html>'''
	print tb

parse()