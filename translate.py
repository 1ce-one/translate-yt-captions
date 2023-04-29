# From: https://github.com/ahmeterenodaci/easygoogletranslate/blob/main/easygoogletranslate.py

import concurrent.futures
import requests
import re
import os
import html
import urllib.parse

class EasyGoogleTranslate:
    def __init__(self, source_language='auto', target_language='tr', timeout=5):
        self.source_language = source_language
        self.target_language = target_language
        self.timeout = timeout
        self.pattern = r'(?s)class="(?:t0|result-container)">(.*?)<'

    def make_request(self, target_language, source_language, text, timeout):
        escaped_text = urllib.parse.quote(text.encode('utf8'))
        url = 'https://translate.google.com/m?tl=%s&sl=%s&q=%s'%(target_language, source_language, escaped_text)
        response = requests.get(url, timeout=timeout)
        result = response.text.encode('utf8').decode('utf8')
        result = re.findall(self.pattern, result)
        if not result:
            print('\nError: Unknown error.')
            f = open('error.txt')
            f.write(response.text)
            f.close()
            exit(0)
        return html.unescape(result[0])

    def translate(self, text, target_language='', source_language='', timeout=''):
        if not target_language:
            target_language = self.target_language
        if not source_language:
            source_language = self.source_language
        if not timeout:
            timeout = self.timeout
        if len(text) > 5000:
            print('\nError: It can only detect 5000 characters at once. (%d characters found.)'%(len(text)))
            exit(0)    
        if type(target_language) is list:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.make_request, target, source_language, text, timeout) for target in target_language]
                return_value = [f.result() for f in futures]
                return return_value
        return self.make_request(target_language, source_language, text, timeout)

def get_text_from_srt():
    file = open( "files-to-test/js-netflix-doco.srt", "r")
    lines = file.readlines()
    file.close()
    to_trans_text = ''
    to_split_text = ''
    for line in lines:
        if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
            to_trans_text += '' + line.rstrip('\n')
            to_split_text += "|" + line.rstrip('\n') 
            # (?) Figure-out a symbol that the translator ignores, but that works to split.
            # (?) Make a pattern to put the translated text properly on new srt.
        to_trans_text = to_trans_text.lstrip()
        to_split_text = to_split_text.lstrip()
    return to_trans_text, to_split_text

to_trans, to_split = get_text_from_srt()
translator = EasyGoogleTranslate(source_language='en', target_language='pt')
result1 = translator.translate(text=to_trans)
result2 = translator.translate(text=to_split)
print(result1)
print('\n')
print(result2)
