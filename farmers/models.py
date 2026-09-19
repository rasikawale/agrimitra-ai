from django.db import models

# Create your models here.



class Farmer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="Maharashtra")
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
class Farm(models.Model):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        related_name='farms'
    )

    farm_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    soil_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farm_name} - {self.farmer.name}"