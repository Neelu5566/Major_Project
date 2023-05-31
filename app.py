
# import numpy as np
# from tensorflow.keras.models import model_from_json
# from PIL import Image,ImageDraw,ImageGrab
# from PIL import ImageTk
# import split1
# import json
# import uuid
# import cv2
# from sympy import *

# image_list = None
# uploaded_image = None
# print('Loading Model...')
# model_json = open('model/model.json', 'r')
# loaded_model_json = model_json.read()
# model_json.close()
# model = model_from_json(loaded_model_json)

# print('Loading weights...')
# model.load_weights("model/model_weights.h5")

# labels = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','+','-','x']

# class Solver:

#     def __init__(self, equation):
#         self.equation = str(equation)
#         self.leftEqu = []

#     def convertEquationIntoGeneralForm(self):

#         leftSide, rightSide = '', ''
#         equalIndx = self.equation.index('=')
#         leftSide = self.equation[0:equalIndx]
#         rightSide = self.equation[equalIndx+1:len(self.equation)]

#         if rightSide[0].isalpha() or rightSide[0].isdigit():
#             rightSide = '+' + rightSide

#         for i in range(0, len(rightSide)):
#             if rightSide[i] == '+':
#                 rightSide = rightSide[0:i] + '-' + rightSide[i+1:len(rightSide)]
#             elif rightSide[i] == '-':
#                 rightSide = rightSide[0:i] + '+' + rightSide[i+1:len(rightSide)]
#             leftSide += rightSide[i]

#         self.equation = leftSide + '=' + '0'
#         self.leftEqu = leftSide

#     def solveEquation(self):

#         self.convertEquationIntoGeneralForm()
#         sympy_eq = sympify("Eq(" + self.equation.replace("=", ",") + ")")
#         roots = solve(sympy_eq)
        
#         return roots
    
# def predictFromArray(arr):
#     #result = model.predict_classes(arr)
#     result = np.argmax(model.predict(arr), axis=-1)
#     return result                    

# def solution(image_name = "canvas.jpg"):
    
#     img = cv2.imread(image_name,cv2.IMREAD_GRAYSCALE)
#     img = ~img
#     ret,thresh = cv2.threshold(img,127, 255,cv2.THRESH_BINARY)
#     ctrs,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
#     img_data = []
#     rects = []
#     for c in cnt :
#         x, y, w, h = cv2.boundingRect(c)
#         rect = [x, y, w, h]
#         rects.append(rect)
#     final_rect = [i for i in rects]
#     for r in final_rect:
#         x,y,w,h = r[0],r[1],r[2],r[3]
#         img = thresh[y:y+h+10, x:x+w+10]
#         img = cv2.resize(img, (28, 28)) 
#         img = np.reshape(img, (1, 28, 28)) 
#         img_data.append(img)
        
#     mainEquation=[]
#     operation = ''
#     for i in range(len(img_data)):
#                 img_data[i] = np.array(img_data[i])
#                 img_data[i] = img_data[i].reshape(-1, 28, 28, 1)
#                 result=predictFromArray(img_data[i])
#                 i=result[0]
#                 mainEquation.append(labels[i])
        
#     StringEquation=""
#     for i in range(len(mainEquation)):
#             a=mainEquation[i]
#             if(a.isdigit()==False and a.isalpha()==False and i<len(mainEquation)-1):
#                 if(a==mainEquation[i+1]=='-'):
#                     StringEquation+='='
#                 else:
#                     StringEquation+=a
#             if(a.isalpha()==True):
#                 if(i>0):
#                     if(mainEquation[i-1].isdigit()):
#                         StringEquation+="*"+a
#                     else:
#                         StringEquation+=a
#                 else:
#                     StringEquation+=a
#             if(a.isdigit()==True):
#                 if(i>0):
#                     if(mainEquation[i-1].isdigit()):
#                         StringEquation+=a
#                     elif(mainEquation[i-1].isalpha()):
#                          StringEquation+="^"+a
#                     else:
#                         StringEquation+=a
#                 else:
#                     StringEquation+=a
            
#     newStr=""
#     l=list(StringEquation)   
#     for i in range(len(l)):
#             if(l[i]=="="):
#                 newStr=l[:i+1]+l[i+2:]
#     print(newStr)
#     equ=""
#     for i in newStr:
#             equ+=i
#     print("equ",equ)
#     solution=Solver(equ)
            
#     str1=''        
#     roots=solution.solveEquation()
#     st=[]
#     for i in roots:
#         i=str(i)
#         st.append(i)
       
#     str1=', '.join(st)
#     print("str",str1)
#     if image_name == 'canvas.jpg':
#         # solving(equ,str1)
#         print(image_name)
#     else:
#         return equ,str1
    
# def predict_all():
#     global image_list
    

# # Sample array of dictionaries
#     data = [    ]
    

