
try:
    from datetime import timedelta
    from flask import Flask, render_template, flash, redirect, request, url_for, send_file, session
    import datetime
    import os
    from cloudant.client import Cloudant
    from cloudant.error import CloudantException
    from cloudant.result import Result, ResultByKey
    from authlib.integrations.flask_client import OAuth
    import json
    from werkzeug.utils import secure_filename
    # from werkzeug import secure_filename
    from sqlalchemy import create_engine , MetaData,Table,Column,Integer,String,BLOB
    import sqlalchemy
    from sqlalchemy.sql import text
    import cv2
    import time
    from matplotlib import pyplot as plt
    import numpy as np
    import pandas as pd
    import pickle
    import os
    import random
    # from sendgrid import SendGridAPIClient
    # from sendgrid.helpers.mail import Mail
    from datetime import date,datetime
    import urllib
    import hashlib
except Exception as e:
    print("Some Modules are Missing : {} ".format(e))


# App config
app = Flask(__name__)

# ====================Change me  =======================================
global client_id
global client_secret
global client

client = Cloudant.iam("e9a1474d-2a68-4b11-b60c-a60c87c061a9-bluemix","oUFFwB9qB-SghbaQbaj7y7TSu7N4yS3mWrDdyYHxtjJn",connect=True)
client.connect()


client_id = "778520672114-0nnem7bqng6l8u0o1vs08onno2k8hngd.apps.googleusercontent.com"
client_secret = "v8kyQb4VhO5ZqMFAfsctwjF4"

# Session config
app.secret_key = "dhutrr"
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
# ======================================================================


# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


def isLoggedIN():
    try:
        user = dict(session).get('profile', None)
        if user:
            return True, user.get("name"),user.get("email")
        else:
            return False,{},{}
    except Exception as e:
        return False,{},{}

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    print(user_info)
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route('/')
def hello_world():
    flag,user,email = isLoggedIN()
    print(flag,user,email)
    return render_template("Index1.html", flag=flag, user=user)


#================================History==========================================================================================================

@app.route('/history2/<dateurl>',methods=["POST","GET"])
def histroy2(dateurl):
    msg=""
    if "data" in client:
        db = client["data"]
    else:
        db = client.create_database("data")

    result = Result(db.all_docs, include_docs=True)
    # print(result,list(result))

    for i in list(result):
        if i['doc']['dateurl']==dateurl:
            i1=i['doc']
    print(i1)
    return render_template("history3.html",flag=1,alldata=i1)





@app.route('/history1/<email11>',methods=["POST","GET"])
def histroy1(email11):
    msg=""

    if "data" in client:
        db = client["data"]
    else:
        db = client.create_database("data")

    result = Result(db.all_docs, include_docs=True)
    # print(result,list(result))
    dates=[]
    dupdate=[]
    for i in list(result):
        if i['doc']['email']==email11 and  i['doc']['date'] not in dates:
            dates.append(i['doc']['date'])
            dupdate.append(i['doc']['dateurl'])
    return render_template("history1.html",flag=1,dates=dates,dupdate=dupdate,length1=range(len(dates)))




@app.route('/history',methods=["POST","GET"])
def histroy():
    flag,user,email = isLoggedIN()
    msg=""
    if "data" in client:
        db = client["data"]
    else:
        db = client.create_database("data")

    result = Result(db.all_docs, include_docs=True)
    emails=[]
    for i in list(result):
        if i['doc']['email'] not in emails:
            emails.append(i['doc']['email'])
    return render_template("history.html",flag=1,emails=emails)

#========================main================================================================================================================
@app.route('/main1',methods=['POST','GET'])
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return redirect('/')

#=============================canvas=========================================================================================================


@app.route('/canvas',methods=['POST','GET'])
def canvas():
    return render_template("canvas1.html")

