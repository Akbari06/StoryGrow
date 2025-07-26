'use client'

import { useRouter, usePathname } from 'next/navigation'

export default function KidsNavigation() {
  const router = useRouter()
  const pathname = usePathname()

  // Don't show on home page
  if (pathname === '/kids') return null

  return (
    <div className="fixed top-4 left-4 z-50">
      <button
        onClick={() => router.back()}
        className="bg-white/80 backdrop-blur-sm rounded-full p-4 shadow-lg hover:shadow-xl transition-all hover:scale-110 flex items-center gap-2"
      >
        <span className="text-3xl">←</span>
        <span className="text-xl font-medium pr-2">Back</span>
      </button>
    </div>
  )
}