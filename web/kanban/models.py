from django.db import models

class KanbanColumn(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    order_index = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'kanban_columns'
        verbose_name = "Colonne"
        verbose_name_plural = "Colonnes"
        ordering = ['order_index']

    def __str__(self):
        return self.name or f"Column {self.id}"


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    color = models.CharField(max_length=20, default="#CCCCCC")

    class Meta:
        managed = False
        db_table = 'tags'
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name or f"Tag {self.id}"


class Activity(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    column = models.ForeignKey(KanbanColumn, on_delete=models.SET_NULL, blank=True, null=True, related_name='activities')
    tags = models.ManyToManyField(Tag, db_table='activity_tags', blank=True)

    class Meta:
        managed = False
        db_table = 'activities'
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['date']

    def __str__(self):
        return self.name or f"Activity {self.id}"

    @property
    def urgency_class(self):
        from datetime import date, timedelta
        if not self.date:
            return ""
        
        today = date.today()
        # Red: Overdue (date < today)
        if self.date < today:
            return "border-red"
        # Orange: <= 15 days remaining
        if self.date <= today + timedelta(days=15):
            return "border-orange"
        # Yellow: <= 30 days remaining
        if self.date <= today + timedelta(days=30):
            return "border-yellow"
        
        return ""


class Scelle(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True, related_name='scelles')
    cta_validated = models.BooleanField(default=False)
    reparations_validated = models.BooleanField(default=False)
    reparations_details = models.TextField(blank=True, null=True)
    important_info = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, db_table='scelle_tags', blank=True)

    class Meta:
        managed = False
        db_table = 'scelles'
        verbose_name = "Scellé"
        verbose_name_plural = "Scellés"

    def __str__(self):
        return self.name or f"Scelle {self.id}"


class Traitement(models.Model):
    description = models.TextField()
    scelle = models.ForeignKey(Scelle, on_delete=models.CASCADE, blank=True, null=True, related_name='traitements')
    done = models.BooleanField(default=False)
    done_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traitements'
        verbose_name = "Traitement"
        verbose_name_plural = "Traitements"

    def __str__(self):
        return self.description[:50]


class Tache(models.Model):
    description = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    scelle = models.ForeignKey(Scelle, on_delete=models.CASCADE, blank=True, null=True, related_name='taches')
    done_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taches'
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"

    def __str__(self):
        return self.description[:50]
