from django import forms
from django.utils.safestring import mark_safe


class BaseModelForm(forms.ModelForm):

    def __load_css(self):
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form__input'

    def as_custom(self):
        self.__load_css()
        html = ''
        for field, value in self.fields.items():
            html += f'''
                <div class="form__group">
                    <label class="form__label" for="{self[field].id_for_label}">{self[field].label}</label>
                    {self[field]}
                </div>
            '''

        return mark_safe(html)