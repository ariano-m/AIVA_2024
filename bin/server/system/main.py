from flask import Flask, request, Response, jsonify, make_response
import mysql.connector as cpy
from system import MySystem
from waitress import serve
from image import MyImage
from model import Model
import numpy as np
import datetime
import base64
import cv2

# variable for Flask server
app = Flask(__name__)


config = {
    "host": "mysql-master", #mysql-master",  # name service docker
    "port": 3306,
    "user": "root",
    "password": "1234",
    "use_pure": True,
    "database": "MY_IMAGE"
}

my_system = None


def load_system() -> MySystem:
    """
        Loads the system with a pre-trained model for image processing.
    :return: An instance of MySystem initialized with the pre-trained model.
    """
    save_path = '../models/'
    name = 'Yolo_Training2'
    model_ = Model()
    model_.load_model(f'{save_path}/{name}/weights/best.pt')
    return MySystem(model_)


@app.route('/image', methods=['POST'])
def process_petition() -> Response:
    """
        Processes an image received via POST request, performs image processing, and stores relevant information in the database.
    :return: A JSON response indicating the successful receipt and processing of the image.
    """

    image_bytes = base64.b64decode(request.data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    image_figures = main(image)

    _, buffer = cv2.imencode('.png', image_figures)
    base64_image_figures = base64.b64encode(buffer).decode('utf-8')

    response = make_response(base64_image_figures)
    response.headers.set('Content-Type', 'application/octet-stream')
    return response


def add_row_db(image: MyImage):
    """
        Adds information about the processed image to the MySQL database.
    :param image: An instance of MyImage containing information about the processed image.
    :return: None
    """
    #docker run --name mysql -e MYSQL_ROOT_PASSWORD=1234 -d arm64v8/mysql:latest
    #docker exec -it mysql bash -l
    #mysql -p

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
    """
        Main function for processing the received image, detecting damages, and storing relevant information in the database.
    :param img: The image to be processed.
    :return: None
    """
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
    return image


if __name__ == "__main__":
    my_system = load_system()
    serve(app, host='0.0.0.0', port=5005)
