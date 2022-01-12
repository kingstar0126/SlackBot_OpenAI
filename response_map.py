import responses as rsp


response_dict = {
    'comic': [
        rsp.comic
    ],
    'define': [
        rsp.define
    ],
    'hello': [
        "Sup",
        "hey guys",
        "yo",
        "what's the word",
        "hi"
    ],
    'joke': [
        rsp.joke
    ],
    'no_command': [
        "I don't know what you want from me",
    ],
    'pics': [
        rsp.get_pic
    ],
    'quote': [
        rsp.get_quote
    ],
    'search': [
        rsp.search_words
    ],
    'synonyms': [
        rsp.synonyms
    ],
    'weather': [
        rsp.check_weather
    ],
    'wordcount': [
        rsp.word_count
    ],
    'youtube': [
        rsp.get_video
    ],
}
