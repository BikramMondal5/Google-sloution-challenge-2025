import os
import logging
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from crop_data import get_crop_recommendation
from disease_detection import analyze_plant_disease
from weather_service import WeatherService
from ml_service import CropMLService

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Initialize services
weather_service = WeatherService()
ml_service = CropMLService()

# Log API key status (without revealing the key)
logger.debug("Weather API Key status: %s", "Present" if os.environ.get('OPENWEATHERMAP_API_KEY') else "Missing")

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    try:
        # Get weather data for a default location (can be made dynamic later)
        logger.debug("Attempting to fetch weather data for Mumbai")
        weather_data = weather_service.get_weather('Mumbai')

        if weather_data is None:
            logger.warning("Weather data fetch failed, rendering template with warning")
            return render_template('index.html', weather=None, 
                                weather_error="Unable to fetch weather data. Please check your API key.")

        logger.debug("Weather data fetched successfully: %s", weather_data)
        return render_template('index.html', weather=weather_data)

    except Exception as e:
        logger.error("Error in index route: %s", str(e))
        return render_template('index.html', weather=None, 
                             weather_error="An error occurred while fetching weather data.")

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.form
        soil_type = data.get('soil_type')
        season = data.get('season')

        # If temperature and rainfall are not provided, get them from weather API
        if not data.get('temperature') or not data.get('rainfall'):
            weather_data = weather_service.get_weather('Mumbai')
            if weather_data:
                temperature = weather_data['temperature']
                rainfall = weather_data['rainfall']
            else:
                return jsonify({'error': 'Could not fetch weather data'}), 500
        else:
            temperature = float(data.get('temperature', 0))
            rainfall = float(data.get('rainfall', 0))

        if not all([soil_type, season]):
            return jsonify({'error': 'All fields are required'}), 400

        # Use ML service for recommendations
        recommendation = ml_service.get_crop_recommendations(soil_type, season, temperature, rainfall)
        return render_template('recommendation.html', recommendation=recommendation)

    except ValueError as e:
        return jsonify({'error': 'Invalid numeric values provided'}), 400
    except Exception as e:
        logging.error(f"Error in recommendation: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

# Keep the disease detection routes unchanged
@app.route('/disease-detection')
def disease_detection():
    return render_template('disease_detection.html')

@app.route('/analyze-disease', methods=['POST'])
def analyze_disease():
    if 'plant_image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['plant_image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Analyze the image using our disease detection module
        result = analyze_plant_disease(filepath)

        if result:
            result['image_url'] = url_for('static', filename=f'uploads/{filename}')
            return render_template('disease_result.html', result=result)
        else:
            return render_template('disease_detection.html', 
                                 error="Could not detect any known diseases. Please try with a clearer image.")

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)