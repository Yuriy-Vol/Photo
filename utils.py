from PIL import Image, ImageDraw, ImageColor
import numpy as np
import math
from config import*


#______________функции______________
#загрузка изображения
def get_image(source):
    image = Image.open(source)
    width, height = image.size
    return image, width, height

#получение цветов точки
def get_color(image,x,y):
    pixel = image.getpixel((x, y))
    return pixel
        

#создание контрольного фото с помеченной точкой поиска
def draw_control_image(image,center_x,center_y):

    #прорисовка контрольной точки
    draw = ImageDraw.Draw(image)

    for x in range(center_x-10,center_x+10):
        draw.point((x, center_y), fill=ImageColor.getrgb("rgb(255, 0, 0)"))
    for y in range(center_y-10,center_y+10):
        draw.point((center_x, y), fill=ImageColor.getrgb("rgb(255, 0, 0)"))

    # Сохраняем измененное изображение
    modified_image = image.save('control_image.jpg')

#получение количества точек в которых меняется градиент от центра по оси y
def gradient_points(image, center_x, center_y,gradient_layers,grad_changing, red, green, blue):
    point_grad_down=0
    point_grad_up=0
    gradient=gradient_layers
    y=center_y
    while y!=0:
        pixel = get_color(image, center_x, y)

        if ((pixel[0]-red)**2 > grad_changing) or ((pixel[1]-green)**2 > grad_changing) or ((pixel[2]-blue)**2 > grad_changing):
            gradient-=1
        if gradient==0:
            point_grad_up=y
            break
        y-=1

    #получение количества точек в которых меняется градиент от центра к краю по оси y
    gradient=gradient_layers
    y=center_y
    while y!=center_y*2:
        pixel = get_color(image, center_x, y)
            
        if ((pixel[0]-red)**2 > grad_changing) or ((pixel[1]-green)**2 > grad_changing) or ((pixel[2]-blue)**2 > grad_changing):
            gradient-=1
        if gradient==0:
            point_grad_down=y
            break
        y+=1
    return point_grad_up, point_grad_down

#получение средних цветов точек по оси У соответственно координат крайних точек градиента
def gradient_average_point(image, dict_y, center_x, coordinates_up, coordinates_down):
    delta = coordinates_down-coordinates_up
    r=0
    g=0
    b=0
    for y in range(coordinates_up,coordinates_down):
        pixel = get_color(image, center_x, y)
        dict_y[(center_x,y)] = (pixel[0], pixel[1], pixel[2])
        r=r+pixel[0]
        g=g+pixel[1]
        b=b+pixel[2]
    return dict_y, r/delta, g/delta, b/delta

#подтверждение совпадений
def confirmation_matches(image, sovpad, center_x, y_up, delta_up, delta_down, confirm_matches, filter_sovpad_point, sovpad_podt_list, sovpad_podt_dict, dict_y):
        podtver=0        

        for key in sovpad:
            y_center=y_up
            for y in range(key[1]-delta_up,key[1]+delta_down):
                pixel = get_color(image, key[0], y)
                
                if ((pixel[0]-dict_y[(center_x,y_center)][0])**2<confirm_matches) and ((pixel[1]-dict_y[(center_x,y_center)][1])**2<confirm_matches) and ((pixel[2]-dict_y[(center_x,y_center)][2])**2<confirm_matches):
                    podtver+=1
                
                y_center+=1
        
            if podtver>=(delta_up+delta_down)*filter_sovpad_point:
                sovpad_podt_list.append(key)
                sovpad_podt_dict[(key)]=podtver

            podtver=0


#фильтрация конечных точек по близости значений к контрольной точки
def filtering_matches(sovpad_podt_dict, sovpad_podt, filter_sovpad):
    big_key=0
    big=0
    for key in sovpad_podt_dict:
        if sovpad_podt_dict[key]>big:
            big_key=key
            big=sovpad_podt_dict[key]

    for key,value in sovpad_podt_dict.items():
        if value>=big*filter_sovpad: 
            sovpad_podt.append(key)

#Создание модифицированного фото с прорисованным результатом 
def draw_modif_image(image,sovpad_podt):
    #прорисовка точек совпадений
    draw = ImageDraw.Draw(image)

    for x_y in sovpad_podt:
            
        for y in range(x_y[1]-10,x_y[1]+10):
            draw.point((x_y[0], y), fill=ImageColor.getrgb("rgb(255, 0, 0)"))
        for x in range(x_y[0]-10,x_y[0]+10):
            draw.point((x, x_y[1]), fill=ImageColor.getrgb("rgb(255, 0, 0)"))

    # Сохраняем измененное изображение
    modified_image = image.save('modified_image.jpg')