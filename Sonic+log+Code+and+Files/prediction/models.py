from django.db import models

class SonicLogPrediction(models.Model):
    """
    Model to store sonic log predictions
    """
    # Input features
    cal = models.FloatField('Caliper (Inch)', help_text='Caliper measurement in inches')
    cnc = models.FloatField('Neutron (dec)', help_text='Neutron log in decimal units')
    gr = models.FloatField('Gamma Ray (API)', help_text='Gamma Ray log in API units')
    hrd = models.FloatField('Deep Resistivity (Ohm/m)', help_text='Deep resistivity in Ohm per meter')
    hrm = models.FloatField('Medium Resistivity (Ohm/m)', help_text='Medium resistivity in Ohm per meter')
    pe = models.FloatField('Photo-electric Factor (Barn)', help_text='Photo-electric factor in Barn')
    zden = models.FloatField('Density (g/m³)', help_text='Density in grams per cubic meter')
    
    # Predictions
    dtc_predicted = models.FloatField('Predicted DTC (ns/ft)', null=True, blank=True)
    dts_predicted = models.FloatField('Predicted DTS (ns/ft)', null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    prediction_method = models.CharField(
        max_length=20,
        choices=[('xgboost', 'XGBoost'), ('xgboost_wavelet', 'XGBoost with Wavelet')],
        default='xgboost_wavelet'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Sonic Log Prediction'
        verbose_name_plural = 'Sonic Log Predictions'
    
    def __str__(self):
        return f"Prediction {self.id} - DTC: {self.dtc_predicted:.2f}, DTS: {self.dts_predicted:.2f}"
