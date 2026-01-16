import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import axios from 'axios'
import { BookOpen, Clock, Award, TrendingUp } from 'lucide-react'

const Dashboard = () => {
  const { user } = useAuth()
  const [stats, setStats] = useState({
    totalExams: 0,
    completedExams: 0,
    averageScore: 0
  })
  const [recentAttempts, setRecentAttempts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token')
      const [examsRes, attemptsRes] = await Promise.all([
        axios.get('http://127.0.0.1:8000/api/exams/', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://127.0.0.1:8000/api/students/my-attempts/', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ])

      const completedAttempts = attemptsRes.data.filter(a => a.status === 'completed')
      const avgScore = completedAttempts.length > 0
        ? completedAttempts.reduce((sum, a) => sum + (a.score || 0), 0) / completedAttempts.length
        : 0

      setStats({
        totalExams: examsRes.data.length,
        completedExams: completedAttempts.length,
        averageScore: avgScore.toFixed(1)
      })

      setRecentAttempts(attemptsRes.data.slice(0, 5))
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.username}!</h1>
          <p className="text-gray-600 mt-2">Here's your exam overview</p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Total Exams</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.totalExams}</p>
                  </div>
                  <BookOpen className="h-12 w-12 text-blue-600" />
                </div>
              </div>

              <div className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Completed</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.completedExams}</p>
                  </div>
                  <Award className="h-12 w-12 text-green-600" />
                </div>
              </div>

              <div className="card">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Average Score</p>
                    <p className="text-3xl font-bold text-gray-900">{stats.averageScore}</p>
                  </div>
                  <TrendingUp className="h-12 w-12 text-purple-600" />
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
                <div className="space-y-3">
                  <Link to="/exams" className="block p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors">
                    <div className="flex items-center space-x-3">
                      <BookOpen className="h-6 w-6 text-blue-600" />
                      <div>
                        <p className="font-medium text-gray-900">Browse Exams</p>
                        <p className="text-sm text-gray-600">View all available exams</p>
                      </div>
                    </div>
                  </Link>
                  <Link to="/results" className="block p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors">
                    <div className="flex items-center space-x-3">
                      <Award className="h-6 w-6 text-green-600" />
                      <div>
                        <p className="font-medium text-gray-900">View Results</p>
                        <p className="text-sm text-gray-600">Check your exam results</p>
                      </div>
                    </div>
                  </Link>
                </div>
              </div>

              <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Activity</h2>
                {recentAttempts.length > 0 ? (
                  <div className="space-y-3">
                    {recentAttempts.map((attempt) => (
                      <div key={attempt.id} className="p-3 bg-gray-50 rounded-lg">
                        <div className="flex justify-between items-start">
                          <div>
                            <p className="font-medium text-gray-900">Exam #{attempt.exam_id}</p>
                            <p className="text-sm text-gray-600">
                              Status: <span className={attempt.status === 'completed' ? 'text-green-600' : 'text-yellow-600'}>
                                {attempt.status}
                              </span>
                            </p>
                          </div>
                          {attempt.score !== null && (
                            <span className="text-lg font-bold text-blue-600">{attempt.score}</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">No recent activity</p>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default Dashboard
