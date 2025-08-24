import React from 'react'
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom'

export default function App() {
  const nav = useNavigate()
  const loc = useLocation()
  const isAuthed = !!localStorage.getItem('token')

  function logout() {
    localStorage.removeItem('token')
    nav('/login')
  }
  const pill = (path, label) => (
    <Link
      to={path}
      className={`nav-pill ${loc.pathname === path ? 'nav-pill-active' : ''}`}
    >
      {label}
    </Link>
  )

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b bg-white/80 backdrop-blur">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center gap-4">
          <div className="font-extrabold tracking-tight text-xl">Vendor & Shop</div>
          <nav className="ml-auto flex items-center gap-2">
            {pill('/search', 'Search Nearby')}
            {isAuthed && pill('/dashboard', 'Dashboard')}
            {isAuthed && pill('/shops/new', 'Add Shop')}
            {isAuthed ? (
              <button className="nav-pill" onClick={logout}>Logout</button>
            ) : (
              pill('/login', 'Login')
            )}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>

      <footer className="border-t py-6 text-center text-sm text-gray-500">
        © {new Date().getFullYear()} Vendor & Shop
      </footer>
    </div>
  )
}