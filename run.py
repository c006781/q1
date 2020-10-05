#! /usr/bin/env python
# -*- coding: utf-8 -*-



import cv2
import time
import threading
import numpy 
#from threading import Thread
#import math

from multiprocessing.pool import ThreadPool
#from app_thermometer import face_detector
#face_detector.path.append("./app_thermometer/")

from app_thermometer import face_detector, processing_recognition, teplovizor, dataBase, pirometr, valid, led_red_pin, led_green_pin, on_buzer





last_photo_recognition_people = {"personID": None, "phpto": None}
#Recognition
#face_detector = cv2.CascadeClassifier(r'C:\Users\Admin\Desktop\python\haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

hread_Bool_faces = False
hread_Bool_teplo = False
hread_Bool_face = False
#frame
x = y = w = h = 0
def faces_x_y(frame, x , y , w , h):#,fase_RGB_200_200
    x = y = w = h = 0
    #fase_RGB_200_200 = None
    if not frame is None:
        #face_detector = cv2.CascadeClassifier(r'C:\Users\Admin\Desktop\python\haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        #time.sleep(1) # пауза во время которой изменяем 
        #time.sleep(1000) # пауза во время которой изменяем 
        for (x , y , w , h) in faces:
            x , y , w , h = x , y , w , h
        #fase_RGB_200_200 = numpy.copy((frame)[y:y + w, x:x + h])##frame[0] на temp_frame_original ?
                            
    #else:
        #x = y = w = h = 0
    """
    cv2.putText(frame, "Привет, {}".format(x), (10, 410), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "Привет, {}".format(y), (10, 430), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "Привет, {}".format(w), (10, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "Привет, {}".format(h), (10, 470), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    """
    return x , y , w , h#, fase_RGB_200_200

def Id_to_face(fase_RGB_200_200, id_person):
    hread_Bool_face = False
    id_person = processing_recognition.predict_freme(fase_RGB_200_200)
    #del last_photo_recognition_people
    #last_photo_recognition_people = {"personID": self.person_id, "phpto": numpy.copy(fase_RGB_200_200)}
    hread_Bool_face = True
    return id_person

def faces_x_y(frame, x , y , w , h, hread): #,fase_RGB_200_200
    hread_Bool_faces = False 
    x = y = w = h = 0
    #fase_RGB_200_200 = None
    if not frame is None:
        #face_detector = cv2.CascadeClassifier(r'C:\Users\Admin\Desktop\python\haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        #time.sleep(1) # пауза во время которой изменяем 
        #time.sleep(1000) # пауза во время которой изменяем 
        for (x , y , w , h) in faces:
            x , y , w , h = x , y , w , h
            
        #запуск потока по поимку в бд
        if id_hread is None:
            id_hread = pool.apply_async(Id_to_face, (numpy.copy((frame)[y:y + w, x:x + h]),-1)) 

    hread_Bool_faces = True 
    return x , y , w , h, id_hread #, fase_RGB_200_200

def teplo(temp_tepl, tempPir):
    hread_Bool_teplo = False 
    temp_tepl = teplovizor.getMaxTemp()
    #if GPIO.input(18) == False:#у нас есть отжатая кнопа? 
    tempPir = pirometr.get_object_1()
    hread_Bool_teplo = True 
    return temp_tepl, tempPir





def Str_ID(id_person):
    if id_person == None:
        temp_text =  "Не распознан"
        GPIO.output(led_red_pin, GPIO.HIGH)
    elif id_person == -1:
        temp_text = "Подойдите ближе для распознования"
        GPIO.output(led_red_pin, GPIO.HIGH)
        GPIO.output(led_green_pin, GPIO.HIGH)
    else :
        #name_user = dataBase.get_people_name_by_person_id(self.person_id)
        temp_text = "Привет, {}".format(dataBase.get_people_name_by_person_id(id_person))
        GPIO.output(led_green_pin, GPIO.HIGH)
    return temp_text

