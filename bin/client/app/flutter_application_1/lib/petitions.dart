import 'package:http/http.dart' as http;
//import 'package:image/image.dart';
import 'dart:convert';
import 'dart:io';

Future<void> sendImageToServer() async {
  final String path = '/Users/arm/PycharmProjects/MUVA/INDUSTRIALES/AIVA_2024_MADERAS/dataset/MuestrasMaderas/01.png';
  final File imageFile = File(path);
  final List<int> bytes = await imageFile.readAsBytes();
  print(await imageFile.length());
  final String base64Image = base64Encode(bytes);

  //final image = decodeImage(await imageFile.readAsBytes())!;
  //final String base64Image = base64.encode(encodePng(image));

  final String url = 'http://localhost:5005/image';
  final Map<String, String> headers = {'content-type': 'application/octet-stream'};

  final http.Response response = await http.post(
    Uri.parse(url),
    headers: headers,
    body: base64Image,
  );

  print(response.statusCode);
}

