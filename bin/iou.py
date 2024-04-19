from INDUSTRIALES.AIVA_2024_MADERAS.bin.server.system.model import Model
from INDUSTRIALES.AIVA_2024_MADERAS.bin.server.system.system import MySystem
from sklearn.model_selection import train_test_split
import numpy as np
import cv2 as cv
import glob


def bb_intersection_over_union(boxA, boxB) -> float:
    # code from https://pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/

    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    return interArea / float(boxAArea + boxBArea - interArea)


def bb_intersection_over_unionII(ground_truth, pred) -> float:
    # https://learnopencv.com/intersection-over-union-iou-in-object-detection-and-segmentation/
    # coordinates of the area of intersection.
    ix1 = np.maximum(ground_truth[0], pred[0])
    iy1 = np.maximum(ground_truth[1], pred[1])
    ix2 = np.minimum(ground_truth[2], pred[2])
    iy2 = np.minimum(ground_truth[3], pred[3])

    # Intersection height and width.
    i_height = np.maximum(iy2 - iy1 + 1, np.array(0.))
    i_width = np.maximum(ix2 - ix1 + 1, np.array(0.))

    area_of_intersection = i_height * i_width

    # Ground Truth dimensions.
    gt_height = ground_truth[3] - ground_truth[1] + 1
    gt_width = ground_truth[2] - ground_truth[0] + 1

    # Prediction dimensions.
    pd_height = pred[3] - pred[1] + 1
    pd_width = pred[2] - pred[0] + 1

    area_of_union = gt_height * gt_width + pd_height * pd_width - area_of_intersection

    iou = area_of_intersection / area_of_union

    return iou


def split_train_val_test(path: str) -> ():
    """
        function for creating training datat
    :param path:
    :param classes:
    :return:
    """
    images_ls: list = sorted(glob.glob(path + '*.png'))
    train_data, rest_data = train_test_split(images_ls, train_size=0.8, shuffle=True, random_state=42)
    validation_data, test_data = train_test_split(rest_data, test_size=0.5, shuffle=False, random_state=42)
    return train_data, validation_data, test_data


def predict(my_system, img):
    bbox_defects = my_system.detect_damage(img)
    return bbox_defects


def read_yaml(file: str) -> np.array:
    try:
        fs: cv.FileStorage = cv.FileStorage(file, cv.FILE_STORAGE_READ)
        fn: cv.FileNode = fs.getNode("rectangles")
        return fn.mat()
    except:
        return np.array([])


def read_reg_file(file) -> [[]]:
    data = read_yaml(file)

    if data.size == 0:
        return []

    data = np.hstack(data).tolist()
    number_bb = len(data) // 4

    if number_bb == 1:
        return [[data[0],
                 data[1],
                 data[0] + data[2],
                 data[3] + data[1]]]

    lists_of_list = [data[i:i + number_bb] for i in range(0, len(data), number_bb)]
    results = []
    for i in list(zip(*lists_of_list)):
        cords = [i[0],
                 i[1],
                 i[0] + i[2],
                 i[3] + i[1]]

        results.append(cords)

    return results


save_path = './server/models/'
name = 'Yolo_Training2'
model_ = Model()
model_.load_model(f'{save_path}/{name}/weights/best.pt')
my_system = MySystem(model_)

_, _, test_data = split_train_val_test('../dataset/MuestrasMaderas/')

metrics_history = {}
for i in test_data:
    img = cv.imread(i)
    bboxes_pred = predict(my_system, img)
    bboxes_gt = read_reg_file(i.replace('.png', '.reg'))

    print(i)
    print(bboxes_pred)
    print(bboxes_gt)

    for x1, y1, x2, y2 in  bboxes_pred:
        img = cv.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 1)

    for x1, y1, x2, y2 in  bboxes_gt:
        img = cv.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 1)

    cv.imwrite('./evaluation/' + i.split('/')[-1], img)

    if len(bboxes_gt) == 0:
        metrics_history[i] = []
        continue

    result = [[] for i in range(len(bboxes_gt))]
    for idx, gt in enumerate(bboxes_gt):
        for pred in bboxes_pred:
            r = bb_intersection_over_unionII(gt, pred)
            result[idx].append(r)

    metrics = [max(r) >= 0.5 for r in result]

    metrics_history[i] = metrics
    for r in result:
        print(r)
    print(metrics)


total = []
for i, j in metrics_history.items():
    total.extend(j)
    print(i, j)

print(total.count(False))
print(total.count(True))

a = (225, 254, 253, 296)
b = [227, 255, 251, 287]

a = (339, 256, 356, 280)
b = [343, 259, 355, 275]
print(bb_intersection_over_union(b, a))