def Str_teplo(temp_tepl, tempPir):
    temp_text_telo = "Ваша температура {}".format(temp_temp_tepl)  
    if (32 < temp_tempPir < 45):
        temp_text_Pir = "Ваша температура по руке {}".format(temp_tempPir)
    else : 
        temp_text_Pir = "Поднесите руку"
    flag_disease, temp_text_tepl = valid(temp_tepl, tempPir)
    return flag_disease, temp_text_telo, temp_text_Pir, temp_text_tepl



class faseThread(threading.Thread):# поток на камеру
    def __init__(self):
        super().__init__()
        self.x = self.y = self.w = self.h = 0
        self.frame_original = None
    def run(self):
        self.x , self.y , self.w , self.h = faces_x_y(self.frame_original, 0 , 0 , 0 , 0)

    
        
        
        
        
#fasehread = faseThread()
time_temp1 = time.time()
time_out = 6# таймер на определение человека
time_ = 0
frame = cap.read()
#
i = 0
time_if = False
fase_RGB_200_200 = None
color = (255, 255, 255)
pool = ThreadPool(processes=1)
temp_text_telo =""
temp_text_Pir =""
temp_text_tepl =""
flag_disease = False 
# потоки
fasehread = None
id_hread = None
#pool = Pool(processes=3)#????????????????????
while(True):
    #if not time_if:## если не время для сейва в бд, обнуляем id
    id_person =-1
    fase_RGB_200_200 = None
    temp_tepl = tempPir = 0
    flag_disease = False 

    #
    ret , frame = cap.read()
    frame = frame[:, 185:455]
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    #if not frame is None:
    #x = y = w = h = 0
    #x, y, w, h = faceshread.x , faceshread.y , faceshread.w , faceshread.h  
    ##for (x, y, w, h) in faces:
    #x = y = w = h = 0
    time_ = time.time() - time_temp1
    if not frame is None:
        """
        # может  определять лицо тут
            после отправить лицо на индификатор 
            узнать температуры
            получить ид лица?
        """
        #fasehread.frame_original = frame
        #fasehread = Thread(target=faces_x_y, args=(frame, x , y, w, h))
        print("11111111111")
        if hread_Bool_faces: #закончил ли поток faces_x_y
            if not id_hread is None and time_ < time_out-2:#???????
                id_person = id_hread.get() 
                if id_person is None:
                    id_hread = None
           
        print("22222222222222{}".format(not hread_Bool_faces)) 
        if not fasehread is None and not hread_Bool_faces:
            
            print("fasehread ") 
            fasehread = pool.apply_async(faces_x_y, (frame, x , y, w, h, id_hread))#, fase_RGB_200_200
        #x, y, w, h, id_hread  = faces_x_y(frame, x , y, w, h, id_hread)
        
        #if id_hread is None:
        #    id_hread = pool.apply_async(Id_to_face, (numpy.copy((frame)[y:y + w, x:x + h]),-1)) 

        temp_text_telo =""
        temp_text_Pir =""
        temp_text_tepl =""
        flag_disease = False 
        #fasehread.start()
        #x, y, w, h = fasehread.join()
        
        ##сюды сканы
        """
        temp_tepl = teplovizor.getMaxTemp()
        if GPIO.input(18) == False:#у нас есть отжатая кнопа? 
            tempPir = pirometr.get_object_1()
        """
        temp_tepl, tempPir = teplo(0, 0)# надо в поток?
        #x, y, w, h, id_hread  = faces_x_y(frame, x , y, w, h, id_hread)
        
        print("33333333333")
        if not fasehread is None and hread_Bool_faces:
            print("fasehread1")
            x, y, w, h, id_hread = fasehread.get() 
            fasehread = None 
        
        print("44444444444")
        #person_id = Id_to_face(numpy.copy((frame)[y:y + w, x:x + h]),0)

        #x, y, w, h, fase_RGB_200_200 = fasehread.get() 
        #if hread_Bool_faces: #закончил ли поток faces_x_y
        #####x, y, w, h, id_hread = fasehread.get() 
        #else:
        #    x = y = w = h = 0
        #x, y, w, h = faces_x_y(frame, 0 , 0 , 0 , 0)
        #fasehread.join()
    else:
        x = y = w = h = 0
    if (x==0 and y==0 and w==0 and h==0) or (150>w or 150>h ):
        time_temp1 = time.time()
        i=0
    if w >= 150 and h >= 150:# при лице больше ...
        if time_> time_out:# при истечении таймера фокусировки лица
            fase_RGB_200_200 = numpy.copy((frame)[y:y + w, x:x + h])##frame[0] на temp_frame_original ?
            
            ## поиск в бд по морде
            
            
            
            #person_id = Id_to_face(fase_RGB_200_200,-1)#processing_recognition.predict_freme(fase_RGB_200_200)
            #flag_disease, text_3 = valid(temp_tepl, tempPir)
            flag_disease, temp_text_telo, temp_text_Pir, temp_text_tepl = Str_teplo(temp_tepl, tempPir)
            
            
            
            
            i=i+1
            time_temp1 = time.time()
        #cv2.rectangle(frame, (fasehread.x, fasehread.y), (fasehread.x + fasehread.w, fasehread.y + fasehread.h), (255, 0, 0), 2)##
        
        ## вывод всякого текста, для заполнения времени
        
        #cv2.putText(frame_temp, "Ваша температура {}".format(temp_tepl), (5, 435), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)##
        #cv2.putText(frame_temp, "Ваша температура по руке {}".format(tempPir), (5, 450), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)##
        
        cv2.rectangle(frame, (0, 480), (270, 380), (255, 255, 255), -1)
        #cv2.putText(frame, temp_text_telo, (5, 435), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)##
        #cv2.putText(frame, temp_text_Pir, (5, 450), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)##
        #cv2.putText(frame, temp_text_tepl, (5, 470), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)##
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)##вывод квадратика
        #вывод таймера на морде
        if time_ < time_out-1:
            time_if = True
            cv2.putText(frame, "{}".format(int(time_out - (time_))), (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, w/23, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            #если id, то V Иначе X
            
            if not id_hread is None and id_person ==-1:#если есть поток и нет id, то спрашиваем ID
                while hread_Bool_faces:
                    time.sleep(0.05)
                id_person = id_hread.get() 
                id_hread = None
            if not id_person is None:#if i%2 == 1:#если нашли человека, то
                cv2.putText(frame, "V", (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, w/23, (0, 255, 0), 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, "X", (x, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, w/23, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, Str_ID(id_perso), (10, 410), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
                
            if time_if :#условие на 1ное обращение в течении time_out секунд(на начале последней секунды)
                time_if = False
                if id_person != -1:#if not temp_id is None:# если поток отработал, то сохраняем в бд
                    if ((32 < tempPir < 45) or (32 < temp_tepl < 45)):# and (person_id >= 0):
                        #flag_disease, text_3 = valid(temp_tepl, tempPir)
                        on_buzer(True)
                        #dataBase.push_data_log(flag_disease, last_photo_recognition_people['photo'],  person_id=last_photo_recognition_people['personID'], temp_pirom=tempPir, temp_teplovizor=temp_temp_tepl, raw_teplovizor=temp_tepl)
                        #dataBase.push_data_log(flag_disease, fase_RGB_200_200,  person_id=id_person, temp_pirom=tempPir, temp_teplovizor=temp_temp_tepl, raw_teplovizor=temp_tepl)
            
                ## сейв в бд
            
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)##
        #cv2.putText(frame, "Привет, {}".format(i), (10, 410), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    
    cv2.putText(frame, "time, {}".format(time.time() - time_temp1), (10, 390), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "Попытка, {} , {}".format(i, id_person), (10, 410), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "x: {},y: {}, w: {}, h: {}".format(x,y,w,h), (10, 430), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    """
    cv2.putText(frame, "Привет, {}".format(x), (10, 410), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "Привет, {}".format(y), (10, 430), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "Привет, {}".format(w), (10, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    cv2.putText(frame, "Привет, {}".format(h), (10, 470), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)##
    """
    """
    if not fase_RGB_200_200 is None:#if w >= 150 and h >= 150:## удалить. тест
        frame = fase_RGB_200_200
    """
    
    cv2.imshow('window', frame)
    # cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        #faceshread.mode_run = False
        cv2.destroyAllWindows()
        break

cap.release()
#cv2.destroyAllWindows()

