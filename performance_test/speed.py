import asyncio
import re
import time

import httpx
import requests


def count_https_in_web_pages():
    with open('/home/girish/VisualCodeWorkspace/skills-brushup/apps/poc/performance_test/top15USWebsites.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]

    htmls = []
    for url in urls:
        htmls = htmls + [requests.get(url).text]

    count_https = 0
    count_http = 0
    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print('finished parsing')
    time.sleep(2.0)
    print(f'{count_https=}')
    print(f'{count_http=}')
    print(f'{count_https/count_http=}')


async def better_count_https_in_web_pages():
    with open('/home/girish/VisualCodeWorkspace/skills-brushup/apps/poc/performance_test/top15USWebsites.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]

    async with httpx.AsyncClient() as client:
        tasks = (client.get(url) for url in urls)
        reqs = await asyncio.gather(*tasks)

    htmls = [req.text for req in reqs]

    count_https = 0
    count_http = 0
    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print('finished parsing')
    print(f'{count_https=}')
    print(f'{count_http=}')
    print(f'{count_https/count_http=}')


def main():
    import cProfile
    import pstats

    # start = time.perf_counter()
    # count_https_in_web_pages()
    # elapsed = time.perf_counter() - start
    # print(f'done in {elapsed:.2f}s')

    # with cProfile.Profile() as pr:
    #     count_https_in_web_pages()
    
    with cProfile.Profile() as pr:
        asyncio.run(better_count_https_in_web_pages())

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='/home/girish/VisualCodeWorkspace/skills-brushup/apps/poc/performance_test/needs_profiling.prof')
    # snakeviz /home/girish/VisualCodeWorkspace/skills-brushup/apps/poc/performance_test/needs_profiling.prof


if __name__ == '__main__':
    import sys, os
    sys.path.append(os.getcwd())

    main()
