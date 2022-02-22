from flask import Flask, request
from requests import get, Response

from utils import refill_response_content

app = Flask(__name__)
SITE_NAME = 'https://news.ycombinator.com/'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path: str):
    url_name: str = f'{SITE_NAME}{path}'
    if request.query_string:
        url_name += f'?{request.query_string.decode()}'
    r: Response = get(url_name)
    if '.' not in r.url.split('/')[-1]:
        new_text = refill_response_content(resp=r)
        protocol: str = request.url.split('://')[0]
        r._content = bytes(new_text.replace(f'href="{SITE_NAME[:-1]}', f'href="{protocol}://{request.host}'), 'utf-8')
    return r.content, r.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
