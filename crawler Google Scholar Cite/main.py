#coding:utf-8
import urllib.request
import re
import time
import mytools
import random

COOKIE = open("cookie.txt", 'r').read()

def get_url_info(url):

    # 构造请求头信息
    header = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Mobile Safari/537.36 Edg/87.0.664.52",
        "cookie": COOKIE    }

    req = urllib.request.Request(url, headers=header)

    respons = urllib.request.urlopen(req, timeout=25).read().decode()

    time.sleep(1.5 + random.random()*3)
    return respons

def get_title(title):

    # 构造查询网址
    query_url = "https://scholar.google.com/scholar?hl=zh-CN&as_sdt=0%2C5&q=qqqqqqqq&btnG=".replace("qqqqqqqq","+".join(title.split(" ")))
    print("Query url: ", query_url)
    root_paper = get_url_info(query_url)
    print("Get root paper info successful.")

    # 查引用id------>>查本文引用
    f = re.finditer("cites=", root_paper)
    tmp_str = ""
    for item in f:
        start, end = item.span()
        tmp_str = root_paper[start: start+50]
        break

    # 没有引用直接退出
    if (tmp_str == "") or ("找到约" in root_paper):
        print("No one cite.")
        last_infos = []
        last_infos.append(title)
        last_infos.append("-------------------------------")
        mytools.log_to_txt(last_infos,"infomations/" + title.replace(":","").replace("/","") + ".txt")
        return None

    f = re.finditer("&amp;as", tmp_str.replace("cites=",""))
    for item in f:
        start, end = item.span()
    root_paper_id = tmp_str.replace("cites=","")[:start]
    print("Get root paper id successful.")
    print("Root paper id: ",root_paper_id)

    # 得到ROOT_ID后，构造查询引用网址
    bib_seqs = []
    bib_seqs_all_info = {}
    start_index = 150
    for ii in range(0, 5):
        query_cite_url = "https://scholar.google.com/scholar?start=wwwwww&hl=zh-CN&as_sdt=2005&sciodt=1,5&cites=qqqqqq&scipsc=".replace("wwwwww",str(start_index)).replace("qqqqqq",root_paper_id)
        print("    Cite url: ", query_cite_url)
        cite_paper = get_url_info(query_cite_url)
        print("    Get cite paper info successful.")

        # 从cite paper info中查引用
        f = re.finditer(" data-did=", cite_paper)
        start_ends = []
        for item in f:
            start_ends.append(item.span())
        if len(start_ends) == 0:
            break
        else:
            for idx,(start, end) in enumerate(start_ends):
                try:
                    b_seq = cite_paper[start:start+50][11:23]
                    if b_seq not in bib_seqs:
                        bib_seqs.append(b_seq)
                        bib_seqs_all_info[b_seq] = {
                            "start": start_index + idx,
                            "cites": root_paper_id
                        }
                except:
                    pass
        print(len(bib_seqs),bib_seqs)
        if len(bib_seqs)%10 !=0:
            break
        start_index += 10
    print("Bib indexs get successful.")
    print("Bib indexs:",bib_seqs)

    # 得到bib信息
    last_infos = []
    last_infos.append(title)
    last_infos.append("-------------------------------")

    for bib in bib_seqs:
        bib_query_url = "https://scholar.google.com/scholar?q=info:qqqqqq:scholar.google.com/&output=cite&scirp=0&hl=zh-CN".replace("qqqqqq", bib)
        print("    Current bib query url:" ,bib_query_url)
        tmp = get_url_info(bib_query_url)

        # 解析信息
        f = re.finditer("gs_citr", tmp)
        for item in f:
            _, start = item.span()
            # break
        f = re.finditer("</div></td></tr></table></div><div id=", tmp)
        for item in f:
            end, _ = item.span()
            break
        info_item = tmp[start+2:end]
        print("    cite:", info_item)
        last_infos.append(info_item)

    # 整合写入txt
    mytools.log_to_txt(last_infos,"infomations/"+title.replace(":","").replace("/","")+".txt")

if __name__ == "__main__":

    # title = "Automatic ship detection in remote sensing images from google earth of complex scenes based on multiscale rotation Dense Feature Pyramid Networks"
    # get_title(title)
    # exit(0)

    from tqdm import tqdm
    import numpy as np
    import pandas as pd
    start_from = 0
    # data = np.array(pd.read_excel("论文题目单独-孙.xlsx"))[start_from:]
    txt = mytools.load_from_txt("second_index.txt")[start_from:]
    for d in tqdm(txt):
        # print(d[0].replace("\n",""))
        # get_title(d[0].replace("\n",""))
        print(d.replace("\n",""))
        get_title(d.replace("\n",""))


