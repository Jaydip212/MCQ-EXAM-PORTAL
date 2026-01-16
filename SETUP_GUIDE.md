# MCQ Exam Portal - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git (optional)

### Installation Steps

#### 1. Install Backend Dependencies
```bash
cd mcqexam
pip install -r requirements.txt
```

#### 2. Setup Database
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

#### 3. Create Admin User
```bash
python create_admin.py
```

**Default Admin Credentials:**
- Username: `jay9921`
- Password: `Jaydip@123`
- Email: `jay9921@example.com`

#### 4. Install Frontend Dependencies
```bash
cd frontend
npm install
```

#### 5. Start Servers

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```
Backend runs on: `http://127.0.0.1:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:3000`

### 🔗 Important URLs

- **Frontend Application:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8000/api/
- **Admin Panel:** http://127.0.0.1:8000/admin
- **API Documentation:** http://127.0.0.1:8000/api/ (DRF Browsable API)

---

## 📁 Project Structure

```
mcqexam/
├── backend/                    # Django Backend
│   ├── api/                   # Main API App
│   │   ├── models.py         # Database Models
│   │   ├── serializers.py    # DRF Serializers
│   │   ├── views.py          # API Views
│   │   ├── urls.py           # API Routes
│   │   └── admin.py          # Admin Configuration
│   ├── config/               # Django Settings
│   │   ├── settings.py       # Main Settings
│   │   ├── urls.py           # URL Configuration
│   │   └── wsgi.py           # WSGI Config
│   ├── manage.py             # Django Management
│   ├── create_admin.py       # Admin User Creator
│   └── db.sqlite3            # SQLite Database
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/       # Reusable Components
│   │   │   ├── Navbar.jsx
│   │   │   └── PrivateRoute.jsx
│   │   ├── context/          # React Context
│   │   │   └── AuthContext.jsx
│   │   ├── pages/            # Page Components
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ExamList.jsx
│   │   │   ├── TakeExam.jsx
│   │   │   ├── Results.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   └── CreateExam.jsx
│   │   ├── App.jsx           # Main App
│   │   ├── main.jsx          # Entry Point
│   │   └── index.css         # Global Styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── requirements.txt           # Python Dependencies
├── package.json              # Node Dependencies
├── run.bat                   # Auto-start Script
├── reset_db.bat             # Database Reset Script
└── README.md                # Main Documentation
```

---

## 🔧 Troubleshooting

### Database Issues

**Problem:** Migration errors or database locked
```bash
# Stop all servers first (Ctrl+C)
cd backend
del db.sqlite3
rmdir /s api\migrations
mkdir api\migrations
echo. > api\migrations\__init__.py
python manage.py makemigrations
python manage.py migrate
python create_admin.py
```

Or simply run:
```bash
.\reset_db.bat
```

### Port Already in Use

**Backend (Port 8000):**
```bash
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Frontend (Port 3000):**
```bash
# Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Registration/Login Not Working

1. Check backend server is running
2. Check frontend is connecting to correct API URL
3. Clear browser cache and cookies
4. Check browser console for errors (F12)

---

## 🎯 Usage Guide

### For Students

1. **Register Account**
   - Go to http://localhost:3000
   - Click "Register"
   - Fill in details and create account

2. **Browse Exams**
   - Login with your credentials
   - Go to "Exams" section
   - View available exams

3. **Take Exam**
   - Click "Start Exam"
   - Answer all questions
   - Submit before time runs out

4. **View Results**
   - Go to "Results" section
   - Check your scores and performance

### For Admins

1. **Access Admin Panel**
   - Go to http://127.0.0.1:8000/admin
   - Login with admin credentials
   - Manage all data from here

2. **Create Exam (Frontend)**
   - Login to frontend
   - Go to "Admin Dashboard"
   - Click "Create New Exam"
   - Add exam details and questions

3. **Create Exam (Admin Panel)**
   - Login to Django admin
   - Add Exam with details
   - Add Questions for that exam

---

## 📊 Database Schema

### User Model
- username (unique)
- email (unique)
- password (hashed)
- role (student/admin)

### Student Model
- user (OneToOne with User)
- name
- email
- phone
- enrollment_no

### Exam Model
- title
- description
- duration (minutes)
- total_marks
- passing_marks
- is_active

### Question Model
- exam (ForeignKey)
- question_text
- option_a, option_b, option_c, option_d
- correct_answer (A/B/C/D)
- marks
- image (optional)

### ExamAttempt Model
- student (ForeignKey)
- exam (ForeignKey)
- start_time
- end_time
- score
- total_questions
- correct_answers
- status (in_progress/completed)

### StudentAnswer Model
- attempt (ForeignKey)
- question (ForeignKey)
- selected_answer
- is_correct

---

## 🔐 Security Notes

1. **Change Default Admin Password**
   ```python
   # Edit backend/create_admin.py
   username = 'your_username'
   password = 'your_strong_password'
   ```

2. **Update Django Secret Key**
   ```python
   # In backend/config/settings.py
   SECRET_KEY = 'your-new-secret-key'
   ```

3. **For Production:**
   - Set `DEBUG = False`
   - Use PostgreSQL instead of SQLite
   - Configure ALLOWED_HOSTS
   - Use environment variables for secrets
   - Enable HTTPS
   - Set up proper CORS settings

---

## 🛠️ Development Tips

### Adding New Features

1. **Backend (Django):**
   - Add models in `api/models.py`
   - Create serializers in `api/serializers.py`
   - Add views in `api/views.py`
   - Update URLs in `api/urls.py`
   - Run migrations

2. **Frontend (React):**
   - Create components in `src/components/`
   - Add pages in `src/pages/`
   - Update routes in `App.jsx`
   - Add API calls using axios

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Code Style

- **Python:** Follow PEP 8
- **JavaScript:** Use ES6+ features
- **React:** Functional components with hooks
- **CSS:** Tailwind utility classes

---

## 📝 Common Commands

### Django Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Frontend Commands
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🚀 Deployment

### Backend (Django)

1. **Update Settings:**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Use PostgreSQL:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Deploy to:**
   - Heroku
   - Railway
   - PythonAnywhere
   - AWS EC2
   - DigitalOcean

### Frontend (React)

1. **Build:**
   ```bash
   npm run build
   ```

2. **Deploy to:**
   - Vercel
   - Netlify
   - GitHub Pages
   - AWS S3 + CloudFront

---

## 📞 Support

For issues or questions:
1. Check this documentation
2. Review README.md
3. Check Django/React documentation
4. Debug using browser console (F12)
5. Check backend logs in terminal

---

## 📄 License

MIT License - Free to use and modify
