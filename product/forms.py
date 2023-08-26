from django import forms

from .models import Images, Product



class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={"multiple":True}))
    
    class Meta:
        model = Images
        fields = [
            "image",
        ]



class EditProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'product_title', 'description', 'price', 'discount_price', 'category', 'subcategory', 'number_product', 'image')
