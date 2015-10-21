#!/usr/bin/env python
import re
import json,httplib
import sys

f = open(sys.argv[1])
location = open(sys.argv[2])



tdRegex = re.compile(r"<td\b[^>]*>(.*?)</td>")
headerRegex = re.compile(r"<thead\b[^>]*>(.*?)</thead>")
columnTitleRegex = re.compile(r"<th\b[^>]*>(.*?)</th>")

titleList = []
GPSList = {}
finaldata = {}

locationRegex = re.compile(r"([-+]?[0-9]*\.[0-9]+|[0-9]+)")
numericRegex = re.compile(r"([-+]?[0-9]*\.*[0-9]+|[0-9]+)")

for line in location:
    number = re.findall(locationRegex,line)
    if("latitude:" in line):
        GPSList.update({"latitude":number})
    elif ("longitude:" in line):
        GPSList.update({"longitude":number})
      


for line in f:
    t = re.findall(headerRegex,line)
    e = re.findall(tdRegex,line)
    if t:
        headerLine = t[0]
        header = re.findall(columnTitleRegex,headerLine)
        for entry in range(0,19):
            if not(entry == 2 or entry ==3 or entry==9 or entry == 12 or entry ==13 or entry==14 or entry==15 or entry==16 or entry ==17 or entry==18):
                formattedEntry = header[entry].replace(" ","")
                titleList.append(formattedEntry)
    if e:
        SSID = e[0]
        if("wustl" in SSID):
            entryList = []
            for entry in range(0,19):
                if not(entry == 2 or entry ==3 or entry==9 or entry == 12 or entry ==13 or entry==14 or entry==15 or entry==16 or entry ==17 or entry==18):
                    entryList.append(e[entry])
            parseRow = {}
            
            counter = 0
            for (title,entry) in zip(titleList,entryList):
                if (counter == 2 or counter == 3 or counter == 4 or counter == 5 or counter == 6 or counter == 7 or counter == 8 ):
                    numberParse = re.findall(numericRegex,entry)
                    numericEntry = float(numberParse[0])
                    parseRow.update({title:numericEntry})
                    parseRow.update({"latitude":float(GPSList["latitude"][0])})
                    parseRow.update({"longitude":float(GPSList["longitude"][0])})
                    parseRow.update({"location":sys.argv[3]})
                else:
                    parseRow.update({title:entry})
                    parseRow.update({"latitude":float(GPSList["latitude"][0])})
                    parseRow.update({"longitude":float(GPSList["longitude"][0])})
                    parseRow.update({"location":sys.argv[3]})
                    counter+=1
            
            jsonData = json.dumps(dict(parseRow))
            connection = httplib.HTTPSConnection('api.parse.com', 443)
            connection.connect()
            connection.request('POST', '/1/classes/data', jsonData, {
            "X-Parse-Application-Id": "Wgyx5HivoZXhRuAjRsSpgd4Zr7uME2hsV5YWg1lW",
            "X-Parse-REST-API-Key": "KCm4qysQhflsX2VgaCTFMgWrjQozOBzAsw5MCFLO",
            "Content-Type": "application/json"
             })
            result = json.loads(connection.getresponse().read())
            print result    

