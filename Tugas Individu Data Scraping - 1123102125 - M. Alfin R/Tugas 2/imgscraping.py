import os
import requests
from bs4 import BeautifulSoup

# URL target
url = 'https://news.detik.com/'  # Ganti dengan URL website yang ingin Anda scrape
response = requests.get(url)

# Parsing HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Direktori untuk menyimpan gambar
output_dir = 'scraped_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Mencari semua tag <img>
images = soup.find_all('img')

# Menyimpan URL gambar dan file gambar
for img in images:
    # Mencari atribut yang mengarah ke gambar resolusi tinggi
    img_url = (
        img.get('data-src') or
        img.get('data-lazy-src') or
        img.get('srcset') or  # srcset sering digunakan untuk gambar besar
        img.get('src')
    )
    if img_url:
        # Jika atribut srcset ditemukan, ambil gambar resolusi tertinggi
        if 'srcset' in img.attrs:
            srcset = img.attrs['srcset'].split(',')[-1]  # Ambil gambar terakhir
            img_url = srcset.split(' ')[0]

        # Tambahkan protokol jika URL relatif
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        elif img_url.startswith('/'):
            img_url = url + img_url
        
        # Filter hanya untuk file gambar
        if img_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Mendapatkan nama file
            filename = os.path.join(output_dir, img_url.split('/')[-1])
            
            # Menyimpan gambar ke file
            try:
                img_data = requests.get(img_url).content
                with open(filename, 'wb') as f:
                    f.write(img_data)
                print(f"Gambar disimpan: {filename}")
            except Exception as e:
                print(f"Error saat mengunduh {img_url}: {e}")

print(f"Semua gambar telah disimpan di direktori '{output_dir}'")
