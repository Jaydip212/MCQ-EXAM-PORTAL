# MCQ Exam Portal - Development Notes

## 📅 Project Timeline

**Created:** January 16, 2026
**Developer:** Jay (jay9921)
**Tech Stack:** Django + React + Vite + Tailwind CSS

---

## 🎯 Project Overview

Complete MCQ (Multiple Choice Questions) exam portal with:
- Student registration and authentication
- Admin panel for exam management
- Timed exams with automatic submission
- Result tracking and analytics
- Modern, responsive UI

---

## 🔧 Technical Decisions

### Why Django?
- Powerful ORM for database management
- Built-in admin panel
- Django REST Framework for API
- Excellent security features
- Easy to deploy

### Why React + Vite?
- Fast development with hot reload
- Modern build tool (Vite)
- Component-based architecture
- Great ecosystem and libraries

### Why SQLite?
- Easy setup for development
- No external database server needed
- Can migrate to PostgreSQL for production

### Why Tailwind CSS?
- Utility-first approach
- Fast styling
- Consistent design
- Small bundle size

---

## 📊 Database Design

### User Authentication Flow
```
1. User registers → User model created
2. If role = 'student' → Student profile auto-created
3. JWT token generated on login
4. Token stored in localStorage
5. Token sent with each API request
```

### Exam Taking Flow
```
1. Student starts exam → ExamAttempt created
2. Timer starts (duration from Exam model)
3. Student answers questions
4. On submit → StudentAnswer records created
5. Score calculated automatically
6. ExamAttempt updated with results
```

---

## 🔐 Authentication System

### JWT Implementation
- **Library:** djangorestframework-simplejwt
- **Token Lifetime:** 24 hours (1 day)
- **Storage:** localStorage in browser
- **Header:** Authorization: Bearer <token>

### User Roles
1. **Student:**
   - Can take exams
   - View own results
   - Browse available exams

2. **Admin:**
   - All student permissions
   - Create/edit/delete exams
   - Add questions
   - View all results
   - Access Django admin panel

---

## 🎨 Frontend Architecture

### Context API
- **AuthContext:** Manages user authentication state
  - login()
  - register()
  - logout()
  - user data
  - token management

### Protected Routes
- **PrivateRoute:** Requires authentication
- **AdminRoute:** Requires admin role
- Redirects to login if not authenticated

### Pages Structure
```
Public Pages:
- Login
- Register

Student Pages:
- Dashboard
- Exam List
- Take Exam
- Results

Admin Pages:
- Admin Dashboard
- Create Exam
```

---

## 🔌 API Endpoints

### Authentication
```
POST /api/auth/register
POST /api/auth/login
```

### Exams
```
GET    /api/exams/              # List all active exams
GET    /api/exams/{id}/         # Get exam with questions
POST   /api/exams/              # Create exam (admin)
PUT    /api/exams/{id}/         # Update exam (admin)
DELETE /api/exams/{id}/         # Delete exam (admin)
```

### Questions
```
POST   /api/questions/                  # Create question (admin)
GET    /api/questions/exam/{exam_id}/   # Get exam questions (admin)
PUT    /api/questions/{id}/             # Update question (admin)
DELETE /api/questions/{id}/             # Delete question (admin)
```

### Students
```
GET  /api/students/me/              # Get current student profile
POST /api/students/start-exam/      # Start exam attempt
POST /api/students/submit-exam/     # Submit exam answers
GET  /api/students/my-attempts/     # Get student's attempts
```

### Results
```
GET /api/results/attempt/{id}/  # Get result by attempt ID
GET /api/results/exam/{id}/     # Get all results for exam (admin)
```

---

## 💡 Key Features Implemented

### 1. Timer System
- Countdown timer in TakeExam component
- Auto-submit when time runs out
- Warning when < 5 minutes remaining
- Time displayed in MM:SS format

### 2. Answer Tracking
- Real-time answer count
- Shows answered vs unanswered questions
- Visual feedback for selected options
- Confirmation before submit

### 3. Score Calculation
- Automatic scoring on submit
- Marks per question configurable
- Pass/Fail based on passing marks
- Percentage calculation

### 4. Admin Features
- Create exams with multiple questions
- Set duration, marks, passing criteria
- View all student attempts
- Manage questions (CRUD operations)

### 5. Student Dashboard
- Quick stats (total exams, completed, avg score)
- Recent activity
- Quick action buttons
- Performance overview

---

## 🐛 Issues Fixed

### 1. Database Migration Issue
**Problem:** Custom User model migrations conflicting
**Solution:** Reset database and create migrations in correct order

### 2. CORS Issues
**Problem:** Frontend couldn't connect to backend
**Solution:** Added django-cors-headers with proper configuration

### 3. Authentication State
**Problem:** User state not persisting on refresh
**Solution:** Store token and user in localStorage, restore on mount

