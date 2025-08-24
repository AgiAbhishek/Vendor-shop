import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ShopForm from '../components/ShopForm'
import { createShop } from '../lib/api'

export default function NewShop() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const nav = useNavigate()

  async function onSubmit(payload) {
    setLoading(true)
    setError('')
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        nav('/login')
        return
      }
      await createShop(payload)
      nav('/dashboard')
    } catch (e) {
      setError(e.message || 'Failed to create')
      throw e
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-6">
      <div className="flex items-center gap-3">
        <h2 className="text-2xl font-bold">Add New Shop</h2>
      </div>

      <section className="card">
        {error && <div className="mb-3 text-sm text-red-600">{error}</div>}
        <ShopForm onSubmit={onSubmit} loading={loading} />
      </section>
    </div>
  )
}