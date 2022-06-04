from django import forms


class StudentGroupForm(forms.ModelForm):
    def populate_start_year(self):
        self.instance.start_year = self.instance.calculate_start_year()

    def save(self, commit):
        self.populate_start_year()
        return super().save(commit)
