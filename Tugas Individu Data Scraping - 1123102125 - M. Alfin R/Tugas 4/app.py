from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Halaman Utama
@app.route('/')
def index():
    return render_template('index.html')

# Scrape Data dan Tampilkan
@app.route('/scrape', methods=['POST'])
def scrape():
    # URL target (dari form di index.html)
    target_url = request.form.get('url')

    # Request halaman target
    response = requests.get(target_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Ambil elemen gambar
    images = soup.find_all('img')
    img_urls = []
    for img in images:
        img_url = img.get('src') or img.get('data-src')
        if img_url:
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif img_url.startswith('/'):
                img_url = target_url + img_url
            img_urls.append(img_url)

    return render_template('result.html', images=img_urls)

if __name__ == '__main__':
    app.run(debug=True)
