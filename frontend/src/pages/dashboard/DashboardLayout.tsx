import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import {
  Zap, LayoutDashboard, User, FileText, Briefcase, Plus,
  Shield, LogOut, ChevronRight,
} from 'lucide-react'
import { useAuthStore } from '@/store/auth'
import { clsx } from 'clsx'

export default function DashboardLayout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const navItems = [
    { to: '/dashboard', label: 'Обзор', icon: LayoutDashboard, end: true },
    { to: '/dashboard/profile', label: 'Профиль', icon: User },
    ...(user?.role === 'soiskatel'
      ? [{ to: '/dashboard/applications', label: 'Мои отклики', icon: FileText }]
      : []),
    ...(user?.role === 'employer'
      ? [
          { to: '/dashboard/opportunities', label: 'Мои вакансии', icon: Briefcase },
          { to: '/dashboard/opportunities/new', label: 'Создать вакансию', icon: Plus },
        ]
      : []),
    ...(user?.role === 'curator'
      ? [{ to: '/dashboard/admin', label: 'Администрирование', icon: Shield }]
      : []),
  ]

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex">
      {/* Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-white dark:bg-slate-900 border-r border-slate-100 dark:border-slate-800 fixed top-0 left-0 h-full z-40">
        {/* Logo */}
        <div className="flex items-center gap-2 px-6 py-5 border-b border-slate-100 dark:border-slate-800">
          <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center shadow-sm">
            <Zap size={16} className="text-white" />
          </div>
          <span className="font-display font-bold text-slate-900 dark:text-white">Трамплин</span>
        </div>

        {/* User info */}
        <div className="px-4 py-4 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-800">
            <div className="w-9 h-9 rounded-full bg-brand-100 dark:bg-brand-900 flex items-center justify-center text-brand-700 dark:text-brand-300 font-bold text-sm">
              {user?.full_name?.[0]?.toUpperCase()}
            </div>
            <div className="min-w-0">
              <p className="text-sm font-semibold text-slate-900 dark:text-white truncate">{user?.full_name}</p>
              <p className="text-xs text-slate-500 capitalize">{
                user?.role === 'soiskatel' ? 'Соискатель' :
                user?.role === 'employer' ? 'Работодатель' : 'Куратор'
              }</p>
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={'end' in item ? item.end : false}
              className={({ isActive }) =>
                clsx(
                  'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all',
                  isActive
                    ? 'bg-brand-50 dark:bg-brand-950 text-brand-700 dark:text-brand-300'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-200'
                )
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>

        {/* Logout */}
        <div className="px-3 py-4 border-t border-slate-100 dark:border-slate-800">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-medium text-red-500 hover:bg-red-50 dark:hover:bg-red-950/30 transition-colors"
          >
            <LogOut size={18} />
            Выйти
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 md:ml-64">
        {/* Mobile topbar */}
        <div className="md:hidden bg-white dark:bg-slate-900 border-b border-slate-100 dark:border-slate-800 px-4 py-3 flex items-center gap-3">
          <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center">
            <Zap size={16} className="text-white" />
          </div>
          <span className="font-display font-bold text-slate-900 dark:text-white">Трамплин</span>
        </div>

        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
