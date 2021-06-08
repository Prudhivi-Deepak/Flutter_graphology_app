import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:hello_world/Admin.dart';
import 'package:hello_world/results.dart';


final Color yellow = Color(0xfffbc31b);
final Color orange = Color(0xfffb6900);


class Choose extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')), body: Admin1());
  }
}

class Admin1 extends StatefulWidget {
  @override
  _Admin1State createState() => _Admin1State();
}

class _Admin1State extends State<Admin1> {

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
          detect="There is no such user in database";
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


  final titleController = TextEditingController();
  String text = "";
  String pass1 = "";

  final titleController1 = TextEditingController(text: "trrtrt");
  void _setText() {
    setState(() {
      text = titleController.text;
      if (text=="root" && pass1=="root") {
          text="Successfully logging in";
          this.show();
      } 
      else {
        text = "Either Admin name or Passsword is Wrong";
      }
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
           Container(
            height: 55,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(50.0),
                    bottomRight: Radius.circular(50.0)),
                gradient: LinearGradient(
                    colors: [orange, yellow],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight)),
          ),
          SizedBox(height: 50,),
          Column(children: [
            Text('Admin Login',style: TextStyle(color: Colors.black, fontSize: 25,fontWeight: FontWeight.bold)),
          ],),
          Padding(
            padding: const EdgeInsets.all(15),
            child: TextField(
              decoration: InputDecoration(labelText: 'Admin Name',
              hintText:'Enter Your Admin Name',),
              autofocus: false,
              controller: titleController,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(15),
            child: TextField(
              decoration: InputDecoration(labelText: 'Password',
              hintText:'Enter Your Password',),
              autofocus: false,
              obscureText: false,
              onChanged: (value)=>pass1=value,
              // controller: titleController,
            ),
          ),
          SizedBox(
            height: 8,
          ),
          RaisedButton(
            onPressed: _setText,
            child: Text('Submit'),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
            elevation: 8,
            splashColor: Colors.redAccent,
            color: Colors.lightBlueAccent,
            hoverColor: Colors.green,
            padding: EdgeInsets.all(20),
          ),
          SizedBox(
            height: 20,
          ),
          Text(text),
        ],
      ),
    );
  }
}