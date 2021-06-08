// import 'dart:html';
import 'dart:io';
import 'dart:typed_data';
import 'dart:ui';
import 'dart:ui' as ui;
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
// import 'package:flutter/services.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:hello_world/paintsend.dart';

var picture;
List<Paint> ppoints; 
List<Offset> ppoints1;

class Paintsig extends StatelessWidget {
  final FirebaseUser user;
  Paintsig(this.user);

  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text('Personality Detection')), body: Paintsignature(this.user));
  }
}
class Paintsignature extends StatefulWidget {
  final FirebaseUser user;
  Paintsignature(this.user);
  @override
  _PaintsignatureState createState() => new _PaintsignatureState();
}

class DrawingArea {
  Offset point;
  Paint areaPaint;
  DrawingArea({this.point, this.areaPaint});
}


class _PaintsignatureState extends State<Paintsignature> {
  List<Paint> _points = <Paint>[];
  List<Offset> _points1 = <Offset>[];
  Color selectedColor;
  double strokeWidth;
  ByteData imgBytes;

  @override
  void initState() {
    super.initState();
    selectedColor = Colors.black;
    strokeWidth = 2.0;
  }

  void selectColor() {
      showDialog(
        context: context,
        child: AlertDialog(
          title: const Text('Color Chooser'),
          content: SingleChildScrollView(
            child: BlockPicker(
              pickerColor: selectedColor,
              onColorChanged: (color) {
                this.setState(() {
                  selectedColor = color;
                });
              },
            ),
          ),
          actions: <Widget>[
            FlatButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text("Close"))
          ],
        ),
      );
    }

    Future<String> getFilePath() async {
        Directory appDocumentsDirectory = await getApplicationDocumentsDirectory();
        String appDocumentsPath = appDocumentsDirectory.path;
        String filePath = '$appDocumentsPath/image.png';
        print(filePath);
        return filePath;
      }


    void rendered() async{
        final recorder = ui.PictureRecorder();
        Canvas canvas = Canvas(recorder);
        for (int i = 0; i < _points1.length - 1; i++) {
          if (_points1[i] != null && _points1[i + 1] != null) {
            canvas.drawLine(_points1[i], _points1[i + 1],_points[i]);
          }
        }

        final picture = recorder.endRecording();
        final img = await picture.toImage(500, 500);
        final pngBytes = await img.toByteData(format: ImageByteFormat.png);

        print("oksighoiugh");
        setState(() {
          imgBytes = pngBytes;
          print(imgBytes);
          if(imgBytes != null){
                Navigator.push(context,MaterialPageRoute(builder: (context) => Paintsend(imgBytes,widget.user)));
          }           
        });
    }

  @override
  Widget build(BuildContext context) {
    final double width = MediaQuery.of(context).size.width;
    final double height = MediaQuery.of(context).size.height;
    return new Scaffold(
      body:
            new Stack(
              children: <Widget>[            
                  Container(
                  decoration: BoxDecoration(
                      gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [
                            Colors.deepOrangeAccent,
                        Color.fromRGBO(138, 35, 135, 1.0),
                        Color.fromRGBO(233, 64, 87, 1.0),
                        Color.fromRGBO(242, 113, 33, 1.0),
                      ])),
                  ),
                  Padding(
                        padding: const EdgeInsets.all(10.0),
                        child: Container(
                          width: width * 0.95,
                          height: height * 0.50,
                          decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.all(Radius.circular(20.0)),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.4),
                                  blurRadius: 5.0,
                                  spreadRadius: 1.0,
                                )
                              ]),
                              child: GestureDetector(
                                onPanUpdate: (DragUpdateDetails details) {
                                    setState(() {
                                      RenderBox object = context.findRenderObject();
                                      Offset _localPosition =
                                          object.globalToLocal(details.globalPosition);
                                      _points1 = new List.from(_points1)..add(_localPosition);
                                      _points.add(Paint()
                                          ..strokeCap = StrokeCap.round
                                          ..isAntiAlias = true
                                          ..color = selectedColor
                                          ..strokeWidth = strokeWidth);
                                    });
                                },
                                onPanEnd: (DragEndDetails details) { 
                                  setState(() {
                                  _points1.add(null);
                                  _points.add(null);               
                                  });
                                },                         
                                child: SizedBox.expand(
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.all(Radius.circular(20.0)),
                                    child: CustomPaint(
                                      painter: Signature(points1:_points1,points:_points),
                                      size: Size.infinite,
                                    ),
                                  ),
                                ),
                            ),
                        ),
                      ),
                  Center(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: <Widget>[
                      Container(
                        width: width * 0.80,
                        decoration: BoxDecoration(
                            color: Colors.transparent, borderRadius: BorderRadius.all(Radius.circular(20.0))),
                        child: Row(
                          children: <Widget>[
                            RaisedButton(
                              onPressed: ()=>this.rendered(),
                              child: Text('Submit'),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(45)),
                              elevation: 8,
                              splashColor: Colors.redAccent,
                              color: Colors.lightBlueAccent,
                            ),

                            IconButton(
                                icon: Icon(
                                  Icons.color_lens,
                                  color: selectedColor,
                                ),
                                onPressed: () {
                                  selectColor();
                                }),

                            Expanded(
                              child: Slider(
                                min: 1.0,
                                max: 10.0,
                                label: "Stroke $strokeWidth",
                                activeColor: selectedColor,
                                value: strokeWidth,
                                onChanged: (double value) {
                                  this.setState(() {
                                    strokeWidth = value;
                                  });
                                },
                              ),
                            ),

                            IconButton(
                                icon: Icon(
                                  Icons.layers_clear,
                                  color: Colors.black,
                                ),
                                onPressed: () {
                                  this.setState((){
                                    _points.clear();
                                    _points1.clear();
                                  });
                                }),
                          ],
                        ),
                      )
                    ],
                  ),
                ),
            
            ],
            ),
    );
  }
}

class Signature extends CustomPainter {
  List<Paint> points; 
  List<Offset> points1;

  Signature({this.points1,this.points});
  @override
  void paint(canvas, Size size) {
    for (int i = 0; i < points1.length - 1; i++) {
      if (points1[i] != null && points1[i + 1] != null) {
        canvas.drawLine(points1[i], points1[i + 1],points[i]);
        // canvas.drawLine(points1[i], points1[i + 1],points[i+1]);
      }
    }
  }
  @override
  bool shouldRepaint(Signature oldDelegate) => oldDelegate.points1 != points1;
}
