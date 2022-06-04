from django import forms

from elnure_core.models import Block
from utils import get_study_year_by_semester


class SemesterForm(forms.ModelForm):
    blocks = forms.ModelMultipleChoiceField(Block.objects, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial["blocks"] = self.instance.blocks.all()

    def populate_study_year(self):
        self.instance.study_year = get_study_year_by_semester(self.instance.id)

    def _save_m2m(self):
        if "blocks" in self.changed_data:
            self.instance.blocks.set(self.cleaned_data["blocks"])
        return super()._save_m2m()

    def save(self, commit):
        self.populate_study_year()
        return super().save(commit)
