'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import MoodSelector from '@/components/MoodSelector'

export default function KidsHomePage() {
  const router = useRouter()
  const [selectedMood, setSelectedMood] = useState<string | null>(null)
  const [showMascot, setShowMascot] = useState(true)

  const handleMoodSelect = (mood: string) => {
    setSelectedMood(mood)
    // Store mood in session
    sessionStorage.setItem('currentMood', mood)
    
    // Animate transition
    setTimeout(() => {
      router.push('/kids/record')
    }, 1000)
  }

  return (
    <div className="min-h-screen p-8 flex flex-col items-center justify-center">
      {/* Mascot */}
      {showMascot && (
        <div className="mb-8 animate-bounce-in">
          <div className="w-48 h-48 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center text-8xl shadow-2xl">
            🦋
          </div>
        </div>
      )}

      {/* Greeting */}
      <h1 className="text-5xl font-bold text-purple-600 mb-4 text-center">
        Hi there, Superstar! 🌟
      </h1>
      
      <p className="text-2xl text-gray-700 mb-12 text-center">
        How are you feeling today?
      </p>

      {/* Mood Selector */}
      <MoodSelector 
        onMoodSelect={handleMoodSelect}
        selectedMood={selectedMood}
        isKidsMode={true}
      />

      {selectedMood && (
        <div className="mt-8 animate-pulse">
          <p className="text-2xl text-green-500 font-bold">
            Great choice! Let's create some magic... ✨
          </p>
        </div>
      )}
    </div>
  )
}