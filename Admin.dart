import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:hello_world/results.dart';

class Admin extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')),body: Adminblog());
  }
}

class Adminblog extends StatefulWidget {
  @override
  _AdminblogState createState() => _AdminblogState();
}

class _AdminblogState extends State<Adminblog> {

  var decoded1;
  int length1;
  bool showing=true;
  String emailvalue="";
  String detect="";
  void show() async{
    // ignore: await_only_futures
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
          detect="There is no  data in database";
        });
      }
      print(emailvalue);
      if(length1!=0){
          setState(() {
            // showing=false;
            Navigator.push(context,
              MaterialPageRoute(builder: (context) => Result(decoded1,length1)));
            print("navigation");
          });
      }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold( 
      body: Column(
        mainAxisAlignment:MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [  
          Column(children: [
            Text('Admin Blog',style: TextStyle(color: Colors.black, fontSize: 25,fontWeight: FontWeight.bold)),
          ],),
          SizedBox(height: 10,),
          Text("If you want to see all users Data then Click Submit Button without Filling User's Email",style: TextStyle(color: Colors.black, fontSize: 25,fontWeight: FontWeight.bold)),
          Padding(
            padding: const EdgeInsets.all(10),
            child: TextField(
              decoration: InputDecoration(labelText: "User's Email",
              labelStyle: TextStyle(color: Colors.black, fontSize: 25,fontWeight: FontWeight.bold),
              hintText:'Enter Users Email',),
              autofocus: false,
              onChanged: (value)=>emailvalue=value,
            ),
          ),
          RaisedButton(
            onPressed: ()=> this.show(),
            child: Text('Submit'),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
            elevation: 8,
            splashColor: Colors.redAccent,
            color: Colors.lightBlueAccent,
            hoverColor: Colors.green,
            padding: EdgeInsets.all(20),
          ),
          Text(detect,style:TextStyle(color: Colors.black, fontSize: 25,fontWeight: FontWeight.bold),)
        ],
      )
      );
      
  }
}
