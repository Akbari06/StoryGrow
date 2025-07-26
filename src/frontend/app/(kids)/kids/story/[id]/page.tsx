'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import StoryViewer from '@/components/StoryViewer'
import { config } from '@/lib/config'

interface Story {
  id: string
  title: string
  scenes: Array<{
    sceneNumber: number
    text: string
    imagePrompt: string
    imageUrl?: string
  }>
  metadata: {
    createdAt: string
  }
}

export default function StoryPage() {
  const params = useParams()
  const router = useRouter()
  const [story, setStory] = useState<Story | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStory()
  }, [params.id])

  const fetchStory = async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/story/${params.id}`)
      const data = await response.json()
      setStory(data)
    } catch (error) {
      console.error('Error fetching story:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-4xl animate-pulse">Loading your story... 📖</div>
      </div>
    )
  }

  if (!story) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-2xl text-gray-600 mb-4">Story not found!</p>
          <button 
            onClick={() => router.push('/kids/home')}
            className="kids-button"
          >
            Create a new story
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <StoryViewer story={story} isKidsMode={true} />
      
      <div className="fixed bottom-8 right-8">
        <button
          onClick={() => router.push('/kids/home')}
          className="bg-gradient-to-r from-green-400 to-blue-400 text-white px-8 py-4 rounded-full text-xl font-bold shadow-xl hover:scale-110 transition-transform"
        >
          New Story! 🌟
        </button>
      </div>
    </div>
  )
}