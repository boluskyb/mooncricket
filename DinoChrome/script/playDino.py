from ultralytics import YOLO 
from PIL import ImageGrab
from time import sleep 
import pyautogui 
import numpy as np

class object_position:

    def __init__(self, array_val):
        self.x =  int(array_val[0])
        self.y =  int(array_val[1])
        self.x1 = int(array_val[2])
        self.y1 = int(array_val[3])
        self.Height =  self.y1 - self.y
        self.xCenter =  int(self.x/2) +int(self.x1/2)
        self.yCenter =  (self.y+self.y1)//2


        self.top_central = (self.xCenter,self.y)
        self.middle_central=  (self.xCenter,self.yCenter)
        self.bottom_central = (self.xCenter,self.y1)


        self.rightCenter =  (self.x1, self.yCenter)
        self.leftCenter =  (self.x, self.yCenter)
    

# image =  'test2.png'

model = YOLO('dino.pt')

# results = model.predict(image)



while True:
    img =  np.array(ImageGrab.grab(bbox=(0,0,1350,739)))
        
    
    results = model.predict(source=img)
    obs =[]
    raptor=''
    char=''
    for result in results:
        
        for idx,clss in enumerate(result.boxes.cls):
            clss= int(clss)
            if clss ==0:
                char =  object_position(result.boxes.xyxy.numpy()[idx])

            elif clss ==1:
                raptor =  object_position(result.boxes.xyxy.numpy()[idx])

            else:
                obs.append(result.boxes.xyxy.numpy()[idx])



    
        if char:
            
            if obs:

                if len(obs)> 1:
                    obs =  sorted(obs,key=lambda x:x[0], reverse=False)
                    obs =  object_position(obs[0])
                    if ( obs.x - char.x1) < 105 :
                        pyautogui.press("space")
                        print("jump")

                else:
                    obs =  object_position(obs[0])
                    if ( obs.x - char.x1) < 105 :
                        pyautogui.press("space")
                        print("jump!!")
            elif raptor:
                print("raptor found")
                if ( raptor.x - char.x1) < 115 :
                        pyautogui.press("space")
                        
                        print("jump")

                else:
                    pass
                 
            else:
                print("obstacle not found")
        else:
            print("Character not found")
        

        