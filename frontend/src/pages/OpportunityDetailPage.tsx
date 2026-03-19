import { useParams, Link } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import { ArrowLeft, MapPin, Briefcase, Clock, Users, Eye, Heart, ExternalLink, Send } from 'lucide-react'
import { useState } from 'react'
import toast from 'react-hot-toast'
import Navbar from '@/components/common/Navbar'
import type { Opportunity } from '@/types'
import api from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { clsx } from 'clsx'

const TYPE_LABELS: Record<string, string> = {
  vacancy: 'Вакансия', internship: 'Стажировка', mentorship: 'Менторство', event: 'Мероприятие',
}
const FORMAT_LABELS: Record<string, string> = {
  office: '🏢 Офис', remote: '🏠 Удалёнка', hybrid: '🔄 Гибрид',
}
const LEVEL_LABELS: Record<string, string> = {
  junior: 'Junior', middle: 'Middle', senior: 'Senior', any: 'Любой уровень',
}

function formatSalary(from?: number, to?: number, currency?: string): string {
  if (!from && !to) return 'Зарплата не указана'
  const fmt = (n: number) => n.toLocaleString('ru-RU')
  if (from && to) return `${fmt(from)} – ${fmt(to)} ${currency}`
  if (from) return `от ${fmt(from)} ${currency}`
  return `до ${fmt(to!)} ${currency}`
}

