from django.core.exceptions import ValidationError
import os


# bu fonksiyon resim dosyalarının uzantılarının ne olabileceğini ayarlamak için kullanıldı : png, jpg, jpeg harici uzantı kullanılamaz !!

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] #cover-img.jpg
    print(ext)
    valid_extensions = [ '.png','.jpg','.jpeg']

    if not ext.lower() in valid_extensions:
        raise ValidationError('Desteklenmeyen dosya uzantıları.İzin verilen uzantılar :'+ str(valid_extensions))