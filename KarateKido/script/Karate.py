
from ultralytics import YOLO 
from PIL import ImageGrab
from time import sleep 
import pyautogui 
import numpy as np

'''
    JUST A  HEADS UP, THERE IS ZERO ARTIFICIAL INTELIGENCE IN WHAT I WROTE       o_-
'''

'''
MY SCREEN SIZE IS 1366 x 768
MAKE SURE YOU OPEN CHROME IN FULL MODE AND NOT M 
'''

pt =  "../model/sweat.pt"
model = YOLO(pt)


print("Starting now")

up = []
obs = []
ice=0
times=0

obs_d =  dict()


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


    def get_point(self,arg=""):
        if arg.lower() == 'mb' or arg.lower() ==  'bm':
            return dict( mc=self.middle_central, bc=self.bottom_central)
        elif arg.lower() == 'tb' or arg.lower() == 'bt':
            return dict(tc=self.top_central, bc=self.bottom_central)
        elif arg.lower() == "tm" or arg.lower() == 'mt':
            return dict(tc=self.top_central, mc=self.middle_central)
        elif arg.lower() == "t":
            return dict(tc=self.top_central)
        elif arg.lower() == "m":
            return dict(mc=self.middle_central)
        elif arg.lower() == "b":
            return dict(bc=self.bottom_central)
        else:
            return dict(tc=self.top_central, mc=self.middle_central, bc=self.bottom_central)


    def lor(self,poll):
        if self.xCenter < poll.xCenter:
            return 0
        else:
            return 1
    

    def press(self,poll):
        if self.lor(poll) :
            pyautogui.press("right")
        else:
            pyautogui.press("left")


    


    

# button presser
def press (char,poll, obp):
    global threshold

    # if character is at the left
    # char.lor takes an argument  of class positin and this runs the calculatin of the middle poll and gets the 
    # current location of the character if right or left

    # this checks first if the character is at the left side and the obstacle is also at the left side
    # once character position has been solved it checks for object position . 
    # once object position has been gotten it calculates the gap difference on the y-axis, if its below the threshold then an action would be taken

    if char.lor(poll) ==0:
        if obp.lor(poll)==0:
            if (char.y - obp.y1 ) <= threshold:
                pyautogui.press("right")
            else:
                char.press(poll)

            
        elif obp.lor(poll) ==1:
            if (char.y - obp.y1 ) <= threshold:
                char.press(poll)



    elif char.lor(poll)==1:
        if obp.lor(poll)==1:
            if (char.y - obp.y1) <threshold:
                pyautogui.press('left')
            else:
                char.press(poll)
        elif obp.lor(poll) ==0:
            if (char.y- obp.y1) <=threshold:
                char.press(poll)



    


    

def run():

    
    global up ,times,ice,threshold,char,obp,poll, cont_click
    cont_click=False ,
    threshold=0
    obs=[]
    char = None

    while True:

        # cropped the image gotten  so as to focus on the important aspect that matters in the game
        img =  np.array(ImageGrab.grab(bbox=(0,500,1350,739)))
        
        im =  img/255.0
        results = model.predict(source=img)
        # sleep(.3)

        print(results[0].boxes.numpy())
        print("*"*100)
        for result in results :
            for  idx,clss in enumerate(result.boxes.cls):
                clss =  int(clss)
                if clss ==3:
                    char = object_position(result.boxes.xyxy.numpy()[idx])
                    
                    # calculate the height of the box and make inference as to which character has is currently picked
                elif clss ==2:
                    poll =  object_position(result.boxes.xyxy.numpy()[idx])

                # elif clss==6:
                #     up =  object_position(result.boxes.xyxy.numpy()[idx])
                
                # elif clss==1 or clss==4 or clss==8 or clss==9 :
                #     times =  object_position(result.boxes.xyxy.numpy()[idx])
                # elif clss==6 or clss==4:
                #     ice =  object_position(result.boxes.xyxy.numpy()[idx])

                elif clss==0:
                    obs.append(result.boxes.xyxy.numpy()[idx])

                # else:
                #     pass

       
            if char:

                if obs:
                    obs = sorted(obs, key=lambda x:x[3], reverse=True)
                    cont_click=False
                    print("click cont_click is false")
                else:
                    cont_click= True
                    print("click cont_click is True")


                        
                if cont_click:
                    char.press(poll)
                   
                    print("pressed by char object")
                    
                else:

                    for ob in obs:
                        

                    
                        obp = object_position(ob)

                        if char.Height < 70:
                            # threshold  : once the obstacle crosses this line the character would take action
                            threshold=70
                            press(char,poll,obp)

                            print("Shortest master")
                                    
                                        
                        elif char.Height >=78 and char.Height<=91:
                            threshold=30
                            press(char,poll,obp)
                            print("Medium master ")

                                    
                        else:
                            threshold=22
                            press(char,poll,obp)
                            print("grandmaster")
            else:
                print("Char not found")              

            print()
            cont_click =  False
            char =  None
            obs.clear()
            

if __name__ == "__main__":
    run()
