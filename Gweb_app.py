from flask import Flask,redirect,render_template,request,session,url_for
from werkzeug import secure_filename
from sqlalchemy import create_engine , MetaData,Table,Column,Integer,String,BLOB
from PIL import Image
import base64
import io
import sqlalchemy
import hashlib
from sqlalchemy.sql import text
import requests
import cv2
import time
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle
import os
import random
from datetime import date,datetime
from nbformat.v2.rwbase import base64_decode
import urllib

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=os.path.dirname(__file__)+'/static/img'
# r"C:\Users\user\Documents\2nd_year_2nd_Sem\IBM_person_project\data_subset\static\"
app.config["SECRET_KEY"]="safkl"
app.jinja_env.filters['zip']=zip

@app.route('/')
def home1():
    return render_template("home1.html")


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login1')
def login1():
    return render_template("login.html")

@app.route('/signup1')
def signup1():
    return render_template("sign_up.html")

@app.route('/login1')
def login():
    return render_template("login.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/admin1',methods=["POST","GET"])
def admin1():
    msg=""
    if request.method == 'POST':
        email1=request.form['email']
        pass1=request.form['password']
        if(str(email1)=="root@gmail.com" and str(pass1)=="root"):
            engine = create_engine('sqlite:///database2.db',echo=True)
            conn  =engine.connect()
            res11 = conn.execute("SELECT * FROM data")
            alldata = res11.fetchall()
            newlist=[]
            list1=[]
            for data1 in range(len(alldata)):
                print(list(alldata[data1][5].split(",")))
                list1.append( list(alldata[data1][5].split(",")) )
            for i1,i2 in zip(alldata,list1):
                print("---------------------------------------------",i2[0][3:-3])
                print("---------------------------------------------",i2[1][3:-3])
                print("---------------------------------------------",i2[2][3:-3])
                print("---------------------------------------------",i2[3][3:-3])
                print("---------------------------------------------",i2[4][3:-3])
                print("---------------------------------------------",i2[5][3:-3])
                i2[0]=i2[0][3:-3]
                i2[1]=i2[1][3:-3]
                i2[2]=i2[2][3:-3]
                i2[3]=i2[3][3:-3]
                i2[4]=i2[4][3:-3]
                i2[5]=i2[5][3:-3]

                newlist.append([i1,i2])
            print("---------------------------------------------------------------------------------------------------------")
            for i in newlist:
                print(i)
            # print(alldata[0][0],alldata[0][1],alldata[0][2],alldata[0][3],alldata[0][4])#id , email , input , output1 , output2 , info.
    return render_template("admin.html",flag=1,alldata=newlist,length1=range(len(newlist[0][1])))

@app.route('/admin2',methods=["POST","GET"])
def admin2():
    return render_template("admin1.html",flag=0)

@app.route('/admin22',methods=["POST","GET"])
def admin22():
    msg=""
    if request.method == 'POST':
        email1=request.form['email']
        engine = create_engine('sqlite:///database2.db',echo=True)
        conn  =engine.connect()
        res11 = conn.execute("SELECT * FROM data WHERE email =?",(str(email1)))
        alldata = res11.fetchall()
        if(len(alldata)==0):
            return  render_template("admin1.html",flag=0,msg=str(email1)+" Email Address Haven't used Our website for  image")
        newlist=[]
        list1=[]
        for data1 in range(len(alldata)):
            print(list(alldata[data1][5].split(",")))
            list1.append( list(alldata[data1][5].split(",")) )
        for i1,i2 in zip(alldata,list1):
            print("---------------------------------------------",i2[0][3:-3])
            print("---------------------------------------------",i2[1][3:-3])
            print("---------------------------------------------",i2[2][3:-3])
            print("---------------------------------------------",i2[3][3:-3])
            print("---------------------------------------------",i2[4][3:-3])
            print("---------------------------------------------",i2[5][3:-3])
            i2[0]=i2[0][3:-3]
            i2[1]=i2[1][3:-3]
            i2[2]=i2[2][3:-3]
            i2[3]=i2[3][3:-3]
            i2[4]=i2[4][3:-3]
            i2[5]=i2[5][3:-3]

            newlist.append([i1,i2])
        print("---------------------------------------------------------------------------------------------------------")
        for i in newlist:
            print(i)
        # print(alldata[0][0],alldata[0][1],alldata[0][2],alldata[0][3],alldata[0][4])#id , email , input , output1 , output2 , info.
    return render_template("admin1.html",flag=1,alldata=newlist,length1=range(len(newlist[0][1])))


@app.route('/admin3',methods=["POST","GET"])
def admin3():
    msg=""
    engine = create_engine('sqlite:///database2.db',echo=True)
    conn  =engine.connect()
    res11 = conn.execute("SELECT * FROM data")
    alldata = res11.fetchall()
    if(len(alldata)==0):
        return  render_template("admin1.html",flag=0,msg=" Email Address Haven't used Our website for  image")
    newlist=[]
    list1=[]
    for data1 in range(len(alldata)):
        print(list(alldata[data1][5].split(",")))
        list1.append( list(alldata[data1][5].split(",")) )
    for i1,i2 in zip(alldata,list1):
        print("---------------------------------------------",i2[0][3:-3])
        print("---------------------------------------------",i2[1][3:-3])
        print("---------------------------------------------",i2[2][3:-3])
        print("---------------------------------------------",i2[3][3:-3])
        print("---------------------------------------------",i2[4][3:-3])
        print("---------------------------------------------",i2[5][3:-3])
        i2[0]=i2[0][3:-3]
        i2[1]=i2[1][3:-3]
        i2[2]=i2[2][3:-3]
        i2[3]=i2[3][3:-3]
        i2[4]=i2[4][3:-3]
        i2[5]=i2[5][3:-3]

        newlist.append([i1,i2])
    # print("---------------------------------------------------------------------------------------------------------")

    # print(alldata[0][0],alldata[0][1],alldata[0][2],alldata[0][3],alldata[0][4])#id , email , input , output1 , output2 , info.
    return render_template("admin1.html",flag=1,alldata=newlist,length1=range(len(newlist[0][1])))


@app.route('/signup',methods=["POST","GET"])
def signup_():
    msg=""
    if request.method == 'POST':
            name1=request.form['username']
            email1=request.form['email']
            pass1=request.form['password1']
            pass2=request.form['password2']
            # print(name1,email1,pass1,pass2)
            session["name"]=name1
            session["email"]=email1
            session["password1"]=pass1
            session["password2"]=pass2
            num = random.randint(1000,100000)
            import os 
            from cred import api
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            message = Mail(from_email="masteravanger2@gmail.com",
                            to_emails=session["email"],
                            subject="OTP Verification for Graphology Website",
                            plain_text_content="This is Your otp "+str(num))
            try:
                sg = SendGridAPIClient(api)
                response = sg.send(message)
                # print(response.status_code)
                # print(response.body)
                # print(response.headers)
            except Exception as e:
                print(e)
            # print(session["name"],session["email"],session["password1"])
            engine = create_engine('sqlite:///database2.db',echo=True)
            meta = MetaData()
            users = Table(
                'users',meta,
                Column('id',Integer,primary_key=True),
                Column('username',String),
                Column('email',String),
                Column('password',String),
                Column("otp",String)
            )
            meta.create_all(engine)
            conn  =engine.connect()
            res1 = conn.execute("SELECT * FROM users WHERE username=? ",(str(session["name"])))
            res2 = conn.execute("SELECT * FROM users WHERE email=?",(str(session["email"])))
            l1=len(list(res1.fetchall()))
            l2=len(list(res2.fetchall()))
            if(l1>0):
                msg = "Username  Already Exists"
                return render_template("sign_up.html",msg=msg)
            elif(l2>0):
                msg = "Email Already Exists"
                return render_template("sign_up.html",msg=msg)
            else:
                if(str(session['password1'])!=str(session['password2'])):
                    msg = "Password doesn't matched"
                    return render_template("sign_up.html",msg=msg)
                else:
                    insert1 = users.insert().values(username = session["name"],email = session["email"],password= hashlib.md5(session["password1"].encode("utf8")).hexdigest(),otp=str(num))
                    result = conn.execute(insert1)
                    # print("result :",result.inserted_primary_key[0])
                    # session.pop("name")
                    # session.pop("email")
                    # session.pop("password1")
                    # session.pop("password2")
                    msg="Please Confirm your email address"
    return render_template("otp.html",msg=msg)

@app.route('/otpverify',methods=["POST","GET"])
def otp():
    msg1=''
    if request.method == 'POST':
        pass1=request.form['password']
        engine = create_engine('sqlite:///database2.db',echo=True)
        meta = MetaData()
        users = Table(
            'users',meta,
            Column('id',Integer,primary_key=True),
            Column('username',String),
            Column('email',String),
            Column('password',String),
            Column("otp",String)
        )
        meta.create_all(engine)
        conn  =engine.connect()
        res2 = conn.execute("SELECT otp FROM users WHERE email=?",(str(session["email"])))
        if(str(res2.fetchone()[0])!=str(pass1)):
            delete = users.delete().where(users.c.email==session["email"])
            result = conn.execute(delete)
            return render_template("sign_up.html",msg="Otp is not verified Please Signup Again")
        else:
            return render_template("login.html",msg1="Your email otp is successfully verified")
    

@app.route('/login',methods=["POST","GET"])
def login_():
    msg1=''
    if request.method == 'POST':
        # print(request.form['email'])
        email1=request.form['email']
        pass1=request.form['password']
        session["email"]=email1
        engine = create_engine('sqlite:///database2.db',echo=True)
        conn = engine.connect()
        res1 = conn.execute("SELECT * FROM users WHERE email=?",(str(email1)))
        res2 = conn.execute("SELECT * FROM users WHERE email=? AND password = ?",(str(email1),hashlib.md5(str(pass1).encode("utf8")).hexdigest() ))
        list1=list(res1.fetchall())
        len1 = len(list1)
        if(len1==1 and len(list(res2.fetchall()))==0):
            msg1="Password is incorrect"
            return render_template("login.html",msg1=msg1)
        elif(len1>0):
            return render_template("home.html")
        else:
            msg1="User doesn't exists"
            return render_template("login.html",msg1=msg1)


@app.route('/main1',methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/canvas',methods=['POST','GET'])
def canvas():
    return render_template("canvas1.html")

@app.route('/canvas1',methods=['POST','GET'])
def canvas1():
    info=[]
    import os
    if request.method=='POST':
        image = request.form["image1"]
        my_path = os.path.dirname(__file__)
        filename1= "img/inputnew"+str(time.time())+".png"
        new_name_i = my_path+'/static/'+filename1
        # print(new_name_i)
        # print("Image-----------------------------------------------------------",image)
        response = urllib.request.urlopen(image)
        response1 = urllib.request.urlopen(image)

        with open("input.png",'wb') as f:
            f.write(response.file.read())
        f.close()
        with open(new_name_i,'wb') as f:
            f.write(response1.file.read())
        f.close()

        image = cv2.imread("input.png",1)

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
        cv2.waitKey(0)
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
        img = cv2.imread('./data_subset/'+str(i),1)
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
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        if(count==0):
            count=1
        if(height<0):
            height=-height
        if(width<0):
            width=-width
        Letter_size_height.append(height/count)
        Letter_size_width.append(width/count)

        features = pd.read_csv("Features1.csv")
        x_test1 =[baseline_angles_list[0],top_margin[0],word_spacing_ratio[0],written_spacing_ratio[0],pen_pressure[0],slant_letters_angle[0],Letter_size_height[0],Letter_size_width[0]]
    #     print(x_test1)
        res=[]
        for y in features.columns:
            name1="model"+str(y)
            with open(name1,"rb") as f:
                model=pickle.load(f)
                res.append(model.predict([x_test1])[0])
        print(res)
        
        res1=[]
        if(res[0]==0):
            info.append(" This person is very sad. ")
            res1.append("sad")
        elif(res[0]==1):
            info.append(" This person is disturbed. ")
            res1.append("disturbed")
        elif(res[0]==2):
            info.append(" This person is very happy. ")
            res1.append("happy")
        elif(res[0]==3):
            info.append(" This person is very much Excited. ")
            res1.append("Excited")

        
        if(res[1]==0):
            info.append(" This person is very irresponsible. ")
            res1.append("irresponsible")
        elif(res[1]==1):
            info.append(" This person don't feels respect towards elders. ")
            res1.append("don't respect")
        elif(res[1]==2):
            info.append(" This person feels respect towards elders. ")
            res1.append("Shows respect")
        elif(res[1]==3):
            info.append(" This person is very much responsible. ")
            res1.append("Responsible")


        if(res[2]==0):
            info.append(" This person is very unconfident. ")
            res1.append("Unconfident")
        elif(res[2]==1):
            info.append(" This person don't belives in himself. ")
            res1.append("don't belives")
        elif(res[2]==2):
            info.append(" This person belives in himself. ")
            res1.append("belives")
        elif(res[2]==3):
            info.append(" This person is very confident. ")
            res1.append("very Confident")
        
        if(res[3]==0):
            info.append(" This person is selfish and unregular. ")
            res1.append("selfish and unregular")
        elif(res[3]==1):
            info.append(" This person is not well disciplined. ")
            res1.append("Undisciplined")
        elif(res[3]==2):
            info.append(" This person shows good attitude towars others. ")
            res1.append("Good attitude")
        elif(res[3]==3):
            info.append(" This person is very disciplined and well scheduleded with his time table. ")
            res1.append("disciplined")

        if(res[4]==0):
            info.append(" This person is lack of communication. ")
            res1.append("lack of communication")
        elif(res[4]==1):
            info.append(" This person dont have good softskills. ")
            res1.append(" bad softskills")
        elif(res[4]==2):
            info.append(" This person have good softskills. ")
            res1.append("good softskills")
        elif(res[4]==3):
            info.append(" This person is having good communication skills. ")
            res1.append("good communication")

        if(res[5]==0):
            info.append(" This person is not very keen with social activities. ")
            res1.append("good social acts")
        elif(res[5]==1):
            info.append(" This person have social responsiblitity. ")
            res1.append("bad social acts")


        from matplotlib import pyplot as plt
        from matplotlib import pyplot as plt1
        import os
        # my_path=os.path.dirname(__file__)+"\static\img"
        # os.remove(os.path.join(my_path,file))
        # try:
        #     print("try-----------------------------------------------------try",my_path)
        #     for file in os.listdir(my_path):
        #         print(file)
        #         if file.endswith('.png'):
        #             os.remove(os.path.join(my_path,file))
        #             print(file)
        # except:
        #     pass
       
        # my_path=os.path.dirname(__file__)
        # image_input = cv2.imread("input.png")
        # plt.axis("off")
        # cv2.cvtColor(image_input,cv2.COLOR_BGR2RGB)
        # new_name = "img/input"+str(time.time())+".png"
        # plt.savefig(my_path+'/static/'+new_name,bbox_inches='tight')
        # plt.clf()

        x1=res
        # print("x1-----------------------------------------------------------------------------------------",x1)
        y1=[4, 4, 4, 4, 4, 2]
        names=["Emotion","mental","modesty","discipline","c2c","social"]

        barplot=plt.plot(names,x1,color="green")
        plt.scatter(names,x1)
        my_path=os.path.dirname(__file__)
        new_name1 = "img/plot1"+str(time.time())+".png"
        # print("new_name1 :",new_name1,time.time())
        plt.savefig(my_path+'/static/'+new_name1,dpi=300,bbox_inches='tight')
        plt.clf()
        
        plt1.rc('font',size=7)
        barplot=plt1.bar(names,x1,color="green")
        for h,bar in enumerate(barplot):
            yval=bar.get_height()
            plt1.text(bar.get_x()+bar.get_width()//2.0,yval,str(res1[h]),va="bottom")
        plt1.scatter(names,y1)
        plt1.plot(names,y1)
        new_name2 = "img/plot2"+str(time.time())+".png"
        # print("new_name2 :",new_name2,time.time())
        plt.savefig(my_path+'/static/'+new_name2,dpi=300,bbox_inches='tight')
        plt.clf()

        engine2 = create_engine('sqlite:///database2.db',echo=True)
        meta2 = MetaData()
        data = Table(
            'data',meta2,
            Column('id',Integer,primary_key=True),
            Column('email',String),
            Column('input',String),
            Column('output1',String),
            Column('output2',String),
            Column('info',String),
            Column('date',String)
        )
        meta2.create_all(engine2)
        conn2  =engine2.connect()

        today = date.today()
        d1 = today.strftime("%B %d %Y")
        d2 = datetime.now().strftime("%H:%M:%S")

        my_path=os.path.dirname(__file__)
        os.remove(os.path.join(my_path,"input.png"))

        insert11 = data.insert().values(email = session["email"],input=str(filename1),output1=str(new_name1),output2=str(new_name2),info=str(info),date=d1+" "+d2)
        result1 = conn2.execute(insert11)

    return render_template("index.html",i=1,plot1=new_name1,plot2=new_name2,info=info)



@app.route('/main',methods=['POST','GET'])
def main():
    info=[]
   
    if request.method=='POST':
        f = request.files['image']
        f.save(secure_filename(f.filename))
        session["filename"]=secure_filename(f.filename)
        # print("filename  :-------------------------------------------------------------------------------------- ",session['filename'])

        image = cv2.imread(session["filename"],1)

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
        cv2.waitKey(0)
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

        features = pd.read_csv("Features1.csv")
        x_test1 =[baseline_angles_list[0],top_margin[0],word_spacing_ratio[0],written_spacing_ratio[0],pen_pressure[0],slant_letters_angle[0],Letter_size_height[0],Letter_size_width[0]]
    #     print(x_test1)
        res=[]
        for y in features.columns:
            name1="model"+str(y)
            with open(name1,"rb") as f:
                model=pickle.load(f)
                res.append(model.predict([x_test1])[0])
        # print(res)
        res1=[]
        if(res[0]==0):
            info.append(" This person is very sad. ")
            res1.append("sad")
        elif(res[0]==1):
            info.append(" This person is disturbed. ")
            res1.append("disturbed")
        elif(res[0]==2):
            info.append(" This person is very happy. ")
            res1.append("happy")
        elif(res[0]==3):
            info.append(" This person is very much Excited. ")
            res1.append("Excited")

        
        if(res[1]==0):
            info.append(" This person is very irresponsible. ")
            res1.append("irresponsible")
        elif(res[1]==1):
            info.append(" This person don't feels respect towards elders. ")
            res1.append("don't respect")
        elif(res[1]==2):
            info.append(" This person feels respect towards elders. ")
            res1.append("Shows respect")
        elif(res[1]==3):
            info.append(" This person is very much responsible. ")
            res1.append("Responsible")


        if(res[2]==0):
            info.append(" This person is very unconfident. ")
            res1.append("Unconfident")
        elif(res[2]==1):
            info.append(" This person don't belives in himself. ")
            res1.append("don't belives")
        elif(res[2]==2):
            info.append(" This person belives in himself. ")
            res1.append("belives")
        elif(res[2]==3):
            info.append(" This person is very confident. ")
            res1.append("very Confident")
        
        if(res[3]==0):
            info.append(" This person is selfish and unregular. ")
            res1.append("selfish and unregular")
        elif(res[3]==1):
            info.append(" This person is not well disciplined. ")
            res1.append("Undisciplined")
        elif(res[3]==2):
            info.append(" This person shows good attitude towars others. ")
            res1.append("Good attitude")
        elif(res[3]==3):
            info.append(" This person is very disciplined and well scheduleded with his time table. ")
            res1.append("disciplined")

        if(res[4]==0):
            info.append(" This person is lack of communication. ")
            res1.append("lack of communication")
        elif(res[4]==1):
            info.append(" This person dont have good softskills. ")
            res1.append(" bad softskills")
        elif(res[4]==2):
            info.append(" This person have good softskills. ")
            res1.append("good softskills")
        elif(res[4]==3):
            info.append(" This person is having good communication skills. ")
            res1.append("good communication")

        if(res[5]==0):
            info.append(" This person is not very keen with social activities. ")
            res1.append("good social acts")
        elif(res[5]==1):
            info.append(" This person have social responsiblitity. ")
            res1.append("bad social acts")


        from matplotlib import pyplot as plt
        from matplotlib import pyplot as plt1
        import os
        # my_path=os.path.dirname(__file__)+"\static\img"
        # os.remove(os.path.join(my_path,file))
        # try:
        #     print("try-----------------------------------------------------try",my_path)
        #     for file in os.listdir(my_path):
        #         print(file)
        #         if file.endswith('.png'):
        #             os.remove(os.path.join(my_path,file))
        #             print(file)
        # except:
        #     pass

        my_path=os.path.dirname(__file__)
        image_input = cv2.imread(session["filename"],1)
        plt.axis("off")
        plt.imshow(cv2.cvtColor(image_input,cv2.COLOR_BGR2RGB))
        new_name = "img/input"+str(time.time())+".png"
        plt.savefig(my_path+'/static/'+new_name,bbox_inches='tight')
        plt.clf()


        x1=res
        # print("x1-----------------------------------------------------------------------------------------",x1)
        y1=[4, 4, 4, 4, 4, 2]
        names=["Emotion","mental","modesty","discipline","c2c","social"]

        barplot=plt.plot(names,x1,color="green")
        plt.scatter(names,x1)
        my_path=os.path.dirname(__file__)
        new_name1 = "img/plot1"+str(time.time())+".png"
        # print("new_name1 :",new_name1,time.time())
        plt.savefig(my_path+'/static/'+new_name1,dpi=300,bbox_inches='tight')
        plt.clf()
        
        plt1.rc('font',size=7)
        barplot=plt1.bar(names,x1,color="green")
        for h,bar in enumerate(barplot):
            yval=bar.get_height()
            plt1.text(bar.get_x()+bar.get_width()//2.0,yval,str(res1[h]),va="bottom")
        plt1.scatter(names,y1)
        plt1.plot(names,y1)
        new_name2 = "img/plot2"+str(time.time())+".png"
        # print("new_name2 :",new_name2,time.time())
        plt.savefig(my_path+'/static/'+new_name2,dpi=300,bbox_inches='tight')
        plt.clf()

        engine2 = create_engine('sqlite:///database2.db',echo=True)
        meta2 = MetaData()
        data = Table(
            'data',meta2,
            Column('id',Integer,primary_key=True),
            Column('email',String),
            Column('input',String),
            Column('output1',String),
            Column('output2',String),
            Column('info',String),
            Column('date',String)
        )
        meta2.create_all(engine2)
        conn2  =engine2.connect()

        today = date.today()
        d1 = today.strftime("%B %d %Y")
        d2 = datetime.now().strftime("%H:%M:%S")

        my_path=os.path.dirname(__file__)
        os.remove(os.path.join(my_path,session["filename"]))

        insert11 = data.insert().values(email = session["email"],input=str(new_name),output1=str(new_name1),output2=str(new_name2),info=str(info),date=d1+" "+d2)
        result1 = conn2.execute(insert11)

    return render_template("index.html",i=1,plot1=new_name1,plot2=new_name2,info=info)


if __name__ == "__main__":
    app.run(debug=True)