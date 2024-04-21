import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';


class MyPickerGallery {
    final ImagePicker ip = ImagePicker();
    var image;

    Future getImage() async {
      try {
        final XFile? image = await ip.pickImage(source: ImageSource.gallery);
        File imageFile = File(image!.path);
        Uint8List imageRaw = await imageFile.readAsBytes();
        this.image = imageRaw;
      } on PlatformException catch(e) {
        print('Failed to pick image: $e');
    }
    }
}