import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import App from './App'
import Login from './pages/Login'
import ShopsSearch from './pages/Shops'        // renamed meaning: public/search page
import Dashboard from './pages/Dashboard'      // new
import NewShop from './pages/NewShop'          // new

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <ShopsSearch /> },
      { path: 'login', element: <Login /> },
      { path: 'search', element: <ShopsSearch /> },
      { path: 'dashboard', element: <Dashboard /> },
      { path: 'shops/new', element: <NewShop /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)