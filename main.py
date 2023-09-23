import cv2 as cv
import time
import numpy as np
from object_classes import Objects, Box, are_rectangles_intersecting, State, CameraState, are_rectangles_intersecting_v2
from video_logging import logonefile, logfilestart
import eel
import base64
import os
import tkinter as tk
from tkinter import filedialog
import json


with open("settings.json", 'r') as json_file:
    settings = json.load(json_file)


root = tk.Tk()
root.title('Выбор файла')
root.geometry('0x0-1-1')


# Функция для скрытия окна
def hide_window():
    root.withdraw()


# Функция для показа окна
def show_window():
    root.deiconify()


hide_window()

eel.init('web', allowed_extensions=['.js', '.html', '.css'])
logfilestart()  # начало логирования

camera_coordinates = (56, 75)
KNOWN_DISTANCE = 5  # metres
KNOWN_WIDTH = 1  # metres

Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]


rzd_names = 'rzd.names'
rzd_final_weights = 'rzd_final.weights'
rzd_cfg = 'rzd.cfg'


class_name = []
with open(rzd_names, 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]
net = cv.dnn.readNet(rzd_final_weights, rzd_cfg)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)


model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]


# cap = cv.VideoCapture('1578400498_.jpg')
# cap = cv.VideoCapture('elon1.mp4')
# Get the names of the output layers
output_layers = net.getUnconnectedOutLayersNames()

# Set the threshold values for confidence and non-maximum suppression
Conf_threshold = 0.5
NMS_threshold = 0.4


# Set the class names for YOLOv4
class_name = []
with open(rzd_names, "r") as f:
    class_name = [cname.strip() for cname in f.readlines()]


def publish_event():
    pass


# cap = cv.VideoCapture('elon1.mp4')

# start_alarms()


def video_processing(filename='', filepath='', update_image=None):
    print(f'video_processing for {filename}, {filepath}' + '\n' + '...')
    cap = cv.VideoCapture(filepath)
    state = State()
    starting_time = time.time()
    frame_counter = 0
    while True:
        ret, frame = cap.read()
        frame_counter += 1
        if not ret:
            break
        height, width, channels = frame.shape

        classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
        p_color = (settings["box-color"]['r'], settings["box-color"]['g'], settings["box-color"]['b'])
        objects = Objects(
            p_color
        )

        for (classid, score, box) in zip(classes, scores, boxes):
            objects.add_object(Box(box), class_name[classid])

        # конец обработки объектов

        for platform in objects.platforms.list:
            for person in objects.persons.list:
                if not are_rectangles_intersecting_v2(platform.box, person.box, height, width):
                    pass
                    # print('нет пересечения (are_rectangles_intersecting_v2)')
                    # is_dangerous = True
                else:
                    person.is_collision = True
                    # print('есть пересечение (are_rectangles_intersecting_v2)')

        # пост-отрисовка
        is_dangerous = False
        for object_type in objects.get_all_objects():
            for i in object_type.list:
                if object_type.classid == 'person' and not i.is_collision:
                    is_dangerous = True
                    dangerous_color = (0, 0, 255)
                    label = "%s: dangerous!!!" % (object_type.classid)
                    cv.putText(frame, label, (i.box[0], i.box[1] - 10),
                               cv.FONT_HERSHEY_COMPLEX, settings['font-scale'], dangerous_color, 1)
                    cv.rectangle(frame, i.box, (0, 0, 255), 2)
                else:
                    label = "%s" % (object_type.classid)
                    cv.putText(frame, label, (i.box[0], i.box[1] - 10),
                               cv.FONT_HERSHEY_COMPLEX, settings['font-scale'], object_type.color, 1)
                    cv.rectangle(frame, i.box, object_type.color, 1)

        is_alert = state.check_collision(is_dangerous, starting_time)
        # if is_alert:
        #     start_alarms()

        ending_time = time.time() - starting_time
        fps = frame_counter/ending_time
        cv.putText(frame, f'FPS: {fps}', (20, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
        # cv.imshow('frame', frame)
        update_image(frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            exit(0)

    # логируются данные
    logonefile(filename, state.events, state.event_len())
    # logonefile(filename, state.events, state.event_len())

    cap.release()
    cv.destroyAllWindows()


# тут будет запуст фронта, логирование и контроль запуска.
def update_image(frame):
    _, buffer = cv.imencode('.jpg', frame, [int(cv.IMWRITE_JPEG_QUALITY), 90, int(cv.IMWRITE_JPEG_PROGRESSIVE), 1])
    image_data = base64.b64encode(buffer).decode('utf-8')

    # Передача изображения в JS через Eel
    eel.updateImage(image_data)()


const = 'rzd_tiny_ver_2.mp4'
# if os.path.isfile(const):
#     const = None
camera_state = CameraState(const, const)


def video_flow(videos):
    current_directory = os.getcwd()
    for i in range(len(videos)):
        filepath = os.path.relpath(videos[i], current_directory)
        filename = os.path.basename(filepath)
        print(f'current-video: {filename}, {filepath}')
        eel.preparing_for_display()
        video_processing(
            filename=filename,
            filepath=filepath,
            update_image=update_image
        )

    print('конец обработки')
    eel.navigate_main()


@eel.expose
def get_settings():
    return settings


@eel.expose
def open_file(filepath):
    print(filepath)


@eel.expose
def tk_file_dialog():
    print('run tk_file_dialog')
    show_window()
    dialog_filepath = filedialog.askopenfilename()
    if dialog_filepath:
        hide_window()
        try:
            filepath = os.path.relpath(dialog_filepath, os.getcwd())
            filename = os.path.basename(filepath)
            print(filepath, filename)
            camera_state.set_camera(filename, filepath)
            eel.preparing_for_display()
            video_processing(
                filename=filename,
                filepath=filepath,
                update_image=update_image
            )
        except:
            return
    else:
        print("Файл не выбран")
        hide_window()


def find_video_in_folder(folder_path):
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        mp4_files = [f for f in files if f.endswith('.mp4')]
        if mp4_files:
            full_paths = []

            for mp4_file in mp4_files:
                full_path = os.path.join(folder_path, mp4_file)
                full_paths.append(full_path)


            video_flow(full_paths)
        else:
            print("В выбранной папке нет MP4 файлов.")


@eel.expose
def tk_folder_dialog():
    print('run tk_folder_dialog')
    show_window()
    dialog_folder_path = filedialog.askdirectory()
    if dialog_folder_path:
        hide_window()
        dialog_folder_path = dialog_folder_path.replace('/', os.sep).replace('\\', os.sep)
        find_video_in_folder(dialog_folder_path)
    else:
        hide_window()


@eel.expose
def open_camera():
    video_processing(
        filename=camera_state.default_camera_name,
        filepath=camera_state.default_camera_path,
        update_image=update_image
    )
    eel.navigate_main()


@eel.expose
def open_last_camera():
    video_processing(
        filename=camera_state.filename,
        filepath=camera_state.filepath,
        update_image=update_image
    )
    eel.navigate_main()


@eel.expose
def second_screen():
    print('second_screen')


eel.start('index.html', size=(1920, 1080))
