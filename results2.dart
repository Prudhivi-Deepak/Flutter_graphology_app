import 'dart:ffi';
import 'package:flutter/material.dart';
import 'package:hello_world/results3.dart';

class Result1 extends StatelessWidget {
  int length1;
  var decoded1;
  String email;
  Result1(this.decoded1, this.length1,this.email);

  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')),body: Resultblog1(this.decoded1, this.length1,this.email));
  }
}

// ignore: must_be_immutable
class Resultblog1 extends StatefulWidget {
  int length1;
  var decoded1;
    String email;
  Resultblog1(this.decoded1, this.length1,this.email);
  @override
  _Resultblog1State createState() => _Resultblog1State();
}

class _Resultblog1State extends State<Resultblog1> {

  List<String> dates = [];
  @override
  void initState(){
    super.initState();
    for(var i=0;i<widget.length1;i++){
      if(widget.email==widget.decoded1["Output"][i.toString()]["email"]){
        if(dates.contains(widget.decoded1["Output"][i.toString()]["time"])){
            print("present");
          }
        else{
            dates.add(widget.decoded1["Output"][i.toString()]["time"]);
        }
      }
    }
    print(dates.length);
  }


  @override
  Widget build(BuildContext context) {
    return 
        ListView.builder(
          itemCount: dates.length,
          itemBuilder: (context,index){
            return Card(
              child:ListTile(
                  title: Text(dates[index],style: TextStyle(fontSize: 20,fontWeight: FontWeight.bold),),
                  leading:Icon(Icons.timer),
                  trailing:IconButton(
                      icon:Icon(Icons.arrow_forward),
                      onPressed:()=> Navigator.push(context,
                        MaterialPageRoute(builder: (context)=>Result2(widget.decoded1,widget.length1,widget.email,dates[index]))),
                      ),
                ),
            );
          }
        );
  }
}