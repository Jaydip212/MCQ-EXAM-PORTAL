import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import axios from 'axios'
import { Clock, CheckCircle, AlertCircle } from 'lucide-react'

const TakeExam = () => {
  const { examId } = useParams()
  const navigate = useNavigate()
  const [exam, setExam] = useState(null)
  const [attemptId, setAttemptId] = useState(null)
  const [answers, setAnswers] = useState({})
  const [timeLeft, setTimeLeft] = useState(0)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    startExam()
  }, [examId])

  useEffect(() => {
    if (timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000)
      return () => clearTimeout(timer)
    } else if (timeLeft === 0 && exam) {
      handleSubmit()
    }
  }, [timeLeft])

  const startExam = async () => {
    try {
      const [examRes, attemptRes] = await Promise.all([
        axios.get(`/api/exams/${examId}`),
        axios.post('/api/students/start-exam', { exam_id: parseInt(examId) })
      ])

      setExam(examRes.data)
      setAttemptId(attemptRes.data.id)
      setTimeLeft(examRes.data.duration * 60)
      
      const initialAnswers = {}
      examRes.data.questions.forEach(q => {
        initialAnswers[q.id] = ''
      })
      setAnswers(initialAnswers)
    } catch (error) {
      console.error('Error starting exam:', error)
      alert('Failed to start exam')
      navigate('/exams')
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({
      ...answers,
      [questionId]: answer
    })
  }

  const handleSubmit = async () => {
    if (submitting) return

    const unanswered = Object.values(answers).filter(a => !a).length
    if (unanswered > 0) {
      if (!confirm(`You have ${unanswered} unanswered questions. Submit anyway?`)) {
        return
      }
    }

    setSubmitting(true)

    try {
      const submission = {
        attempt_id: attemptId,
        answers: Object.entries(answers).map(([questionId, selectedAnswer]) => ({
          question_id: parseInt(questionId),
          selected_answer: selectedAnswer
        }))
      }

      await axios.post('/api/students/submit-exam', submission)
      alert('Exam submitted successfully!')
      navigate('/results')
    } catch (error) {
      console.error('Error submitting exam:', error)
      alert('Failed to submit exam')
    } finally {
      setSubmitting(false)
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="card mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{exam.title}</h1>
              <p className="text-gray-600 mt-1">{exam.description}</p>
            </div>
            <div className="text-right">
              <div className={`flex items-center space-x-2 ${timeLeft < 300 ? 'text-red-600' : 'text-blue-600'}`}>
                <Clock className="h-6 w-6" />
                <span className="text-2xl font-bold">{formatTime(timeLeft)}</span>
              </div>
              <p className="text-sm text-gray-600 mt-1">Time Remaining</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {exam.questions.map((question, index) => (
            <div key={question.id} className="card">
              <div className="mb-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-lg font-medium text-gray-900">
                    Question {index + 1}
                  </h3>
                  <span className="text-sm text-gray-600">{question.marks} marks</span>
                </div>
                <p className="text-gray-700">{question.question_text}</p>
                {question.image_url && (
                  <img src={question.image_url} alt="Question" className="mt-3 rounded-lg max-w-md" />
                )}
              </div>

              <div className="space-y-2">
                {['A', 'B', 'C', 'D'].map((option) => (
                  <label
                    key={option}
                    className={`flex items-center p-3 border-2 rounded-lg cursor-pointer transition-colors ${
                      answers[question.id] === option
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value={option}
                      checked={answers[question.id] === option}
                      onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                      className="mr-3"
                    />
                    <span className="font-medium mr-2">{option}.</span>
                    <span>{question[`option_${option.toLowerCase()}`]}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="card mt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-green-600">
                <CheckCircle className="h-5 w-5 mr-2" />
                <span>{Object.values(answers).filter(a => a).length} Answered</span>
              </div>
              <div className="flex items-center text-yellow-600">
                <AlertCircle className="h-5 w-5 mr-2" />
                <span>{Object.values(answers).filter(a => !a).length} Unanswered</span>
              </div>
            </div>
            <button
              onClick={handleSubmit}
              disabled={submitting}
              className="btn-primary disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : 'Submit Exam'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TakeExam
