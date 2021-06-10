from django import forms


class LayerForm(forms.ModelForm):
    _popup_attributes = forms.CharField(widget=forms.Textarea, required=False, label='Toon deze velden',
                                        help_text='Voer één veld per regel in. Bij een leeg veld worden alle velden getoond.')
    _search_fields = forms.CharField(widget=forms.Textarea, required=False, label='Doorzoek deze velden',
                                     help_text='Voer één veld per regel in. Bij een leeg veld worden alle tekstvelden doorzocht.')


class LinkedDataForm(forms.ModelForm):
    popup_attributes = forms.CharField(widget=forms.Textarea, required=False)
