'use client'

import { useState, useEffect } from 'react'
import { CalendarIcon, BellIcon, UserPlusIcon } from '@heroicons/react/24/outline'
import { formatDate } from 'date-fns'
import { pl } from 'date-fns/locale'

interface NameDay {
  id: number
  name: string
  month: number
  day: number
}

interface Contact {
  id: number
  name: string
  phone: string
  email: string
  name_day: number
  name_day_details: NameDay | null
  notes: string
}

export default function Home() {
  const [todayNameDays, setTodayNameDays] = useState<NameDay[]>([])
  const [upcomingContacts, setUpcomingContacts] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock data for demonstration
    // In production, fetch from API
    setTodayNameDays([
      { id: 1, name: 'Jan', month: 11, day: 9 },
      { id: 2, name: 'Teodor', month: 11, day: 9 },
    ])

    setUpcomingContacts([
      {
        date: new Date(),
        days_until: 0,
        contacts: [
          {
            id: 1,
            name: 'Jan Kowalski',
            phone: '+48 123 456 789',
            email: 'jan@example.com',
            name_day_details: { name: 'Jan', month: 11, day: 9 },
          },
        ],
      },
    ])

    setLoading(false)
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Ładowanie...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-red-50 to-white">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <CalendarIcon className="h-8 w-8 text-primary-600" />
              <h1 className="text-3xl font-bold text-gray-900">
                Imieniny Reminder
              </h1>
            </div>
            <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
              <UserPlusIcon className="h-5 w-5 mr-2" />
              Dodaj kontakt
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Today's Name Days */}
        <section className="mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
              <CalendarIcon className="h-6 w-6 mr-2 text-primary-600" />
              Dzisiejsze Imieniny
            </h2>
            <div className="flex flex-wrap gap-2">
              {todayNameDays.length > 0 ? (
                todayNameDays.map((nameDay) => (
                  <span
                    key={nameDay.id}
                    className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-primary-100 text-primary-800"
                  >
                    {nameDay.name}
                  </span>
                ))
              ) : (
                <p className="text-gray-500">Brak imienin dzisiaj</p>
              )}
            </div>
          </div>
        </section>

        {/* Upcoming Name Days */}
        <section className="mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
              <BellIcon className="h-6 w-6 mr-2 text-primary-600" />
              Nadchodzące Imieniny Znajomych
            </h2>
            {upcomingContacts.length > 0 ? (
              <div className="space-y-4">
                {upcomingContacts.map((day, index) => (
                  <div key={index} className="border-l-4 border-primary-500 pl-4">
                    <div className="text-sm text-gray-500 mb-2">
                      {day.days_until === 0
                        ? 'Dzisiaj'
                        : `Za ${day.days_until} ${day.days_until === 1 ? 'dzień' : 'dni'}`}
                    </div>
                    <div className="space-y-3">
                      {day.contacts.map((contact: any) => (
                        <div
                          key={contact.id}
                          className="bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors"
                        >
                          <div className="flex justify-between items-start">
                            <div>
                              <h3 className="font-semibold text-lg text-gray-900">
                                {contact.name}
                              </h3>
                              <p className="text-sm text-gray-600">
                                Imieniny: {contact.name_day_details?.name}
                              </p>
                              {contact.phone && (
                                <p className="text-sm text-gray-500 mt-1">
                                  📱 {contact.phone}
                                </p>
                              )}
                              {contact.email && (
                                <p className="text-sm text-gray-500">
                                  ✉️ {contact.email}
                                </p>
                              )}
                            </div>
                            <button className="text-primary-600 hover:text-primary-800 text-sm font-medium">
                              Wyślij życzenia
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">
                Brak nadchodzących imienin w najbliższych dniach
              </p>
            )}
          </div>
        </section>

        {/* Features Info */}
        <section>
          <div className="bg-gradient-to-r from-primary-500 to-red-600 rounded-lg shadow-lg p-8 text-white">
            <h2 className="text-2xl font-bold mb-4">
              Nigdy nie zapomnij o imieninach!
            </h2>
            <ul className="space-y-2">
              <li className="flex items-center">
                <svg
                  className="h-5 w-5 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                Automatyczne przypomnienia o imieninach znajomych
              </li>
              <li className="flex items-center">
                <svg
                  className="h-5 w-5 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                Pełny kalendarz polskich imienin
              </li>
              <li className="flex items-center">
                <svg
                  className="h-5 w-5 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                Powiadomienia email i push
              </li>
              <li className="flex items-center">
                <svg
                  className="h-5 w-5 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                Jednorazowa płatność - pełny dostęp bez subskrypcji
              </li>
            </ul>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="bg-gray-50 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            © 2025 Imieniny Reminder. Wszystkie prawa zastrzeżone.
          </p>
        </div>
      </footer>
    </main>
  )
}
