# Stock Data Django Application

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose
- AWS CLI (for deployment)
- Python 3.9

### Local Setup
1. Clone the repository:
   ```sh
   git clone <repository-url>
2. Create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install the dependencies:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```
5. Start the server:
```
python manage.py runserver
```
### Docker Setup
1. Build and run the Docker containers:
```commandline
docker-compose up --build
```
