import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:hello_world/upload2.dart';
import 'package:hello_world/results.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:hello_world/paintsig.dart';
class MyHomePage1 extends StatelessWidget {
  final FirebaseUser user1;
  MyHomePage1(this.user1);
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')), body: MyHomePage(this.user1));
  }
}

class MyHomePage extends StatefulWidget {
  final FirebaseUser user;

  MyHomePage(this.user);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var decoded1;
  int length1;
  bool showing=true;
  String emailvalue="";
  String detect="";
  void predict({user1}){
    Navigator.push(context,
              MaterialPageRoute(builder: (context) => Uploading1(user1)));
    print("predict----------------------------------------------");
  }

  void show() async{
    // ignore: await_only_futures
    emailvalue = widget.user.email;
    print(emailvalue);
    if(emailvalue==""){
      emailvalue="999";
      detect="Fetching All Users data";
    }
    final response = await await await http.get(Uri.parse('https://flutter-graphology.herokuapp.com/show/'+emailvalue));
    print(response.body);
    decoded1 = json.decode(response.body) as Map<String, dynamic>; 
    print("decoded1-----------------------------------------------------------------------");
    print(decoded1);
    print(decoded1["Output"]["0"]);
    length1= decoded1["Output"].length;
    print(length1);
    if(length1==0){
        setState(() {
          detect="There is no such user in database";
        });
      }
      print(emailvalue);
      if(length1!=0){
          setState(() {
            // showing=false;
            Navigator.push(context,
              MaterialPageRoute(builder: (context) => Result(decoded1,length1)));
          });
      }

  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body:Column(
          mainAxisAlignment:MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            Container(
            height: 220,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(50.0),
                    bottomRight: Radius.circular(50.0)),
                gradient: LinearGradient(
                    colors: [Colors.redAccent, yellow,orange],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight)),
          ),
          Image.network(widget.user.photoUrl,height: 130,width: 400,),
          Expanded(child: Text(" Welcome "+widget.user.displayName, style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),)
          ),
          Expanded(
            child:Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> predict(user1: widget.user),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("Image",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
            )
          ),
          Expanded(
            child:Column(
              children: <Widget>[
                RaisedButton(
                  onPressed: ()=> this.show(),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("History",style: TextStyle(color: Colors.white, fontSize: 25)),
                )
              ]
            )
          ),
          Expanded(
            child:Column(
              children: <Widget>[
                  RaisedButton(
                  onPressed: ()=> Navigator.push(context,
              MaterialPageRoute(builder: (context) => Paintsig(widget.user))),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                  elevation: 10,
                  splashColor: Colors.redAccent,
                  color: Colors.lightBlue,
                  hoverColor: Colors.green,
                  child: Text("Digital Pen",style: TextStyle(color: Colors.white, fontSize: 25)),
                )])),
        ],));
  }
}
