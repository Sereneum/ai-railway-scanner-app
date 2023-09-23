import time
import numpy
import math


class Box:
    def __init__(self, box):
        self.box = box
        self.x = box[0]
        self.y = box[1]
        self.w = box[2]
        self.h = box[3]
        self.is_collision = False


def are_rectangles_intersecting(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    # Вычисляем координаты верхнего левого и нижнего правого углов для каждого прямоугольника
    x1_right = x1 + w1
    y1_bottom = y1 + h1
    x2_right = x2 + w2
    y2_bottom = y2 + h2

    true_collision = (x1 < x2_right and x1_right > x2 and y1 < y2_bottom and y1_bottom > y2)
    if true_collision:
        return True
    else:
        return False


def are_rectangles_intersecting_v2(rect1, rect2, screen_height, screen_width):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    h1 -= 30
    w1 += 50
    if x1 + w1/2 <= screen_width:
        x1 -= 50
    else:
        x1 += 50

    x1_right = x1 + w1
    y1_bottom = y1 + h1
    x2_right = x2 + w2
    y2_bottom = y2 + h2

    # случай, при котором человек заходить за белую линию
    margin_w1 = 0.1 * w1
    margin_h1 = 0.1 * h1
    margin_w2 = 0.1 * w2
    margin_h2 = 0.1 * h2

    true_collision = (x1 < x2_right - margin_w2 and x1_right > x2 + margin_w2 and
                      y1 < y2_bottom - margin_h2 and y1_bottom > y2 + margin_h2)

    if true_collision:
        return True

    # если человек находтся в нижних крайних углах.
    if y2 + h2 >= 0.7 * screen_height and (x2 + w2 >= 0.73 * screen_width or x2 <= 0.27 * screen_width):
        return True

    #

    return False


class ObjectTemp:
    def __init__(self, color, classid):
        self.list = []
        self.color = color
        self.classid = classid


class CameraState:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        self.default_camera_name = filename
        self.default_camera_path = filepath

    def set_camera(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath


class State:
    def __init__(self, start_alarms=None, stop_alarms=None):
        self.is_dangerous = False
        self.events = []

    def save_event(self, starting_time):
        # timestamp = time.strftime('%d.%m.%Y %H:%M', time.localtime(time.time()))
        timestamp = time.time() - starting_time
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = int(timestamp % 60)
        print(f'save_event: starting_time={starting_time}, cur: {time.time()}')
        print(f'{seconds}')
        if hours:
            self.events.append(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.events.append(f"{minutes:02d}:{seconds:02d}")

    def event_len(self):
        return len(self.events)

    def check_collision(self, is_dangerous, starting_time):
        if is_dangerous and not self.is_dangerous:
            # впервые обнаружена опасность
            # print('впервые обнаружена опасность!!!')
            self.is_dangerous = True
            self.save_event(starting_time)
            return True

        if is_dangerous and self.is_dangerous:
            # уже известно об опасности
            # print('уже известно об опасности')
            return False

        if not is_dangerous and self.is_dangerous:
            # опасность миновала
            # print('опасность миновала')
            self.is_dangerous = False
            return False

        if not is_dangerous and not self.is_dangerous:
            # print('опасность не обнаружена')
            # опасность не обнаружена
            return False


class Objects:
    def __init__(self, person_color_box=(95, 222, 116)):
        self.cars = ObjectTemp((240, 160, 48), 'car')
        self.persons = ObjectTemp(person_color_box, 'person')
        self.workers = ObjectTemp((237, 144, 38), 'worker')
        self.platforms = ObjectTemp((76, 56, 156), 'platform')

    def print_persons(self):
        for p in self.persons.list:
            print(p.box, p.is_collision)

    def get_all_objects(self):
        return [self.platforms, self.persons, self.workers]

    def add_object(self, box, classid):
        if classid == 'person':
            self.persons.list.append(box)
        if classid == 'worker':
            self.workers.list.append(box)
        if classid == 'platform':
            self.platforms.list.append(box)












