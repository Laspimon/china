"""Generate archive urls, download archives, scan for links, download articles.

"""
#import json

from archiver import archiver, url_tools

CLEAN_ARCHIVE = bool(0)
SCAN_ARCHIVE  = bool(1)
SCAN_ARTICLES = bool(1)
EXTRACT_TEXT  = bool(1)
LIMIT = '075000'

#RESTORER = json.load(open('data_restore/mapping.json', 'r'))
RESTORER = None

if __name__ == '__main__':
    all_urls = url_tools.get_archive_urls(
        from_date = '2016-04-01',
        earliest_date='2012-02-06',
        schema = 'http://politics.people.com.cn/GB/70731/review/{}.html')

    agent = archiver.Agent(
        directory = 'data',
        archive_folder = 'archives',
        db = 'db')

    if CLEAN_ARCHIVE:
        agent.clean()
        agent = archiver.Agent(
            directory = 'data',
            archive_folder = 'archives',
            db = 'db')

    agent.seed_archive(all_urls)

    if SCAN_ARCHIVE:
        agent.load_unfetched_seeds('000000', RESTORER)
        agent.find_links_in_archive(target_element = 'ul', target_class = 'list_16')

    if SCAN_ARTICLES:
        agent.load_unfetched_links(LIMIT, RESTORER)
        home = 'http://politics.people.com.cn'

    if EXTRACT_TEXT:
        for i, max_i, name, url, text in agent.extract_text_from_articles():
            print ('{}/{}'.format(i, max_i), name, url, text)

    #for x in article_urls: print (x)
    #c = agent.count_links()

    #def stripper(href):
    #    return href.strip().replace('GB/index.html','').strip('/')

    #c = {href:count for href, count in c.items()
    #            if not (stripper(href).split('.')[-1] in ['cn', 'com', ''])}

    #agent.show_counter(counter = c, root = 'http://politics.people.com.cn')
