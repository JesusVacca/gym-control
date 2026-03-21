from django import forms

class DatalistSelect(forms.Widget):
    template_name = 'widgets/datalist_select.html'
    def __init__(self, queryset=None, attrs=None):
        self.queryset = queryset
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['queryset'] = self.queryset
        selected = None
        if value:
            try:
                selected = self.queryset.get(id=value)
            except self.queryset.model.DoesNotExist:
                pass
        context["selected"] = selected
        return context