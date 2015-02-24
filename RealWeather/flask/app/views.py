#!/usr/bin/python
# Create views for the html page

from app import app
import json
import time
from flask import jsonify, render_template, request
import happybase
import ast


@app.route('/')
@app.route('/index/')
def index():
    return render_template('cyborg.html')



@app.route('/realtime')
def realtime():
    connection = happybase.Connection('54.67.107.239')
    table = connection.table('full1960_hbase')    
    table2 = connection.table('table2')
    date = []   
    for k,value in table2.scan():
        date.append(value.values())
 
    day = date[0][0]
    month = date[1][0]
    print 'month',month, 'day', day
   
    stations = []
    year = '1960'
          
    dummy = year + month + day
    print dummy 
    for key,data in table.scan(row_prefix=dummy):
    #print key,data
    #converting 'text' to "text"
        if len(data) < 8:
            continue   
        dummy2 = json.dumps(data)
        val = json.loads(dummy2)
    
        stations.append({'date':key.split('-')[0], 'long' : val['c:long'], 'lat' : val['c:lat'], 'snow' : val['c:snow'], 'hail' : val['c:hail'], 'tornado' : val['c:tornado'], 'rain' : val['c:rain'], 'fog' : val['c:fog'], 'thunder' : val['c:thunder']})  
	# c8 is longitude, c7 is latitude
    intday = int(day)
    intmonth = int(month)
    intday = intday + 1
  
    if ( intday > 29 and intmonth == 2):
        intday = 1
        intmonth = intmonth + 1
    
    if ( intday > 30 and (intmonth == 4 or intmonth == 6 or intmonth == 9 or intmonth == 11)):
        intday = 1
        intmonth = intmonth + 1         
    
    if ( intday > 31 and (intmonth == 1 or intmonth == 3 or intmonth == 5 or intmonth == 7
           or intmonth == 8 or intmonth == 10)):
        intday = 1
        intmonth = intmonth + 1
  
    if (intday > 31 and intmonth == 12):
        intday = 1
        intmonth = 1

    day = str(intday)
    month = str(intmonth)
    table2.delete('r1')
    table2.put('r1',{'cf:day':day})
    table2.delete('r2')
    table2.put('r2',{'cf:day':month})
    print day,month
    time.sleep(5)

    return jsonify(stations = stations)       
        
         

