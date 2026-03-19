import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { Menu, X, Zap, Sun, Moon } from 'lucide-react'
import { useAuthStore } from '@/store/auth'
import { clsx } from 'clsx'

interface NavbarProps {
  transparent?: boolean
}

export default function Navbar({ transparent = false }: NavbarProps) {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [dark, setDark] = useState(() => document.documentElement.classList.contains('dark'))

  const toggleDark = () => {
    document.documentElement.classList.toggle('dark')
    setDark(!dark)
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav
      className={clsx(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        transparent
          ? 'bg-transparent'
          : 'bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-slate-100 dark:border-slate-800'
      )}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center shadow-lg shadow-brand-500/30 group-hover:scale-110 transition-transform">
              <Zap size={16} className="text-white" />
            </div>
            <span className="font-display font-bold text-lg text-slate-900 dark:text-white">
              Трамплин
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            <Link to="/opportunities" className="btn-ghost text-sm">Вакансии</Link>
            {user ? (
              <>
                <Link to="/dashboard" className="btn-ghost text-sm">Кабинет</Link>
                <button onClick={handleLogout} className="btn-ghost text-sm text-red-500">Выйти</button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn-ghost text-sm">Войти</Link>
                <Link to="/register" className="btn-primary text-sm">Зарегистрироваться</Link>
              </>
            )}
            <button
              onClick={toggleDark}
              className="btn-ghost ml-1 p-2"
              aria-label="Toggle theme"
            >
              {dark ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden btn-ghost p-2"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden bg-white dark:bg-slate-950 border-t border-slate-100 dark:border-slate-800 px-4 py-4 space-y-2">
          <Link to="/opportunities" className="block btn-ghost text-sm w-full" onClick={() => setMobileOpen(false)}>
            Вакансии
          </Link>
          {user ? (
            <>
              <Link to="/dashboard" className="block btn-ghost text-sm w-full" onClick={() => setMobileOpen(false)}>
                Кабинет
              </Link>
              <button onClick={handleLogout} className="block btn-ghost text-sm w-full text-left text-red-500">
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="block btn-ghost text-sm w-full" onClick={() => setMobileOpen(false)}>
                Войти
              </Link>
              <Link to="/register" className="block btn-primary text-sm w-full justify-center" onClick={() => setMobileOpen(false)}>
                Зарегистрироваться
              </Link>
            </>
          )}
        </div>
      )}
    </nav>
  )
}
