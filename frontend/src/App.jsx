import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ExamList from './pages/ExamList'
import TakeExam from './pages/TakeExam'
import Results from './pages/Results'
import AdminDashboard from './pages/AdminDashboard'
import CreateExam from './pages/CreateExam'
import Leaderboard from './pages/Leaderboard'
import Profile from './pages/Profile'
import PrivateRoute from './components/PrivateRoute'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route path="/dashboard" element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } />
          
          <Route path="/exams" element={
            <PrivateRoute>
              <ExamList />
            </PrivateRoute>
          } />
          
          <Route path="/exam/:examId" element={
            <PrivateRoute>
              <TakeExam />
            </PrivateRoute>
          } />
          
          <Route path="/results" element={
            <PrivateRoute>
              <Results />
            </PrivateRoute>
          } />
          
          <Route path="/admin" element={
            <PrivateRoute adminOnly>
              <AdminDashboard />
            </PrivateRoute>
          } />
          
          <Route path="/admin/create-exam" element={
            <PrivateRoute adminOnly>
              <CreateExam />
            </PrivateRoute>
          } />
          
          <Route path="/leaderboard" element={
            <PrivateRoute>
              <Leaderboard />
            </PrivateRoute>
          } />
          
          <Route path="/profile" element={
            <PrivateRoute>
              <Profile />
            </PrivateRoute>
          } />
          
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
