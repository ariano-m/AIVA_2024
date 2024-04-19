import 'package:flutter/material.dart';
import 'pickerGallery.dart';
import 'myCamera.dart';

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
                decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'IP',
                    hintText: 'Enter valid IP vision system'),
              ),
            ),

            
            Padding(
              padding: const EdgeInsets.only(left:15.0,right: 15.0,top:15,bottom: 0),
              child: TextField(
                decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: 'User',
                    hintText: 'Enter valid username'),
              ),
            ),

            Padding(
              padding: const EdgeInsets.only(left: 15.0, right: 15.0, top: 15, bottom: 0),
              child: TextField(
                obscureText: true,
                decoration: InputDecoration(
                    border: OutlineInputBorder(),
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
                    Navigator.push(context, MaterialPageRoute(builder: (_) => SecondRoute())); //move to other screen
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
                  onPressed: () {
                    takePhoto();
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
                  onPressed: (){
                    my_picker.getImage();
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