# 导入第三方包和模块
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

headers={ 'UserAgent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36' }


# 爬取当前网页信息
def get_list(n):
    item_dict_list = []
    show_category_all_test = []
    url = 'http://chuangshi.qq.com/bang/mo/all-week-2021-%02d.html'%n
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    item_list = soup.select('#rankList > tr')

# 爬取小说近三个月的排名，书名，作者和月票信息
    for item in item_list[1:]:
        show_rank = item.select('td')[0].select('strong')
        show_category_test = item.select('td')[1]
        show_category = [i.replace('[','').replace(']','') for i in show_category_test]
        show_name = item.select('td')[2].select('a')
        show_author = item.select('td')[3].select('a')
        show_ticket = item.select('td')[4]
        show_category_all_test.append(show_category)

        for show_rank, show_category, show_name, show_author, show_ticket in zip(show_rank, show_category, show_name, show_author, show_ticket):
            item_dict = {
                     'show_rank': show_rank.get_text().strip(), \
                     'show_category': show_category.strip(), \
                     'show_name': show_name.get_text().strip(), \
                     'show_author':show_author.get_text().strip(),\
                     'show_ticket':show_ticket.strip()}

            item_dict_list.append(item_dict)

# 分类统计各类别（show_category）的数量和月票总数
    show_category_all = []
    show_category_all.extend([x[0] for x in show_category_all_test])
    item_dict_2 = dict()
    data = dict()

    for key, i in zip(show_category_all, item_dict_list):
        item_dict_2 = data.get(key,[0,0])
        item_dict_2[0] = item_dict_2[0] + 1
        item_dict_2[1] = item_dict_2[1] + int(i['show_ticket'])
        data[key] = item_dict_2

    # 各类别图书数量及月票信息
    show_category_numAndticket = []
    for k in data.keys():
        show_category_numAndticket.append([k])
    for i, j in enumerate(data.values()):
        show_category_numAndticket[i].append(j[0])
        show_category_numAndticket[i].append(j[1])
    show_category_numAndticket.sort(key=lambda  x:x[1], reverse=True)

    return item_dict_list,  show_category_numAndticket

if __name__=='__main__':
    # novel_list是个多维列表:
    # novel_list[i]代表每个月的图书信息(包括1-3月，对应[0]到[2]);
    # novel_list[i][0]代表当前月的排名，书名，作者和月票信息，novel_list[i][1]代表当前月各类别图书数量及月票信息
    novel_list = []
    for i in range(1,4):
        novel_list.append(get_list(i))

    name = ['1月','2月','3月']
    plt.figure(figsize=(16, 8), dpi=80)
    plt.figure(1)

    ax1 = plt.subplot(131)
    plt.barh([i[0] + str(i[1]) + '本' for i in novel_list[0][1]], [i[2] for i in novel_list[0][1]], color = 'red')
    plt.title(name[0])

    ax2 = plt.subplot(132)
    plt.barh([i[0] + str(i[1]) + '本' for i in novel_list[1][1]], [i[2] for i in novel_list[1][1]], color='yellow')
    plt.title(name[1])

    ax3 = plt.subplot(133)
    plt.barh([i[0] + str(i[1]) + '本' for i in novel_list[2][1]], [i[2] for i in novel_list[2][1]], color='blue')
    plt.title(name[2])

    plt.show()  # 显示图像

