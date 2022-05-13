import os
from collections import Counter
from urllib import response
from flask import request
from google.cloud import texttospeech_v1
import json
from modules.image_search import get_search_params
#add accents to google translate

AUDIO_FOLDER = "audio/"
CWD = os.getcwd()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(CWD, 'service_account.json')

#if the user input gives certain language then use that language
def get_language(language):
    if language == "spanish":
        return "es"
    if language == "french":
        return "fr"
    if language == "german":
        return "de"
    if language == "italian":
        return "it"
    if language == "portuguese":
        return "pt"
    if language == "russian":
        return "ru"
    if language == "chinese":
        return "zh"
    if language == "japanese":
        return "ja"
    if language == "korean":
        return "ko"
    if language == "arabic":
        return "ar"
    if language == "bengali":
        return "bn"
    if language == "dutch":
        return "nl"
    if language == "greek":
        return "el"
    if language == "hebrew":
        return "he"
    if language == "hindi":
        return "hi"
    if language == "indonesian":
        return "id"
    if language == "malay":
        return "ms"
    if language == "marathi":
        return "mr"
    if language == "persian":
        return "fa"
    if language == "polish":
        return "pl"
    if language == "portuguese":
        return "pt"
    if language == "punjabi":
        return "pa"
    if language == "romanian":
        return "ro"
    if language == "sanskrit":
        return "sa"
    if language == "serbian":
        return "sr"
    if language == "tagalog":
        return "tl"
    if language == "thai":
        return "th"
    if language == "turkish":
        return "tr"
    if language == "ukrainian":
        return "uk"
    if language == "vietnamese":
        return "vi"
    else:
        return "en"



def init_text2speech_client():
    data = json.loads(request.get_data())
    input = data["input"][2]
    #input = json.parse(input)
    next_input = input["childhood"]
    language = next_input["language"]
    print(language)

    
    client = texttospeech_v1.TextToSpeechClient()
    voice = texttospeech_v1.VoiceSelectionParams(
        #use get_language to get the language code
        language_code= get_language(language),
        ssml_gender=texttospeech_v1.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech_v1.AudioConfig(audio_encoding = texttospeech_v1.AudioEncoding.MP3)

    return client, voice, audio_config

def generate_audio(event, event_number, sentence, client, voice, audio_config):
    synthesis_input = texttospeech_v1.SynthesisInput(text=sentence)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    is_exist = os.path.exists(os.path.join(CWD, AUDIO_FOLDER))
    if not is_exist:
        os.makedirs(os.path.join(CWD, AUDIO_FOLDER))

    file_path = os.path.join(CWD, f'{AUDIO_FOLDER}{event}_{event_number}.mp3')
    with open(file_path,'wb') as output:
        output.write(response.audio_content)

    return file_path

def delete_all_audio():
    is_exist = os.path.exists(os.path.join(CWD, AUDIO_FOLDER))
    if is_exist:
        for filename in os.listdir(os.path.join(CWD, AUDIO_FOLDER)):
            f = os.path.join(CWD, AUDIO_FOLDER, filename)
            os.remove(f)

# dictionary with the template strings for each event
# the variables names in the templates MUST match the dictionary keys
# from the input
# as of rn, ALL arguments for each event are required
TEMPLATE_MAP = {
    "birth": "{pronoun_1} {last_name} was born on {date} in {location}. The most popular movie during this year was {movie}",
    "childhood": "{pronoun_1} {last_name} spent most of {pronoun_3} childhood in {location} between {start_year} to {end_year} speaking {language}.",
    "school": "{pronoun_1} {last_name} attended {name} in {location} from {start_year} to {end_year}.",
    "previous_home": "{pronoun_1} {last_name} lived in {location} from {start_year} to {end_year}.",
    "previous_work": "From {start_year} to {end_year}, {pronoun_1} {last_name} worked at {name} as a {position}",
    "wedding": "On {wedding_date}, {pronoun_1} {last_name} married {spouse_name} in {location}.",
    "current_status": "Currently at the age of {age}, {pronoun_1} {last_name} lives in {location} as a {occupation} at {company}",
    "children": "{pronoun_1} {spouse_name} had {pronoun_3} {number} child, {child_name}, on {birth_date} in {location}.",  
    "death": "{pronoun_1} passed away on {death_date} at the age of {age} in {location}", #  {death_date - birth_date}
}

# input looks like
# [
#    { "name": { "first:", "xxx", "last": "xxx", "pronoun_1": "xxx he/she", "pronoun_2": "xxx him/her",  "pronoun_3": "xxx his/hers"}},
#    { "birth": { "date": "xxx", "location": "xxx" }},
#    { "school": { "name": "xxx", "start_date": "xxx", "end_date": "xxx", "location": "xxx" }}
# ]

# output looks like
# [
#    { "birth": "Person was born on {date} in {location}." },
#    { "school": "They attended {name} in {location} from {start_date} to {end_date}." }
# ]
def generate_sentences(data):
    result = []
    #name_map = {}

    for i, curr in enumerate(data):
        sentence = dict()
        if "name" in curr:
            name_map = curr["name"]
            pronoun_2, pronoun_3 = name_map["pronoun_2"], name_map["pronoun_3"]
            continue
        if (i - 1) % 3 == 0:
            pronoun_1 = name_map["first"]
        else:
            pronoun_1 = name_map["pronoun_1"]
        last_name = name_map["last"] if i == 1 else ""

        # event is e.g. "birth"
        for event, event_dict in curr.items():
            # unpack dictionary as arguments: https://note.nkmk.me/en/python-argument-expand/
            sentence[event] = TEMPLATE_MAP[event].format(pronoun_1=pronoun_1, pronoun_2=pronoun_2, pronoun_3=pronoun_3, last_name=last_name, **event_dict)
        result.append(sentence)

    return result

# input looks like
# [
#    { "birth": { "date": "xxx", "location": "xxx" }},
#    { "school": { "name": "xxx", "start_year": "xxx", "end_year": "xxx", "location": "xxx" }}
# ]

# output looks like
# [
#    { "birth": "path/to/file/birth.mp3" },
#    { "school": "path/to/file/school.mp3" }
# ]
def text_to_speech(data):
    delete_all_audio()
    client, voice, audio_config = init_text2speech_client()
    sentences_lst = generate_sentences(data)
    result = []
    counter = Counter()
    for event_dict in sentences_lst:
        speech = {}
        for event, sentence in event_dict.items():
            counter[event] += 1
            file_path = generate_audio(event, counter[event], sentence, client, voice, audio_config)
            speech[f"{event}_{counter[event]}"] = file_path
        result.append(speech)

    return result
        

if __name__ == "__main__":
    input = [
        { "name": { "first": "Ken", "last": "Griffin", "pronoun_1": "he", "pronoun_2": "his", "pronoun_3": "him" }},
        { "birth": { "date": "October 15, 1968", "location": "Florida, USA" }},
        { "childhood": { "location": "Boca Raton, Florida", "start_year": "1968", "end_year": "1986",  }},
        { "school": { "name": "Harvard College", "start_year": "1986", "end_year": "1989", "location": "Cambridge, Massachusetts" }},
        {"previous_work": {"start_year": "1989", "end_year": "1990", "name": "Glenwood Capital Investments", "position": "treader"}},
        {"current_status": {"age": "53", "location": "Chicago, Illinois", "occupation": "CEO", "company": "Citadel LLC"}},
        {"wedding": {"wedding_date": "July 19, 2003","spouse_name": "Anne Dias-Griffin", "location": "Chicago, Illinois"}}
    ]
    print(generate_sentences(input))
                
