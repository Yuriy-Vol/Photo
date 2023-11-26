from PIL import Image, ImageDraw, ImageColor
import numpy as np
import math
import time
from config import*
from utils import*


#______________старт______________
start_time = time.time()

job=False
cycle=1

while job==False:

    try:

        image_param = get_image(source_control)

        center_x = image_param[1] // 2
        center_y = image_param[2] // 2
        point_grad_up=0
        point_grad_down=0
        dict_y={}
        dict_x={}
        dict_r={}
        dict_g={}
        dict_b={}
        r=0
        g=0
        b=0
        start=0
        control_point_diag_up=[]
        control_point_diag_down=[]

        draw_control_image(image_param[0],center_x,center_y)

        image_param = get_image(source_control)

        #определение цветов центральной точки
        pixel = get_color(image_param[0], center_x, center_y)
        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]

        start=1
        while start==1:
            delta = gradient_points(image_param[0], center_x, center_y, gradient_layers, grad_changing, red, green, blue)

            delta_up=(center_y-delta[0])
            delta_down=(delta[1]-center_y)
            print("точек по У вверх и вниз от центра - ", gradient_layers, delta_up,delta_down)
            if (delta[1]-delta[0])>delta_y_point:
                start=0
            else:
                gradient_layers+=1
                grad_changing+=grad_change_step

        #получение средних цветов точек по оси У
        rgb_point=gradient_average_point(image_param[0], dict_y, center_x, delta[0], delta[1])
        
        dict_r[(center_x,center_y)]=rgb_point[1]
        dict_g[(center_x,center_y)]=rgb_point[2]
        dict_b[(center_x,center_y)]=rgb_point[3]

        image_param = get_image(source)

        #поиск совпадений по среднему цвету
        sovpad={}
        r=0
        g=0
        b=0
        delta_y=delta[1]-delta[0]

        for x in range(50,int(image_param[1] / 2) + 20):

            for y in range(int(image_param[2]/2)-20,int(image_param[2])-delta_down):
                pixel = get_color(image_param[0], x, y)

                if (pixel[0]-red)**2<dif_сontrol_current_point  and (pixel[1]-green)**2<dif_сontrol_current_point and (pixel[2]-blue)**2<dif_сontrol_current_point:                   
                    sovpad[(x,y-1)]=int(r/delta_y),int(g/delta_y),int(b/delta_y)

                    r=0
                    g=0
                    b=0

                    rgb_point_contin=gradient_average_point(image_param[0], dict_y, x, delta[0], delta[1])
                    r=rgb_point_contin[1]
                    g=rgb_point_contin[2]
                    b=rgb_point_contin[3]

        print("количество первичных совпадений - ", len(sovpad))

        #подтверждение совпадений
        sovpad_podt=[]
        sovpad_podt_list=[]
        sovpad_podt_dict={}
        confirmation_matches(image_param[0], sovpad, center_x, delta[0], delta_up, delta_down, confirm_matches, filter_sovpad_point, sovpad_podt_list, sovpad_podt_dict, dict_y)

        #фильтрация конечных точек по близости значений к контрольной точки
        filtering_matches(sovpad_podt_dict, sovpad_podt, filter_sovpad)

        print(sovpad_podt_dict)
        print("список подтвержденных совпадений - ", sovpad_podt)
        print("сдвиг по Х - ", center_x-sovpad_podt[0][0],"    сдвиг по У - ", center_y-sovpad_podt[0][1])


        #прорисовка точек совпадений
        draw_modif_image(image_param[0],sovpad_podt)

        job=True
    except Exception as e:
        print(e)
        filter_sovpad_point-=0.01*cycle
        confirm_matches+=5*cycle
        dif_сontrol_current_point+=cycle
        print("фильтр - ", filter_sovpad_point, "confirm_matches - ", confirm_matches)
        cycle+=1

print("время работы программы - ", time.time() - start_time)