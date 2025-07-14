# classifier_app/models.py

from django.db import models

class SymptomEntry(models.Model):
    """
    Model to store each symptom entry and its classification,
    now including additional AI-generated details.
    """
    symptom_text = models.TextField()
    classification = models.CharField(max_length=50, blank=True, null=True)
    response_message = models.TextField(blank=True, null=True) # Primary response from the specific node
    timestamp = models.DateTimeField(auto_now_add=True)

    # New fields to store AI-generated content
    detailed_info = models.TextField(blank=True, null=True)
    # Storing list of questions as JSON string
    follow_up_questions_json = models.TextField(blank=True, null=True)
    initial_advice = models.TextField(blank=True, null=True)
    conversation_summary = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Symptom: {self.symptom_text[:50]}... -> {self.classification}"

    class Meta:
        verbose_name_plural = "Symptom Entries"
        ordering = ['-timestamp']
