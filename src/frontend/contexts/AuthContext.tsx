'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'

interface User {
  id: string
  email: string
  role: 'parent' | 'kid' | 'admin'
  fullName?: string
}

interface Child {
  id: string
  name: string
  age: number
  avatarEmoji: string
}

interface AuthContextType {
  user: User | null
  loading: boolean
  error: string | null
  
  // For authenticated users
  isAuthenticated: boolean
  isParent: boolean
  isKid: boolean
  
  // For parents managing multiple children
  children: Child[]
  selectedChildId: string | null
  selectChild: (childId: string) => void
  
  // Auth methods
  login: (email: string, password: string, role: 'parent' | 'kid') => Promise<void>
  logout: () => Promise<void>
  
  // Helper to get current child ID (own ID for kids, selected child for parents)
  getCurrentChildId: () => string | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [childrenList, setChildrenList] = useState<Child[]>([])
  const [selectedChildId, setSelectedChildId] = useState<string | null>(null)

  // In development, use demo IDs
  const isDevelopment = process.env.NODE_ENV === 'development'
  
  useEffect(() => {
    // Initialize auth state
    initializeAuth()
  }, [])

  const initializeAuth = async () => {
    try {
      if (isDevelopment) {
        // Use demo user in development
        // Uncomment the role you want to test:
        
        // Demo parent
        setUser({
          id: '11111111-1111-1111-1111-111111111111',
          email: 'demo@parent.com',
          role: 'parent',
          fullName: 'Demo Parent'
        })
        setChildrenList([{
          id: 'demo_child_123',
          name: 'Demo Kid',
          age: 7,
          avatarEmoji: '🦄'
        }])
        setSelectedChildId('demo_child_123')
        
        // Demo kid
        // setUser({
        //   id: '22222222-2222-2222-2222-222222222222',
        //   email: 'demo@child.com',
        //   role: 'kid',
        //   fullName: 'Demo Kid'
        // })
      } else {
        // TODO: Implement real auth check with Firebase/Supabase
        // const authUser = await checkAuthStatus()
        // if (authUser) {
        //   setUser(authUser)
        //   if (authUser.role === 'parent') {
        //     await loadChildren(authUser.id)
        //   }
        // }
      }
    } catch (err) {
      console.error('Auth initialization error:', err)
      setError('Failed to initialize authentication')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string, role: 'parent' | 'kid') => {
    setError(null)
    try {
      // TODO: Implement real login
      // const authResponse = await signIn(email, password)
      // setUser(authResponse.user)
      
      // For now, just redirect based on role
      if (role === 'parent') {
        router.push('/parents/dashboard')
      } else {
        router.push('/kids/home')
      }
    } catch (err: any) {
      setError(err.message || 'Login failed')
      throw err
    }
  }

  const logout = async () => {
    try {
      // TODO: Implement real logout
      // await signOut()
      setUser(null)
      setChildrenList([])
      setSelectedChildId(null)
      router.push('/')
    } catch (err: any) {
      setError(err.message || 'Logout failed')
      throw err
    }
  }

  const selectChild = (childId: string) => {
    setSelectedChildId(childId)
  }

  const getCurrentChildId = () => {
    if (!user) return null
    
    if (user.role === 'kid') {
      // For kids, find their ID from the kids table
      // In development, return demo ID
      return isDevelopment ? 'demo_child_123' : user.id
    } else if (user.role === 'parent') {
      // For parents, return selected child
      return selectedChildId
    }
    
    return null
  }

  const value: AuthContextType = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    isParent: user?.role === 'parent',
    isKid: user?.role === 'kid',
    children: childrenList,
    selectedChildId,
    selectChild,
    login,
    logout,
    getCurrentChildId
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

// Helper hooks for common patterns
export function useCurrentChildId() {
  const { getCurrentChildId } = useAuth()
  return getCurrentChildId()
}

export function useRequireAuth(redirectTo = '/') {
  const { isAuthenticated, loading } = useAuth()
  const router = useRouter()
  
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push(redirectTo)
    }
  }, [isAuthenticated, loading, router, redirectTo])
  
  return { isAuthenticated, loading }
}

export function useRequireParent() {
  const { isParent, loading } = useAuth()
  const router = useRouter()
  
  useEffect(() => {
    if (!loading && !isParent) {
      router.push('/')
    }
  }, [isParent, loading, router])
  
  return { isParent, loading }
}

export function useRequireKid() {
  const { isKid, loading } = useAuth()
  const router = useRouter()
  
  useEffect(() => {
    if (!loading && !isKid) {
      router.push('/')
    }
  }, [isKid, loading, router])
  
  return { isKid, loading }
}