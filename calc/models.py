from django.db import models

# Create your models here.
class CalculationHistory(models.Model):
    question = models.CharField(max_length=100)
    answer = models.FloatField()

    def __str__(self):
        return f"Question: {self.question}, Answer: {self.answer}"