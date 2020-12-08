import mytools

ctxs = mytools.load_from_txt("b.txt")

save_name = "infomations/Orientation robust object detection in aerial images using deep convolutional neural network.txt"

data = []
for i,d in enumerate(ctxs):
    if len(d) <=5:
        pass
    else:
        data.append(d[10:].replace("\n",""))
mytools.log_to_txt(data,save_name)
