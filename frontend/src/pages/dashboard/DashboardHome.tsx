import { Link } from 'react-router-dom'
import { useAuthStore } from '@/store/auth'
import { ArrowRight, Briefcase, FileText, Star, Shield } from 'lucide-react'

export default function DashboardHome() {
  const user = useAuthStore((s) => s.user)

  const CARDS_BY_ROLE = {
    soiskatel: [
      { icon: FileText, title: 'Мои отклики', desc: 'Следите за статусами откликов', to: '/dashboard/applications', color: 'text-brand-500 bg-brand-50 dark:bg-brand-950' },
      { icon: Star, title: 'Избранное', desc: 'Сохранённые вакансии', to: '/opportunities', color: 'text-amber-500 bg-amber-50 dark:bg-amber-950' },
      { icon: Briefcase, title: 'Вакансии', desc: 'Найдите подходящую работу', to: '/opportunities', color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950' },
    ],
    employer: [
      { icon: Briefcase, title: 'Мои вакансии', desc: 'Управление объявлениями', to: '/dashboard/opportunities', color: 'text-brand-500 bg-brand-50 dark:bg-brand-950' },
      { icon: FileText, title: 'Создать вакансию', desc: 'Разместить новое объявление', to: '/dashboard/opportunities/new', color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950' },
    ],
    curator: [
      { icon: Shield, title: 'Администрирование', desc: 'Модерация и управление', to: '/dashboard/admin', color: 'text-purple-500 bg-purple-50 dark:bg-purple-950' },
    ],
  }

  const cards = CARDS_BY_ROLE[user?.role || 'soiskatel'] || []

  return (
    <div className="max-w-4xl">
      {/* Welcome */}
      <div className="mb-8">
        <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white mb-1">
          Привет, {user?.full_name?.split(' ')[0]}! 👋
        </h1>
        <p className="text-slate-500 dark:text-slate-400">
          Добро пожаловать в личный кабинет Трамплина
        </p>
      </div>

      {/* Status banner */}
      {user?.role === 'employer' && !user?.is_verified && (
        <div className="card p-4 border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/50 mb-6">
          <p className="text-sm text-amber-700 dark:text-amber-300 font-medium">
            ⏳ Ваш аккаунт ожидает верификации куратором. Вакансии будут доступны после проверки.
          </p>
        </div>
      )}

      {/* Quick action cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {cards.map((card) => (
          <Link
            key={card.title}
            to={card.to}
            className="card p-5 hover:shadow-md hover:-translate-y-0.5 transition-all group"
          >
            <div className={`w-11 h-11 rounded-xl flex items-center justify-center mb-3 ${card.color}`}>
              <card.icon size={20} />
            </div>
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-1">
              {card.title}
            </h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 mb-3">{card.desc}</p>
            <span className="text-xs text-brand-600 dark:text-brand-400 font-semibold flex items-center gap-1 group-hover:gap-2 transition-all">
              Перейти <ArrowRight size={12} />
            </span>
          </Link>
        ))}
      </div>

      {/* Profile completeness hint */}
      <div className="card p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="font-display font-semibold text-slate-900 dark:text-white mb-1">Заполните профиль</h3>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Полный профиль увеличивает шансы найти работу. Добавьте резюме, GitHub и портфолио.
            </p>
          </div>
          <Link to="/dashboard/profile" className="btn-primary text-sm shrink-0">
            Заполнить
          </Link>
        </div>
      </div>
    </div>
  )
}
