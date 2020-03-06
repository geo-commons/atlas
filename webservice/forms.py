from django import forms


class LayerForm(forms.ModelForm):
    _popup_attributes = forms.CharField(widget=forms.Textarea, required=False)
    _search_fields = forms.CharField(widget=forms.Textarea, required=False)
