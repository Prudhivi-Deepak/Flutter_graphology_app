from flask import Flask,jsonify,request,session
from flask_mysqldb import MySQL
import os
import cv2
import urllib.request
import time
import numpy as np
import pickle
# hello-world-cba35.appspot.com/
from firebase_admin import credentials, initialize_app, storage
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt1
import os


app = Flask(__name__) #intance of our flask application 
app.config['UPLOAD_FOLDER']=os.path.dirname(__file__)+'/static/img'

app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'RIcvQcz1ZB'
app.config['MYSQL_PASSWORD'] = '98U4LQX9u7'
app.config['MYSQL_DB'] = 'RIcvQcz1ZB'
mysql = MySQL(app)

cred = credentials.Certificate("hello-world-cba35-f184eebe9189.json")
initialize_app(cred, {'storageBucket': 'hello-world-cba35.appspot.com'})

#Route '/' to facilitate get request from our flutter app
@app.route('/',methods = ['GET'])
def index():
    return jsonify({'greetings' : 'Hi! this is python'}) #returning key-value pair in json format

@app.route('/upload/<calledurl>/<ID>',methods = ['GET'])
def upload(calledurl,ID):
    result=[]
    info=[]
    res1=[]
    if request.method=='GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM upload WHERE name = %s and id= %s", (str(calledurl),str(ID)))
        responseout = cursor.fetchall()
        # print(res)
        list1=[]
        for i in range(len(responseout)):
            list1.append(responseout[i][-1])
        print(responseout[-1][-1])
        print(responseout[-1][-2])

        resp = urllib.request.urlopen(responseout[-1][-1])
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        print(image)

        # 1.Baseline line angle

        baseline_angles_list=[]
        MYANGLE=0
        count=0 
        # image1 = cv2.imread('./data_subset/'+str(filenames[0]),1) 
        image1 = cv2.bilateralFilter(image,9,50,50)
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(image1,120,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((5,100), np.uint8)
        image1 = cv2.dilate(thresh,kernel,iterations=1)
        ctrs,hier = cv2.findContours(image1,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(image1,ctrs,-1,(127,127,0),2)
#         cv2.waitKey(0)
        for j, ctr in enumerate(ctrs):    
            count=count+1
            x, y, w, h = cv2.boundingRect(ctr)    
            rect = cv2.minAreaRect(ctr)
            ang=rect[2]
            if(h>w):
                if(ang<0):
                    ang = 90-ang
            else:
                if(ang<0):
                    ang = 180-ang
            MYANGLE=MYANGLE+ang
        #     box = cv2.boxPoints(rect)
        #     box = np.int0(box)
        #     cv2.drawContours(image1,[box],0,(0,0,255),15)
        #     cv2.rectangle(image1,(x,y),(x+w,y+h),(255,0,0),10)
        baseline_angles_list.append((MYANGLE/count))
    #     print(baseline_angles_list,len(baseline_angles_list))
        


        # 2.Top margin
        top_margin=[]
        # image2 = cv2.imread('./data_subset/a01-000u-s00-01.png',1)  
        image2 = cv2.bilateralFilter(image,2,30,30)
        image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        ret,thresh1 = cv2.threshold(image2,100,255,cv2.THRESH_BINARY_INV)
        (h, w) = image2.shape[:2]
        count1=0
        for j in range(h//2):
            row1=0
            row = thresh1[j:j+1, 0:w]
            if(row[0].any()==0):
                count1=count1+1
        top_margin.append(count1)
    #     print(top_margin,len(top_margin))
        

        # 3.word spacing
        word_spacing_ratio=[]
        written_spacing_ratio=[]

        # image3 = cv2.imread('./data_subset/a01-000u-s00-01.png',1)
        image3 = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        space=0
        for j in range(image3.shape[0]):
            row = image3[j:j+1, 0:image3.shape[1]]
            if(np.sum(row)==3*255*image3.shape[1]):
                space+=1
        word_spacing_ratio.append(float(space/image3.shape[0]))
        written_spacing_ratio.append((image3.shape[0]-space)/image3.shape[0])
    #     print(len(word_spacing_ratio),len(written_spacing_ratio))

        # 4.Pen pressure

        pen_pressure=[]
        image4 = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
        h,w  = image4.shape[:2] 
        inverted = image4.copy()
        for x in range(h):
            for y in range(w):
                inverted[x][y] = (255-image4[x][y])

        filtered = cv2.bilateralFilter(inverted,15,75,75)
        ret , thresh4 = cv2.threshold(filtered,150,255,cv2.THRESH_TOZERO)
    #     if(j%50==0):
    #         print(j)
        total_intensity = 0 
        pixel_count = 0 
        for x in range(h):
            for y in range(w):
                if(thresh4[x][y] > 0):
                    total_intensity += thresh4[x][y]
                    pixel_count += 1 
        if(pixel_count==0):
            pixel_count=1
        average_intensity = float(total_intensity)/pixel_count
        pen_pressure.append(average_intensity)
    #     print(len(pen_pressure))


        # 5.Slant letter


        slant_letters_angle=[]

        # image5 = cv2.imread('./data_subset/a01-000u-s00-01.png',1)
        image5 = cv2.bilateralFilter(image,9,50,50)
        image5 = cv2.cvtColor(image5 , cv2.COLOR_BGR2GRAY)
        h,w  = image5.shape[:2] 
        i = image5[:h,w//2-150:w//2+150]
        ret,thresh4 = cv2.threshold(i,120,255,cv2.THRESH_BINARY_INV)

        kernel = np.ones((5,100), np.uint8)
        image5 = cv2.dilate(thresh4,kernel,iterations=1)
        ctrs,hier = cv2.findContours(image5,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(i,ctrs,-1,(127,127,0),2)

        count2=0
        MYANGLE2=0
        for j, ctr in enumerate(ctrs):    
            count=count+1
            x, y, w, h = cv2.boundingRect(ctr)    
            rect = cv2.minAreaRect(ctr)
            ang2=rect[2]
            if(h>w):
                if(ang2<0):
                    ang2 = 90-ang2
            else:
                if(ang2<0):
                    ang2 = 180-ang2
            MYANGLE2=MYANGLE2+ang2
        #     box = cv2.boxPoints(rect)
        #     box = np.int0(box)
        #     cv2.drawContours(i,[box],0,(0,0,255),15)
        #     cv2.rectangle(i,(x,y),(x+w,y+h),(255,0,0),10)
        if(count2==0):
            count2=1
        slant_letters_angle.append((MYANGLE2/count2))
    #     print(len(slant_letters_angle))


        # 6.Letter Size
        Letter_size_height=[]
        Letter_size_width=[]
        h,w = image.shape[:2]
        image7 = image[:h,w//2-150:w//2+150]
        image7 = cv2.bilateralFilter(image7,9,50,50)
        image7 = cv2.cvtColor(image7 , cv2.COLOR_BGR2GRAY)
        
        ret,thresh7 = cv2.threshold(image7,120,255,cv2.THRESH_BINARY_INV)
        
        kernel = np.ones((5,100), np.uint8)
        image7 = cv2.dilate(thresh7,kernel,iterations=1)
        ctrs,hier = cv2.findContours(image7,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.drawContours(image7,ctrs,-1,(127,127,0),2)
        count=0
        height=0
        width=0
        for j, ctr in enumerate(ctrs):    
            count+=1
            x, y, w, h = cv2.boundingRect(ctr) 
            height=h-y
            width=w-x
        if(count==0):
            count=1
        if(height<0):
            height=-height
        if(width<0):
            width=-width
        Letter_size_height.append(height/count)
        Letter_size_width.append(width/count)

        # features = pd.read_csv("Features1.csv")
        features =["Emotion","mental","modesty","discipline","c2c","social"]
        x_test1 =[baseline_angles_list[0],top_margin[0],word_spacing_ratio[0],written_spacing_ratio[0],pen_pressure[0],slant_letters_angle[0],Letter_size_height[0],Letter_size_width[0]]
    #     print(x_test1)
        res=[]
        for y in features:
            name1="model"+str(y)
            with open(name1,"rb") as f:
                model=pickle.load(f)
                res.append(model.predict([x_test1])[0])
        print("res--------------",res)
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO sessions1 VALUES (%s, %s , %s, %s)', (str(ID), responseout[-1][1],responseout[-1][3],responseout[-1][4]))
        mysql.connection.commit()
        
    return jsonify({"output":{"see":str(res)}})


@app.route('/predict/<list1>/<id1>',methods = ['GET'])
def predict1(list1,id1):
    info=[]
    res1=[]
    if request.method=='GET':
        res = list(map(int,list(list1[1:-1].split(','))))
        print(res)
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM sessions1 WHERE id = %s", (str(id1),))
        responseout1 = cursor.fetchall()
 
        if(res[0]==0):
            info.append(" This person is very sad")
            res1.append("sad")
        elif(res[0]==1):
            info.append(" This person is disturbed")
            res1.append("disturbed")
        elif(res[0]==2):
            info.append(" This person is very happy")
            res1.append("happy")
        elif(res[0]==3):
            info.append(" This person is very much Excited")
            res1.append("Excited")

        
        if(res[1]==0):
            info.append(" and very irresponsible")
            res1.append("irresponsible")
        elif(res[1]==1):
            info.append(" and don't feels respect towards elders")
            res1.append("don't respect")
        elif(res[1]==2):
            info.append(" and feels respect towards elders")
            res1.append("Shows respect")
        elif(res[1]==3):
            info.append(" and is very much responsible")
            res1.append("Responsible")


        if(res[2]==0):
            info.append(" and very unconfident")
            res1.append("Unconfident")
        elif(res[2]==1):
            info.append(" and don't belives in himself")
            res1.append("don't belives")
        elif(res[2]==2):
            info.append(" and belives in himself")
            res1.append("belives")
        elif(res[2]==3):
            info.append(" and is very confident")
            res1.append("very Confident")
        
        if(res[3]==0):
            info.append(" and is selfish , unregular")
            res1.append("selfish and unregular")
        elif(res[3]==1):
            info.append(" and not well disciplined")
            res1.append("Undisciplined")
        elif(res[3]==2):
            info.append(" and shows good attitude towars others")
            res1.append("Good attitude")
        elif(res[3]==3):
            info.append(" and is very disciplined")
            res1.append("disciplined")

        if(res[4]==0):
            info.append(" and lack of communication")
            res1.append("lack of communication")
        elif(res[4]==1):
            info.append("and dont have good softskills")
            res1.append(" bad softskills")
        elif(res[4]==2):
            info.append(" and have good softskills")
            res1.append("good softskills")
        elif(res[4]==3):
            info.append(" and is having good communication skills")
            res1.append("good communication")

        if(res[5]==0):
            info.append(" and not very keen with social activities")
            res1.append("bad social acts")
        elif(res[5]==1):
            info.append(" and have social responsiblitity")
            res1.append("good social acts")
         
        x1=res
        # print("x1-----------------------------------------------------------------------------------------",x1)
        y1=[4, 4, 4, 4, 4, 2]
        names=["Emotion","mental","modesty","discipline","Communication","social"]

        barplot=plt.plot(names,x1,color="green")
        plt.scatter(names,x1)
        my_path=os.path.dirname(__file__)
        new_name1 = "plot1"+str(time.time())+".png"
        print(new_name1)
        # print("new_name1 :",new_name1,time.time())
        plt.savefig(new_name1,dpi=300,bbox_inches='tight')
        plt.clf()
        
        plt1.rc('font',size=7)
        barplot=plt1.bar(names,x1,color="green")
        for h,bar in enumerate(barplot):
            yval=bar.get_height()
            plt1.text(bar.get_x()+bar.get_width()//2.0,yval,str(res1[h]),va="bottom")
        plt1.scatter(names,y1)
        plt1.plot(names,y1)
        new_name2 = "plot2"+str(time.time())+".png"
        # print("new_name2 :",new_name2,time.time())
        plt.savefig(new_name2,dpi=300,bbox_inches='tight')
        plt.clf()
        
        fileName1=new_name1
        bucket1 = storage.bucket()
        blob1 = bucket1.blob(fileName1)
        blob1.upload_from_filename(fileName1)
        blob1.make_public()
        output1url = blob1.public_url
        
        fileName2=new_name2
        bucket2 = storage.bucket()
        blob2 = bucket2.blob(fileName2)
        blob2.upload_from_filename(fileName2)
        blob2.make_public()
        output2url = blob2.public_url
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO predict VALUES (%s, %s , %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s)', (responseout1[-1][0],str(responseout1[-1][1]),str(responseout1[-1][3]),str(output1url),str(output2url),str(info[0]),str(info[1]),str(info[2]),str(info[3]),str(info[4]),str(info[5]),str(responseout1[-1][2])))
        mysql.connection.commit()

        my_path=os.path.dirname(__file__)
        os.remove(os.path.join(my_path,new_name1))
        os.remove(os.path.join(my_path,new_name2))
        
    return jsonify({"Output":{"ID":responseout1[-1][0],
                              "email":responseout1[-1][1],
                        "inputimgurl":str(responseout1[-1][3]),
                        "outputimgurl1":output1url,
                        "outputimgurl2":output2url,
                        "info0":info[0],
                        "info1":info[1],
                        "info2":info[2],
                        "info3":info[3],
                        "info4":info[4],
                        "info5":info[5],
                        "time":str(responseout1[-1][2])
                        }})

@app.route('/show/<emailvalue>',methods = ['GET'])
def show(emailvalue):
    dict2 = {}
    cursor = mysql.connection.cursor()
    if(emailvalue =="999"):
        cursor.execute('select * from  predict')
    else:
        cursor.execute('select * from  predict where email = %s',(emailvalue,))
    response = cursor.fetchall()
    print(response)
    for k,j in enumerate(response):
        dict1 = {}
        print("\n----------------------------------------------------------------------------------------------------\n")
        dict1["id"]=j[0]
        dict1["email"]=j[1]
        dict1["input"]=j[2]
        dict1["output1"]=j[3]
        dict1["output2"]=j[4]
        dict1["info0"]=j[5]
        dict1["info1"]=j[6]
        dict1["info2"]=j[7]
        dict1["info3"]=j[8]
        dict1["info4"]=j[9]
        dict1["info5"]=j[10]
        dict1["time"]=j[11]
        dict2[k]=dict1
    print(dict2)
    mysql.connection.commit()
    return jsonify({'Output':dict2 })
    

        
if __name__ == "__main__":
    app.run() 
