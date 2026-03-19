import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Clock, CheckCircle, XCircle, BookmarkCheck } from 'lucide-react'
import api from '@/lib/api'
import type { Application } from '@/types'
import { clsx } from 'clsx'

const STATUS_CONFIG = {
  pending:  { label: 'На рассмотрении', icon: Clock,          class: 'badge-slate' },
  accepted: { label: 'Принят',          icon: CheckCircle,    class: 'badge-green' },
  rejected: { label: 'Отклонён',        icon: XCircle,        class: 'badge-red'   },
  reserve:  { label: 'Резерв',          icon: BookmarkCheck,  class: 'badge-orange'},
}

export default function MyApplications() {
  const { data, isLoading } = useQuery<Application[]>({
    queryKey: ['my-applications'],
    queryFn: async () => {
      const { data } = await api.get('/applications/my')
      return data
    },
  })

  return (
    <div className="max-w-3xl">
      <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white mb-6">Мои отклики</h1>

      {isLoading ? (
        <div className="space-y-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="card h-20 animate-pulse bg-slate-100 dark:bg-slate-800" />
          ))}
        </div>
      ) : !data?.length ? (
        <div className="card p-10 text-center text-slate-400">
          <Clock size={40} className="mx-auto mb-3 opacity-30" />
          <p className="font-display font-semibold text-lg text-slate-600 dark:text-slate-400">Откликов пока нет</p>
          <p className="text-sm mt-1">Найдите интересные вакансии и откликнитесь</p>
          <Link to="/opportunities" className="btn-primary mt-4 inline-flex">Найти вакансии</Link>
        </div>
      ) : (
        <div className="space-y-3">
          {data.map((app) => {
            const cfg = STATUS_CONFIG[app.status]
            return (
              <div key={app.id} className="card p-4 flex items-center justify-between gap-4">
                <div className="min-w-0">
                  <Link
                    to={`/opportunities/${app.opportunity_id}`}
                    className="font-semibold text-slate-900 dark:text-white hover:text-brand-600 dark:hover:text-brand-400 text-sm"
                  >
                    Вакансия →
                  </Link>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {new Date(app.created_at || '').toLocaleDateString('ru-RU')}
                  </p>
                  {app.cover_letter && (
                    <p className="text-xs text-slate-500 mt-1 line-clamp-1">{app.cover_letter}</p>
                  )}
                </div>
                <span className={clsx('badge shrink-0', cfg.class)}>
                  {cfg.label}
                </span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
