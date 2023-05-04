import pysrt
from mtranslate import translate
chunksize=100
def translate_srt(input_file, output_file, source_language, target_language,chunksize):
    """A (possible) future NLP to identify a group that forms a phrase must be applied in translated_text"""
    text = ''
    subs = pysrt.open(input_file)
    maxsize = len(subs)

    for i in range(0,maxsize,chunksize):
        chunk = subs[i:i+chunksize]
        for sub in chunk:
            text += sub.text + '\n'

        translated_text = translate(text, from_language=source_language, to_language=target_language)
        translated_lines = translated_text.split('\n')

        for i, sub in enumerate(chunk):
            sub.text = translated_lines[i]
        text = ''
    subs.save(output_file, encoding='utf-8')

    
    # Add time informations in the SRT file
    with open(output_file, 'r+', encoding='utf-8') as f:
        content = f.readlines()
        print(content)
        f.seek(0)
        f.truncate()
        line_index = 0
        for sub in subs:
            f.write(str(line_index+1)+'\n')
            f.write(str(sub.start)+' --> '+str(sub.end)+'\n')
            f.write(sub.text + '\n\n') 
            line_index += 1

output_file = 'output.srt'
input_file = 'input.srt'
source_language = 'en'
target_language = 'pt'
translate_srt(input_file, output_file, source_language, target_language,chunksize)
