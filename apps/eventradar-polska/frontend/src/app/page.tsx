'use client'

import { useState, useEffect } from 'react'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            EventRadar Polska
          </h1>
          <p className="text-gray-600 mt-2">
            Local events aggregator for Polish cities
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Witamy w EventRadar Polska!
          </h2>
          <p className="text-gray-600">
            Aplikacja w fazie rozwoju. Wkrótce dostępne nowe funkcje.
          </p>
        </div>
      </div>
    </main>
  )
}
