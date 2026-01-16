import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { LogOut, BookOpen, Trophy, UserCircle } from 'lucide-react'
import Notifications from './Notifications'

const Navbar = () => {
  const { user, logout, isAdmin } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">MCQ Exam Portal</span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <Link to="/dashboard" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
              Dashboard
            </Link>
            <Link to="/exams" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
              Exams
            </Link>
            <Link to="/results" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
              Results
            </Link>
            <Link to="/leaderboard" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition flex items-center gap-1">
              <Trophy className="h-4 w-4" />
              Leaderboard
            </Link>
            {isAdmin && (
              <Link to="/admin" className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition">
                Admin
              </Link>
            )}
            
            <div className="flex items-center space-x-3 border-l pl-4">
              <Notifications />
              
              <Link to="/profile" className="flex items-center gap-2 text-gray-700 hover:text-indigo-600 transition">
                <UserCircle className="h-5 w-5" />
                <span className="text-sm font-medium">{user?.username}</span>
              </Link>
              
              <button
                onClick={handleLogout}
                className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-md transition-colors"
                title="Logout"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
