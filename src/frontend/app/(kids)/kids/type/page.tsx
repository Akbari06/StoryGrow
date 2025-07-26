'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { config } from '@/lib/config'

export default function TypeStoryPage() {
  const router = useRouter()
  const [storyText, setStoryText] = useState('')
  const [currentMood, setCurrentMood] = useState('neutral')
  const [isProcessing, setIsProcessing] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!storyText.trim()) return

    setIsProcessing(true)

    try {
      // Create story from text
      const storyResponse = await fetch(`${config.apiUrl}/api/story/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text_input: storyText,
          child_id: 'demo_child_123', // TODO: Replace with useCurrentChildId() from AuthContext
          session_mood: currentMood,
          educational_focus: ['sharing', 'nature'],
          include_elements: [],
        }),
      })

      if (!storyResponse.ok) {
        throw new Error(`API error: ${storyResponse.status}`)
      }

      const data = await storyResponse.json()
      
      if (!data.story_id) {
        throw new Error('No story ID returned')
      }

      // Navigate to story view
      router.push(`/kids/story?id=${data.story_id}`)
    } catch (error) {
      console.error('Error creating story:', error)
      alert('Oops! Something went wrong creating your story. Please try again.')
      setIsProcessing(false)
    }
  }

  const moods = [
    { value: 'happy', emoji: '😊', color: 'yellow' },
    { value: 'sad', emoji: '😢', color: 'blue' },
    { value: 'excited', emoji: '🤩', color: 'purple' },
    { value: 'angry', emoji: '😠', color: 'red' },
    { value: 'scared', emoji: '😨', color: 'gray' },
    { value: 'neutral', emoji: '😐', color: 'gray' }
  ]

  if (isProcessing) {
    return (
      <div className="min-h-screen p-8 flex flex-col items-center justify-center">
        <div className="text-center">
          <div className="w-64 h-64 mb-8 relative">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full animate-pulse" />
            <div className="absolute inset-4 bg-white rounded-full flex items-center justify-center text-8xl animate-spin-slow">
              ✨
            </div>
          </div>
          
          <h2 className="text-4xl font-bold text-purple-600 mb-4">
            Creating your magical story...
          </h2>
          
          <p className="text-2xl text-gray-700">
            The story wizards are working their magic! 🧙‍♂️
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen p-8 bg-gradient-to-br from-yellow-100 to-pink-100">
      {/* Back button */}
      <button
        onClick={() => router.push('/kids/record')}
        className="mb-6 text-purple-600 text-xl flex items-center gap-2 hover:text-purple-800"
      >
        <span className="text-2xl">←</span> Back to recording
      </button>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold text-purple-600 mb-4 text-center">
          Type Your Story! ✍️
        </h1>
        
        <p className="text-2xl text-gray-700 mb-8 text-center">
          How are you feeling today?
        </p>

        {/* Mood selector */}
        <div className="flex justify-center gap-4 mb-8">
          {moods.map((mood) => (
            <button
              key={mood.value}
              onClick={() => setCurrentMood(mood.value)}
              className={`text-6xl p-4 rounded-full transition-all ${
                currentMood === mood.value
                  ? 'bg-white shadow-lg scale-125'
                  : 'hover:scale-110'
              }`}
            >
              {mood.emoji}
            </button>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <textarea
              value={storyText}
              onChange={(e) => setStoryText(e.target.value)}
              placeholder="Tell me about your day! What happened? What did you see? How did you feel?"
              className="w-full h-64 text-2xl p-4 rounded-xl border-2 border-gray-200 focus:border-purple-400 focus:outline-none resize-none"
              autoFocus
            />
          </div>

          <div className="text-center">
            <button
              type="submit"
              disabled={!storyText.trim()}
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-3xl font-bold px-12 py-6 rounded-full hover:scale-105 transition-transform disabled:opacity-50 disabled:hover:scale-100 shadow-xl"
            >
              Create My Story! 🌟
            </button>
          </div>
        </form>

        <div className="mt-8 text-center">
          <button
            onClick={() => router.push('/kids/record')}
            className="text-purple-600 underline text-xl hover:text-purple-800"
          >
            Use voice instead
          </button>
        </div>
      </div>
    </div>
  )
}