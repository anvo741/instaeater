from lxml import html

import bs4
import os
import random
import requests
import sys
import time

def notify(title, subtitle, message):
  t = '-title {!r}'.format(title)
  s = '-subtitle {!r}'.format(subtitle)
  m = '-message {!r}'.format(message)
  os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def scan(url):
  try:
     page = requests.get(url)
  except:
    return
  soup = bs4.BeautifulSoup(page.text, "lxml")
  print(soup)
  links = soup.select('.r a')
  print(links[0]['href'])
  #links = soup.find_all('a', href=True)                                                                                                                                                                
  for link in links:
    print("Found the URL: " + link[0]['href'])

while True:
  scan("https://www.instagram.com/eater_sf/")
  time.sleep(random.randint(5,10))