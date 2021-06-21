from django.db import models
from simple_history.models import HistoricalRecords

class Project(models.Model):

    # Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('State', default = True)
    created_date = models.DateField('Creation date', auto_now = False, auto_now_add = True)
    modified_date = models.DateField('Modified date', auto_now = True, auto_now_add = False)
    deleted_date = models.DateField('Delete', auto_now = True, auto_now_add = False)

    project_name = models.CharField(max_length=30)
    category_project = model.ForeignKey(ProjectCategory, on_delete = models.CASCADE, verbose_name = "Project Category")
    historical = HistoricalRecords()

    @property
    def _history_date(self):
        return self.__history_date

    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = value
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        """Unicode representation of Product."""
        return self.project_name

class ProjectCategory(model.Model):

    # Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('State', default = True)
    created_date = models.DateField('Creation date', auto_now = False, auto_now_add = True)
    modified_date = models.DateField('Modified date', auto_now = True, auto_now_add = False)
    deleted_date = models.DateField('Delete', auto_now = True, auto_now_add = False)

    category_name = models.CharField('Descripcion', max_length = 50, unique = True, null = False, blank = False)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:

        verbose_name = 'Project Category'
        verbose_name_plural = 'Projects Categories'

    def __str__(self):
        return self.category_name