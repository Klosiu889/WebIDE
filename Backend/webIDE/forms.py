from django import forms

from .models import Directory, File


class AddFileForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'File name',
                                      'class': 'add-name',
                                      'id': 'add-file-name'})
    )
    parent = forms.CharField(
        max_length=1000,
        widget=forms.HiddenInput(attrs={'id': 'add-file-parent'})
    )
    type = forms.CharField(
        initial='file',
        widget=forms.HiddenInput()
    )

    class Meta:
        model = File
        fields = ('name',)


class AddDirectoryForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Directory name',
                                      'class': 'add-name'})
    )
    parent = forms.CharField(
        max_length=1000,
        widget=forms.HiddenInput(attrs={'id': 'add-dir-parent'})
    )
    type = forms.CharField(
        initial='directory',
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Directory
        fields = ('name',)


class DeleteItemForm(forms.Form):
    path = forms.CharField(
        max_length=1000,
        widget=forms.HiddenInput(attrs={'id': 'delete-path'})
    )
    type = forms.CharField(
        max_length=100,
        widget=forms.HiddenInput(attrs={'id': 'delete-type'})
    )

    class Meta:
        model = Directory
        fields = ('path',)


class SaveFileForm(forms.Form):
    path = forms.CharField(
        max_length=1000,
        widget=forms.HiddenInput(attrs={'id': 'save-path'})
    )
    content = forms.CharField(
        max_length=100000,
        widget=forms.HiddenInput(attrs={'id': 'save-content'})
    )

    class Meta:
        model = File
        fields = ('path', 'content')


class CompileFileForm(forms.Form):
    file = forms.CharField(
        max_length=1000,
        widget=forms.HiddenInput(attrs={'id': 'compile-file'})
    )
    standard = forms.CharField(
        max_length=100,
        widget=forms.HiddenInput(attrs={'id': 'compile-standard'})
    )
    optimisation = forms.CharField(
        max_length=100,
        widget=forms.HiddenInput(attrs={'id': 'compile-optimisation'})
    )
    processor = forms.CharField(
        max_length=100,
        widget=forms.HiddenInput(attrs={'id': 'compile-processor'})
    )
    dependant = forms.CharField(
        max_length=100,
        widget=forms.HiddenInput(attrs={'id': 'compile-dependant'})
    )

    class Meta:
        model = File
        fields = ('path', 'content')
