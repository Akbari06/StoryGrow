'use client'

import { useState } from 'react'

interface StoryViewerProps {
  story: {
    title: string
    scenes: Array<{
      sceneNumber: number
      text: string
      imagePrompt: string
      imageUrl?: string
    }>
  }
  isKidsMode?: boolean
}

export default function StoryViewer({ story, isKidsMode = false }: StoryViewerProps) {
  const [currentScene, setCurrentScene] = useState(0)

  const nextScene = () => {
    if (currentScene < story.scenes.length - 1) {
      setCurrentScene(currentScene + 1)
    }
  }

  const prevScene = () => {
    if (currentScene > 0) {
      setCurrentScene(currentScene - 1)
    }
  }

  const scene = story.scenes[currentScene]

  if (isKidsMode) {
    return (
      <div className="min-h-screen p-8 flex flex-col items-center justify-center">
        {/* Story Title */}
        <h1 className="text-4xl md:text-5xl font-bold text-purple-600 mb-8 text-center">
          {story.title}
        </h1>

        {/* Scene Display */}
        <div className="max-w-4xl w-full">
          {/* Image */}
          <div className="aspect-video bg-gradient-to-br from-purple-200 to-pink-200 rounded-3xl mb-8 shadow-2xl flex items-center justify-center">
            {scene.imageUrl ? (
              <img 
                src={scene.imageUrl} 
                alt={`Scene ${scene.sceneNumber}`}
                className="w-full h-full object-cover rounded-3xl"
              />
            ) : (
              <div className="text-center p-8">
                <div className="text-8xl mb-4">🖼️</div>
                <p className="text-2xl text-purple-700">
                  Picture coming soon!
                </p>
              </div>
            )}
          </div>

          {/* Text */}
          <div className="bg-white rounded-3xl p-8 shadow-xl mb-8">
            <p className="text-2xl md:text-3xl leading-relaxed text-gray-800">
              {scene.text}
            </p>
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center">
            <button
              onClick={prevScene}
              disabled={currentScene === 0}
              className={`
                text-6xl transition-all duration-200
                ${currentScene === 0 
                  ? 'opacity-30 cursor-not-allowed' 
                  : 'hover:scale-110 active:scale-95'
                }
              `}
            >
              ⬅️
            </button>

            {/* Progress Dots */}
            <div className="flex gap-2">
              {story.scenes.map((_, index) => (
                <div
                  key={index}
                  className={`
                    w-3 h-3 rounded-full transition-all duration-300
                    ${index === currentScene 
                      ? 'bg-purple-600 w-8' 
                      : 'bg-purple-300'
                    }
                  `}
                />
              ))}
            </div>

            <button
              onClick={nextScene}
              disabled={currentScene === story.scenes.length - 1}
              className={`
                text-6xl transition-all duration-200
                ${currentScene === story.scenes.length - 1 
                  ? 'opacity-30 cursor-not-allowed' 
                  : 'hover:scale-110 active:scale-95'
                }
              `}
            >
              ➡️
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Parent view - more compact
  return (
    <div className="parent-card">
      <h2 className="text-2xl font-bold mb-4">{story.title}</h2>
      
      <div className="space-y-4">
        {story.scenes.map((scene, index) => (
          <div key={index} className="border-l-4 border-indigo-200 pl-4">
            <p className="font-medium text-sm text-gray-600 mb-1">
              Scene {scene.sceneNumber}
            </p>
            <p className="text-gray-800">{scene.text}</p>
          </div>
        ))}
      </div>
    </div>
  )
}