'use client'

import { useEffect, useState } from 'use'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { CalendarIcon, BellIcon, UserIcon, CogIcon } from '@heroicons/react/24/outline'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

export default function DashboardPage() {
  const { isAuthenticated, user, logout } = useAuth()
  const router = useRouter()
  const [contacts, setContacts] = useState([])
  const [upcomingNameDays, setUpcomingNameDays] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
    } else {
      loadData()
    }
  }, [isAuthenticated])

  const loadData = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const headers = { Authorization: `Bearer ${token}` }

      const [contactsRes, upcomingRes] = await Promise.all([
        axios.get(`${API_URL}/api/contacts/`, { headers }),
        axios.get(`${API_URL}/api/contacts/upcoming_namedays/`, { headers })
      ])

      setContacts(contactsRes.data)
      setUpcomingNameDays(upcomingRes.data)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Ładowanie...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <CalendarIcon className="h-8 w-8 text-red-600 mr-2" />
              <span className="text-xl font-bold">Imieniny Reminder</span>
            </div>
            <div className="flex items-center space-x-4">
              <a href="/dashboard" className="text-gray-700 hover:text-red-600">Dashboard</a>
              <a href="/contacts" className="text-gray-700 hover:text-red-600">Kontakty</a>
              <a href="/settings" className="text-gray-700 hover:text-red-600">Ustawienia</a>
              <button
                onClick={logout}
                className="text-gray-700 hover:text-red-600"
              >
                Wyloguj
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Witaj, {user?.username}!
        </h1>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <UserIcon className="h-8 w-8 text-red-600 mr-3" />
              <div>
                <div className="text-2xl font-bold">{contacts.length}</div>
                <div className="text-gray-600">Kontaktów</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <BellIcon className="h-8 w-8 text-red-600 mr-3" />
              <div>
                <div className="text-2xl font-bold">{upcomingNameDays.length}</div>
                <div className="text-gray-600">Nadchodzące Imieniny</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <CalendarIcon className="h-8 w-8 text-red-600 mr-3" />
              <div>
                <div className="text-2xl font-bold">Aktywne</div>
                <div className="text-gray-600">Powiadomienia</div>
              </div>
            </div>
          </div>
        </div>

        {/* Upcoming Name Days */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">Nadchodzące Imieniny</h2>
          {upcomingNameDays.length > 0 ? (
            <div className="space-y-4">
              {upcomingNameDays.map((day: any) => (
                <div key={day.date} className="border-l-4 border-red-500 pl-4">
                  <div className="text-sm text-gray-500 mb-2">
                    {day.days_until === 0 ? 'Dzisiaj' : `Za ${day.days_until} dni`}
                  </div>
                  {day.contacts.map((contact: any) => (
                    <div key={contact.id} className="bg-gray-50 rounded p-3 mb-2">
                      <div className="font-semibold">{contact.name}</div>
                      <div className="text-sm text-gray-600">
                        {contact.name_day_details?.name}
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">Brak nadchodzących imienin</p>
          )}
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Szybkie Akcje</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a
              href="/contacts/add"
              className="block bg-red-600 text-white text-center py-3 px-6 rounded-lg hover:bg-red-700"
            >
              + Dodaj Kontakt
            </a>
            <a
              href="/contacts"
              className="block bg-gray-200 text-gray-700 text-center py-3 px-6 rounded-lg hover:bg-gray-300"
            >
              Zobacz Wszystkie Kontakty
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
