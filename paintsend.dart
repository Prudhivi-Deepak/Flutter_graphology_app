import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'dart:typed_data';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:async';
import 'package:mysql1/mysql1.dart';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:math';

class Paintsend extends StatelessWidget {
  ByteData imgBytes;
  FirebaseUser user;
  Paintsend(this.imgBytes,this.user);
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')), body: Paintsend1(this.imgBytes,this.user));
  }
}

// ignore: must_be_immutable
class Paintsend1 extends StatefulWidget {
  ByteData imgBytes;
  FirebaseUser user;
  Paintsend1(this.imgBytes,this.user);

  @override
  _Paintsend1State createState() => _Paintsend1State();
}

class _Paintsend1State extends State<Paintsend1> {
    var calledurl;
    String valueapi="";
    String fileName;
    String datetime1;
    String ID;
    BuildContext context;
    bool bool1=false;
    bool screen=true;
    var decodedurls;
    var decoded1;
    String com ="0";

    
  void urlget(String cd) async{
    // ignore: await_only_futures
    final response = await await await http.get(Uri.parse('https://flutter-graphology.herokuapp.com/upload/'+cd)); 
    print(response.body);
    final decoded = json.decode(response.body) as Map<String, dynamic>; 
    print(decoded["output"]["see"]);
    setState(() {
          com="75";
    });

    final response1 =  await http.get(Uri.parse('https://flutter-graphology.herokuapp.com/predict/'+decoded["output"]["see"]+'/'+ID)); 
    decodedurls = response1.body;
    print(response1.body);
    decoded1 =json.decode(response1.body) as Map<String, dynamic>; 
    print("decoded1-----------------------------------");
    print(decoded1["Output"]);
    setState(() {
          com="100";
          bool1=true;
          print(bool1);
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
    print(widget.user.email+"\n"+fileName+"\n"+datetime1+"\n"+valueapi);
    var result = await conn.query('insert into upload (email, name ,time, image) values (?,?,?,?)',[widget.user.email,fileName,datetime1,valueapi]);
    print('Inserted row id=${result.insertId}');
    ID = '${result.insertId}';
    print(ID);
    print(calledurl+"/"+ID);
    this.urlget(calledurl+"/"+ID);
    setState(() {
      com="50";
    });
  }



   Future uploadImageToFirebase(BuildContext context) async {
    Random random = new Random();
    int randomNumber = random.nextInt(100);
    final time = DateTime.now();
    final formatter = DateFormat(r'''dd/MM/yyyy kk:mm:ss''');
    final formatter1 = DateFormat(r'''dd_MM_yyyy_kk_mm_ss''');
    final String datetime = formatter.format(time);
    final String datetime123 = formatter1.format(time);
    this.datetime1=datetime;
    print(datetime);

    final buffer = widget.imgBytes.buffer;
    Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
    String path = appDocumentsDirectory.path;
    fileName = "inputfile"+randomNumber.toString()+datetime123;
    var filepath = File(path+"inputfile"+randomNumber.toString()+datetime123);
    print(filepath);
    final file12 = await filepath.writeAsBytes(buffer.asUint8List(widget.imgBytes.offsetInBytes,widget.imgBytes.lengthInBytes));

    String email = widget.user.email;
    StorageReference firebaseStorageRef =
        FirebaseStorage.instance.ref().child('$email'+'/$filepath');
    StorageUploadTask uploadTask = firebaseStorageRef.putFile(file12);
    StorageTaskSnapshot taskSnapshot = await uploadTask.onComplete;
    setState(() {
      com="25";
    });
    taskSnapshot.ref.getDownloadURL().then(
          (value) => this.viewer('$value'),
    );
  }



  @override
  Widget build(BuildContext context) {
    return bool1 ? Scaffold(
                        body: Stack(
                          children: <Widget>[
                            Container(
                              height: 400,
                              decoration: BoxDecoration(
                                  borderRadius: BorderRadius.only(
                                      bottomLeft: Radius.circular(50.0),
                                      bottomRight: Radius.circular(50.0)),
                                  gradient: LinearGradient(
                                      colors: [Colors.orange, Colors.yellow],
                                      begin: Alignment.topLeft,
                                      end: Alignment.bottomRight)),
                            ),
                            new SingleChildScrollView(
                                child: new Column(children:<Widget>[
                                  new Align(alignment: Alignment.bottomLeft,child: new  Text(decoded1["Output"]["time"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
                                  Text("Input Image ",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
                                  Image.network(decoded1["Output"]["inputimgurl"],height: 250,),
                                  // Text("Output Image1 :",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
                                  // Image.network(decoded1["Output"]["outputimgurl1"],height: 300,width: 400,),
                                  Text("Predicted Image ",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
                                  Image.network(decoded1["Output"]["outputimgurl2"],height: 300),
                                  
                                  new Align(alignment: Alignment.bottomCenter,child: new  Text("Personality Trait",style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.center,),),
                                  new Align(alignment: Alignment.bottomRight,child: new  Text(decoded1["Output"]["info0"]+decoded1["Output"]["info1"]+decoded1["Output"]["info2"]+decoded1["Output"]["info3"]+decoded1["Output"]["info4"]+decoded1["Output"]["info5"],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),textAlign: TextAlign.start,),),
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
                      ,)
                    :
                    Column(
                      children: [
                        Container(
                            child: Center(
                              child: Image.memory(
                              Uint8List.view(widget.imgBytes.buffer),
                              width: 700,
                              height:500,
                              )
                          ),
                        ),
                        Text(""+com+"%",style: TextStyle(color: Colors.black, fontSize: 25)),
                        RaisedButton(
                          onPressed: ()=>this.uploadImageToFirebase(context),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                          elevation: 10,
                          splashColor: Colors.redAccent,
                          color: Colors.lightBlue,
                          hoverColor: Colors.green,
                          child: Text("Predict Now",style: TextStyle(color: Colors.white, fontSize: 25)),
                        ),
                    ],);
  }
}