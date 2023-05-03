import pysrt
from mtranslate import translate

def translate_srt(input_file, output_file, source_language, target_language):
    """A (possible) future NLP to identify a group that forms a phrase must be applied in translated_text"""
    text = ''
    subs = pysrt.open(input_file)
    for sub in subs:
        text += sub.text + '\n'

    translated_text = translate(text, from_language=source_language, to_language=target_language)
    translated_lines = translated_text.split('\n')
   
    for i, sub in enumerate(subs):
        sub.text = translated_lines[i]
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
            f.write(translated_lines[line_index] + '\n\n') 
            line_index += 1

output_file = 'output.srt'
input_file = 'files-to-test/tate-first-interview.srt'
source_language = 'en'
target_language = 'pt'
translate_srt(input_file, output_file, source_language, target_language)
