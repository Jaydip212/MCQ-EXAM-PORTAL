import { useState, useEffect } from 'react';
import axios from 'axios';
import { Trophy, Medal, Award, TrendingUp } from 'lucide-react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('global'); // global or exam
  const [exams, setExams] = useState([]);
  const [selectedExam, setSelectedExam] = useState('');

  useEffect(() => {
    fetchLeaderboard();
    fetchExams();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:8000/api/leaderboard/global_leaderboard/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchExams = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://127.0.0.1:8000/api/exams/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setExams(response.data);
    } catch (error) {
      console.error('Error fetching exams:', error);
    }
  };

  const fetchExamLeaderboard = async (examId) => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://127.0.0.1:8000/api/leaderboard/exam/${examId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching exam leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExamChange = (examId) => {
    setSelectedExam(examId);
    if (examId) {
      fetchExamLeaderboard(examId);
    } else {
      fetchLeaderboard();
    }
  };

  const getRankIcon = (rank) => {
    if (rank === 1) return <Trophy className="w-6 h-6 text-yellow-500" />;
    if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />;
    if (rank === 3) return <Award className="w-6 h-6 text-amber-600" />;
    return <span className="text-lg font-bold text-gray-600">#{rank}</span>;
  };

  const getRankBg = (rank) => {
    if (rank === 1) return 'bg-gradient-to-r from-yellow-50 to-yellow-100 border-yellow-300';
    if (rank === 2) return 'bg-gradient-to-r from-gray-50 to-gray-100 border-gray-300';
    if (rank === 3) return 'bg-gradient-to-r from-amber-50 to-amber-100 border-amber-300';
    return 'bg-white border-gray-200';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="w-8 h-8 text-indigo-600" />
          <h1 className="text-3xl font-bold text-gray-900">Leaderboard</h1>
        </div>
        <p className="text-gray-600">Top performers and rankings</p>
      </div>

      {/* View Toggle & Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex gap-2">
            <button
              onClick={() => {
                setView('global');
                setSelectedExam('');
                fetchLeaderboard();
              }}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                view === 'global'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Global Rankings
            </button>
            <button
              onClick={() => setView('exam')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                view === 'exam'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Exam Rankings
            </button>
          </div>

          {view === 'exam' && (
            <select
              value={selectedExam}
              onChange={(e) => handleExamChange(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="">Select an exam</option>
              {exams.map((exam) => (
                <option key={exam.id} value={exam.id}>
                  {exam.title}
                </option>
              ))}
            </select>
          )}
        </div>
      </div>

      {/* Leaderboard Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-semibold">Rank</th>
                <th className="px-6 py-4 text-left text-sm font-semibold">Student</th>
                <th className="px-6 py-4 text-center text-sm font-semibold">Total Points</th>
                <th className="px-6 py-4 text-center text-sm font-semibold">Exams Completed</th>
                <th className="px-6 py-4 text-center text-sm font-semibold">Average Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {leaderboard.map((entry) => (
                <tr
                  key={entry.rank}
                  className={`${getRankBg(entry.rank)} border-l-4 transition hover:shadow-md`}
                >
                  <td className="px-6 py-4">
                    <div className="flex items-center justify-center w-12">
                      {getRankIcon(entry.rank)}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      {entry.profile_image ? (
                        <img
                          src={entry.profile_image}
                          alt={entry.student_name}
                          className="w-10 h-10 rounded-full object-cover"
                        />
                      ) : (
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold">
                          {entry.student_name.charAt(0)}
                        </div>
                      )}
                      <span className="font-medium text-gray-900">{entry.student_name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-indigo-100 text-indigo-800">
                      {entry.total_points} pts
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className="text-gray-900 font-medium">{entry.exams_completed}</span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className="text-gray-900 font-medium">{entry.average_score.toFixed(1)}%</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {leaderboard.length === 0 && (
          <div className="text-center py-12">
            <Trophy className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No rankings available yet</p>
            <p className="text-gray-400 text-sm mt-2">Complete exams to appear on the leaderboard!</p>
          </div>
        )}
      </div>

      {/* Stats Cards */}
      {leaderboard.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg p-6 border border-yellow-200">
            <div className="flex items-center gap-3 mb-2">
              <Trophy className="w-6 h-6 text-yellow-600" />
              <h3 className="font-semibold text-gray-900">Top Scorer</h3>
            </div>
            <p className="text-2xl font-bold text-gray-900">{leaderboard[0]?.student_name}</p>
            <p className="text-sm text-gray-600 mt-1">{leaderboard[0]?.total_points} points</p>
          </div>

          <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-lg p-6 border border-indigo-200">
            <div className="flex items-center gap-3 mb-2">
              <TrendingUp className="w-6 h-6 text-indigo-600" />
              <h3 className="font-semibold text-gray-900">Total Participants</h3>
            </div>
            <p className="text-2xl font-bold text-gray-900">{leaderboard.length}</p>
            <p className="text-sm text-gray-600 mt-1">Active students</p>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-6 border border-purple-200">
            <div className="flex items-center gap-3 mb-2">
              <Award className="w-6 h-6 text-purple-600" />
              <h3 className="font-semibold text-gray-900">Avg Performance</h3>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {(leaderboard.reduce((sum, e) => sum + e.average_score, 0) / leaderboard.length).toFixed(1)}%
            </p>
            <p className="text-sm text-gray-600 mt-1">Overall average</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;
