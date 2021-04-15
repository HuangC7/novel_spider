# 导入第三方包和模块
import requests
from bs4 import BeautifulSoup
import csv
headers={ 'UserAgent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36' }

item_dict_list = []

# 循环改变url值，遍历1月到3月的网页
for i in range(1,4):
    url = 'http://chuangshi.qq.com/bang/mo/all-week-2021-0'+str(i)+'.html'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    item_list = soup.select('#rankList > tr')
    for item in item_list[1:]:
        show_rank = item.select('td')[0].select('strong')
        show_name = item.select('td')[2].select('a')
        show_author = item.select('td')[3].select('a')
        show_ticket = item.select('td')[4]

        # print(show_ticket)
        # print(show_name)

        for show_rank, show_name, show_author, show_ticket in zip(show_rank, show_name, show_author, show_ticket):
            item_dict = {
                     'show_rank': show_rank.get_text().strip(), \
                     'show_name': show_name.get_text().strip(), \
                     'show_author':show_author.get_text().strip(),\
                     'show_ticket':show_ticket.strip()}
            item_dict_list.append(item_dict)

    with open('result.csv', 'w', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
                                               'show_rank',
                                               'show_name',
                                               'show_author',
                                               'show_ticket'])
        writer.writeheader()
        writer.writerows(item_dict_list)
