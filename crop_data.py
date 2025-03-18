CROP_DATA = {
    'rice': {
        'soil_types': ['clay', 'loamy'],
        'seasons': ['summer', 'monsoon'],
        'temp_range': (20, 35),
        'rainfall_range': (150, 300),
        'description': 'A staple grain crop that thrives in wet conditions.',
        'image_url': 'https://images.unsplash.com/photo-1530267981375-f0de937f5f13'
    },
    'wheat': {
        'soil_types': ['loamy', 'clay'],
        'seasons': ['winter'],
        'temp_range': (15, 25),
        'rainfall_range': (75, 150),
        'description': 'A hardy grain crop suitable for cooler temperatures.',
        'image_url': 'https://images.unsplash.com/photo-1528839390497-a161db4bac71'
    },
    'corn': {
        'soil_types': ['loamy', 'sandy'],
        'seasons': ['summer'],
        'temp_range': (20, 30),
        'rainfall_range': (50, 100),
        'description': 'A versatile crop that requires warm weather and moderate rainfall.',
        'image_url': 'https://images.unsplash.com/photo-1516234137022-7d61576807db'
    },
    'cotton': {
        'soil_types': ['black', 'loamy'],
        'seasons': ['summer', 'monsoon'],
        'temp_range': (25, 35),
        'rainfall_range': (50, 150),
        'description': 'A cash crop that thrives in warm weather.',
        'image_url': 'https://images.unsplash.com/photo-1527762031550-522c5d9240fd'
    }
}

def get_crop_recommendation(soil_type, season, temperature, rainfall):
    suitable_crops = []
    
    for crop, data in CROP_DATA.items():
        if (soil_type in data['soil_types'] and
            season in data['seasons'] and
            data['temp_range'][0] <= temperature <= data['temp_range'][1] and
            data['rainfall_range'][0] <= rainfall <= data['rainfall_range'][1]):
            
            suitable_crops.append({
                'name': crop.title(),
                'description': data['description'],
                'image_url': data['image_url'],
                'optimal_temp': f"{data['temp_range'][0]}°C - {data['temp_range'][1]}°C",
                'optimal_rainfall': f"{data['rainfall_range'][0]}mm - {data['rainfall_range'][1]}mm"
            })
    
    return suitable_crops
