

from django.db import models

class SymptomEntry(models.Model):
    symptom_text = models.TextField()
    classification = models.CharField(max_length=50, blank=True, null=True)
    response_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Symptom: {self.symptom_text[:50]}... -> {self.classification}"

    class Meta:
        verbose_name_plural = "Symptom Entries"
        ordering = ['-timestamp']