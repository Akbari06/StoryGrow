'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function HomePage() {
  const router = useRouter()
  const [selectedRole, setSelectedRole] = useState<'kids' | 'parents' | null>(null)

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-yellow-50 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
            StoryGrow
          </h1>
          <p className="text-2xl text-gray-700">Where imagination meets growth</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Kids Portal */}
          <div 
            className={`
              relative overflow-hidden rounded-3xl p-8 cursor-pointer transition-all duration-300
              ${selectedRole === 'kids' ? 'scale-105 ring-4 ring-purple-400' : 'hover:scale-105'}
              bg-gradient-to-br from-purple-400 to-pink-400 text-white
            `}
            onClick={() => setSelectedRole('kids')}
          >
            <div className="relative z-10">
              <div className="text-6xl mb-4">🌟</div>
              <h2 className="text-3xl font-bold mb-2">For Kids!</h2>
              <p className="text-lg opacity-90">Tell your stories and watch magic happen</p>
              
              {selectedRole === 'kids' && (
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    router.push('/kids/home')
                  }}
                  className="mt-6 bg-white text-purple-600 px-6 py-3 rounded-full font-bold hover:bg-yellow-100 transition-colors"
                >
                  Let's Go! →
                </button>
              )}
            </div>
            
            {/* Decorative elements */}
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-yellow-300 rounded-full opacity-20" />
            <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-blue-300 rounded-full opacity-20" />
          </div>

          {/* Parent Portal */}
          <div 
            className={`
              relative overflow-hidden rounded-xl p-8 cursor-pointer transition-all duration-300
              ${selectedRole === 'parents' ? 'scale-105 ring-4 ring-indigo-400' : 'hover:scale-105'}
              bg-gradient-to-br from-indigo-500 to-blue-600 text-white
            `}
            onClick={() => setSelectedRole('parents')}
          >
            <div className="relative z-10">
              <div className="text-6xl mb-4">👨‍👩‍👧‍👦</div>
              <h2 className="text-3xl font-bold mb-2">For Parents</h2>
              <p className="text-lg opacity-90">Guide, monitor, and cherish their growth</p>
              
              {selectedRole === 'parents' && (
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    router.push('/parents/login')
                  }}
                  className="mt-6 bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Enter Dashboard →
                </button>
              )}
            </div>
            
            {/* Decorative elements */}
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-green-300 rounded-full opacity-20" />
          </div>
        </div>

        <div className="text-center mt-12 text-gray-600">
          <p className="text-sm">
            StoryGrow uses AI to transform everyday moments into magical learning adventures
          </p>
        </div>
      </div>
    </div>
  )
}