import requests
from bs4 import BeautifulSoup as bs



payload = {'from': '/bbs/Gossiping/index.html',
               'yes': 'yes'}
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18', data=payload)



def crawlPostLinks(bname):
    prefix = 'https://www.ptt.cc'
    link_list = []
    count = 1
    url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(bname, count)

    while rs.get(url):

        soup = bs(rs.get(url).text, 'lxml')
        titles = soup.find_all(class_='title')
        for t in titles:
            try:
                link_list.append(prefix + t.a['href'])
            except:
                pass
        count += 1
        url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(bname, count)

    return link_list

def searchBoard(bname, query):
    prefix = 'https://www.ptt.cc'
    link_list = []
    count = 1
    url = 'https://www.ptt.cc/bbs/{}/search?page={}&q={}'.format(bname, count, query)
    while rs.get(url):

        soup = bs(rs.get(url).text, 'lxml')
        titles = soup.find_all(class_='title')
        for t in titles:
            try:
                link_list.append(prefix + t.a['href'])
            except:
                pass
        count += 1
        url = 'https://www.ptt.cc/bbs/{}/search?page={}&q={}'.format(bname, count, query)

    return(link_list)



def CommentParser(plink):
    comment_list = []
    soup = bs(rs.get(plink).text, 'lxml')
    push = soup.find_all(class_='push')
    for c in push:
        comment = {'tag': '', 'user_id': '', 'content': '', 'time': ''}
        s = c.find_all('span')
        comment['tag'] += s[0].get_text()
        comment['user_id'] += s[1].get_text()
        comment['content'] += s[2].get_text()
        comment['time'] += s[3].get_text()
        comment_list.append(comment)

    return comment_list



def crawlPost(plink):
    post = {'author': '', 'title': '', 'time': '', 'content': '', 'comment': []}
    soup = bs(rs.get(plink).text, 'lxml')
    meta = soup.find_all(class_="article-meta-value")
    post['author'] += meta[0].get_text()
    try:
        post['title'] += meta[2].get_text()
        post['time'] += meta[3].get_text()
    except:
        post['title'] += meta[1].get_text()
        post['time'] += meta[2].get_text()

    text = soup.find(class_="bbs-screen bbs-content").get_text().split('--\n※')[0].split(post['time'])[1]
    post['content'] += text
    post['comment'].extend(CommentParser(plink))

    return post




def crawlBoard(bname):
    results = {'post_list': [], 'failed_links': []}
    links = crawlPostLinks(bname)
    for plink in links:
        try:
            results['post_list'].append(crawlPost(plink))
        except:
            results['failed_links'].append(plink)

    return results




def crawlBoard_with_Querry(bname, query):
    results = {'post_list': [], 'failed_links': []}
    links = searchBoard(bname, query)
    for plink in links:
        try:
            results['post_list'].append(crawlPost(plink))
        except:
            results['failed_links'].append(plink)

    return results




