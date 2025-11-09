'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import axios from 'axios'
import { loadStripe } from '@stripe/stripe-js'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY!)

export default function PricingPage() {
  const { isAuthenticated } = useAuth()
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [hasPurchased, setHasPurchased] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login?redirect=/pricing')
    } else {
      checkPurchaseStatus()
    }
  }, [isAuthenticated])

  const checkPurchaseStatus = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(`${API_URL}/api/payments/status/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setHasPurchased(response.data.has_purchased)
    } catch (error) {
      console.error('Error checking purchase status:', error)
    }
  }

  const handlePurchase = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.post(
        `${API_URL}/api/payments/create-checkout/`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )

      const stripe = await stripePromise
      if (stripe) {
        const { error } = await stripe.redirectToCheckout({
          sessionId: response.data.sessionId
        })
        if (error) {
          console.error('Stripe error:', error)
        }
      }
    } catch (error) {
      console.error('Purchase error:', error)
    } finally {
      setLoading(false)
    }
  }

  if (hasPurchased) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-red-50 to-white">
        <div className="max-w-md w-full text-center p-8 bg-white rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Już masz pełny dostęp! 🎉
          </h2>
          <p className="text-gray-600 mb-6">
            Dziękujemy za zakup. Możesz teraz korzystać ze wszystkich funkcji.
          </p>
          <button
            onClick={() => router.push('/dashboard')}
            className="bg-red-600 text-white px-6 py-3 rounded-lg hover:bg-red-700"
          >
            Przejdź do Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-red-50 to-white py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Wybierz Plan
          </h1>
          <p className="text-xl text-gray-600">
            Jednorazowa płatność - dożywotni dostęp
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-red-500 to-red-600 px-8 py-6">
            <h3 className="text-2xl font-bold text-white">Pełny Dostęp</h3>
            <p className="text-red-100 mt-2">Wszystkie funkcje bez ograniczeń</p>
          </div>

          <div className="p-8">
            <div className="text-center mb-8">
              <div className="text-5xl font-bold text-gray-900">49 zł</div>
              <div className="text-gray-600 mt-2">jednorazowo</div>
            </div>

            <ul className="space-y-4 mb-8">
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-gray-700">Nielimitowana liczba kontaktów</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-gray-700">Automatyczne powiadomienia email i push</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-gray-700">Pełny kalendarz polskich imienin</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-gray-700">Dożywotni dostęp do wszystkich funkcji</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-gray-700">Wszystkie przyszłe aktualizacje</span>
              </li>
              <li className="flex items-start">
                <svg className="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-gray-700">Wsparcie techniczne</span>
              </li>
            </ul>

            <button
              onClick={handlePurchase}
              disabled={loading}
              className="w-full bg-red-600 text-white py-4 px-6 rounded-lg text-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50"
            >
              {loading ? 'Przekierowywanie...' : 'Kup teraz za 49 zł'}
            </button>

            <p className="text-center text-sm text-gray-500 mt-4">
              Bezpieczna płatność przez Stripe
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
