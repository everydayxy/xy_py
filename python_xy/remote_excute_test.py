# coding:utf-8
from concurrent import futures
import urllib2

URLS = ['http://www.xiaorui.cc/',
        'http://blog.xiaorui.cc/',
        'http://ops.xiaorui.cc/',
        'http://www.sohu.com/']


def load_url(url, timeout):
    print
    '收到任务{0}'.format(url)
    return urllib2.urlopen(url, timeout=timeout).read()


with futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = dict((executor.submit(load_url, url, 60), url)
                         for url in URLS)

    for future in futures.as_completed(future_to_url):
        url = future_to_url[future]
        if future.exception() is not None:
            print('%r generated an exception: %s' % (url,
                                                     future.exception()))
        else:
            print('%r page is %d bytes' % (url, len(future.result())))