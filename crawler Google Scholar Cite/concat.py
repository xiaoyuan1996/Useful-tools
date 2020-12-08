import mytools
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

root_path = "infomations/"
files = os.listdir(root_path)
info_1 = {}
for f in files:
    ctxs = mytools.load_from_txt(root_path+f)

    info_1[ctxs[0].replace("\n","")] = [i.replace("\n", "") for i in ctxs[2:]]


# root_path = "infomations_3/"
# files = os.listdir(root_path)
# for f in files:
#     ctxs = mytools.load_from_txt(root_path+f)
#
#     info_1[ctxs[0].replace("\n","")] += [i.replace("\n", "") for i in ctxs[2:]]
#
# root_path = "infomations/"
# files = os.listdir(root_path)
# for f in files:
#     ctxs = mytools.load_from_txt(root_path+f)
#
#     info_1[ctxs[0].replace("\n","")] += [i.replace("\n", "") for i in ctxs[2:]]
#


tmp_info = {}
for title in tqdm(info_1.keys()):
    cites = info_1[title]

    if len(cites) == 0:
        tmp_info[title] = [[' ', ' ', ' ', ' ']]
        continue

    for cite in cites:

        paper_author = cite.split(").")[0]
        if len(paper_author)>=2:
            paper_author += ")."
        paper_name = "".join(cite.split(").")[1:]).split("<i>")[0][1:]
        paper_time = cite.replace(paper_author,"").replace(paper_name,"")
        publisher = paper_time.split("</i>")[0].replace("<i>","")[1:]
        paper_time = cite.replace(paper_author,"").replace(paper_name,"").replace(publisher,"").replace("<i>","").replace("</i>","")[2:]

        # print(paper_author)
        # print(paper_name)
        # print(publisher)
        # print(paper_time)
        if title not in tmp_info:
            tmp_info[title] = [[
            paper_author, paper_name.replace("&amp; ",""), publisher, paper_time
        ]]
        else:
            tmp_info[title].append([
            paper_author, paper_name.replace("&amp; ",""), publisher, paper_time
        ])




# 保存
save_info = []
for k in tmp_info.keys():
    save_info.append(["*************", k, "**************", "****************"])
    save_info.append(["----","--------","----","----"])
    save_info.append(["作者", "题目", "出版者", "时间"])
    for item in tmp_info[k]:
        save_info.append(item)

    for i in range(5):
        save_info.append([" ", " ", " ", " "])


data = pd.DataFrame(np.array(save_info), index=None, columns=[" ", " ", " ", " "])


data.to_excel("all_info.xls", index=None)
np.array(tmp_info)





# root_path = "infomations/"
# files = os.listdir(root_path)
# for f in files:
#     ctxs = mytools.load_from_txt(root_path+f)
#
#     cnt = 0
#     for ctx in ctxs:
#         if "------" in ctx:
#             cnt += 1
#     if cnt >= 2:
#         print(f)
# print("=============")
#
# root_path = "infomations/"
# files = os.listdir(root_path)
# for f in files:
#     ctxs = mytools.load_from_txt(root_path+f)
#
#     if len(ctxs) >=50:
#         print(f.replace(".txt",""))
