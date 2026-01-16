import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import axios from 'axios'
import { Award, TrendingUp, Calendar, CheckCircle, XCircle } from 'lucide-react'

const Results = () => {
  const [attempts, setAttempts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchResults()
  }, [])

  const fetchResults = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://127.0.0.1:8000/api/students/my-attempts/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const completed = response.data.filter(a => a.status === 'completed')
      setAttempts(completed)
    } catch (error) {
      console.error('Error fetching results:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Results</h1>
          <p className="text-gray-600 mt-2">View your exam performance</p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : attempts.length === 0 ? (
          <div className="card text-center py-12">
            <Award className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">No Results Yet</h3>
            <p className="text-gray-600">Complete an exam to see your results here</p>
          </div>
        ) : (
          <div className="space-y-6">
            {attempts.map((attempt) => {
              const percentage = attempt.total_questions > 0 
                ? ((attempt.correct_answers / attempt.total_questions) * 100).toFixed(1)
                : 0

              return (
                <div key={attempt.id} className="card">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900">Exam #{attempt.exam_id}</h3>
                      <div className="flex items-center text-sm text-gray-600 mt-1">
                        <Calendar className="h-4 w-4 mr-1" />
                        <span>{formatDate(attempt.end_time)}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-blue-600">{attempt.score}</div>
                      <div className="text-sm text-gray-600">Score</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-green-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Correct Answers</p>
                          <p className="text-2xl font-bold text-green-600">{attempt.correct_answers}</p>
                        </div>
                        <CheckCircle className="h-8 w-8 text-green-600" />
                      </div>
                    </div>

                    <div className="bg-red-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Wrong Answers</p>
                          <p className="text-2xl font-bold text-red-600">
                            {attempt.total_questions - attempt.correct_answers}
                          </p>
                        </div>
                        <XCircle className="h-8 w-8 text-red-600" />
                      </div>
                    </div>

                    <div className="bg-blue-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Percentage</p>
                          <p className="text-2xl font-bold text-blue-600">{percentage}%</p>
                        </div>
                        <TrendingUp className="h-8 w-8 text-blue-600" />
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default Results
