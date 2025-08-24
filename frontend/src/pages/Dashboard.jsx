import React, { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { deleteShop, listMyShops } from '../lib/api'

export default function Dashboard() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const nav = useNavigate()

  async function load() {
    setLoading(true)
    setError('')
    try {
      const token = localStorage.getItem('token')
      if (!token) return nav('/login')
      const data = await listMyShops()
      setItems(data.results || data)
    } catch (e) {
      setError(e.message || 'Failed to load')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const kpis = useMemo(() => {
    const total = items.length
    const types = new Set(items.map(i => (i.business_type || '').trim().toLowerCase()).filter(Boolean)).size
    const last = items[0]?.updated_at ? new Date(items[0].updated_at) : null
    return { total, types, last }
  }, [items])

  async function onDelete(id) {
    if (!confirm('Delete this shop?')) return
    setLoading(true)
    try {
      await deleteShop(id)
      await load()
    } catch (e) {
      setError(e.message || 'Delete failed')
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-6">
      {/* Hero */}
      <div className="flex flex-wrap items-center gap-3">
        <div>
          <h2 className="text-2xl md:text-3xl font-extrabold tracking-tight">Your Vendor Dashboard</h2>
          <p className="text-gray-600">Manage shops, track coverage, and keep data fresh.</p>
        </div>
        <Link className="btn btn-primary ml-auto" to="/shops/new">+ Add Shop</Link>
      </div>

      {/* KPI cards */}
      <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="card">
          <div className="text-sm text-gray-500">Total Shops</div>
          <div className="text-3xl font-semibold mt-1">{kpis.total}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-500">Unique Types</div>
          <div className="text-3xl font-semibold mt-1">{kpis.types}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-500">Last Updated</div>
          <div className="text-3xl font-semibold mt-1">{kpis.last ? kpis.last.toLocaleDateString() : '—'}</div>
        </div>
      </section>

      {/* List */}
      <section className="card">
        <div className="flex items-center gap-3 mb-3">
          <h3 className="text-lg font-semibold">My Shops</h3>
          <div className="ml-auto text-sm text-gray-500">{items.length} item(s)</div>
        </div>

        {error && <div className="mb-3 text-sm text-red-600">{error}</div>}

        {loading ? (
          <div className="text-sm text-gray-500">Loading…</div>
        ) : items.length === 0 ? (
          <div className="text-sm text-gray-500">
            You don’t have any shops yet. <Link className="underline" to="/shops/new">Create one</Link>.
          </div>
        ) : (
          <div className="grid gap-3">
            {items.map(s => (
              <div key={s.id} className="border border-black/10 rounded-2xl p-4 flex flex-wrap items-center gap-3">
                <div className="flex-1 min-w-[240px]">
                  <div className="font-semibold">{s.name}</div>
                  <div className="text-sm text-gray-600">
                    Owner: {s.owner_name} • {s.business_type || '—'}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    ({s.latitude}, {s.longitude})
                  </div>
                </div>
                <button className="btn" onClick={() => onDelete(s.id)}>Delete</button>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}