import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:hello_world/myHomePage.dart';
import 'auth.dart';
import 'chose.dart';

class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')), body: Body());
  }
}

class Body extends StatefulWidget {
  @override
  _BodyState createState() => _BodyState();
}

class _BodyState extends State<Body> {
  FirebaseUser user;

  @override
  void initState() {
    super.initState();
    signOutGoogle();
  }

  void click() {
    signInWithGoogle().then((user) => {
          this.user = user,
          Navigator.push(context,
              MaterialPageRoute(builder: (context) => MyHomePage1(user)))
        });
    print("login-----------------------------------------");
    print(user);
  }

  void admin(){
    Navigator.push(context,
              MaterialPageRoute(builder: (context) => Choose()));
  }

  Widget googleLoginButton() {
    return Column(
        mainAxisAlignment:MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
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
          SizedBox(height: 10,),
          Column(
            mainAxisAlignment:MainAxisAlignment.end,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
            Text("User Login",style: TextStyle(color: Colors.black, fontSize: 25,fontWeight: FontWeight.bold)),
          ],),
          SizedBox(height: 10,),
          OutlineButton(
          onPressed: this.click,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
          splashColor: Colors.grey,
          borderSide: BorderSide(color: Colors.grey),
          child: 
          Padding(
              padding: EdgeInsets.fromLTRB(5, 10, 0, 10),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Image(image: AssetImage('assets/google_logo.png'), height: 35),
                  Padding(
                      padding: EdgeInsets.only(left: 10),
                      child: Text('Sign in with Google',
                          style: TextStyle(color: Colors.grey, fontSize: 25)))
                ],
              )
          )
        ),
        SizedBox(height: 15,),
        // Column(
        //     mainAxisAlignment:MainAxisAlignment.end,
        //     crossAxisAlignment: CrossAxisAlignment.end,
        //     children: [
        //     Text("Go to Admin Login",style: TextStyle(color: Colors.black, fontSize: 25,fontWeight: FontWeight.bold)),
        //   ],),
          SizedBox(height: 10,),
          RaisedButton(
            onPressed: ()=> this.admin(),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
            elevation: 10,
            splashColor: Colors.redAccent,
            color: Colors.lightBlue,
            hoverColor: Colors.green,
            padding: EdgeInsets.all(18),
            child: Text("Admin Login",style: TextStyle(color: Colors.white, fontSize: 25)),
          ),
          SizedBox(height: 10,),
          Container(
            height: 200,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(50.0),
                    topRight: Radius.circular(50.0),
                    bottomLeft: Radius.circular(50.0),
                    bottomRight: Radius.circular(50.0)),
                gradient: LinearGradient(
                    colors: [Colors.redAccent, yellow,orange],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight)),
          ),
         
    ],);
  }

  @override
  Widget build(BuildContext context) {
    return Align(alignment: Alignment.center, child: googleLoginButton());
  }
}
