'use client'

import { useState, useEffect } from 'react'
import EmotionChart from '@/components/EmotionChart'
import AlertCard from '@/components/AlertCard'

interface DashboardData {
  childName: string
  todayMood: string
  recentStories: number
  emotionTrend: 'improving' | 'stable' | 'concerning'
  alerts: Array<{
    type: string
    severity: string
    message: string
    timestamp: string
  }>
}

export default function ParentDashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [selectedChild, setSelectedChild] = useState('demo_child_123')

  useEffect(() => {
    // In production, fetch real data
    setData({
      childName: 'Emma',
      todayMood: 'happy',
      recentStories: 3,
      emotionTrend: 'stable',
      alerts: []
    })
  }, [selectedChild])

  if (!data) {
    return <div>Loading...</div>
  }

  return (
    <div className="max-w-7xl mx-auto">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back! Here's {data.childName}'s day
        </h1>
        <p className="text-gray-600 mt-2">
          {new Date().toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </p>
      </header>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="parent-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Today's Mood</p>
              <p className="text-2xl font-semibold mt-1 capitalize">
                {data.todayMood} 😊
              </p>
            </div>
            <div className="text-4xl">
              {data.todayMood === 'happy' ? '😊' : '😐'}
            </div>
          </div>
        </div>

        <div className="parent-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Stories This Week</p>
              <p className="text-2xl font-semibold mt-1">{data.recentStories}</p>
            </div>
            <div className="text-4xl">📚</div>
          </div>
        </div>

        <div className="parent-card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Emotional Trend</p>
              <p className="text-2xl font-semibold mt-1 capitalize">
                {data.emotionTrend}
              </p>
            </div>
            <div className="text-4xl">
              {data.emotionTrend === 'improving' ? '📈' : '➡️'}
            </div>
          </div>
        </div>
      </div>

      {/* Emotion Chart */}
      <div className="parent-card mb-8">
        <h2 className="text-xl font-semibold mb-4">Emotional Journey (Last 7 Days)</h2>
        <EmotionChart childId={selectedChild} />
      </div>

      {/* Alerts */}
      {data.alerts.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Alerts</h2>
          <div className="space-y-4">
            {data.alerts.map((alert, index) => (
              <AlertCard key={index} alert={alert} />
            ))}
          </div>
        </div>
      )}

      {/* Recent Stories */}
      <div className="parent-card">
        <h2 className="text-xl font-semibold mb-4">Recent Stories</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
              <div className="aspect-video bg-gradient-to-br from-purple-100 to-pink-100 rounded mb-3" />
              <h3 className="font-medium">The Butterfly Adventure</h3>
              <p className="text-sm text-gray-600 mt-1">2 hours ago</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}