@app.route('/canvas1',methods=['POST','GET'])
def canvas1():
    info=[]
    import os
    flag,user,email = isLoggedIN()
    new_name1=""
    new_name2=""
    if request.method=='POST' and flag:
        image = request.form["image1"]
        my_path = os.path.dirname(__file__)
        filename1= "img/inputnew"+str(time.time())+".png"
        new_name_i = my_path+'/static/'+filename1
        print(new_name_i)
        print("Image-----------------------------------------------------------")
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
        # cv2.waitKey(0)
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
        if(count2==0):
            count2=1
        slant_letters_angle.append((MYANGLE2/count2))


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

        res=[]
        for y in features.columns:
            name1="model"+str(y)
            with open(name1,"rb") as f:
                model=pickle.load(f)
                res.append(model.predict([x_test1])[0])
        print(res)
        
        res1=[]
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
            info.append(" and is very irresponsible")
            res1.append("irresponsible")
        elif(res[1]==1):
            info.append(" and don't feels respect towards elders ")
            res1.append("don't respect")
        elif(res[1]==2):
            info.append(" and feels respect towards elders ")
            res1.append("Shows respect")
        elif(res[1]==3):
            info.append(" and is very much responsible")
            res1.append("Responsible")


        if(res[2]==0):
            info.append(" and is very unconfident")
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
            info.append(" and is selfish and unregular")
            res1.append("selfish and unregular")
        elif(res[3]==1):
            info.append(" and is not well disciplined")
            res1.append("Undisciplined")
        elif(res[3]==2):
            info.append(" and shows good attitude towars others")
            res1.append("Good attitude")
        elif(res[3]==3):
            info.append(" and is very disciplined and well scheduleded with his time table")
            res1.append("disciplined")

        if(res[4]==0):
            info.append(" and is lack of communication")
            res1.append("lack of communication")
        elif(res[4]==1):
            info.append(" and dont have good softskills")
            res1.append(" bad softskills")
        elif(res[4]==2):
            info.append(" and have good softskills")
            res1.append("good softskills")
        elif(res[4]==3):
            info.append(" and is having good communication skills")
            res1.append("good communication")

        if(res[5]==0):
            info.append(" and is not very keen with social activities")
            res1.append("bad social acts")
        elif(res[5]==1):
            info.append(" and have social responsiblitity. ")
            res1.append("good social acts")


        from matplotlib import pyplot as plt
        from matplotlib import pyplot as plt1
        import os

        x1=res
        y1=[4, 4, 4, 4, 4, 2]
        names=["Emotion","mental","modesty","discipline","c2c","social"]

        barplot=plt.plot(names,x1,color="green")
        plt.scatter(names,x1)
        my_path=os.path.dirname(__file__)
        new_name1 = "img/plot1"+str(time.time())+".png"
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
        plt.savefig(my_path+'/static/'+new_name2,dpi=300,bbox_inches='tight')
        plt.clf()
        try:
            if "data" in client:
                db = client["data"]
            else:
                db = client.create_database("data")
        except:
            print("exception")


        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        d2 = datetime.now().strftime("%H:%M:%S")

        d11 = today.strftime("%d_%m_%Y")
        d22 = datetime.now().strftime("%H_%M_%S")



        my_path=os.path.dirname(__file__)
        os.remove(os.path.join(my_path,"input.png"))

        input_data = {"email":email,
            "input": str(filename1),
            "output1":str(new_name1),
            "output2":str(new_name2),
            "info":"".join(info),
            "date":d1+" "+d2,
            "dateurl":d11+d22
        }

        print(input_data)

        db.create_document(input_data)
    else:
        return "<h1>Your Session maybe expired Please signin again<h1>"

    return render_template("index.html",i=1,plot1=new_name1,plot2=new_name2,info=info)

#========================/main=================================================================================================================

