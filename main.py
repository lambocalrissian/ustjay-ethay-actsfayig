import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()


@app.route('/')
def home():
    fact = get_fact()

    url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    # 'https://hidden-journey-62459.herokuapp.com/'
    data = {'input_text': fact}

    response = requests.post(url, data=data)

    url = response.url
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    quote = soup.find("body")

    print(f'{quote}\n')

    print(type(quote))
    body = str(soup.body)
    print()
    h2_tag = '/h2>'
    start_pos = body.find(h2_tag)
    start_pos += len(h2_tag)
    end_pos = body.find('</body')
    piglatin = body[start_pos: end_pos].strip()

    return f'<a href="{url}">{piglatin}</a>'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

