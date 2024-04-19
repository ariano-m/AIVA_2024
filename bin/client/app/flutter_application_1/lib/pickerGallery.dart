import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';



class MyPickerGallery {
    final ImagePicker ip = ImagePicker();
    XFile? _image;

    Future getImage() async {
      try {
        final XFile? image = await ip.pickImage(source: ImageSource.gallery);
        _image = image;
      } on PlatformException catch(e) {
        print('Failed to pick image: $e');
    }
    }
}