@app.route('/main',methods=['POST','GET'])
def main():
    info=[]
    flag,user,email = isLoggedIN()
    new_name1=""
    new_name2=""
    if request.method=='POST' and flag:
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
        # cv2.waitKey(0)
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
            info.append(" and is very irresponsible")
            res1.append("irresponsible")
        elif(res[1]==1):
            info.append(" and don't feels respect towards elders ")
            res1.append("don't respect")
        elif(res[1]==2):
            info.append(" and feels respect towards elders ")
            res1.append("Shows respect")
        elif(res[1]==3):
            info.append(" and is very much responsible")
            res1.append("Responsible")


        if(res[2]==0):
            info.append(" and is very unconfident")
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
            info.append(" and is selfish and unregular")
            res1.append("selfish and unregular")
        elif(res[3]==1):
            info.append(" and is not well disciplined")
            res1.append("Undisciplined")
        elif(res[3]==2):
            info.append(" and shows good attitude towars others")
            res1.append("Good attitude")
        elif(res[3]==3):
            info.append(" and is very disciplined and well scheduleded with his time table")
            res1.append("disciplined")

        if(res[4]==0):
            info.append(" and is lack of communication")
            res1.append("lack of communication")
        elif(res[4]==1):
            info.append(" and dont have good softskills")
            res1.append(" bad softskills")
        elif(res[4]==2):
            info.append(" and have good softskills")
            res1.append("good softskills")
        elif(res[4]==3):
            info.append(" and is having good communication skills")
            res1.append("good communication")

        if(res[5]==0):
            info.append(" and is not very keen with social activities")
            res1.append("bad social acts")
        elif(res[5]==1):
            info.append(" and have social responsiblitity. ")
            res1.append("good social acts")


        from matplotlib import pyplot as plt
        from matplotlib import pyplot as plt1
        import os
        my_path=os.path.dirname(__file__)
        image_input = cv2.imread(session["filename"],1)
        plt.axis("off")
        plt.imshow(cv2.cvtColor(image_input,cv2.COLOR_BGR2RGB))
        new_name = "img/input"+str(time.time())+".png"
        plt.savefig(my_path+'/static/'+new_name,bbox_inches='tight')
        plt.clf()


        x1=res
        y1=[4, 4, 4, 4, 4, 2]
        names=["Emotion","mental","modesty","discipline","c2c","social"]

        barplot=plt.plot(names,x1,color="green")
        plt.scatter(names,x1)
        my_path=os.path.dirname(__file__)
        new_name1 = "img/plot1"+str(time.time())+".png"
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
        plt.savefig(my_path+'/static/'+new_name2,dpi=300,bbox_inches='tight')
        plt.clf()
        try:
            if "data" in client:
                db = client["data"]
            else:
                db = client.create_database("data")
        except:
            print("exception")

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        d2 = datetime.now().strftime("%H:%M:%S")

        d11 = today.strftime("%d_%m_%Y")
        d22 = datetime.now().strftime("%H_%M_%S")

        my_path=os.path.dirname(__file__)
        os.remove(os.path.join(my_path,session["filename"]))

        input_data = {"email":email,
            "input": str(new_name),
            "output1":str(new_name1),
            "output2":str(new_name2),
            "info":"".join(info),
            "date":d1+" "+d2,
            "dateurl":d11+d22
        }
        print(input_data)
        db.create_document(input_data)
    return render_template("index.html",i=1,plot1=new_name1,plot2=new_name2,info=info)

#================================Admin login=================================================================================================

@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/adminh3/<dateurl>',methods=["POST","GET"])
def adminh3(dateurl):
    msg=""
    if "data" in client:
        db = client["data"]
    else:
        db = client.create_database("data")

    result = Result(db.all_docs, include_docs=True)

    for i in list(result):
        if i['doc']['dateurl']==dateurl:
            i1=i['doc']
    print(i1)
    return render_template("admin1.html",flag=1,alldata=i1)


@app.route('/adminh2/<email11>',methods=["POST","GET"])
def adminh2(email11):
    msg=""

    if "data" in client:
        db = client["data"]
    else:
        db = client.create_database("data")
    result = Result(db.all_docs, include_docs=True)
    dates=[]
    dupdate=[]
    for i in list(result):
        if i['doc']['email']==email11 and  i['doc']['date'] not in dates:
            dates.append(i['doc']['date'])
            dupdate.append(i['doc']['dateurl'])
    return render_template("adminh2.html",flag=1,dates=dates,dupdate=dupdate,length1=range(len(dates)))


@app.route('/admin11',methods=["POST","GET"])
def admin11():
    msg=""
    emails=[]
    try:
        if "data" in client:
            db = client["data"]
        else:
            db = client.create_database("data")
        result = Result(db.all_docs, include_docs=True)
        for i in list(result):
            if i['doc']['email'] not in emails:
                emails.append(i['doc']['email'])
    except:
        msgs = "An Exception Occured"
        return render_template("admin.html",msgs=msgs)
    return render_template("adminh.html",flag=1,emails=emails)

@app.route('/admin1',methods=["POST","GET"])
def admin1():
    msg=""
    newlist=[]
    if request.method == 'POST':
        email1=request.form['email']
        pass1=request.form['password']
        if(str(email1)=="root@gmail.com" and str(pass1)=="root"):
            try:
                if "data" in client:
                    db = client["data"]
                else:
                    db = client.create_database("data")
                result = Result(db.all_docs, include_docs=True)
                # print(result,list(result))
                emails=[]
                for i in list(result):
                    if i['doc']['email'] not in emails:
                        emails.append(i['doc']['email'])
         
            except:
                msgs = "An Exception Occured"
                return render_template("admin.html",msgs=msgs)
        else:
            msgs="Wrong Credentials"
            print(msgs)
            return render_template("admin.html",msgs=msgs)
    return render_template("adminh.html",flag=1,emails=emails)

@app.route('/admin2',methods=["POST","GET"])
def admin2():
    return render_template("admin1.html",flag=0)


@app.route('/admin22',methods=["POST","GET"])
def admin22():
    msg=""
    if request.method == 'POST':
        email1=request.form['email']
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
    return render_template("admin1.html",flag=1,alldata=newlist,length1=range(len(newlist[0][1])))


if __name__ == "__main__":
    app.run(debug=True)
