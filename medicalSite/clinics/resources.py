from import_export import resources, fields, widgets

from doctors.models import Doctor
from .models import Clinic, ClinicLanguages, Country, Currency, Language, RankingClinics, category_choices

from treatment.models import Treatment

# import ForeignKeyWidget from django-import-export
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

class ClinicCountryForeignKeyWidget(ForeignKeyWidget):
    def __init__(self, model, field='country', *args, **kwargs):
        super().__init__(model, field, *args, **kwargs)
        self.model = model
        
    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.filter(language__code=row['language'])

class ClinicResource(resources.ModelResource):
    language = fields.Field(column_name='language',attribute='language', widget=ForeignKeyWidget(Language, 'code'))
    country = fields.Field(column_name='country',attribute='country', widget=ClinicCountryForeignKeyWidget(model = Country, field ='name'))
    clinic_languages = fields.Field(widget=ManyToManyWidget(ClinicLanguages, field='name'), attribute='clinic_languages')

    class Meta:
        model = Clinic
        fields = ('code', 'name', 'city', 'score')
        exclude = ('id',)
        import_id_fields = ('code', 'name', 'city', 'score', 'language', 'country')


class ChoicesWidget(widgets.Widget):
    """
    Widget that uses choice display values in place of database values
    """
    def __init__(self, choices, *args, **kwargs):
        """
        Creates a self.choices dict with a key, display value, and value,
        db value, e.g. {'Chocolate': 'CHOC'}
        """
        self.choices = dict(choices)
        self.revert_choices = dict((v, k) for k, v in self.choices.items())

    def clean(self, value, row=None, *args, **kwargs):
        """Returns the db value given the display value"""
        return self.revert_choices.get(value, value) if value else None

    def render(self, value, obj=None):
        """Returns the display value given the db value"""
        return self.choices.get(value, '')


class ClinicRankingResource(resources.ModelResource):
    language = fields.Field(column_name='language',attribute='language', widget=ForeignKeyWidget(Language, 'code'))
    category = fields.Field(widget=ChoicesWidget(category_choices), attribute='category')
    class Meta:
        model = RankingClinics
        fields = ('country', 'code', 'name', 'city', 'feedback_score', 'quality_score', 'final_score')
        exclude = ('id',)
        import_id_fields = ('code', 'name', 'city', 'language', 'category', 'feedback_score', 'quality_score', 'final_score', 'country')


class TreatmentForeignKeyWidget(ForeignKeyWidget):
    def __init__(self, model=Clinic, field='code', *args, **kwargs):
        super().__init__(model, field, *args, **kwargs)
        self.model = model
        
    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.filter(language__code=row['language'])





class TreatmentResource(resources.ModelResource):
    currency = fields.Field(column_name='currency',attribute='currency', widget=ForeignKeyWidget(Currency, 'name'))
    language = fields.Field(column_name='language',attribute='language', widget=ForeignKeyWidget(Language, 'code'))
    clinic = fields.Field(column_name='clinic',attribute='clinic', widget=TreatmentForeignKeyWidget(Clinic, 'code'))

    class Meta:
        model = Treatment
        fields = ('searched_treatment', 'price_type', 'price', 'package_info_1', 'package_info_2', 'package_info_3', 'package_info_4')
        exclude = ('id',)
        import_id_fields = ('searched_treatment', 'price_type', 'price', 'package_info_1', 'package_info_2', 'package_info_3', 'package_info_4', 'currency', 'language', 'clinic')



class DoctorResource(resources.ModelResource):
    language = fields.Field(column_name='language',attribute='language', widget=ForeignKeyWidget(Language, 'code'))
    clinic = fields.Field(column_name='clinic',attribute='clinic', widget=TreatmentForeignKeyWidget(Clinic, 'code'))

    class Meta:
        model = Doctor
        fields = ('name', 'description')
        exclude = ('id',)
        import_id_fields = ('name','language', 'clinic', 'description')


class CountryResource(resources.ModelResource):
    language = fields.Field(column_name='language',attribute='language', widget=ForeignKeyWidget(Language, 'code'))
    class Meta:
        model = Country
        fields = ('name', 'phone_code')
        exclude = ('id',)
        import_id_fields = ('name', 'phone_code', 'language')