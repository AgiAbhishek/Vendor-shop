import React, { useState } from 'react'
import { getCurrentPosition } from '../lib/geo'

export default function ShopForm({ onSubmit, loading, initial = {} }) {
  const [form, setForm] = useState({
    name: initial.name || '',
    owner_name: initial.owner_name || '',
    business_type: initial.business_type || '',
    latitude: initial.latitude ?? '',
    longitude: initial.longitude ?? ''
  })
  const [geoBusy, setGeoBusy] = useState(false)
  const [err, setErr] = useState('')

  function handle(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function useLocation() {
    setErr('')
    setGeoBusy(true)
    try {
      const { lat, lng } = await getCurrentPosition()
      setForm(f => ({ ...f, latitude: lat.toFixed(6), longitude: lng.toFixed(6) }))
    } catch (e) {
      setErr(e.message || 'Failed to get location')
    } finally {
      setGeoBusy(false)
    }
  }

  function submit(e) {
    e.preventDefault()
    setErr('')
    const lat = parseFloat(form.latitude)
    const lng = parseFloat(form.longitude)
    if (Number.isNaN(lat) || lat < -90 || lat > 90) return setErr('Latitude must be between -90 and 90')
    if (Number.isNaN(lng) || lng < -180 || lng > 180) return setErr('Longitude must be between -180 and 180')
    onSubmit({ ...form, latitude: lat, longitude: lng }).catch(e => setErr(e.message || 'Save failed'))
  }

  return (
    <form onSubmit={submit} className="grid sm:grid-cols-2 gap-3">
      {err && <div className="sm:col-span-2 text-sm text-red-600">{err}</div>}
      <div className="sm:col-span-2">
        <div className="label">Shop Name</div>
        <input name="name" className="input" value={form.name} onChange={handle} required />
      </div>
      <div>
        <div className="label">Owner Name</div>
        <input name="owner_name" className="input" value={form.owner_name} onChange={handle} required />
      </div>
      <div>
        <div className="label">Business Type</div>
        <input name="business_type" className="input" value={form.business_type} onChange={handle} placeholder="grocery, pharmacy…" />
      </div>
      <div>
        <div className="label">Latitude</div>
        <input name="latitude" className="input" value={form.latitude} onChange={handle} type="number" step="any" required />
      </div>
      <div>
        <div className="label">Longitude</div>
        <input name="longitude" className="input" value={form.longitude} onChange={handle} type="number" step="any" required />
      </div>
      <div className="flex items-center gap-2 sm:col-span-2">
        <button type="button" className="btn" onClick={useLocation} disabled={geoBusy}>
          {geoBusy ? 'Locating…' : 'Use Your Current Location'}
        </button>
        <button className="btn btn-primary ml-auto" disabled={loading}>
          {loading ? 'Saving…' : 'Create Shop'}
        </button>
      </div>
    </form>
  )
}