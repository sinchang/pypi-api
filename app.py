from flask import Flask
from flask import jsonify
from flask import request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<a href="https://github.com/sinchang/pypi-api">Project GitHub</a>'

@app.route('/package/<name>')
def get_package_info(name):
  url = 'https://pypi.org/project/' + name
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')

  if r.status_code != 200:
    return jsonify(message="Not Found",status=-1), 404

  ret = {}

  release_history = []
  maintainers = []
  releases = soup.find_all('div', class_='release__card')
  maintainers_ele = soup.select('.sidebar-section--maintainers a')
  meta = soup.select('.sidebar-section')[2].find_all('p')

  for release in releases:
    version = release.find('a').text
    datetime = release.find('time').get('datetime')
    release_history.append({
      'version': version,
      'date': datetime
    })

  for maintainer in maintainers_ele:
    maintainers.append({
      'profile_url': 'https://pypi.org/' + maintainer.get('href'),
      'name': maintainer.get('data-original-label'),
      'avatar': maintainer.find('img').get('src')
    })

  ret['name'] = name
  ret['url'] = url
  ret['release_history'] = release_history
  ret['desc'] = soup.find('p', class_='package-description__summary').text
  ret['license'] = meta[0].text.split(': ')[1]
  ret['author'] = meta[1].text.split(': ')[1]
  ret['homepage'] = soup.select('.sidebar-section')[1].find_all('a')[0].get('href')
  ret['maintainers'] = maintainers
  ret['status'] = 1
  return jsonify(ret)

@app.route('/search')
def search_package():
  q = request.args.get('q')
  page = request.args.get('page') or 1

  r = requests.get(f'https://pypi.org/search?q={q}&page={page}')

  if r.status_code != 200:
    return jsonify(message="Not Found",status=-1), 404
  
  soup = BeautifulSoup(r.text, 'html.parser')

  ret = {}
  projects = []
  projects_ele = soup.find_all('div', class_='package-snippet')

  for project in projects_ele:
    projects.append({
      'name': project.select('.package-snippet__title a')[0].text,
      'url': 'https://pypi.org' + project.select('.package-snippet__title a')[0].get('href'),
      'latest_version': project.select('.package-snippet__version')[0].text,
      'desc': project.select('.package-snippet__description')[0].text
    })

  ret['projects'] = projects
  ret['status'] = 1

  return jsonify(ret)

if __name__ == '__main__':
  app.run(debug=True)
