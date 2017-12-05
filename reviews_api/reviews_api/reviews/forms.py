from django import forms
#from pagedown.widgets import PagedownWidget
from .models import Reviews


class ReviewsForm(forms.ModelForm):
    content = forms.CharField()
    publish = forms.DateField()
    class Meta:
        model = Reviews
        fields = [
            "company",
            "pub_date",
            "user_name",
            #"ip_address",
            "comment",
            "rating",
            "publish",
        ]