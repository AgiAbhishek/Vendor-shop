import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login, register } from '../lib/api'

export default function Login() {
  const nav = useNavigate()
  const [isRegister, setIsRegister] = useState(false)
  const [form, setForm] = useState({ username: '', email: '', password: '' })
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function handle(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function onSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      if (isRegister) {
        if (!form.email) throw new Error('Email is required')
        await register({ username: form.username, email: form.email, password: form.password })
      }
      await login(form.username, form.password)
      nav('/dashboard')
    } catch (err) {
      setError(err?.message || 'Authentication failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-bg min-h-[calc(100vh-64px-72px)] -mt-8 -mb-6 grid place-items-center px-4">
      <div className="grid w-full max-w-5xl grid-cols-1 md:grid-cols-2 gap-6 animate-in">
        {/* Brand side */}
        <div className="card-ghost md:h-full flex flex-col justify-center p-8">
          <div className="text-3xl md:text-4xl font-extrabold tracking-tight">
            Manage your shops with ease
          </div>
          <p className="mt-3 text-gray-600">
            Add locations, keep details up to date, and quickly find shops near you everything in one place.
          </p>
          <ul className="mt-6 grid gap-2 text-sm text-gray-700">
            <li>• Add & manage multiple shops</li>
            <li>• Find nearby shops (distance-based)</li>
            <li>• Fast, responsive experience</li>
          </ul>
        </div>

        {/* Form side */}
        <div className="card p-8">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold">
              {isRegister ? 'Create your vendor account' : 'Welcome back'}
            </h1>
            <button className="btn btn-soft" onClick={() => setIsRegister(s => !s)}>
              {isRegister ? 'Have an account?' : 'Create account'}
            </button>
          </div>

          {error && <div className="mt-4 text-sm text-red-600">{error}</div>}

          <form onSubmit={onSubmit} className="mt-6 grid gap-4">
            <div>
              <div className="label">Username</div>
              <input name="username" className="input" value={form.username} onChange={handle} autoFocus required />
              <div className="help mt-1">Pick a unique vendor username</div>
            </div>

            {isRegister && (
              <div>
                <div className="label">Email</div>
                <input type="email" name="email" className="input" value={form.email} onChange={handle} required />
              </div>
            )}

            <div>
              <div className="label">Password</div>
              <div className="flex gap-2">
                <input
                  name="password"
                  className="input flex-1"
                  type={showPass ? 'text' : 'password'}
                  value={form.password}
                  onChange={handle}
                  required
                />
                <button type="button" className="btn btn-soft" onClick={() => setShowPass(p => !p)}>
                  {showPass ? 'Hide' : 'Show'}
                </button>
              </div>
            </div>

            <button className="btn btn-primary w-full mt-2" disabled={loading}>
              {loading ? (isRegister ? 'Creating…' : 'Signing in…') : (isRegister ? 'Create account' : 'Sign in')}
            </button>

            {!isRegister && (
              <div className="text-xs text-gray-500 text-center">
                New here? Use “Create account” to get started.
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  )
}