from django import forms
from .models import User,UserProfile
from .validators import allow_only_images_validator

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','password']

    def clean(self):
        cleaned_data = super(UserRegisterForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password does not match !')

class UserProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start Typing ...','required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    cover_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])

    ###### google maps kullanıldığı zaman latitude ve longitude alanları readonly yani sadece okunur olacak müdahele engellenecek ###

    # latitude  = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude  = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = UserProfile   
        fields = ['profile_picture','cover_picture','city','address','state','country','pin_code','latitude','longitude']
    
    # latitude ve longitude alanları sadece okunur şekilde ayarlamak için

    # def __init__(self,*args,**kwargs):
    #     super(UserProfileForm,self).__init__(*args,**kwargs)
    #     for field in self.fields:
    #         if field == 'latitude' or field == 'longitude':
    #             self.fields[field].widget.attrs['readonly'] = 'readonly'



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']

