import React, { useState } from 'react'
import { nearby, geocodeCity } from '../lib/api'
import { getCurrentPosition } from '../lib/geo'

export default function ShopsSearch() {
  const [lat, setLat] = useState('')
  const [lng, setLng] = useState('')
  const [radius, setRadius] = useState(5)
  const [city, setCity] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState([])
  const [error, setError] = useState('')

  async function useMyLocation() {
    setError('')
    try {
      const { lat, lng } = await getCurrentPosition()
      setLat(lat.toFixed(6))
      setLng(lng.toFixed(6))
    } catch (e) {
      setError(e.message || 'Unable to get location')
    }
  }

  async function useCity() {
    setError('')
    if (!city.trim()) return setError('Enter a city name')
    try {
      const { lat, lng } = await geocodeCity(city.trim())
      setLat(lat.toFixed(6))
      setLng(lng.toFixed(6))
    } catch (e) {
      setError(e.message || 'City not found')
    }
  }

  async function doNearby() {
    setError('')
    const nlat = parseFloat(lat)
    const nlng = parseFloat(lng)
    const nrad = parseFloat(radius)
    if (Number.isNaN(nlat) || Number.isNaN(nlng)) return setError('Latitude and Longitude are required')
    setLoading(true)
    try {
      const data = await nearby(nlat, nlng, nrad)
      setResults(data)
    } catch (e) {
      setError(e.message || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-6">
      <section className="card">
        <h2 className="text-xl font-bold mb-4">Find Shops Nearby</h2>

        {error && <div className="mb-3 text-sm text-red-600">{error}</div>}

        <div className="grid sm:grid-cols-2 gap-3">
          <div>
            <div className="label">City (optional)</div>
            <div className="flex gap-2">
              <input className="input flex-1" value={city} onChange={e=>setCity(e.target.value)} placeholder="e.g., New Delhi" />
              <button className="btn" onClick={useCity}>Use City</button>
            </div>
          </div>

          <div className="sm:col-span-2 flex flex-wrap items-end gap-3">
            <div>
              <div className="label">Latitude</div>
              <input className="input" value={lat} onChange={e=>setLat(e.target.value)} placeholder="28.6139" />
            </div>
            <div>
              <div className="label">Longitude</div>
              <input className="input" value={lng} onChange={e=>setLng(e.target.value)} placeholder="77.2090" />
            </div>
            <div>
              <div className="label">Radius (km)</div>
              <input className="input" type="number" value={radius} onChange={e=>setRadius(e.target.value)} />
            </div>
            <button className="btn" onClick={useMyLocation}>Use Your Location</button>
            <button className="btn btn-primary" onClick={doNearby} disabled={loading}>
              {loading ? 'Searching…' : 'Search'}
            </button>
          </div>
        </div>
      </section>

      <section className="card">
        <h3 className="text-lg font-semibold mb-3">Results</h3>
        {loading ? (
          <div className="text-sm text-gray-500">Loading…</div>
        ) : results.length === 0 ? (
          <div className="text-sm text-gray-500">No shops found for this area.</div>
        ) : (
          <div className="grid gap-3">
            {results.map(s => (
              <div key={s.id} className="border rounded-xl p-4 flex items-center justify-between">
                <div>
                  <div className="font-semibold">{s.name}</div>
                  <div className="text-sm text-gray-500">
                    {s.owner_name} • {s.business_type || '—'} • ({s.latitude}, {s.longitude})
                  </div>
                </div>
                <div className="text-sm">{s.distance_km} km</div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}