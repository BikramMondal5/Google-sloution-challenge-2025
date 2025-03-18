import numpy as np
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

class CropMLService:
    def __init__(self):
        # Initialize label encoders for categorical data
        self.soil_encoder = LabelEncoder()
        self.season_encoder = LabelEncoder()
        
        # Train encoders with possible values
        self.soil_encoder.fit(['clay', 'loamy', 'sandy', 'black'])
        self.season_encoder.fit(['summer', 'winter', 'monsoon'])
        
        # Define optimal conditions for each crop (based on domain knowledge)
        self.crop_conditions = {
            'rice': {
                'temp_range': (20, 35),
                'rainfall_range': (150, 300),
                'soil_preference': ['clay', 'loamy'],
                'season_preference': ['summer', 'monsoon']
            },
            'wheat': {
                'temp_range': (15, 25),
                'rainfall_range': (75, 150),
                'soil_preference': ['loamy', 'clay'],
                'season_preference': ['winter']
            },
            'corn': {
                'temp_range': (20, 30),
                'rainfall_range': (50, 100),
                'soil_preference': ['loamy', 'sandy'],
                'season_preference': ['summer']
            },
            'cotton': {
                'temp_range': (25, 35),
                'rainfall_range': (50, 150),
                'soil_preference': ['black', 'loamy'],
                'season_preference': ['summer', 'monsoon']
            }
        }

    def calculate_crop_scores(self, soil_type, season, temperature, rainfall):
        """Calculate suitability scores for each crop based on conditions."""
        scores = {}
        
        for crop, conditions in self.crop_conditions.items():
            # Initialize base score
            score = 100
            
            # Temperature suitability
            temp_min, temp_max = conditions['temp_range']
            if temperature < temp_min or temperature > temp_max:
                temp_penalty = min(40, abs(temperature - (temp_min + temp_max) / 2) * 4)
                score -= temp_penalty
            
            # Rainfall suitability
            rain_min, rain_max = conditions['rainfall_range']
            if rainfall < rain_min or rainfall > rain_max:
                rain_penalty = min(30, abs(rainfall - (rain_min + rain_max) / 2) / 5)
                score -= rain_penalty
            
            # Soil type suitability
            if soil_type not in conditions['soil_preference']:
                score -= 20
            
            # Season suitability
            if season not in conditions['season_preference']:
                score -= 25
            
            scores[crop] = max(0, score)  # Ensure score doesn't go below 0
        
        return scores

    def get_crop_recommendations(self, soil_type, season, temperature, rainfall):
        """Get crop recommendations with confidence scores."""
        # Calculate scores for all crops
        scores = self.calculate_crop_scores(soil_type, season, temperature, rainfall)
        
        # Sort crops by score
        sorted_crops = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top recommendations with high confidence
        recommendations = []
        for crop, score in sorted_crops:
            if score >= 60:  # Only recommend crops with decent confidence
                recommendations.append({
                    'name': crop.title(),
                    'confidence': f"{score:.1f}%",
                    'description': CROP_DATA[crop]['description'],
                    'image_url': CROP_DATA[crop]['image_url'],
                    'optimal_temp': f"{self.crop_conditions[crop]['temp_range'][0]}°C - {self.crop_conditions[crop]['temp_range'][1]}°C",
                    'optimal_rainfall': f"{self.crop_conditions[crop]['rainfall_range'][0]}mm - {self.crop_conditions[crop]['rainfall_range'][1]}mm"
                })
        
        return recommendations

# Import crop data from existing module
from crop_data import CROP_DATA