export default function OpportunityDetailPage() {
  const { id } = useParams<{ id: string }>()
  const user = useAuthStore((s) => s.user)
  const [showApplyForm, setShowApplyForm] = useState(false)
  const [coverLetter, setCoverLetter] = useState('')

  const { data: opp, isLoading } = useQuery<Opportunity>({
    queryKey: ['opportunity', id],
    queryFn: async () => {
      const { data } = await api.get(`/opportunities/${id}`)
      return data
    },
  })

  const applyMutation = useMutation({
    mutationFn: async () => {
      await api.post('/applications', {
        opportunity_id: id,
        cover_letter: coverLetter || undefined,
      })
    },
    onSuccess: () => {
      toast.success('Отклик отправлен!')
      setShowApplyForm(false)
    },
    onError: (err: unknown) => {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Ошибка'
      toast.error(msg)
    },
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
        <Navbar />
        <div className="pt-24 max-w-4xl mx-auto px-4">
          <div className="card h-96 animate-pulse bg-slate-100 dark:bg-slate-800" />
        </div>
      </div>
    )
  }

  if (!opp) return null

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <Navbar />
      <div className="pt-20 pb-16">
        <div className="max-w-4xl mx-auto px-4">
          {/* Back */}
          <Link to="/opportunities" className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-slate-900 dark:hover:text-white mb-6 group">
            <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" />
            Назад к вакансиям
          </Link>

          <div className="grid lg:grid-cols-3 gap-6">
            {/* Main */}
            <div className="lg:col-span-2 space-y-6">
              <div className="card p-6">
                {/* Header */}
                <div className="flex items-start gap-4 mb-4">
                  {opp.company.logo_url ? (
                    <img src={opp.company.logo_url} alt="" className="w-14 h-14 rounded-xl object-cover border border-slate-100 dark:border-slate-800" />
                  ) : (
                    <div className="w-14 h-14 rounded-xl bg-brand-50 dark:bg-brand-950 flex items-center justify-center">
                      <Briefcase size={24} className="text-brand-500" />
                    </div>
                  )}
                  <div className="flex-1 min-w-0">
                    <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white mb-1 leading-tight">
                      {opp.title}
                    </h1>
                    <p className="text-slate-600 dark:text-slate-400 font-medium">
                      {opp.company.name}
                      {opp.company.is_verified && <span className="ml-2 text-brand-500 text-sm">✓ Верифицировано</span>}
                    </p>
                  </div>
                </div>

                {/* Badges */}
                <div className="flex flex-wrap gap-2 mb-4">
                  <span className="badge-blue">{TYPE_LABELS[opp.type]}</span>
                  <span className="badge-slate">{FORMAT_LABELS[opp.format]}</span>
                  <span className="badge-slate">{LEVEL_LABELS[opp.level]}</span>
                </div>

                {/* Salary */}
                <p className="text-2xl font-display font-bold text-slate-900 dark:text-white mb-4">
                  {formatSalary(opp.salary_from, opp.salary_to, opp.salary_currency)}
                </p>

                {/* Meta */}
                <div className="flex flex-wrap gap-4 text-sm text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-800 pt-4">
                  {opp.city && <span className="flex items-center gap-1.5"><MapPin size={14} />{opp.city}</span>}
                  <span className="flex items-center gap-1.5"><Eye size={14} />{opp.views_count} просмотров</span>
                  <span className="flex items-center gap-1.5"><Users size={14} />{opp.applications_count || 0} откликов</span>
                  <span className="flex items-center gap-1.5"><Clock size={14} />{new Date(opp.created_at).toLocaleDateString('ru-RU')}</span>
                </div>
              </div>

              {/* Description */}
              <div className="card p-6">
                <h2 className="font-display font-bold text-lg text-slate-900 dark:text-white mb-4">Описание</h2>
                <div className="prose prose-slate dark:prose-invert max-w-none text-sm leading-relaxed whitespace-pre-wrap">
                  {opp.description}
                </div>
              </div>

              {/* Tags */}
              {opp.tags.length > 0 && (
                <div className="card p-6">
                  <h2 className="font-display font-bold text-lg text-slate-900 dark:text-white mb-4">Технологии</h2>
                  <div className="flex flex-wrap gap-2">
                    {opp.tags.map((tag) => (
                      <span key={tag.id} className="px-3 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-sm font-mono">
                        {tag.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Apply form */}
              {showApplyForm && (
                <div className="card p-6 border-2 border-brand-200 dark:border-brand-800">
                  <h2 className="font-display font-bold text-lg text-slate-900 dark:text-white mb-4">Отклик</h2>
                  <div className="mb-4">
                    <label className="label">Сопроводительное письмо (необязательно)</label>
                    <textarea
                      value={coverLetter}
                      onChange={(e) => setCoverLetter(e.target.value)}
                      rows={5}
                      placeholder="Расскажите почему вы подходите на эту позицию..."
                      className="input resize-none"
                    />
                  </div>
                  <div className="flex gap-3">
                    <button
                      onClick={() => applyMutation.mutate()}
                      disabled={applyMutation.isPending}
                      className="btn-primary"
                    >
                      {applyMutation.isPending ? (
                        <div className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
                      ) : (
                        <><Send size={16} /> Отправить</>
                      )}
                    </button>
                    <button onClick={() => setShowApplyForm(false)} className="btn-secondary">Отмена</button>
                  </div>
                </div>
              )}
            </div>

            {/* Sidebar */}
            <div className="space-y-4">
              {/* Apply button */}
              {user?.role === 'soiskatel' && !showApplyForm && (
                <button
                  onClick={() => setShowApplyForm(true)}
                  className="btn-primary w-full justify-center py-3 text-base"
                >
                  Откликнуться
                </button>
              )}
              {!user && (
                <Link to="/login" className="btn-primary w-full justify-center py-3 text-base">
                  Войдите для отклика
                </Link>
              )}

              {/* Company card */}
              <div className="card p-5">
                <h3 className="font-display font-semibold text-base text-slate-900 dark:text-white mb-3">Компания</h3>
                <p className="font-semibold text-slate-800 dark:text-slate-200 mb-1">{opp.company.name}</p>
                {opp.company.city && (
                  <p className="text-sm text-slate-500 flex items-center gap-1.5">
                    <MapPin size={13} /> {opp.company.city}
                  </p>
                )}
              </div>

              {/* Address */}
              {opp.address && (
                <div className="card p-5">
                  <h3 className="font-display font-semibold text-base text-slate-900 dark:text-white mb-2">Адрес</h3>
                  <p className="text-sm text-slate-500 flex items-start gap-1.5">
                    <MapPin size={13} className="mt-0.5 shrink-0" /> {opp.address}
                  </p>
                </div>
              )}

              {/* Expiry */}
              {opp.expires_at && (
                <div className="card p-5">
                  <p className="text-xs text-slate-400">Актуально до</p>
                  <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mt-0.5">
                    {new Date(opp.expires_at).toLocaleDateString('ru-RU')}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
