'use client'

import { useEffect, useState } from 'react'

interface EmotionData {
  date: string
  happiness: number
  sadness: number
  fear: number
  anger: number
}

export default function EmotionChart({ childId }: { childId: string }) {
  const [data, setData] = useState<EmotionData[]>([])

  useEffect(() => {
    // Mock data - in production, fetch from API
    const mockData: EmotionData[] = [
      { date: 'Mon', happiness: 0.8, sadness: 0.1, fear: 0.0, anger: 0.1 },
      { date: 'Tue', happiness: 0.7, sadness: 0.2, fear: 0.1, anger: 0.0 },
      { date: 'Wed', happiness: 0.9, sadness: 0.0, fear: 0.0, anger: 0.1 },
      { date: 'Thu', happiness: 0.6, sadness: 0.3, fear: 0.1, anger: 0.0 },
      { date: 'Fri', happiness: 0.8, sadness: 0.1, fear: 0.0, anger: 0.1 },
      { date: 'Sat', happiness: 0.9, sadness: 0.0, fear: 0.0, anger: 0.1 },
      { date: 'Sun', happiness: 0.7, sadness: 0.2, fear: 0.0, anger: 0.1 },
    ]
    setData(mockData)
  }, [childId])

  const emotions = [
    { key: 'happiness', color: 'bg-green-400', label: 'Happy' },
    { key: 'sadness', color: 'bg-blue-400', label: 'Sad' },
    { key: 'fear', color: 'bg-purple-400', label: 'Worried' },
    { key: 'anger', color: 'bg-red-400', label: 'Angry' },
  ]

  return (
    <div>
      {/* Legend */}
      <div className="flex gap-4 mb-6">
        {emotions.map((emotion) => (
          <div key={emotion.key} className="flex items-center gap-2">
            <div className={`w-4 h-4 rounded ${emotion.color}`} />
            <span className="text-sm text-gray-600">{emotion.label}</span>
          </div>
        ))}
      </div>

      {/* Chart */}
      <div className="relative h-64">
        <div className="absolute inset-0 flex items-end justify-between gap-2">
          {data.map((day, index) => (
            <div key={index} className="flex-1 flex flex-col items-center">
              <div className="w-full flex flex-col-reverse gap-1 mb-2">
                {emotions.map((emotion) => {
                  const value = day[emotion.key as keyof EmotionData] as number
                  const height = value * 200 // Scale to max 200px
                  
                  return (
                    <div
                      key={emotion.key}
                      className={`w-full ${emotion.color} rounded-t transition-all duration-500`}
                      style={{ height: `${height}px` }}
                    />
                  )
                })}
              </div>
              <span className="text-sm text-gray-600">{day.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}