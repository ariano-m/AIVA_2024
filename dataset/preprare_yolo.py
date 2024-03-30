import numpy as np
import cv2 as cv
import glob


def read_yaml(file: str):
    try:
        fs: cv.FileStorage = cv.FileStorage(file, cv.FILE_STORAGE_READ)
        fn: cv.FileNode = fs.getNode("rectangles")
        r: np.ndarray = fn.mat()
    except:
        r: np.ndarray = np.array([])
    return r


files = sorted(glob.glob("./MuestrasMaderas/*.reg"))
for idx, file in enumerate(files):
    print(f"#{idx}")
    data = read_yaml(file)
    if data.size == 0:
        continue
    data = np.hstack(data).tolist()

    number_bb = len(data) // 4
    print(data)

    msg = ""
    if number_bb > 1:
        lists_of_list = [data[i:i + number_bb] for i in range(0, len(data), number_bb)]
        lists_of_list = zip(*lists_of_list)
        for i in lists_of_list:
            i = list(i)
            i[0] = (i[0] + int(i[2] / 2)) / 488
            i[1] = (i[1] + int(i[3] / 2)) / 422
            i[2] = i[2] / 488
            i[3] = i[3] / 422
            string_list = [str(num) for num in i]
            msg += "0 " + ' '.join(map(str, string_list)) + "\n"
    else:
        data[0] = (data[0] + int(data[2] / 2)) / 488
        data[1] = (data[1] + int(data[3] / 2)) / 422
        data[2] = data[2] / 488
        data[3] = data[3] / 422
        msg += "0 " + ' '.join(map(str, data)) + "\n"

    file = file.split("/")[-1]
    file = file.replace(".reg", ".txt")

    with open(f'./MuestrasMaderas/{file}', 'w') as file:
        file.write(msg)
