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
