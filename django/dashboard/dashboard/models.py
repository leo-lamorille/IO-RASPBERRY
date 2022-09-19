from django.db import models

class sensor(models.Model):

    #Fields 

    macAddress = models.CharField(max_length=19, primary_key = True)
    name = models.TextField(blank = True, null = True)
    interval = models.IntegerField()	

    #Meta
    class Meta:
        ordering = ['name']

    
    #Methods 
    def __str__(self):
        return self.name

class datas(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    sensor = models.ForeignKey(sensor, on_delete = models.CASCADE)	
    t_stamp =models.BigIntegerField()
    value = models.BigIntegerField()

    # Metadata
    class Meta:
        ordering = ['t_stamp']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.sensor
       
