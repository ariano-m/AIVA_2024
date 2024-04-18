from flask import Flask, request, Response, jsonify, make_response
import mysql.connector as cpy
from system import MySystem
from waitress import serve
from image import MyImage
from model import Model
import numpy as np
import datetime
import base64

# variable for Flask server
app = Flask(__name__)


config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "admin",
    "password": "1234",
    "use_pure": True,
    "database": "MY_IMAGE"
}

my_system = None


def load_system() -> MySystem:
    save_path = '../models/'
    name = 'Yolo_Training2'
    model_ = Model()
    model_.load_model(f'{save_path}/{name}/weights/best.pt')
    return MySystem(model_)


@app.route('/image', methods=['POST'])
def process_petition() -> Response:
    image = base64.b64decode(request.data)
    image = np.frombuffer(image, dtype=np.uint8)
    image = image.reshape(442, 488, 3).astype(np.uint8)
    print("SHAPE", image.shape)

    main(image)

    response = {'message': 'image received. size={}x{}'.format(image.shape[1], image.shape[0])}
    response = make_response(jsonify(response))
    response.headers["Content-Type"] = "application/json"
    return response


def add_row_db(image: MyImage):
    """
        #docker run --name mysql -e MYSQL_ROOT_PASSWORD=1234 -d arm64v8/mysql:latest
        #docker exec -it mysql bash -l
        #mysql -p
    :param image:
    :return:
    """

    with cpy.connect(**config) as cnx:
        with cnx.cursor() as cursor:
            query = "SELECT * FROM USER WHERE USER = %s AND PASSWORD = %s"
            values = (image.user, '1234')
            cursor.execute(query, values)
            res = cursor.fetchone()
            if res is None or res == "":
                print("USER NOT FOUND")
                return

            query_1 = 'INSERT INTO IMAGE (USER, IMAGE, DATE) VALUES (%s, %s, %s)'
            values_1 = (image.user, image.original_image.dumps(), image.datetime)
            cursor.execute(query_1, values_1)


            query_2 = ('INSERT INTO BBOX (USER, X1, Y1, X2, Y2, MARGIN, DATE)'
                       'VALUES (%s, %s, %s, %s, %s, %s, %s)')
            for i in image.bbox_imperfections:
                values_2 = (image.user, i[0], i[1], i[2], i[3], False, image.datetime)
                cursor.execute(query_2, values_2)

            x1, y1, x2, y2 = image.bbox_margins
            values_3 = (image.user, x1, y1, x2, y2, True, image.datetime)
            cursor.execute(query_2, values_3)

            cnx.commit()


def main(img):
    img_bin = my_system.preprocess_image(img)
    erode_img = my_system.morphology(img_bin)
    bbox_board = my_system.get_contours(erode_img)

    bbox_defects = my_system.detect_damage(img)
    bbox_figures = my_system.place_figures(img, bbox_defects, bbox_board)
    image = my_system.color_figures(img, bbox_figures)

    my_image = MyImage(image)
    my_image.user = "user1234"
    my_image.original_image = img
    my_image.bbox_imperfections = bbox_defects
    my_image.bbox_margins = bbox_board
    my_image.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_row_db(my_image)


if __name__ == "__main__":
    my_system = load_system()
    serve(app, host='0.0.0.0', port=5005)
