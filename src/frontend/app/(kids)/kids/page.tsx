'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function KidsPage() {
  const router = useRouter()

  useEffect(() => {
    router.replace('/kids/home')
  }, [router])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-4xl animate-pulse">Loading... 🌟</div>
    </div>
  )
}