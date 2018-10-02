from django.db import models

# Create your models here.

class MyWeatherDB(models.Model):


    City =  models.CharField(max_length=50)
    State = models.CharField(max_length=50,default='New York')
    County = models.CharField(max_length=50, default='unknown')
    Country = models.CharField(max_length=50, default='US')
    Origin = models.CharField(max_length=50)
    Destination  = models.CharField(max_length=50)

    Latitude = models.DecimalField(max_digits=9, decimal_places=6) #otherwise decimal field will through errors
    Longitude = models.DecimalField(max_digits=9, decimal_places=6)

    Humidity = models.FloatField()
    Pressure = models.FloatField()
    Temperature = models.FloatField()

    Icon = models.CharField(max_length=20)
    Description = models.CharField(max_length=300)

    def __str__(self):
        return u'%s %s %s %s' % (self.City,self.Origin, self.Destination, self.Description)
