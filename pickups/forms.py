from django import forms

class DailyRoutesForm(forms.Form):
    """
    used to confirm the order of
    dailyroutes
    """
    ordering = forms.CharField()