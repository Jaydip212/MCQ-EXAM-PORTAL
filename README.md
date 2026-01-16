# MCQ Exam Portal

A full-stack web application for conducting online MCQ exams with Python FastAPI backend and React frontend.

## Features

### Student Features
- User registration and authentication
- Browse available exams
- Take timed exams with multiple-choice questions
- Real-time timer countdown
- Submit answers and view results
- View exam history and performance analytics

### Admin Features
- Create and manage exams
- Add/edit/delete questions
- Set exam duration, total marks, and passing marks
- View all exam results
- Manage exam availability

## Tech Stack

### Backend
- **Django** - Python web framework
- **Django REST Framework** - API framework
- **PostgreSQL** - Database
- **Django ORM** - Object-relational mapping
- **Simple JWT** - JWT authentication
- **CORS Headers** - Cross-origin resource sharing

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Project Structure

```
mcqexam/
├── backend/
│   ├── manage.py            # Django management script
│   ├── config/              # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/                 # Django app
│       ├── models.py        # Database models
│       ├── serializers.py   # DRF serializers
│       ├── views.py         # API views
│       ├── urls.py          # URL routing
│       └── admin.py         # Admin configuration
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # Context providers
│   │   ├── pages/           # Page components
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md
```

## Database Schema

- **users** - User accounts (students and admins)
- **students** - Student profiles
- **exams** - Exam details
- **questions** - Exam questions with options
- **exam_attempts** - Student exam attempts
- **student_answers** - Individual question answers

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 1. Clone the repository
```bash
git clone <repository-url>
cd mcqexam
```

### 2. Set up PostgreSQL Database
```bash
# Create database
createdb mcqexam

# Or using psql
psql -U postgres
CREATE DATABASE mcqexam;
\q
```

### 3. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy .env.example to .env and update with your database credentials
copy .env.example .env

# Run migrations
cd backend
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run the backend server
python manage.py runserver
```

The backend will run on `http://localhost:8000`
Admin panel: `http://localhost:8000/admin`

### 4. Frontend Setup
```bash
# Install Node dependencies
cd frontend
npm install

# Run the development server
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

### Creating an Admin Account

**Option 1: Using Django Admin Panel**
1. Create a superuser: `python manage.py createsuperuser`
2. Login to admin panel at `http://localhost:8000/admin`
3. Create users and set their role to 'admin'

**Option 2: Register and Update**
1. Register a new account at `/register`
2. Update the user role in Django admin or database:
```sql
UPDATE api_user SET role = 'admin' WHERE email = 'your-email@example.com';
```

### Student Workflow
1. Register/Login
2. Browse available exams
3. Start an exam
4. Answer questions within the time limit
5. Submit and view results

### Admin Workflow
1. Login with admin credentials
2. Go to Admin Dashboard
3. Create new exam with questions
4. Set exam parameters (duration, marks, etc.)
5. View exam results and analytics

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Exams
- `GET /api/exams` - Get all active exams
- `GET /api/exams/{id}` - Get exam with questions
- `POST /api/exams` - Create exam (admin)
- `PUT /api/exams/{id}` - Update exam (admin)
- `DELETE /api/exams/{id}` - Delete exam (admin)

### Questions
- `POST /api/questions` - Create question (admin)
- `GET /api/questions/exam/{id}` - Get exam questions (admin)
- `PUT /api/questions/{id}` - Update question (admin)
- `DELETE /api/questions/{id}` - Delete question (admin)

### Students
- `GET /api/students/me` - Get current student profile
- `POST /api/students/start-exam` - Start exam attempt
- `POST /api/students/submit-exam` - Submit exam answers
- `GET /api/students/my-attempts` - Get student's exam attempts

### Results
- `GET /api/results/attempt/{id}` - Get result by attempt ID
- `GET /api/results/exam/{id}` - Get all results for exam (admin)

## Environment Variables

Copy `.env.example` to `.env` and update:

```env
DJANGO_SECRET_KEY=your-django-secret-key-change-this-in-production
DEBUG=True
DB_NAME=mcqexam
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

## Development

### Running Tests
```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production
```bash
# Build frontend
cd frontend
npm run build

# The built files will be in frontend/dist/
```

## Security Features

- Password hashing with bcrypt
- JWT-based authentication
- Protected API routes
- Role-based access control (Student/Admin)
- SQL injection prevention via ORM

## Future Enhancements

- [ ] Question bank management
- [ ] Random question selection
- [ ] Negative marking support
- [ ] Detailed answer explanations
- [ ] Export results to PDF/Excel
- [ ] Email notifications
- [ ] Question images upload
- [ ] Multi-language support
- [ ] Mobile app

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
