import 'dart:convert';
import 'dart:ffi';
import 'dart:io';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path/path.dart';
import 'dart:async';
import 'package:mysql1/mysql1.dart';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;

final Color yellow = Color(0xfffbc31b);
final Color orange = Color(0xfffb6900);

class Uploading1 extends StatelessWidget {
  final FirebaseUser user; 
  Uploading1(this.user);
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')), body: UploadingImageToFirebaseStorage(this.user));
  }
}

class UploadingImageToFirebaseStorage extends StatefulWidget {
  final FirebaseUser user1;

  UploadingImageToFirebaseStorage(this.user1);

  @override
  _UploadingImageToFirebaseStorageState createState() =>
      _UploadingImageToFirebaseStorageState();
}

class _UploadingImageToFirebaseStorageState
    extends State<UploadingImageToFirebaseStorage> {
  File _imageFile;
  var calledurl;
  String valueapi="";
  String fileName;
  String datetime1;
  String datetime12;
  String ID;
  BuildContext context;
  bool bool1=false;
  bool screen=true;
  var decodedurls;
  var decoded1;
  String per="0%";
  ///NOTE: Only supported on Android & iOS
  ///Needs image_picker plugin {https://pub.dev/packages/image_picker}
  final picker = ImagePicker();

  Future pickImage() async {
    final pickedFile = await picker.getImage(source: ImageSource.gallery);

    try{
      setState(() {
        _imageFile = File(pickedFile.path);
      });
    }
    catch(e){
      print(e);
    }
  }

  void urlget(String cd) async{
    // ignore: await_only_futures
    setState(() {
      per="25%";
    });
    final response = await await await http.get(Uri.parse('https://flutter-graphology.herokuapp.com/upload/'+cd)); 
    print(response.body);
    final decoded = json.decode(response.body) as Map<String, dynamic>; 
    print(decoded["output"]["see"]);
    setState(() {
      per="50%";
    });
    final response1 =  await http.get(Uri.parse('https://flutter-graphology.herokuapp.com/predict/'+decoded["output"]["see"]+'/'+ID)); 
    decodedurls = response1.body;
    print(response1.body);
    decoded1 =json.decode(response1.body) as Map<String, dynamic>; 
    setState(() {
      per="100%";
    });
    print("decoded1-----------------------------------");
    print(decoded1["Output"]);
    setState(() {
      screen = false;
    });
  }

   void viewer(String s) async{
    valueapi=s;
    print(valueapi);
    final conn = await MySqlConnection.connect(ConnectionSettings(
        host: 'remotemysql.com', 
        port: 3306,
        user: 'RIcvQcz1ZB',
        password: '98U4LQX9u7',
        db: 'RIcvQcz1ZB'
    ));    
    calledurl = fileName;
    // print(widget.user1.email+"\n"+fileName+"\n"+datetime1+"\n"+valueapi);
    print(widget.user1.email+"\n"+fileName+"\n"+"\n"+valueapi);
    var result = await conn.query('insert into upload (email, name ,time, image) values (?,?,?,?)',[widget.user1.email,fileName,datetime12,valueapi]);
    print('Inserted row id=${result.insertId}');
    ID = '${result.insertId}';
    print(ID);
    print(calledurl+"/"+ID);
    setState(() {
          bool1=true;
          print(bool1);
    });

  }


  Future uploadImageToFirebase(BuildContext context) async {
    final time = DateTime.now();
    // final formatter = DateFormat(r'''dd/MM/yyyy_hh_mm_ss''');
    final formatter1 = DateFormat(r'''dd/MM/yyyy kk:mm:ss''');
    // final String datetime = formatter.format(time);
    final String datetime12 = formatter1.format(time);
    this.datetime12=datetime12;
    // this.datetime1=datetime;
    print(datetime12);
    fileName = basename(_imageFile.path);
    print(fileName);
    String email = widget.user1.email;
    StorageReference firebaseStorageRef =
        FirebaseStorage.instance.ref().child('$email'+'/$fileName');
    StorageUploadTask uploadTask = firebaseStorageRef.putFile(_imageFile);
    StorageTaskSnapshot taskSnapshot = await uploadTask.onComplete;
    taskSnapshot.ref.getDownloadURL().then(
          (value) => this.viewer('$value'),
    );
  }

  Widget uploadImageButton(BuildContext context) {
    return Container(
      child: Stack(
        children: <Widget>[
          Container(
            padding:
                const EdgeInsets.symmetric(vertical: 5.0, horizontal: 16.0),
            margin: const EdgeInsets.only(
                top: 30, left: 20.0, right: 20.0, bottom: 20.0),
            decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [yellow, orange],
                ),
                borderRadius: BorderRadius.circular(30.0)),
            child: FlatButton(
              onPressed: () => uploadImageToFirebase(context),
              child: Text(
                "Upload Image",
                style: TextStyle(fontSize: 20),
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return screen ? Scaffold(
      body: Stack(
        children: <Widget>[
          Container(
            height: 360,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(50.0),
                    bottomRight: Radius.circular(50.0)),
                gradient: LinearGradient(
                    colors: [orange, yellow],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight)),
          ),
          Container(
            margin: const EdgeInsets.only(top: 80),
            child: Column(
              children: <Widget>[
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Center(
                    child: Text(
                      "Upload Image to Find the Predictions",
                      style: TextStyle(
                          color: Colors.white,
                          fontSize: 28,
                          fontStyle: FontStyle.italic),
                    ),
                  ),
                ),
                SizedBox(height: 20.0),
                Expanded(
                  child: Stack(
                    children: <Widget>[
                      Container(
                        height: double.infinity,
                        margin: const EdgeInsets.only(
                            left: 30.0, right: 30.0, top: 10.0),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(30.0),
                          child: _imageFile != null
                              ? Image.file(_imageFile)
                              : FlatButton(
                                  child: Icon(
                                    Icons.add_a_photo,
                                    size: 50,
                                  ),
                                  onPressed: pickImage,
                                ),
                        ),
                      ),
                    ],
                  ),
                ),
                uploadImageButton(context),
                Container(
                          padding:
                              const EdgeInsets.symmetric(vertical: 5.0, horizontal: 16.0),
                          margin: const EdgeInsets.only(
                              top: 30, left: 20.0, right: 20.0, bottom: 20.0),
                          decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: bool1 ? [Colors.lightGreen,Colors.green] : [yellow,orange],
                              ),
                              borderRadius: BorderRadius.circular(30.0)),
                          child: FlatButton(
                                  onPressed: ()=>this.urlget(calledurl+'/'+ID),
                                  child: Text(per+
                                    "  predict",
                                    style: TextStyle(fontSize: 20),
                            ),
                      ),
                ),
                  
              ],
            ),
          ),
        ],
      ),
    )
    :Scaffold(
      body: Stack(
        children: <Widget>[
          Container(
            height: 400,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(50.0),
                    bottomRight: Radius.circular(50.0)),
                gradient: LinearGradient(
                    colors: [orange, yellow],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight)),
          ),
          new SingleChildScrollView(
              child: new Column(children:<Widget>[
                new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["time"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                Text("Input Image ",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
                Image.network(decoded1["Output"]["inputimgurl"],height: 100,),
                // Text("Output Image1 :",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
                // Image.network(decoded1["Output"]["outputimgurl1"],height: 300,width: 400,),
                Text("Predicted Image ",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
                Image.network(decoded1["Output"]["outputimgurl2"],height: 300,width: 400,),
                
                new Align(alignment: Alignment.bottomCenter,child: new  Text("Personality Trait ",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.center,),),
                new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info0"]+decoded1["Output"]["info1"]+decoded1["Output"]["info2"]+decoded1["Output"]["info3"]+decoded1["Output"]["info4"]+decoded1["Output"]["info5"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                
                // new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info0"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                // new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info1"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                // new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info2"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                // new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info3"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                // new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info4"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                // new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info5"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                // new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["info5"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),

              
              ],),
            ),
          ]
          )
    ,);
  }
}


