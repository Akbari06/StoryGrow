'use client'

import { useState, useRef, useEffect } from 'react'

interface VoiceRecorderProps {
  onRecordingComplete: (audioBlob: Blob) => void
  maxDuration?: number
  isKidsMode?: boolean
}

export default function VoiceRecorder({ 
  onRecordingComplete, 
  maxDuration = 120,
  isKidsMode = false 
}: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const timerRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    if (isRecording) {
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => {
          if (prev >= maxDuration - 1) {
            stopRecording()
            return prev
          }
          return prev + 1
        })
      }, 1000)
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }, [isRecording, maxDuration])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
        }
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' })
        onRecordingComplete(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setRecordingTime(0)
    } catch (error) {
      console.error('Error accessing microphone:', error)
      alert('Please allow microphone access to record your story!')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (isKidsMode) {
    return (
      <div className="flex flex-col items-center space-y-8">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`
            relative w-48 h-48 rounded-full transition-all duration-300
            ${isRecording 
              ? 'bg-gradient-to-r from-red-500 to-pink-500 animate-pulse' 
              : 'bg-gradient-to-r from-purple-500 to-pink-500 hover:scale-110'
            }
            shadow-2xl flex items-center justify-center
          `}
        >
          <div className="text-white">
            {isRecording ? (
              <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="2" />
              </svg>
            ) : (
              <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
              </svg>
            )}
          </div>
        </button>
        
        {isRecording && (
          <div className="text-center">
            <p className="text-3xl font-bold text-purple-600">
              {formatTime(recordingTime)}
            </p>
            <p className="text-xl text-gray-600 mt-2">
              Keep talking! I'm listening... 🎤
            </p>
          </div>
        )}
        
        {!isRecording && recordingTime > 0 && (
          <p className="text-2xl text-green-500 font-bold">
            Great job! Your story is ready! 🌟
          </p>
        )}
      </div>
    )
  }

  // Parent mode UI
  return (
    <div className="flex items-center space-x-4">
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`
          px-4 py-2 rounded-md font-medium transition-all
          ${isRecording 
            ? 'bg-red-600 hover:bg-red-700 text-white' 
            : 'bg-indigo-600 hover:bg-indigo-700 text-white'
          }
        `}
      >
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      
      {isRecording && (
        <span className="text-sm text-gray-600">
          Recording: {formatTime(recordingTime)}
        </span>
      )}
    </div>
  )
}