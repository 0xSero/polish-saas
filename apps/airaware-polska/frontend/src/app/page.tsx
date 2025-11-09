'use client'

import { useState, useEffect } from 'react'
import { BellAlertIcon, MapPinIcon, CloudIcon } from '@heroicons/react/24/outline'

interface City {
  id: number
  name: string
  voivodeship: string
}

interface AirQualityData {
  aqi: number
  aqi_category: string
  pm25?: number
  pm10?: number
}

export default function Home() {
  const [cities, setCities] = useState<City[]>([])
  const [selectedCity, setSelectedCity] = useState<City | null>(null)
  const [airQuality, setAirQuality] = useState<AirQualityData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock data for demonstration
    const mockCities: City[] = [
      { id: 1, name: 'Warszawa', voivodeship: 'Mazowieckie' },
      { id: 2, name: 'Kraków', voivodeship: 'Małopolskie' },
      { id: 3, name: 'Wrocław', voivodeship: 'Dolnośląskie' },
    ]
    setCities(mockCities)
    setSelectedCity(mockCities[0])
    setAirQuality({
      aqi: 125,
      aqi_category: 'Unhealthy for Sensitive Groups',
      pm25: 45.2,
      pm10: 85.7,
    })
    setLoading(false)
  }, [])

  const getAQIColor = (aqi: number) => {
    if (aqi <= 50) return 'bg-green-500'
    if (aqi <= 100) return 'bg-yellow-500'
    if (aqi <= 150) return 'bg-orange-500'
    if (aqi <= 200) return 'bg-red-500'
    if (aqi <= 300) return 'bg-purple-500'
    return 'bg-red-900'
  }

  const getAQITextColor = (aqi: number) => {
    if (aqi <= 50) return 'text-green-600'
    if (aqi <= 100) return 'text-yellow-600'
    if (aqi <= 150) return 'text-orange-600'
    if (aqi <= 200) return 'text-red-600'
    if (aqi <= 300) return 'text-purple-600'
    return 'text-red-900'
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Ładowanie...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <CloudIcon className="h-8 w-8 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-900">
                AirAware Polska
              </h1>
            </div>
            <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700">
              Zaloguj się
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* City Selector */}
        <section className="mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <MapPinIcon className="h-6 w-6 mr-2 text-blue-600" />
              Wybierz Miasto
            </h2>
            <div className="flex flex-wrap gap-2">
              {cities.map((city) => (
                <button
                  key={city.id}
                  onClick={() => setSelectedCity(city)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedCity?.id === city.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {city.name}
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Current Air Quality */}
        {airQuality && (
          <section className="mb-8">
            <div className="bg-white rounded-lg shadow p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Aktualna Jakość Powietrza - {selectedCity?.name}
              </h2>

              {/* AQI Display */}
              <div className="text-center mb-8">
                <div className={`inline-block rounded-full p-8 ${getAQIColor(airQuality.aqi)} bg-opacity-10`}>
                  <div className={`text-6xl font-bold ${getAQITextColor(airQuality.aqi)}`}>
                    {airQuality.aqi}
                  </div>
                  <div className="text-xl mt-2 text-gray-700">
                    {airQuality.aqi_category}
                  </div>
                </div>
              </div>

              {/* Pollutant Details */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {airQuality.pm25 && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-sm text-gray-600">PM2.5</div>
                    <div className="text-2xl font-bold text-gray-900">
                      {airQuality.pm25} µg/m³
                    </div>
                  </div>
                )}
                {airQuality.pm10 && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-sm text-gray-600">PM10</div>
                    <div className="text-2xl font-bold text-gray-900">
                      {airQuality.pm10} µg/m³
                    </div>
                  </div>
                )}
              </div>
            </div>
          </section>
        )}

        {/* Alerts Section */}
        <section className="mb-8">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-lg p-8 text-white">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <BellAlertIcon className="h-8 w-8 mr-2" />
              Ustaw Alerty Jakości Powietrza
            </h2>
            <p className="mb-6">
              Otrzymuj powiadomienia gdy jakość powietrza przekroczy wybrane progi.
              Zadbaj o swoje zdrowie!
            </p>
            <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors">
              Utwórz Alert
            </button>
          </div>
        </section>

        {/* AQI Scale */}
        <section>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Skala AQI (Indeks Jakości Powietrza)
            </h2>
            <div className="space-y-2">
              <div className="flex items-center">
                <div className="w-16 h-4 bg-green-500 rounded mr-3"></div>
                <span className="text-sm">0-50: Dobra</span>
              </div>
              <div className="flex items-center">
                <div className="w-16 h-4 bg-yellow-500 rounded mr-3"></div>
                <span className="text-sm">51-100: Umiarkowana</span>
              </div>
              <div className="flex items-center">
                <div className="w-16 h-4 bg-orange-500 rounded mr-3"></div>
                <span className="text-sm">101-150: Niezdrowa dla wrażliwych grup</span>
              </div>
              <div className="flex items-center">
                <div className="w-16 h-4 bg-red-500 rounded mr-3"></div>
                <span className="text-sm">151-200: Niezdrowa</span>
              </div>
              <div className="flex items-center">
                <div className="w-16 h-4 bg-purple-500 rounded mr-3"></div>
                <span className="text-sm">201-300: Bardzo niezdrowa</span>
              </div>
              <div className="flex items-center">
                <div className="w-16 h-4 bg-red-900 rounded mr-3"></div>
                <span className="text-sm">300+: Niebezpieczna</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="bg-gray-50 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-500 text-sm">
            © 2025 AirAware Polska. Dane z GIOŚ.
          </p>
        </div>
      </footer>
    </main>
  )
}
