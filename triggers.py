import re


match_triggers = (
    (re.compile("(hey|hi|hello|howdy|greetings)"), "hello"),
    (re.compile("define"), "define"),
    (re.compile("quote"), "quote"),
    #(re.compile("[0-9]"), "search"),
)

search_triggers = (
    (re.compile("weather"), "weather"),
    (re.compile("comic"), "comic"),
    (re.compile("joke"), "joke"),
    (re.compile("pics"), "pics"),
    (re.compile("(search)|(look up)|(google)"), "search"),
    (re.compile("synonyms"), "synonyms"),
    (re.compile("(wordcount)|(word count)"), "wordcount"),
    (re.compile("(play|video|youtube)"), "youtube"),
)


def get_response_key(command):
    for key, value in match_triggers:
        if re.match(key, command):
            return value
    for key, value in search_triggers:
        if re.search(key, command):
            return value
    #return "search"
    #Instead, ask GPT3
    return None
