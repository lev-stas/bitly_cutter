import requests
import os
from dotenv import load_dotenv
import argparse


def count_clicks (token, url):
    get_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary'
    headers = {'Authorization' : f'Bearer {token}'}
    params = {'units' : '-1'}
    response = requests.get(get_url, headers=headers, params=params)
    response.raise_for_status()
    answer = response.json()['total_clicks']
    return answer

def shorten_link(token, url):
    post_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {'Authorization' : f'Bearer {token}'}
    json = {'long_url' : f'{ url}'}
    response = requests.post(post_url, headers=headers, json=json)
    response.raise_for_status()
    short_link = response.json()['link']
    return short_link



if __name__ == '__main__':
  load_dotenv()
  parser = argparse.ArgumentParser(description='Bilty link changer')
  parser.add_argument('url',help='long url or short bitlink')
  args = parser.parse_args()

  token = os.getenv('BITLY_TOKEN')
  url = args.url

  if url.startswith('bit.ly'):
    try:
      answer = count_clicks(token, url)
      print( 'Количество кликов:', answer)
    except requests.exceptions.HTTPError:
      print('Error. Check bitlink address.')
        
        
  elif url.startswith('http'):
    try:
      link = shorten_link(token, url)
      print('Bitlink:', link)
    except requests.exceptions.HTTPError:
        print('Error. Check url address.')
        
  else:
    print('Unknown link format')