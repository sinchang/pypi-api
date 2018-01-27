from flask import Flask
from flask import jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'https://github.com/sinchang/pypi-api'

@app.route('/package/<name>')
def search_package(name):
  r = requests.get('https://pypi.org/project/' + name)
  soup = BeautifulSoup(r.text, 'html.parser')

  if (r.status_code != 200):
    return jsonify(message="出错了",status=-1)

  ret = dict({})

  release_history = []
  maintainers = []
  releases = soup.find_all('div', class_='release__card')
  maintainers_ele = soup.select('.sidebar-section--maintainers a')
  meta = soup.select('.sidebar-section')[2].find_all('p')

  for release in releases:
    version = release.find('a').text
    datetime = release.find('time').get('datetime')
    release_history.append(dict({
      'version': version,
      'date': datetime
    }))

  for maintainer in maintainers_ele:
    maintainers.append(dict({
      'profile_url': 'https://pypi.org/' + maintainer.get('href'),
      'name': maintainer.get('data-original-label'),
      'avatar': maintainer.find('img').get('src')
    }))

  ret['name'] = name
  ret['release_history'] = release_history
  ret['desc'] = soup.find('p', class_='package-description__summary').text
  ret['license'] = meta[0].text.split(': ')[1]
  ret['author'] = meta[1].text.split(': ')[1]
  ret['homepage'] = soup.select('.sidebar-section')[1].find_all('a')[0].get('href')
  ret['maintainers'] = maintainers
  ret['status'] = 1
  return jsonify(ret)

if __name__ == '__main__':
  app.run(debug=True)
