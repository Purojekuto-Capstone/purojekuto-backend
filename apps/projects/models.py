from django.db import models
from simple_history.models import HistoricalRecords
from django.utils.timezone import now

class ProjectCategory(models.Model):
    # Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('State', default = True)
    created_date = models.DateField('Creation date', auto_now = False, auto_now_add = True)
    modified_date = models.DateField('Modified date', auto_now = True, auto_now_add = False)
    deleted_date = models.DateField('Delete', auto_now = True, auto_now_add = False)

    project_category_name = models.CharField('Descripcion', max_length = 50, unique = True, null = False, blank = False)

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
        return self.project_category_name
class Project(models.Model):
    # Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('State', default = True)
    created_date = models.DateField('Creation date', auto_now = False, auto_now_add = True)
    modified_date = models.DateField('Modified date', auto_now = True, auto_now_add = False)
    deleted_date = models.DateField('Delete', auto_now = True, auto_now_add = False)

    project_name = models.CharField(max_length=30)
    project_category = models.ForeignKey(ProjectCategory, on_delete = models.CASCADE, verbose_name = "Project Category")
    is_recurrent = models.BooleanField('Recurrent Project', default = False)
    start_date = models.DateField()
    end_date = models.DateField()
    work_time = models.DurationField(default=None)
    break_time = models.DurationField(default=None)

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
class ActivityCategory(models.Model):
    # Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('State', default = True)
    created_date = models.DateField('Creation date', auto_now = False, auto_now_add = True)
    modified_date = models.DateField('Modified date', auto_now = True, auto_now_add = False)
    deleted_date = models.DateField('Delete', auto_now = True, auto_now_add = False)

    activity_category_name = models.CharField('Descripcion', max_length = 50, unique = True, null = False, blank = False)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Activity Category'
        verbose_name_plural = 'Activities Categories'

    def __str__(self):
        return self.activity_category_name
class Activity(models.Model):
    # Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('State', default = True)
    created_date = models.DateField('Creation date', auto_now = False, auto_now_add = True)
    modified_date = models.DateField('Modified date', auto_now = True, auto_now_add = False)
    deleted_date = models.DateField('Delete', auto_now = True, auto_now_add = False)

    activity_name = models.CharField(max_length=30)
    activity_category = models.ForeignKey(ActivityCategory, on_delete = models.CASCADE, verbose_name = "Project Category")
    is_recurrent = models.BooleanField('Recurrent Project', default = False)
    start_date = models.DateField()
    end_date = models.DateField()

    historical = HistoricalRecords()

    @property
    def _history_date(self):
        return self.__history_date

    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = value
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        """Unicode representation of Product."""
        return self.activity_name