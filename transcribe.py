# based on https://github.com/landonstahl/AWS-Transcribe-JSON-to-SRT/blob/main/json_to_srt.py

import json
import codecs
import time
import math
import os

#s3 = boto3.resource('s3')
def newPhrase():
    return { 'start_time': '', 'end_time': '', 'words' : [] }
    
def getTimeCode(mlseconds):
    seconds = mlseconds/1000
    (frac, whole) = math.modf(seconds)
    frac = frac * 1000
    return str('%S,%03d' % (time.strftime('%H:%M:%S',time.gmtime(whole)), frac))

def getPhrasesFromJSON(json_file):
    _file = open(json_file) 
    json_enc = json.load(_file)  
    # json_enc <- wireMagic, pens, wsWinStyles, wpWinPositions, [events]
    # where: item['events'] contain all the necessary informations to pick 
    # the phrases of a segment

    json_dec = json.loads(json.dumps(json_enc))
    events = json_dec['events']

    phrase =  newPhrase()
    phrases = []
    emptyPhrase = False
    x = 0
    count = 0
    lastEndTime = ""

    print("==> Creating phrases from JSON files...")

    for event in events:
        if ('tStartMs' in event and 'dDurationMs' in event and 'segs' in event):
            #print('\n', event['tStartMs'], event['dDurationMs'])
            # That logic above not will work. Put on paper the variables and compare the .json with the right converted js-netflix-doco.srt
            # to figure out something.
            # Look at: https://github.com/nuhman/yt-timedtext-srt/blob/35aa280e833fcf1103fe4ef8aa9f5e9c86664823/main.js#L166 

            phrase['start_time'] = getTimeCode(float(event['tStartMs']))
            phrase['end_time'] = getTimeCode(float(event['dDurationMs'] + event['tStartMs']))
            
            for seg in event['segs']:
                if seg['utf8'] != '\n':
                    emptyPhrase = False
                    phrase['words'].append(seg['utf8'])
                else:
                    emptyPhrase = True
        else: 
            continue
        
        if not emptyPhrase: 
            #print(''.join(phrase['words']), '\nstart: ', phrase['start_time'], '| end: ', phrase['end_time'], '\n')
            phrases.append(phrase)
            phrase = newPhrase()

    return phrases

def writeSRT(phrases, filename):
    print ("==> Writing phrases to disk...")
    e = codecs.open(filename, "w+", "utf-8")
    x = 1
    for phrase in phrases:
        e.write(str(x) + "\n")
        e.write(phrase["start_time"] + " --> " + phrase["end_time"] + "\n")
        out = ''.join(phrase['words'])
        e.write(out + "\n\n" )
        x += 1
    e.close()
  
def writeJSONToSRT(json_file, srtFileName):
    print( "==> Creating SRT from json")
    phrases = getPhrasesFromJSON(json_file)
    writeSRT(phrases, srtFileName)
    
writeJSONToSRT('netflix-doco.json', 'test.srt')