### 4. Pillow Installation
**Problem:** Pillow failing to install on Python 3.13
**Solution:** Removed Pillow (not critical for MVP)

---

## 🚀 Future Enhancements

### Phase 1 - Core Features
- [x] User authentication
- [x] Exam creation
- [x] Question management
- [x] Exam taking
- [x] Results display
- [x] Admin panel

### Phase 2 - Improvements
- [ ] Question bank system
- [ ] Random question selection
- [ ] Question categories/tags
- [ ] Negative marking option
- [ ] Multiple exam types (practice, mock, final)

### Phase 3 - Advanced Features
- [ ] Image upload for questions
- [ ] Rich text editor for questions
- [ ] Export results to PDF/Excel
- [ ] Email notifications
- [ ] Student progress tracking
- [ ] Analytics dashboard

### Phase 4 - Scale
- [ ] PostgreSQL migration
- [ ] Redis caching
- [ ] Celery for async tasks
- [ ] WebSocket for live updates
- [ ] Mobile app (React Native)

---

## 📝 Code Conventions

### Python (Django)
```python
# Class names: PascalCase
class ExamAttempt(models.Model):
    pass

# Function names: snake_case
def get_exam_results():
    pass

# Constants: UPPER_CASE
MAX_ATTEMPTS = 3
```

### JavaScript (React)
```javascript
// Component names: PascalCase
const Dashboard = () => {}

// Function names: camelCase
const handleSubmit = () => {}

// Constants: UPPER_CASE
const API_BASE_URL = 'http://localhost:8000'
```

### CSS (Tailwind)
```jsx
// Use utility classes
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
```

---

## 🔍 Testing Checklist

### Backend Tests
- [ ] User registration
- [ ] User login
- [ ] Exam creation (admin)
- [ ] Question creation (admin)
- [ ] Start exam attempt
- [ ] Submit exam
- [ ] View results
- [ ] Permission checks

### Frontend Tests
- [ ] Registration form validation
- [ ] Login flow
- [ ] Protected routes
- [ ] Exam list display
- [ ] Exam taking flow
- [ ] Timer functionality
- [ ] Answer submission
- [ ] Results display
- [ ] Admin features

### Integration Tests
- [ ] End-to-end exam flow
- [ ] Admin creating exam → Student taking → Results
- [ ] Multiple students same exam
- [ ] Concurrent exam attempts

---

## 📊 Performance Optimization

### Backend
- Database indexing on frequently queried fields
- Pagination for large result sets
- Caching for static data
- Query optimization (select_related, prefetch_related)

### Frontend
- Code splitting with React.lazy
- Image optimization
- Memoization with useMemo/useCallback
- Virtual scrolling for long lists

---

## 🔒 Security Measures

### Implemented
- ✅ Password hashing (Django default)
- ✅ JWT authentication
- ✅ CORS configuration
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection (React default)
- ✅ CSRF protection (Django)

### To Implement
- [ ] Rate limiting
- [ ] Input sanitization
- [ ] File upload validation
- [ ] Session timeout
- [ ] Two-factor authentication
- [ ] Password strength requirements

---

## 📚 Learning Resources

### Django
- Official Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Django Girls Tutorial

### React
- Official Docs: https://react.dev/
- React Router: https://reactrouter.com/
- Vite Guide: https://vitejs.dev/

### Tailwind CSS
- Official Docs: https://tailwindcss.com/
- Tailwind UI Components

---

## 🎓 Lessons Learned

1. **Custom User Model:** Always define custom user model at project start
2. **Migrations:** Be careful with migration order, especially with dependencies
3. **CORS:** Essential for frontend-backend communication
4. **State Management:** Context API sufficient for small-medium apps
5. **Error Handling:** Always handle API errors gracefully
6. **User Experience:** Loading states and error messages are crucial

---

## 📞 Quick Reference

### Admin Credentials
- Username: jay9921
- Password: Jaydip@123
- Email: jay9921@example.com

### URLs
- Frontend: http://localhost:3000
- Backend: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

### Important Files
- Backend Settings: `backend/config/settings.py`
- API Views: `backend/api/views.py`
- Frontend Routes: `frontend/src/App.jsx`
- Auth Context: `frontend/src/context/AuthContext.jsx`

---

## 🎯 Project Status

**Current Version:** 1.0.0
**Status:** ✅ MVP Complete
**Last Updated:** January 16, 2026

### Completed Features
- ✅ User authentication (register/login)
- ✅ Student dashboard
- ✅ Admin dashboard
- ✅ Exam creation and management
- ✅ Question management
- ✅ Exam taking with timer
- ✅ Result calculation and display
- ✅ Django admin panel
- ✅ Responsive UI

### Known Issues
- None critical

### Next Steps
1. Add question images support
2. Implement question bank
3. Add export functionality
4. Deploy to production

---

**End of Notes**
