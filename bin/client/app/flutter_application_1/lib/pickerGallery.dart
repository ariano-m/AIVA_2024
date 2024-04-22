import 'package:image_picker/image_picker.dart';
import 'package:flutter/services.dart';
import 'dart:io';

/// A class used for getting photos from gallery's phone
class MyPickerGallery {
    final ImagePicker ip = ImagePicker();
    var image;


    /// function for picking an image and reading like a list of bytes.
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