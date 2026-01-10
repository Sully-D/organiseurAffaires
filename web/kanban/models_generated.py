# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activities(models.Model):
    id = models.AutoField()
    name = models.CharField(blank=True, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    column = models.ForeignKey('KanbanColumns', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activities'


class ActivityTags(models.Model):
    activity = models.ForeignKey(Activities, models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_tags'


class KanbanColumns(models.Model):
    id = models.AutoField()
    name = models.CharField(unique=True, blank=True, null=True)
    order_index = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kanban_columns'


class ScelleTags(models.Model):
    scelle = models.ForeignKey('Scelles', models.DO_NOTHING, blank=True, null=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scelle_tags'


class Scelles(models.Model):
    id = models.AutoField()
    name = models.CharField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activities, models.DO_NOTHING, blank=True, null=True)
    cta_validated = models.BooleanField(blank=True, null=True)
    reparations_validated = models.BooleanField(blank=True, null=True)
    reparations_details = models.TextField(blank=True, null=True)
    important_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scelles'


class Taches(models.Model):
    id = models.AutoField()
    description = models.CharField()
    done = models.BooleanField(blank=True, null=True)
    scelle = models.ForeignKey(Scelles, models.DO_NOTHING, blank=True, null=True)
    done_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taches'


class Tags(models.Model):
    id = models.AutoField()
    name = models.CharField(unique=True, blank=True, null=True)
    color = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'


class Traitements(models.Model):
    id = models.AutoField()
    description = models.TextField()
    scelle = models.ForeignKey(Scelles, models.DO_NOTHING, blank=True, null=True)
    done = models.BooleanField(blank=True, null=True)
    done_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traitements'
