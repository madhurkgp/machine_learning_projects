from django.db import models

class PredictionHistory(models.Model):
    depth = models.FloatField()
    gr = models.FloatField()
    rhob = models.FloatField()
    vp = models.FloatField()
    vsh = models.FloatField()
    caliper = models.FloatField()
    porosity = models.FloatField()
    resistivity = models.FloatField()
    stress = models.FloatField()
    predicted_pp = models.FloatField()
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction at {self.depth}m: {self.predicted_pp:.2f} PSI"
