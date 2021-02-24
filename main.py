import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import csv
import sys

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
CYAN = colorama.Fore.CYAN
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
instagram_urls = set()
visited_urls = set()

# number of urls visited so far will be stored here
total_urls_visited = 0
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    try:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
    except requests.exceptions.InvalidSchema:
        print(f'{GRAY}[-] error cannot open {url}{RESET}')
        return set()
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # instagram link
            if href not in instagram_urls and "www.instagram.com" in href:
                print(f"{GRAY}[!] Instagram link: {href}{RESET}")
                instagram_urls.add(href)
            continue
        # print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

def crawl(url, max_urls=50):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `instagram_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    print(f"{GREEN}[*] Internal link: {url}{RESET}")
    global visited_urls
    visited_urls.add(url)
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            return
        if link not in visited_urls:
            crawl(link, max_urls=max_urls)
        else:
            return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Error: need the csv file')
        sys.exit()
    with open(sys.argv[1]) as csv_file_reader:
        reader = csv.DictReader(csv_file_reader, delimiter=',')
        websites = [row ['website'] for row in reader]
    result = []
    for  website in websites:
        print('\n ---------- \n')
        internal_urls = set()
        instagram_urls = set()
        visited_urls = set()
        total_urls_visited = 0
        print(f"{CYAN}-> {website}{RESET}")
        crawl(website, max_urls=200)
        result.append({'websites': website, 'instagram': ' '.join(instagram_urls)})
        print("[+] Total instagram links:", len(instagram_urls))
        print("[+] Total Internal links:", len(internal_urls))
        print("[+] Total:", len(instagram_urls) + len(internal_urls))
    with open('result.csv', 'w') as w:
        w.write('websites,instagrams\n')
        for elem in result:
            w.write('{},{}\n'.format(elem['websites'], elem['instagram']))
