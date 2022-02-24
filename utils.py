from requests import Response

STRINGS_TO_IGNORE = ("™", )


def check_apostrophe(symbol: str, txt: str, index: int) -> bool:
    if symbol in STRINGS_TO_IGNORE:
        return True
    return False


def refill_response_content(resp: Response) -> str:
    new_text: str = ''
    current_word: str = ''
    tag_opened: bool = False
    for i, letter in enumerate(resp.text):
        if len(current_word) == 6 and not letter.isalpha() and not check_apostrophe(symbol=letter, txt=resp.text, index=i):
            new_text += '&trade;'
        if letter == '<':
            tag_opened = True
            current_word = ''
        elif letter == '>':
            tag_opened = False
        elif tag_opened:
            pass
        elif letter.isalpha():
            current_word += letter
        else:
            current_word = ''

        new_text += letter
    return new_text