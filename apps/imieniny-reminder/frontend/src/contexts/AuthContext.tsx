'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

interface User {
  id: number
  email: string
  username: string
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token')
    if (token) {
      // Verify token and get user info
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      // In a real app, validate the token here
      setUser({ id: 1, email: 'user@example.com', username: 'user' })
    }
    setLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    const response = await axios.post(`${API_URL}/api/auth/login/`, {
      username: email,
      password,
    })

    const { access, refresh } = response.data
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    axios.defaults.headers.common['Authorization'] = `Bearer ${access}`

    // Get user info
    setUser({ id: 1, email, username: email })
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      isAuthenticated: !!user,
      loading,
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
