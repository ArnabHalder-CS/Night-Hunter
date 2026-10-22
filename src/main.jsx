import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import LandingPage from './components/LandingPage.jsx'

const isLocal =
  window.location.hostname === 'localhost' ||
  window.location.hostname === '127.0.0.1' ||
  window.location.hostname === '0.0.0.0';

function Root() {
  const path = window.location.pathname;

  // 1. If user navigates to /app or /dashboard, run the full App directly on the server!
  if (path === '/app' || path.startsWith('/app/') || path === '/dashboard') {
    return <App />;
  }

  // 2. If user explicitly requests /landing, show LandingPage
  if (path === '/landing') {
    return <LandingPage />;
  }

  // 3. If running locally on localhost/127.0.0.1, default to App
  const isLocal =
    window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1' ||
    window.location.hostname === '0.0.0.0';

  if (isLocal) {
    return <App />;
  }

  // 4. On public cloud server (Render): show LandingPage with direct 1-click access to /app
  return <LandingPage />;
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Root />
  </StrictMode>,
)
