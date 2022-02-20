from flask import Flask
from requests import get, Response

app = Flask(__name__)
SITE_NAME = 'https://news.ycombinator.com/'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path: str):
    r: Response = get(f'{SITE_NAME}{path}')
    if '.' not in r.url.split('/')[-1]:
        new_text: str = ''
        current_word: str = ''
        tag_opened: bool = False
        for i in r.text:
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
        r._content = bytes(new_text, 'utf-8')
    return r.content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
