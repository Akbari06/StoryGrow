'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function ParentsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  const navItems = [
    { href: '/parents/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/parents/stories', label: 'Stories', icon: '📚' },
    { href: '/parents/insights', label: 'Insights', icon: '🧠' },
    { href: '/parents/settings', label: 'Settings', icon: '⚙️' },
  ]

  return (
    <div className="min-h-screen bg-gray-50 parent-theme">
      <style jsx global>{`
        body {
          font-family: 'Inter', sans-serif;
        }
      `}</style>
      
      <div className="flex">
        {/* Sidebar */}
        <aside className={`
          ${isSidebarOpen ? 'w-64' : 'w-20'} 
          bg-white shadow-lg transition-all duration-300
          min-h-screen
        `}>
          <div className="p-6">
            <h1 className={`
              font-bold text-2xl text-indigo-600 
              ${!isSidebarOpen && 'text-center'}
            `}>
              {isSidebarOpen ? 'StoryGrow' : 'SG'}
            </h1>
          </div>
          
          <nav className="px-4">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  flex items-center px-4 py-3 mb-2 rounded-lg transition-colors
                  ${pathname === item.href 
                    ? 'bg-indigo-50 text-indigo-600' 
                    : 'hover:bg-gray-100 text-gray-700'
                  }
                `}
              >
                <span className="text-xl">{item.icon}</span>
                {isSidebarOpen && (
                  <span className="ml-3">{item.label}</span>
                )}
              </Link>
            ))}
          </nav>
          
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="absolute bottom-4 right-4 p-2 hover:bg-gray-100 rounded-lg"
          >
            {isSidebarOpen ? '←' : '→'}
          </button>
        </aside>

        {/* Main content */}
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  )
}