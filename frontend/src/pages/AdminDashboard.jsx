import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import axios from 'axios'
import { BookOpen, Users, PlusCircle, Trash2, Edit } from 'lucide-react'

const AdminDashboard = () => {
  const [exams, setExams] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchExams()
  }, [])

  const fetchExams = async () => {
    try {
      const response = await axios.get('/api/exams')
      setExams(response.data)
    } catch (error) {
      console.error('Error fetching exams:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteExam = async (examId) => {
    if (!confirm('Are you sure you want to delete this exam?')) return

    try {
      await axios.delete(`/api/exams/${examId}`)
      setExams(exams.filter(e => e.id !== examId))
      alert('Exam deleted successfully')
    } catch (error) {
      console.error('Error deleting exam:', error)
      alert('Failed to delete exam')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-gray-600 mt-2">Manage exams and questions</p>
          </div>
          <Link to="/admin/create-exam" className="btn-primary flex items-center">
            <PlusCircle className="h-5 w-5 mr-2" />
            Create New Exam
          </Link>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : exams.length === 0 ? (
          <div className="card text-center py-12">
            <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">No Exams Created</h3>
            <p className="text-gray-600 mb-4">Create your first exam to get started</p>
            <Link to="/admin/create-exam" className="btn-primary inline-flex items-center">
              <PlusCircle className="h-5 w-5 mr-2" />
              Create Exam
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {exams.map((exam) => (
              <div key={exam.id} className="card">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{exam.title}</h3>
                    <p className="text-gray-600 text-sm mb-3">{exam.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span>Duration: {exam.duration} min</span>
                      <span>•</span>
                      <span>Total Marks: {exam.total_marks}</span>
                      <span>•</span>
                      <span>Passing: {exam.passing_marks}</span>
                      <span>•</span>
                      <span className={exam.is_active ? 'text-green-600' : 'text-red-600'}>
                        {exam.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <button
                      onClick={() => handleDeleteExam(exam.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminDashboard
