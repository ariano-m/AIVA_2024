import 'package:http/http.dart' as http;
import 'dart:typed_data';
import 'dart:convert';

/// Send an [img] to specific [ip] belongs to visual system
Future<Uint8List> sendImageToServer(img, ip) async {
  if (img == null) {
    return Uint8List.fromList([]);
  }

  Uint8List output;

  final String base64Image = base64Encode(img);
  final String url = ip;//'http://10.0.2.2:5005/image';
  final Map<String, String> headers = {'content-type': 'application/octet-stream'};

  final http.Response response = await http.post(
    Uri.parse(url),
    headers: headers,
    body: base64Image,
  );

  print('Request: ${response.statusCode}');
  
  if (response.statusCode == 200) {
    print(response.body);
    output = base64Decode(response.body);
    print(output.length);    
  } else {
    print('Request failed with status: ${response.statusCode}');
    output = Uint8List.fromList([]);
  }

  return output;

}

