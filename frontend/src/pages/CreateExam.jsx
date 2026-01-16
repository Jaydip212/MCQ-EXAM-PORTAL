import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import axios from 'axios'
import { PlusCircle, Trash2, Save } from 'lucide-react'

const CreateExam = () => {
  const navigate = useNavigate()
  const [examData, setExamData] = useState({
    title: '',
    description: '',
    duration: 60,
    total_marks: 0,
    passing_marks: 0,
    is_active: true
  })
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(false)

  const addQuestion = () => {
    setQuestions([
      ...questions,
      {
        question_text: '',
        option_a: '',
        option_b: '',
        option_c: '',
        option_d: '',
        correct_answer: 'A',
        marks: 1,
        image_url: ''
      }
    ])
  }

  const removeQuestion = (index) => {
    setQuestions(questions.filter((_, i) => i !== index))
  }

  const updateQuestion = (index, field, value) => {
    const updated = [...questions]
    updated[index][field] = value
    setQuestions(updated)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (questions.length === 0) {
      alert('Please add at least one question')
      return
    }

    const totalMarks = questions.reduce((sum, q) => sum + parseInt(q.marks), 0)
    
    setLoading(true)

    try {
      const examResponse = await axios.post('/api/exams', {
        ...examData,
        total_marks: totalMarks
      })

      const examId = examResponse.data.id

      for (const question of questions) {
        await axios.post('/api/questions', {
          ...question,
          exam_id: examId,
          marks: parseInt(question.marks)
        })
      }

      alert('Exam created successfully!')
      navigate('/admin')
    } catch (error) {
      console.error('Error creating exam:', error)
      alert('Failed to create exam')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Create New Exam</h1>
          <p className="text-gray-600 mt-2">Fill in the exam details and add questions</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Exam Details</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Exam Title
                </label>
                <input
                  type="text"
                  value={examData.title}
                  onChange={(e) => setExamData({ ...examData, title: e.target.value })}
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={examData.description}
                  onChange={(e) => setExamData({ ...examData, description: e.target.value })}
                  className="input-field"
                  rows="3"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Duration (minutes)
                  </label>
                  <input
                    type="number"
                    value={examData.duration}
                    onChange={(e) => setExamData({ ...examData, duration: parseInt(e.target.value) })}
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Passing Marks
                  </label>
                  <input
                    type="number"
                    value={examData.passing_marks}
                    onChange={(e) => setExamData({ ...examData, passing_marks: parseInt(e.target.value) })}
                    className="input-field"
                    required
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Questions</h2>
              <button
                type="button"
                onClick={addQuestion}
                className="btn-primary flex items-center"
              >
                <PlusCircle className="h-5 w-5 mr-2" />
                Add Question
              </button>
            </div>

            {questions.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No questions added yet</p>
            ) : (
              <div className="space-y-6">
                {questions.map((question, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-4">
                      <h3 className="font-medium text-gray-900">Question {index + 1}</h3>
                      <button
                        type="button"
                        onClick={() => removeQuestion(index)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-5 w-5" />
                      </button>
                    </div>

                    <div className="space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Question Text
                        </label>
                        <textarea
                          value={question.question_text}
                          onChange={(e) => updateQuestion(index, 'question_text', e.target.value)}
                          className="input-field"
                          rows="2"
                          required
                        />
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Option A
                          </label>
                          <input
                            type="text"
                            value={question.option_a}
                            onChange={(e) => updateQuestion(index, 'option_a', e.target.value)}
                            className="input-field"
                            required
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Option B
                          </label>
                          <input
                            type="text"
                            value={question.option_b}
                            onChange={(e) => updateQuestion(index, 'option_b', e.target.value)}
                            className="input-field"
                            required
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Option C
                          </label>
                          <input
                            type="text"
                            value={question.option_c}
                            onChange={(e) => updateQuestion(index, 'option_c', e.target.value)}
                            className="input-field"
                            required
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Option D
                          </label>
                          <input
                            type="text"
                            value={question.option_d}
                            onChange={(e) => updateQuestion(index, 'option_d', e.target.value)}
                            className="input-field"
                            required
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Correct Answer
                          </label>
                          <select
                            value={question.correct_answer}
                            onChange={(e) => updateQuestion(index, 'correct_answer', e.target.value)}
                            className="input-field"
                            required
                          >
                            <option value="A">A</option>
                            <option value="B">B</option>
                            <option value="C">C</option>
                            <option value="D">D</option>
                          </select>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">
                            Marks
                          </label>
                          <input
                            type="number"
                            value={question.marks}
                            onChange={(e) => updateQuestion(index, 'marks', e.target.value)}
                            className="input-field"
                            min="1"
                            required
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => navigate('/admin')}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex items-center disabled:opacity-50"
            >
              <Save className="h-5 w-5 mr-2" />
              {loading ? 'Creating...' : 'Create Exam'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateExam
