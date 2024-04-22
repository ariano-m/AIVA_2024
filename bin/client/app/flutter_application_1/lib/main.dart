import 'package:path_provider/path_provider.dart';
import 'package:flutter/material.dart';
import 'pickerGallery.dart';
import 'dart:typed_data';
import 'petitions.dart';
import 'myCamera.dart' as myCamera;
import 'dart:io';

String IP = "http://10.0.2.2:5005/image";

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoginDemo(),
    );
  }
}

class LoginDemo extends StatefulWidget {
  @override
  _LoginDemoState createState() => _LoginDemoState();
}

class _LoginDemoState extends State<LoginDemo> {
  TextEditingController userController = TextEditingController();  
  TextEditingController passwordController = TextEditingController();  
  TextEditingController ipController = TextEditingController();  

  var _userError = null;
  var _passwordError = null;
  var _ipError = null;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      
      appBar: AppBar(title: Text("Login Page"),),
      
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            
            Padding(
              padding: const EdgeInsets.only(top: 10.0),
              child: Center(
                child: Container(
                  width: 200,
                  height: 100,
                  child: Image.asset('./assets/images/logo.png'),
                ),
              ),
            ),

            Padding(
              padding: EdgeInsets.symmetric(horizontal: 15),
              child: TextField(
                controller: ipController,
                decoration: InputDecoration(
                    errorText: this._ipError,
                    border: OutlineInputBorder(),
                    labelText: 'IP',
                    hintText: 'Enter valid IP like http://localhost:5005'),
              ),
            ),

            
            Padding(
              padding: const EdgeInsets.only(left:15.0,right: 15.0,top:15,bottom: 0),
              child: TextField(
                controller: userController,
                decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    errorText: this._userError,
                    labelText: 'User',
                    hintText: 'Enter valid username'),
              ),
            ),

            Padding(
              padding: const EdgeInsets.only(left: 15.0, right: 15.0, top: 15, bottom: 0),
              child: TextField(
                controller: passwordController,
                obscureText: true,
                decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    errorText: this._passwordError,
                    labelText: 'Password',
                    hintText: 'Enter secure password'),
              ),
            ),
           
            TextButton(
              onPressed: (){}, //habrá que llamar a la nueva pantalla
              child: Text(
                'Forgot Password',
                style: TextStyle(color: Color(0xFF2196F3), fontSize: 15),
              ),
            ),


            Container(
              height: 50,
              width: 250,
              decoration: BoxDecoration(color: Colors.blue, borderRadius: BorderRadius.circular(20)),
              child: TextButton(
                onPressed: () {
                  if (this.ipController.text.isEmpty) {
                    setState(() {
                      this._ipError = 'Please enter your ip';
                    });
                  } else {
                    this._ipError = null;
                  }

                  if (this.userController.text.isEmpty) {
                    setState(() {
                      this._userError = 'Please enter your user';
                    });
                  } else {
                    this._userError = null;
                  }


                  if (this.passwordController.text.isEmpty) {
                    setState(() {
                      this._passwordError = 'Please enter your password';
                    });
                  } else {
                    this._passwordError = null;
                  }


                  if (this.userController.text == 'user1234' &&
                      this.passwordController.text == '1234'){
                      myCamera.IP = this.ipController.text + '/image';
                      IP = this.ipController.text + '/image';
                      Navigator.push(context, MaterialPageRoute(builder: (_) => SecondRoute())); //move to other screen
                  } 
                },
                child: Text('Login', style: TextStyle(color: Colors.white, fontSize: 25),),
              ),
            ),
            
            SizedBox(height: 130,),
            Text('New User? Create Account')
          ],
        ),
      ),
    );
  }
}


class SecondRoute extends StatelessWidget {
  final my_picker = MyPickerGallery();

  SecondRoute();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Actions screen'),
      ),
      
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
              width: 200, // Adjust size as needed
              height: 200, // Adjust size as needed
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.blue,
              ),
              child: Center(
                child: TextButton(
                  onPressed: () async {
                    await myCamera.takePhoto(IP);
                    //await sendImageToServer(my_picker.image, IP);
                  },
                  child: Text('Capture photo', style: TextStyle(color: Colors.white, fontSize: 24),),
                )
              ),
            ),
            
            SizedBox(height: 60), // Adjust spacing between circles
            Container(
              width: 200, // Adjust size as needed
              height: 200, // Adjust size as needed
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Color.fromRGBO(7, 24, 196, 100),
              ),
              child: Center(
                child: TextButton(
                  onPressed: () async {
                    var response = Uint8List.fromList([]);
                    try {
                      await my_picker.getImage();
                      response = await sendImageToServer(my_picker.image, IP);
                      Navigator.push(context, MaterialPageRoute(builder: (_) => Result(image: response,)));
                    } catch(e) {
                      print("error in sendImageToServer");
                      Navigator.push(context, MaterialPageRoute(builder: (_) => SecondRoute()));
                    }
                  },
                  child: Text('Gallery', style: TextStyle(color: Colors.white, fontSize: 24),),
                ),
              ),
            ),
            SizedBox(height: 20), // Adjust spacing between circles
          ],
        ),
      ),
    );
  }
}



class Result extends StatelessWidget {
  final Uint8List image;

  Result({required this.image});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
    home: Scaffold(
              appBar: AppBar(
                  title: const Text(
                      'Result',
                  ),
              ),
              body: Center(
                  child: Column(
                      children: <Widget>[
                          SizedBox(height: 20,),
                          Image.memory(this.image,
                          height: 200,
                          scale: 2.5,
                          ),

                          Padding(
                          padding: const EdgeInsets.only(left:15.0,right: 15.0,top:100,bottom: 0),
                          /*child: Container(
                            width: 200, // Adjust size as needed
                            height: 200, // Adjust size as needed
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: Colors.lightGreen,
                            ),*/
                            child: Center(
                              child: ElevatedButton(
                                onPressed: () async {
                                  //final downloadsDirectory = await getDownloadsDirectory();
                                  String downloadsPath = '/storage/emulated/0/Download';
                                  DateTime _now = DateTime.now();
                                  final String name_image = 'maderas_${_now.hour}${_now.minute}${_now.second}${_now.millisecond}.png';
                                  File file = File(downloadsPath + '/' + name_image);
                                  var newFile = await file.writeAsBytes(image);
                                  await newFile.create();
                                  //File(downloadsPath + '/' + name_image).writeAsBytes(image);
                                  Navigator.push(context, MaterialPageRoute(builder: (_) => SecondRoute())); //move to other screen
                                },
                                child: Text('Finish', style: TextStyle(color: Colors.white, fontSize: 24),),
                                style: ElevatedButton.styleFrom(
                                  shape: CircleBorder(),
                                  padding: EdgeInsets.all(100),
                                  backgroundColor: Colors.green, // <-- Button color
                                  foregroundColor: Colors.greenAccent, // <-- Splash color
                                ),
                              )
                            ),
                          ),
                      ],
                    ),
                  ),
              ),
          );
      }
}


