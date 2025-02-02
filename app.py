
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from flask_ckeditor import CKEditor
from googletrans import Translator
import redis
import json
from flask_wtf import FlaskForm
from wtforms import StringField
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Connecting to MongoDB
mongo = PyMongo(app)
db = mongo.db.faqs

app.config['CKEDITOR_PKG_TYPE'] = 'full'
ckeditor = CKEditor(app)

admin = Admin(app)

# Define FlaskForm
class FAQForm(FlaskForm):
    question = StringField('Question')
    answer = StringField('Answer')
    question_hi = StringField('Question (Hindi)')
    answer_hi = StringField('Answer (Hindi)')
    question_bn = StringField('Question (Bengali)')
    answer_bn = StringField('Answer (Bengali)')

# Custom Flask-Admin View for MongoDB
class FAQModelView(ModelView):
    column_list = ('question', 'answer', 'question_hi', 'answer_hi', 'question_bn', 'answer_bn')

    def scaffold_form(self):
        return FAQForm

admin.add_view(FAQModelView(db, 'FAQs'))

# Translator & Redis Cache
translator = Translator()
cache = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), decode_responses=True)

# Function to Translate and Save FAQ
def save_translations(faq):
    faq['question_hi'] = translator.translate(faq['question'], dest='hi').text
    faq['answer_hi'] = translator.translate(faq['answer'], dest='hi').text
    faq['question_bn'] = translator.translate(faq['question'], dest='bn').text
    faq['answer_bn'] = translator.translate(faq['answer'], dest='bn').text
    return faq

# Function to Fetch Translated FAQs (with Caching)
def get_translated_faqs(lang='en'):
    cached_data = cache.get(f'faqs_{lang}')
    if cached_data:
        return json.loads(cached_data)

    faqs = list(db.find({}, {'_id': 0}))  # Fetch all FAQs
    result = []

    for faq in faqs:
        translated_faq = {
            'question': faq.get(f'question_{lang}', faq['question']),
            'answer': faq.get(f'answer_{lang}', faq['answer'])
        }
        result.append(translated_faq)

    cache.set(f'faqs_{lang}', json.dumps(result), ex=3600)  # Cache for 1 hour
    return result

## fetch_faqs API
@app.route('/api/faqs/', methods=['GET'])
def fetch_faqs():
    lang = request.args.get('lang', 'en')
    faqs = get_translated_faqs(lang)
    return app.response_class(
        json.dumps(faqs, ensure_ascii=False),
        mimetype='application/json'
    )

## add_faq API
@app.route('/api/faqs/', methods=['POST'])
def add_faq():
    data = request.json
    if not data or 'question' not in data or 'answer' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

    new_faq = save_translations({'question': data['question'], 'answer': data['answer']})
    db.insert_one(new_faq)
    cache.delete_pattern('faqs_*') 
    return jsonify({'message': 'FAQ added successfully'}), 201

## delete_faq API
@app.route('/api/faqs/<question>', methods=['DELETE'])
def delete_faq(question):
    result = db.delete_one({'question': question})
    if result.deleted_count > 0:
        cache.delete_pattern('faqs_*') 
        return jsonify({'message': 'FAQ deleted successfully'}), 200
    return jsonify({'error': 'FAQ not found'}), 404

## update_faq API
@app.route('/api/faqs/<question>', methods=['PUT'])
def update_faq(question):
    data = request.json
    if not data or 'answer' not in data:
        return jsonify({'error': 'Invalid input data'}), 400

    updated_faq = save_translations({'question': question, 'answer': data['answer']})
    result = db.update_one({'question': question}, {'$set': updated_faq})

    if result.matched_count > 0:
        cache.delete_pattern('faqs_*')
        return jsonify({'message': 'FAQ updated successfully'}), 200
    return jsonify({'error': 'FAQ not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
