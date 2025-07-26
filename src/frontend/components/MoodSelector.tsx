'use client'

interface MoodSelectorProps {
  onMoodSelect: (mood: string) => void
  selectedMood: string | null
  isKidsMode?: boolean
}

const moods = [
  { id: 'happy', emoji: '😊', label: 'Happy', color: 'from-yellow-400 to-orange-400' },
  { id: 'excited', emoji: '🤗', label: 'Excited', color: 'from-pink-400 to-red-400' },
  { id: 'calm', emoji: '😌', label: 'Calm', color: 'from-blue-400 to-cyan-400' },
  { id: 'sad', emoji: '😢', label: 'Sad', color: 'from-gray-400 to-blue-400' },
  { id: 'angry', emoji: '😠', label: 'Angry', color: 'from-red-500 to-orange-500' },
]

export default function MoodSelector({ onMoodSelect, selectedMood, isKidsMode = false }: MoodSelectorProps) {
  if (isKidsMode) {
    return (
      <div className="flex flex-wrap justify-center gap-6">
        {moods.map((mood) => (
          <button
            key={mood.id}
            onClick={() => onMoodSelect(mood.id)}
            className={`
              relative w-32 h-32 rounded-3xl transition-all duration-300
              ${selectedMood === mood.id 
                ? 'scale-110 ring-4 ring-purple-400' 
                : 'hover:scale-105'
              }
              bg-gradient-to-br ${mood.color} shadow-xl
              flex flex-col items-center justify-center
            `}
          >
            <span className="text-5xl mb-2">{mood.emoji}</span>
            <span className="text-white font-bold">{mood.label}</span>
            
            {selectedMood === mood.id && (
              <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-400 rounded-full flex items-center justify-center text-white">
                ✓
              </div>
            )}
          </button>
        ))}
      </div>
    )
  }

  // Parent mode - simpler design
  return (
    <div className="flex gap-2">
      {moods.map((mood) => (
        <button
          key={mood.id}
          onClick={() => onMoodSelect(mood.id)}
          className={`
            px-4 py-2 rounded-lg border-2 transition-all
            ${selectedMood === mood.id 
              ? 'border-indigo-600 bg-indigo-50' 
              : 'border-gray-200 hover:border-gray-300'
            }
          `}
        >
          <span className="text-2xl mr-2">{mood.emoji}</span>
          <span className="text-sm">{mood.label}</span>
        </button>
      ))}
    </div>
  )
}