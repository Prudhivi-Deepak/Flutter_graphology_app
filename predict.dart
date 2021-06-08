import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

class Predict1 extends StatelessWidget {
  final FirebaseUser user; 
  final decodedurls1;
  Predict1(this.user, this.decodedurls1);
  @override
  Widget build(BuildContext context) {
      return Scaffold(appBar: AppBar(title: Text('Personality Detection')), body: Predict(this.user, this.decodedurls1));
  }
}

class Predict extends StatefulWidget {
  final FirebaseUser user1;
  String id;
  final decodedurls;
  Predict(this.user1,this.decodedurls);
  @override
  _PredictState createState() => _PredictState();
}

class _PredictState extends State<Predict> {


  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text('Main page')),
        body:Column(
          mainAxisAlignment:MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
          Image.network(widget.user1.photoUrl,height: 130,width: 400,),
          Image.network(widget.user1.photoUrl,height: 130,width: 400,),
          Image.network(widget.user1.photoUrl,height: 130,width: 400,),
          Expanded(child: Text(" Welcome "+widget.user1.displayName, style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),)),
          Expanded(child: Text(" Welcome "+widget.decodedurls, style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),)),

          Expanded(
            child:Column(
              children: <Widget>[
                ])),
          Expanded(
            child:Column(
              children: <Widget>[
                  ])),
        ],));
  }
}