from sklearn.metrics import RocCurveDisplay, roc_curve, auc, precision_recall_curve
from INDUSTRIALES.AIVA_2024_MADERAS.bin.server.system.model import Model
from INDUSTRIALES.AIVA_2024_MADERAS.bin.server.system.system import MySystem
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import glob


def accuracy(tp, tn, fp, fn):
    try:
        acc = (tp + tn) / (tp + tn + fp + fn)
    except ZeroDivisionError:
        acc = 0
    return acc


def recall(tp, fn):
    try:
        rcll = tp / (tp + fn)
    except ZeroDivisionError:
        rcll = 0
    return rcll


def precision(tp, fp):
    try:
        prc = tp / (tp + fp)
    except ZeroDivisionError:
        prc = 0
    return prc


def f1(precision, recall):
    try:
        f = 2 * (precision * recall) / (precision + recall)
    except ZeroDivisionError:
        f = 0
    return f

def tasas(TP, TN, FP, FN):
    FPR = FP / (FP + TN)
    FNR = FN / (FN + TP)
    TPR = TP / (TP + FN)
    TNR = TN / (TN + FP)

    return FPR, FNR, TPR, TNR

def plot_precision_recall_curve(y_true, y_scores):
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)

    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='blue', lw=2, label='Curva Precisión-Recall')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Curva Precisión-Recall')
    plt.legend(loc="lower left")
    plt.grid(True)
    plt.show()

def plot_roc_curve(y_true, y_scores):
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='blue', lw=2, label='Curva ROC')
    plt.plot([0, 1], [0, 1], color='red', linestyle='--', label='Clasificador aleatorio')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Tasa de Falsos Positivos (FPR)')
    plt.ylabel('Tasa de Verdaderos Positivos (TPR)')
    plt.title('Curva ROC')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.show()

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


def calc_matrix(test_data):
    global metrics_history
    global prob
    for i in test_data:
        img = cv.imread(i)
        bboxes_pred = predict(my_system, img)
        bboxes_gt = read_reg_file(i.replace('.png', '.reg'))

        for x1, y1, x2, y2 in bboxes_pred:
            img = cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 1)

        for x1, y1, x2, y2 in bboxes_gt:
            img = cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

        # cv.imwrite('./evaluation/' + i.split('/')[-1], img)

        if len(bboxes_gt) == 0:  # False Positive
            if len(bboxes_pred) != 0:
                metrics_history['FP'] += len(bboxes_pred)
                for i in range(len(bboxes_pred)):
                    prob['true'].append(0)
                    prob['score'].append(1)
            continue

        if len(bboxes_pred) == 0:  # False Negative
            if len(bboxes_gt) != 0:
                metrics_history['FN'] += len(bboxes_gt)
                for i in range(len(bboxes_gt)):
                    prob['true'].append(1)
                    prob['score'].append(0)
            continue

        result = [[] for i in range(len(bboxes_gt))]
        for idx, gt in enumerate(bboxes_gt):
            for pred in bboxes_pred:
                r = bb_intersection_over_unionII(gt, pred)
                result[idx].append(r)

            if max(result[idx]) >= 0.4:
                metrics_history['TP'] += 1  # Decimos que hay algo, y hay algo
                prob['true'].append(1)
                prob['score'].append(1)
            else:
                metrics_history['FN'] += 1  # Decimos que no  hay nada, y hay algo
                prob['true'].append(1)
                prob['score'].append(0)

        if len(bboxes_pred) > len(bboxes_gt):
            metrics_history['FP'] += (len(bboxes_pred) - len(bboxes_gt))  # Decimos que hay algo, y no hay nada
            for i in range((len(bboxes_pred) - len(bboxes_gt))):
                prob['true'].append(0)
                prob['score'].append(1)

        if len(bboxes_gt) == 0 and len(bboxes_pred) == 0:
            metrics_history['TN'] += 1  # Decimos que no hay nada, y no hay nada
            prob['true'].append(0)
            prob['score'].append(0)

        print("Imagen ", i, " TP: ", metrics_history['TP'], " TN: ", metrics_history['TN'], " FN: ",
              metrics_history['FN'], " FP: ", metrics_history['FP'])


save_path = './server/models/'
name = 'Yolo_Training2'
model_ = Model()
model_.load_model(f'{save_path}/{name}/weights/best.pt')
my_system = MySystem(model_)

_, _, test_data = split_train_val_test('../dataset/MuestrasMaderas/')

metrics_history = {
    'TP': 0,
    'FP': 0,
    'TN': 0,
    'FN': 0
}
prob = { # 0 no hay bbox, 1 hay bbox
    'true': [],
    'score': []
}

calc_matrix(test_data)

result = {'tp': metrics_history['TP'], 'fn': metrics_history['FN'],
          'fp': metrics_history['FP'], 'tn': metrics_history['TN'],
          'accuracy': accuracy(metrics_history['TP'], metrics_history['TN'], metrics_history['FP'], metrics_history['FN']),
          'precision': precision(metrics_history['TP'], metrics_history['FP']),
          'recall': recall(metrics_history['TP'], metrics_history['FN'])}

result['f1'] = f1(result['precision'], result['recall'])
FPR, FNR, TPR, TNR = tasas(metrics_history['TP'], metrics_history['TN'], metrics_history['FP'], metrics_history['FN'])
result['FPR'] = FPR
result['FNR'] = FNR
result['TPR'] = TPR
result['TNR'] = TNR


print(result)
print(prob)
plot_roc_curve(prob['true'], prob['score'])
plot_precision_recall_curve(prob['true'], prob['score'])