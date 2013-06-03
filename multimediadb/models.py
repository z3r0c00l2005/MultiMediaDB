from django.db import models

class Aircrafttype(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.description)
        
class Aircraftsystem(models.Model):
    WORKSHARE_CHOICES = (
        ('UK', 'UK'),
        ('IT', 'Italy'),
    )
    aircrafttype = models.ForeignKey(Aircrafttype)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    workshare = models.CharField(max_length=2, choices=WORKSHARE_CHOICES)
    status = models.CharField(max_length=25, default='Not Started')
        
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.description)

class Systemgraphic(models.Model):
    GRAPHIC_STATUS_CHOICES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Development Completed', 'Development Completed'),
        ('Tech Review Pass', 'Technical Review Passed'),
        ('Edit Review Pass', 'Editorial Review Passed'),
        ('Internal QA Pass', 'Internal QA Passed'),
        ('Uploaded LCMS', 'Uploaded to LCMS'),
        ('External Review Pass', 'External Review Passed'),
    )
    aircraftsystem = models.ForeignKey(Aircraftsystem)
    media_label = models.CharField(max_length=100)
    version= models.SmallIntegerField(default='00')
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    adjusted_hours = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=25, choices=GRAPHIC_STATUS_CHOICES, default='Not Started')
    on_hold = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'%s - %s' % (self.title, self.description)
        