# # Define the path to the output JSON file
#     output_file = "output.json"
#     for item in image_list:
#         equ,result = solution(item)
#         question = {}
#         question['question'] = equ
#         temp = item.split('/')
#         question['image'] = temp[1] +'/'+ temp[2]
#         question['answer'] = result
#         question['id'] = str(uuid.uuid4())
#         data.append(question)
#     with open(output_file, "w") as file:
#         json.dump(data, file, indent=4)     

from tkinter import *
from tkinter import filedialog
import numpy as np
from tensorflow.keras.models import model_from_json
from PIL import Image,ImageDraw,ImageGrab
from PIL import ImageTk
import split1
import json
import uuid
import cv2
from sympy import *

image_list = None
uploaded_image = None
print('Loading Model...')
model_json = open('model/model.json', 'r')
loaded_model_json = model_json.read()
model_json.close()
model = model_from_json(loaded_model_json)

print('Loading weights...')
model.load_weights("model/model_weights.h5")

labels = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','+','-','x']


    



class Solver:

    def __init__(self, equation):
        self.equation = str(equation)
        self.leftEqu = []

    def convertEquationIntoGeneralForm(self):

        leftSide, rightSide = '', ''
        equalIndx = self.equation.index('=')
        leftSide = self.equation[0:equalIndx]
        rightSide = self.equation[equalIndx+1:len(self.equation)]

        if rightSide[0].isalpha() or rightSide[0].isdigit():
            rightSide = '+' + rightSide

        for i in range(0, len(rightSide)):
            if rightSide[i] == '+':
                rightSide = rightSide[0:i] + '-' + rightSide[i+1:len(rightSide)]
            elif rightSide[i] == '-':
                rightSide = rightSide[0:i] + '+' + rightSide[i+1:len(rightSide)]
            leftSide += rightSide[i]

        self.equation = leftSide + '=' + '0'
        self.leftEqu = leftSide

    def solveEquation(self):

        self.convertEquationIntoGeneralForm()
        sympy_eq = sympify("Eq(" + self.equation.replace("=", ",") + ")")
        roots = solve(sympy_eq)
        
        return roots
      
    
def predictFromArray(arr):
    #result = model.predict_classes(arr)
    result = np.argmax(model.predict(arr), axis=-1)
    return result                    



def solution(image_name):
    
    img = cv2.imread(image_name,cv2.IMREAD_GRAYSCALE)
    img = ~img
    ret,thresh = cv2.threshold(img,127, 255,cv2.THRESH_BINARY)
    ctrs,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    img_data = []
    rects = []
    for c in cnt :
        x, y, w, h = cv2.boundingRect(c)
        rect = [x, y, w, h]
        rects.append(rect)
    final_rect = [i for i in rects]
    for r in final_rect:
        x,y,w,h = r[0],r[1],r[2],r[3]
        img = thresh[y:y+h+10, x:x+w+10]
        img = cv2.resize(img, (28, 28)) 
        img = np.reshape(img, (1, 28, 28)) 
        img_data.append(img)
        
    mainEquation=[]
    operation = ''
    for i in range(len(img_data)):
                img_data[i] = np.array(img_data[i])
                img_data[i] = img_data[i].reshape(-1, 28, 28, 1)
                result=predictFromArray(img_data[i])
                i=result[0]
                mainEquation.append(labels[i])
        
    StringEquation=""
    for i in range(len(mainEquation)):
            a=mainEquation[i]
            if(a.isdigit()==False and a.isalpha()==False and i<len(mainEquation)-1):
                if(a==mainEquation[i+1]=='-'):
                    StringEquation+='='
                else:
                    StringEquation+=a
            if(a.isalpha()==True):
                if(i>0):
                    if(mainEquation[i-1].isdigit()):
                        StringEquation+="*"+a
                    else:
                        StringEquation+=a
                else:
                    StringEquation+=a
            if(a.isdigit()==True):
                if(i>0):
                    if(mainEquation[i-1].isdigit()):
                        StringEquation+=a
                    elif(mainEquation[i-1].isalpha()):
                         StringEquation+="^"+a
                    else:
                        StringEquation+=a
                else:
                    StringEquation+=a
            
    newStr=""
    l=list(StringEquation)   
    for i in range(len(l)):
            if(l[i]=="="):
                newStr=l[:i+1]+l[i+2:]
    print(newStr)
    equ=""
    for i in newStr:
            equ+=i
    print("equ",equ)
    solution=Solver(equ)
            
    str1=''        
    roots=solution.solveEquation()
    st=[]
    for i in roots:
        i=str(i)
        st.append(i)
       
    str1=', '.join(st)
    print("str",str1)
    if image_name == 'canvas.jpg':
        print(image_name)
    else:
        return equ,str1
    

def predict_all(path):
    image_list = split1.divide_image(path,4,2)
    

# Sample array of dictionaries
    data = [    ]
    

# Define the path to the output JSON file
    output_file = "output.json"
    for item in image_list:
        equ,result = solution(item)
        question = {}
        question['question'] = equ
        temp = item.split('/')
        question['image'] = temp[1] +'/'+ temp[2]
        question['answer'] = result
        question['id'] = str(uuid.uuid4())
        data.append(question)
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4) 
