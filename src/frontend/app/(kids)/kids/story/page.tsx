'use client'

import { useState, useEffect, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
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

function StoryContent() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const storyId = searchParams.get('id')
  const [story, setStory] = useState<Story | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (storyId) {
      fetchStory(storyId)
    }
  }, [storyId])

  const fetchStory = async (id: string) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/story/${id}`)
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }
      
      const data = await response.json()
      
      if (!data || !data.scenes) {
        throw new Error('Invalid story data')
      }
      
      setStory(data)
    } catch (error) {
      console.error('Error fetching story:', error)
      // Story will remain null, which shows error state
    } finally {
      setLoading(false)
    }
  }

  if (!storyId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-2xl text-gray-600 mb-4">No story selected!</p>
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

export default function StoryPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-4xl animate-pulse">Loading... 📖</div>
      </div>
    }>
      <StoryContent />
    </Suspense>
  )
}