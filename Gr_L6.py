import numpy as np
import cv2

image = cv2.imread('photo.jpg')
image_original = image.copy()


def _noize_point():
    """Шум точками"""
    global image
    image = image.astype(np.int)
    image = image * (np.random.random(image.shape) + 0.9)
    image[np.where(image > 255)] = 255
    image[np.where(image < 0)] = 0
    image = image.astype(np.uint8)


def _noize_line():
    """Шум линиями"""
    global image

    for i in range(10):
        cv2.line(image, (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])),
             (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])), (0, 128, 0))


def _noize_circle():
    """Шум кругами"""
    global image

    for i in range(10):
        cv2.circle(image, (np.random.randint(0, image.shape[1]), np.random.randint(0, image.shape[0])),
               np.random.randint(0, 20), (128, 128, 128))


def _method_gauss():
    """Шумоподавление - Гаусс"""
    global image
    image = cv2.GaussianBlur(image, (3, 3), 1)


def _method_median():
    """Шумоподавление - Медианный"""
    global image
    image = cv2.medianBlur(image, 3)


def _blur_method():
    """Шумоподавление - Размытие"""
    global image
    image = cv2.blur(image, (3, 3))


def _sharpness():
    """Повышение резкости"""
    global image
    k = 2
    kernel = np.ones((3, 3), np.float32) * (-k / 8)
    kernel[1, 1] = k + 1
    image = cv2.filter2D(image, -1, kernel)
    image = image.astype(np.uint8)


def _stamping():
    """Тиснение"""
    global image
    kernel = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, -1, 0], [0, 0, 0, 0, -1]])

    image = cv2.filter2D(image, -1, kernel)
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            image[x, y] = np.max(image[x, y])

    image += 50
    image[np.where(image > 255)] = 255
    image[np.where(image < 0)] = 0
    image = image.astype(np.uint8)


while True:
    key = cv2.waitKey(1)

    # останова программы - ESC
    if key == 27:
        break

    # Вызов точечного шума 'p'
    if key == ord('p'):
        _noize_point()

    # Вызов шума линиями 'l'
    if key == ord('l'):
        _noize_line()

    # Вызов шума кружками 'c'
    if key == ord('c'):
        _noize_circle()

    # Вызов медиан 'm'
    if key == ord('m'):
        _method_median()

    # Вызов Гаусса 'g'
    if key == ord('g'):
        _method_gauss()

    # Размытие равномерное 'b'
    if key == ord('b'):
        _blur_method()

    # Оригинальное изображение
    if key == ord('o'):
        image = image_original.copy()

    # Повышение резкости
    if key == ord('r'):
        _sharpness()

    # Тиснение
    if key == ord('t'):
        _stamping()

    cv2.imshow('image', image)
