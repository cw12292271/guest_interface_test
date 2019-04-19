from bs4 import BeautifulSoup
import requests


def get_isca(url, headers, payload):
    page = requests.post(url, data=payload, headers=headers).text
    soup = BeautifulSoup(page, 'lxml')
    links = soup.select('td.results_2')
    i = 0
    for link in links:
        print(link.text)
        i += 1
        if (i % 8 == 0):
            print('================')

    links = soup.select('td.results_1')
    i = 0
    for link in links:
        print(link.text)
        i += 1
        if (i % 8 == 0):
            print('================')

if __name__ == '__main__':
    url = 'http://dbsearch.clinicalgenome.org/search/'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'X-Mapping-eeipplmp=4DF199590E46B78FBFB31AEB1821707A',
        'Referer': 'http://dbsearch.clinicalgenome.org/search/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
    }
    payload = {
        'GenomeBuild': 'hg19',
        'Location': 'chrX:70367400-70384667',
        'DirectView': 'View in ...',
        'Type': 'Any',
        'Gender': 'Any',
        'HPOTerm': '',
        'Task': 'Search ISCA Database',
        'pheno_btn_style': '',
    }

    get_isca(url, headers, payload)