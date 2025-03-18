import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array

# Define common plant diseases and their characteristics
PLANT_DISEASES = {
    'mosaic_virus': {
        'name': 'Mosaic Virus',
        'description': 'A viral disease causing mottled patterns of yellow and green on leaves.',
        'treatment': 'Remove and destroy infected plants. Control insect vectors like aphids.',
        'prevention': 'Use disease-resistant varieties, control weeds, and maintain proper spacing.'
    },
    'leaf_spot': {
        'name': 'Leaf Spot',
        'description': 'Fungal disease characterized by brown or black spots on leaves.',
        'treatment': 'Remove affected leaves and apply fungicide.',
        'prevention': 'Maintain good air circulation, avoid overhead watering.'
    },
    'powdery_mildew': {
        'name': 'Powdery Mildew',
        'description': 'Fungal disease appearing as white powdery spots on leaves.',
        'treatment': 'Apply fungicide and improve air circulation.',
        'prevention': 'Space plants properly and avoid high humidity.'
    }
}

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess the image for model input."""
    img = Image.open(image_path)
    img = img.resize(target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalize pixel values
    return img

def analyze_plant_disease(image_path):
    """Analyze plant image for disease detection."""
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)

        # Convert to RGB array for analysis
        img_array = np.array(Image.open(image_path).convert('RGB'))

        # Calculate various image statistics
        color_std = np.std(img_array, axis=(0, 1))
        color_mean = np.mean(img_array, axis=(0, 1))
        texture_variation = np.std(np.diff(img_array.mean(axis=2)))

        # Enhanced mosaic pattern detection
        # Check for alternating patterns in green channel
        green_channel = img_array[:,:,1]
        horizontal_variation = np.mean(np.abs(np.diff(green_channel, axis=1)))
        vertical_variation = np.mean(np.abs(np.diff(green_channel, axis=0)))
        pattern_strength = (horizontal_variation + vertical_variation) / 2

        # Improved disease classification logic
        if (pattern_strength > 20 and  # Strong pattern variation
            color_std[1] > 30 and      # High green channel variation
            texture_variation > 15):    # Significant texture changes
            disease_type = 'mosaic_virus'
            confidence = min(90 + pattern_strength / 5, 98)

        # Check for leaf spots (dark spots on lighter background)
        elif (np.percentile(img_array, 90) - np.percentile(img_array, 10) > 100 and
              color_std[0] > 40):  # High variation in red channel
            disease_type = 'leaf_spot'
            confidence = min(85 + color_std[0] / 4, 95)

        # Check for powdery mildew (bright areas with specific texture)
        elif (color_mean.mean() > 150 and 
              color_std.mean() < 40 and
              texture_variation < 10):
            disease_type = 'powdery_mildew'
            confidence = min(80 + (255 - color_mean.mean()) / 5, 95)
        else:
            return None

        disease_info = PLANT_DISEASES[disease_type]

        return {
            'disease_name': disease_info['name'],
            'confidence': f"{confidence:.1f}%",
            'description': disease_info['description'],
            'treatment': disease_info['treatment'],
            'prevention': disease_info['prevention']
        }

    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return None

def calculate_confidence(img_array, disease_type):
    """Calculate confidence score based on image characteristics."""
    if disease_type == 'mosaic_virus':
        # Higher confidence for clear mosaic patterns
        return min(85 + np.std(img_array) / 5, 95)
    elif disease_type == 'leaf_spot':
        # Higher confidence for distinct spots
        return min(80 + (np.percentile(img_array, 90) - np.percentile(img_array, 10)) / 10, 95)
    else:
        # Base confidence for other patterns
        return 75.0