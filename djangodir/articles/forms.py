from django import forms

class PracticeForm(forms.Form):
    # text = forms.CharField(label='文字入力')
    # num = forms.IntegerField(label='数量')
    def printReflect(self):
        print("call from reflect")
    
    def printReset(self):
        print("call from reset")
