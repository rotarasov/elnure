from django import forms

from utils import get_start_year_by_group_name


class StudentGroupForm(forms.ModelForm):
    def populate_start_year(self):
        self.instance.start_year = get_start_year_by_group_name(self.instance.name)

    def save(self, commit):
        self.populate_start_year()
        return super().save(commit)
