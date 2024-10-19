import os
import time
import requests

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# images_path = 'images/lotr_tome_cards/'
images_path = 'images/tome_commander_cards/'


def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.1 Safari/537.36'}
    
    # TODO - implementar o scrapping das duas bases
    #lotr_tome_collection_url = "http://www.ligamagic.com.br/?view=cards/search&card=edid=480196%20ed=ltr" 
    tome_commander_url = "https://www.ligamagic.com.br/?view=cards/search&card=edid=480238%20ed=lt"

    
    
    driver = webdriver.Chrome()
    driver.get(tome_commander_url)
    SCROLL_PAUSE_TIME = 10
    last_height = driver.execute_script("return document.body.scrollHeight")

    # TODO - deixar o scroll mais lento, está abrindo direto nas páginas finais e as imagens não estão sendo carregadas
    while True:
        # Scroll até o final da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Esperar o carregamento dos novos dados
        time.sleep(SCROLL_PAUSE_TIME + 5)  # Aumenta o tempo de pausa para tornar o scroll mais lento

        # Calcular a nova altura da página e comparar com a altura anterior
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')

    cards = soup.findAll('div', class_='card-item') 
    print(f'{len(cards)} cards encontrados.')

    for card in tqdm(cards):
        # TODO - Armazenar informações do card em um arquivo JSON

        card_name = card.find_all('b')[0].string.replace(" ", "").replace("//", "_ou_")
        card_img = card.find('img', class_='main-card')

        if 'src' in card_img.attrs.keys():
            img_url = 'http:' + card_img['src']
            if img_url.endswith('.jpg'):
                print(f'{cards.index(card)} - {card_name}')
                print(img_url)                    
                img_response = requests.get(img_url, stream=True)
                if img_response.status_code == 200:
                    with open(f"{images_path}item_{cards.index(card)}_{card_name}.jpg", 'wb') as f:
                        for chunk in img_response.iter_content(1024):
                            f.write(chunk)
        else:
            print(card_img.attrs.keys())
            print(f'Imagem não encontrada para o card {card_name}')
        #time.sleep(2)


if __name__ == '__main__':
    os.makedirs(f'{images_path}', exist_ok=True)
    main()
