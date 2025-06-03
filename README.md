# Clone repository
git clone https://github.com/yourusername/recruiter-ats.git
cd recruiter-ats

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy .env.example to .env and set values)
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser (for admin access)
python manage.py createsuperuser

# Run development server
python manage.py runserver






Testing
Run the test suite with:

bash
python manage.py test candidates
Test coverage includes:

Candidate CRUD operations

Search relevancy ordering

Partial match handling

Case insensitivity

Edge cases (empty search, special characters)

Validation and error handling
