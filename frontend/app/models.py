from django.db import models


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"Item(id={self.id}, name={self.name}, quantity={self.quantity})"
