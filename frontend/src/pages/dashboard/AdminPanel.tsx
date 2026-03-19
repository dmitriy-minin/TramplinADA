import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import toast from 'react-hot-toast'
import { CheckCircle, XCircle, Building2, Users, Tag as TagIcon, Plus } from 'lucide-react'
import api from '@/lib/api'
import type { Opportunity, Tag } from '@/types'
import { clsx } from 'clsx'

type AdminTab = 'moderation' | 'companies' | 'users' | 'tags'

export default function AdminPanel() {
  const [tab, setTab] = useState<AdminTab>('moderation')
  const [newTag, setNewTag] = useState('')
  const qc = useQueryClient()

  // Pending opportunities
  const { data: pendingOpps } = useQuery({
    queryKey: ['admin', 'pending'],
    queryFn: async () => {
      const { data } = await api.get('/opportunities', { params: { status: 'pending', per_page: 50 } })
      return data.items as Opportunity[]
    },
    enabled: tab === 'moderation',
  })

  // Companies
  const { data: companies } = useQuery({
    queryKey: ['admin', 'companies'],
    queryFn: async () => { const { data } = await api.get('/companies'); return data },
    enabled: tab === 'companies',
  })

  // Users
  const { data: users } = useQuery({
    queryKey: ['admin', 'users'],
    queryFn: async () => { const { data } = await api.get('/users'); return data },
    enabled: tab === 'users',
  })

  // Tags
  const { data: tags } = useQuery<Tag[]>({
    queryKey: ['tags'],
    queryFn: async () => { const { data } = await api.get('/tags'); return data },
    enabled: tab === 'tags',
  })

  const moderateMutation = useMutation({
    mutationFn: ({ id, status, reason }: { id: string; status: string; reason?: string }) =>
      api.post(`/opportunities/${id}/moderate`, { status, rejection_reason: reason }),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['admin'] }); toast.success('Статус обновлён') },
  })

  const verifyCompanyMutation = useMutation({
    mutationFn: (id: string) => api.patch(`/companies/${id}/verify`),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['admin', 'companies'] }); toast.success('Компания верифицирована') },
  })

  const createTagMutation = useMutation({
    mutationFn: (name: string) => api.post('/tags', { name, category: 'tech' }),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['tags'] }); setNewTag(''); toast.success('Тег создан') },
  })

  const deleteTagMutation = useMutation({
    mutationFn: (id: string) => api.delete(`/tags/${id}`),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['tags'] }); toast.success('Удалено') },
  })

  const TABS = [
    { id: 'moderation', label: 'Модерация', icon: CheckCircle },
    { id: 'companies', label: 'Компании', icon: Building2 },
    { id: 'users', label: 'Пользователи', icon: Users },
    { id: 'tags', label: 'Теги', icon: TagIcon },
  ] as const

  return (
    <div className="max-w-5xl">
      <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white mb-6">Администрирование</h1>

      {/* Tabs */}
      <div className="flex gap-1 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-1 mb-6 w-fit">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={clsx(
              'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              tab === t.id
                ? 'bg-brand-600 text-white'
                : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200'
            )}
          >
            <t.icon size={15} /> {t.label}
          </button>
        ))}
      </div>

      {/* Moderation */}
      {tab === 'moderation' && (
        <div className="space-y-3">
          {!pendingOpps?.length ? (
            <div className="card p-8 text-center text-slate-400">
              <CheckCircle size={32} className="mx-auto mb-2 opacity-30" />
              <p>Нет вакансий на модерации</p>
            </div>
          ) : (
            pendingOpps.map((opp) => (
              <div key={opp.id} className="card p-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <p className="font-semibold text-slate-900 dark:text-white">{opp.title}</p>
                    <p className="text-sm text-slate-500">{opp.company?.name} · {opp.city}</p>
                    <p className="text-xs text-slate-400 mt-1 line-clamp-2">{opp.description}</p>
                  </div>
                  <div className="flex gap-2 shrink-0">
                    <button
                      onClick={() => moderateMutation.mutate({ id: opp.id, status: 'active' })}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 text-xs font-semibold hover:bg-emerald-100 transition-colors"
                    >
                      <CheckCircle size={14} /> Одобрить
                    </button>
                    <button
                      onClick={() => {
                        const reason = prompt('Причина отклонения (необязательно):') || undefined
                        moderateMutation.mutate({ id: opp.id, status: 'rejected', reason })
                      }}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-300 text-xs font-semibold hover:bg-red-100 transition-colors"
                    >
                      <XCircle size={14} /> Отклонить
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Companies */}
      {tab === 'companies' && (
        <div className="space-y-2">
          {companies?.map((c: { id: string; name: string; inn?: string; is_verified: boolean }) => (
            <div key={c.id} className="card p-4 flex items-center justify-between gap-4">
              <div>
                <p className="font-semibold text-slate-900 dark:text-white">{c.name}</p>
                {c.inn && <p className="text-xs text-slate-400">БИН: {c.inn}</p>}
              </div>
              {c.is_verified ? (
                <span className="badge-green">Верифицирована</span>
              ) : (
                <button
                  onClick={() => verifyCompanyMutation.mutate(c.id)}
                  className="btn-primary text-xs px-3 py-1.5"
                >
                  Верифицировать
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Users */}
      {tab === 'users' && (
        <div className="space-y-2">
          {users?.map((u: { id: string; email: string; full_name: string; role: string; is_active: boolean }) => (
            <div key={u.id} className="card p-4 flex items-center justify-between gap-4">
              <div>
                <p className="font-semibold text-slate-900 dark:text-white text-sm">{u.full_name}</p>
                <p className="text-xs text-slate-400">{u.email} · {u.role}</p>
              </div>
              <span className={clsx('badge', u.is_active ? 'badge-green' : 'badge-red')}>
                {u.is_active ? 'Активен' : 'Деактивирован'}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Tags */}
      {tab === 'tags' && (
        <div>
          <div className="flex gap-3 mb-4">
            <input
              type="text"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              placeholder="Название тега (React, Python...)"
              className="input flex-1"
              onKeyDown={(e) => e.key === 'Enter' && newTag.trim() && createTagMutation.mutate(newTag.trim())}
            />
            <button
              onClick={() => newTag.trim() && createTagMutation.mutate(newTag.trim())}
              className="btn-primary"
            >
              <Plus size={16} /> Добавить
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {tags?.map((tag) => (
              <span key={tag.id} className="flex items-center gap-1.5 px-3 py-1.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg text-sm font-mono">
                {tag.name}
                <button
                  onClick={() => deleteTagMutation.mutate(tag.id)}
                  className="text-slate-400 hover:text-red-500 transition-colors"
                >
                  <XCircle size={13} />
                </button>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
