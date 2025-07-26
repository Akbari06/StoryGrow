import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'StoryGrow - AI Family Storytelling',
  description: 'Transform everyday moments into magical stories',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}