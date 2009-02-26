from django import forms

class PostEntryForm(forms.Form):
    content = forms.CharField(max_length=140)

class FollowForm(forms.Form):
    users = forms.CharField(max_length=200)

class EditProfileForm(forms.Form):
    jid = forms.CharField(max_length=255, label="XMPP Account", required=False)

