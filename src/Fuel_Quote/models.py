from django.db import models
from django.conf import settings
from users.models import Profile, Address


class Quote(models.Model):
    id = models.AutoField(primary_key=True)
    profileId = models.ForeignKey(Profile, on_delete=models.CASCADE)
    gallons = models.PositiveIntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    total = models.DecimalField(decimal_places=2, max_digits=20)

    def __str__(self):
        return f"Quote ID: {self.id}  requested by: {self.profileId}"
