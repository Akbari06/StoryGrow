'use client'

import KidsNavigation from '@/components/KidsNavigation'

export default function KidsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-100 via-pink-50 to-yellow-50 kids-theme">
      <KidsNavigation />
      {children}
    </div>
  )
}