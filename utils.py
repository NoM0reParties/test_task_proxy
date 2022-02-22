from requests import Response


def refill_response_content(resp: Response) -> str:
    new_text: str = ''
    current_word: str = ''
    tag_opened: bool = False
    for i in resp.text:
        if len(current_word) == 6 and not i.isalpha():
            new_text += '&trade;'
        if i == '<':
            tag_opened = True
            current_word = ''
        elif i == '>':
            tag_opened = False
        elif tag_opened:
            pass
        elif i.isalpha():
            current_word += i
        else:
            current_word = ''

        new_text += i
    return new_text