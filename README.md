# BharatFD Backend Assignment

## Objective

The objective of this test is to evaluate the candidate's ability to:

- Design and implement Django models with WYSIWYG editor support.
- Store and manage FAQs with multi-language translation.
- Follow PEP8 conventions and best practices.
- Write a clear and detailed README.
- Use proper Git commit messages.

## Task Requirements

### 1. Model Design

Create a model to store FAQs with the following fields:
- **question** (TextField)
- **answer** (RichTextField for WYSIWYG editor support)
- **Language-specific translations** (e.g., question_hi, question_bn, etc.)

A model method is implemented to retrieve translated text dynamically.

### 2. WYSIWYG Editor Integration

The `django-ckeditor` library is used to allow users to format answers properly, supporting multilingual content.

### 3. API Development

A **REST API** is provided for managing FAQs with language support:
- Support language selection via `?lang=` query parameter.
- Fast and efficient responses using pre-translation.

### 4. Caching Mechanism

A **cache framework** is implemented to store translations, with **Redis** used to enhance performance.

### 5. Multi-language Translation Support

The **Google Translate API** or `googletrans` is utilized to automate translations during object creation, with a fallback to English if the translation is unavailable.

### 6. Admin Panel

The FAQ model is registered with Django's Admin site to provide a user-friendly interface for managing FAQs.

### 7. Unit Tests & Code Quality

Unit tests are written using **pytest** (or mocha/chai for JS users). The tests cover model methods and API responses.

Code quality adheres to **PEP8** (for Python) and **ES6** (for JavaScript) guidelines. Linting tools like **flake8** are used to enforce these rules.

### 8. Documentation

A detailed README is provided, covering:
- Installation steps
- API usage examples
- Contribution guidelines

### 9. Git & Version Control

Git is used for version control with conventional commit messages:
- `feat`: Add multilingual FAQ model
- `fix`: Improve translation caching
- `docs`: Update README with API examples

Atomic commits are made with clear and concise messages.

### 10. Deployment & Docker Support (Bonus)

A **Dockerfile** and **docker-compose.yml** are provided to deploy the application locally. The application can optionally be deployed to **Heroku** or **AWS**.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shrinathasati/BharatFD_Backend_assignment.git
   cd BharatFD_Backend_assignment



## example api:
Fetch FAQs in English (default): http://localhost:5000/api/faqs/
Fetch FAQs in Hindi: http://localhost:5000/api/faqs/?lang=hi
Fetch FAQs in Bengali: http://localhost:5000/api/faqs/?lang=bn
Admin: http://localhost:5000/admin
