import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Plus, Eye, Users, Pencil, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '@/lib/api'
import type { Opportunity } from '@/types'
import { clsx } from 'clsx'

const STATUS_COLORS: Record<string, string> = {
  pending:  'badge-slate',
  active:   'badge-green',
  rejected: 'badge-red',
  closed:   'badge-orange',
}

const STATUS_LABELS: Record<string, string> = {
  pending:  'На модерации',
  active:   'Активна',
  rejected: 'Отклонена',
  closed:   'Закрыта',
}

export default function MyOpportunities() {
  const qc = useQueryClient()

  const { data, isLoading } = useQuery<{ items: Opportunity[] }>({
    queryKey: ['my-opportunities'],
    queryFn: async () => {
      const { data } = await api.get('/opportunities', { params: { per_page: 100 } })
      return data
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/opportunities/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['my-opportunities'] })
      toast.success('Удалено')
    },
    onError: () => toast.error('Ошибка при удалении'),
  })

  const handleDelete = (id: string) => {
    if (confirm('Удалить вакансию?')) deleteMutation.mutate(id)
  }

  const opportunities = data?.items || []

  return (
    <div className="max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white">Мои вакансии</h1>
        <Link to="/dashboard/opportunities/new" className="btn-primary text-sm">
          <Plus size={16} /> Создать
        </Link>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="card h-20 animate-pulse bg-slate-100 dark:bg-slate-800" />
          ))}
        </div>
      ) : opportunities.length === 0 ? (
        <div className="card p-10 text-center text-slate-400">
          <p className="font-display font-semibold text-lg mb-2">Нет вакансий</p>
          <Link to="/dashboard/opportunities/new" className="btn-primary mt-2 inline-flex">
            <Plus size={16} /> Создать первую вакансию
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {opportunities.map((opp) => (
            <div key={opp.id} className="card p-4">
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <span className={clsx('badge', STATUS_COLORS[opp.status])}>
                      {STATUS_LABELS[opp.status]}
                    </span>
                    {opp.rejection_reason && (
                      <span className="text-xs text-red-500">Причина: {opp.rejection_reason}</span>
                    )}
                  </div>
                  <Link
                    to={`/opportunities/${opp.id}`}
                    className="font-display font-semibold text-slate-900 dark:text-white hover:text-brand-600 dark:hover:text-brand-400"
                  >
                    {opp.title}
                  </Link>
                  <div className="flex items-center gap-4 text-xs text-slate-400 mt-1">
                    <span className="flex items-center gap-1"><Eye size={12} /> {opp.views_count}</span>
                    <span className="flex items-center gap-1"><Users size={12} /> {opp.applications_count || 0} откликов</span>
                    <span>{new Date(opp.created_at).toLocaleDateString('ru-RU')}</span>
                  </div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <button className="btn-ghost p-2 text-slate-400 hover:text-brand-600">
                    <Pencil size={15} />
                  </button>
                  <button
                    onClick={() => handleDelete(opp.id)}
                    className="btn-ghost p-2 text-slate-400 hover:text-red-500"
                  >
                    <Trash2 size={15} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
