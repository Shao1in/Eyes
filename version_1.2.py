import sys
import numpy as np
import cv2


# параметры цветового фильтра
hsv_min = np.array((2, 28, 65), np.uint8)
hsv_max = np.array((26, 238, 255), np.uint8)

if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow( "result" ) # создаем главное окно
cv2.namedWindow( "settings" ) # создаем окно настроек

#cap = video.create_capture(0)
# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('index', 'settings', 0, 2, nothing)
cv2.createTrackbar('layer', 'settings', 1, 7, nothing)

crange = [0,0,0, 0,0,0]

fn = 'image_5.jpg' # путь к файлу с картинкой

while True:
    img = cv2.imread(fn)
    #flag, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    index = cv2.getTrackbarPos('index', 'settings') - 1
    layer = cv2.getTrackbarPos('layer', 'settings')
    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, h1, h1), np.uint8)
    h_max = np.array((h2, h2, h2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsv, h_min, h_max)

    # получить пороговое изображение
    #filterd_image = cv2.medianBlur(img, 7)
    #img_grey = cv2.cvtColor(filterd_image, cv2.COLOR_BGR2GRAY)
    #ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

    # ищем контуры и складируем их в переменную contours
    contours, hierarchy = cv2.findContours( thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # отображаем контуры поверх изображения
    cv2.drawContours(img, contours, index, (255, 0, 0), 2, cv2.LINE_AA, hierarchy, layer)
    cv2.imshow('result', img)  # выводим итоговое изображение в окно


    ch = cv2.waitKey(5)
    if ch == 27:
        break

#cap.release()
cv2.destroyAllWindows()