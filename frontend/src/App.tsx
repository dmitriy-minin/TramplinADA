import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuthStore } from '@/store/auth'
import LandingPage from '@/pages/LandingPage'
import LoginPage from '@/pages/LoginPage'
import RegisterPage from '@/pages/RegisterPage'
import OpportunitiesPage from '@/pages/OpportunitiesPage'
import OpportunityDetailPage from '@/pages/OpportunityDetailPage'
import DashboardLayout from '@/pages/dashboard/DashboardLayout'
import DashboardHome from '@/pages/dashboard/DashboardHome'
import MyApplications from '@/pages/dashboard/MyApplications'
import MyOpportunities from '@/pages/dashboard/MyOpportunities'
import CreateOpportunity from '@/pages/dashboard/CreateOpportunity'
import ProfilePage from '@/pages/dashboard/ProfilePage'
import AdminPanel from '@/pages/dashboard/AdminPanel'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const user = useAuthStore((s) => s.user)
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}

function GuestRoute({ children }: { children: React.ReactNode }) {
  const user = useAuthStore((s) => s.user)
  if (user) return <Navigate to="/dashboard" replace />
  return <>{children}</>
}

export default function App() {
  const refreshUser = useAuthStore((s) => s.refreshUser)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) refreshUser()
  }, [refreshUser])

  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/opportunities" element={<OpportunitiesPage />} />
        <Route path="/opportunities/:id" element={<OpportunityDetailPage />} />

        {/* Auth */}
        <Route path="/login" element={<GuestRoute><LoginPage /></GuestRoute>} />
        <Route path="/register" element={<GuestRoute><RegisterPage /></GuestRoute>} />

        {/* Dashboard */}
        <Route path="/dashboard" element={<PrivateRoute><DashboardLayout /></PrivateRoute>}>
          <Route index element={<DashboardHome />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="applications" element={<MyApplications />} />
          <Route path="opportunities" element={<MyOpportunities />} />
          <Route path="opportunities/new" element={<CreateOpportunity />} />
          <Route path="admin" element={<AdminPanel />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
