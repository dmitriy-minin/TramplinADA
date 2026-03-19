import { Link } from 'react-router-dom'
import { MapPin, Briefcase, Clock, Heart, Users, Eye } from 'lucide-react'
import type { Opportunity } from '@/types'
import { clsx } from 'clsx'

const TYPE_LABELS: Record<string, string> = {
  vacancy: 'Вакансия',
  internship: 'Стажировка',
  mentorship: 'Менторство',
  event: 'Мероприятие',
}

const FORMAT_LABELS: Record<string, string> = {
  office: 'Офис',
  remote: 'Удалёнка',
  hybrid: 'Гибрид',
}

const LEVEL_LABELS: Record<string, string> = {
  junior: 'Junior',
  middle: 'Middle',
  senior: 'Senior',
  any: 'Любой',
}

const TYPE_COLORS: Record<string, string> = {
  vacancy: 'badge-blue',
  internship: 'badge-green',
  mentorship: 'badge-orange',
  event: 'badge-slate',
}

interface OpportunityCardProps {
  opportunity: Opportunity
  onFavoriteToggle?: (id: string, isFav: boolean) => void
}

function formatSalary(from?: number, to?: number, currency?: string): string {
  if (!from && !to) return 'Зарплата не указана'
  const fmt = (n: number) => n.toLocaleString('ru-RU')
  if (from && to) return `${fmt(from)} – ${fmt(to)} ${currency}`
  if (from) return `от ${fmt(from)} ${currency}`
  return `до ${fmt(to!)} ${currency}`
}

export default function OpportunityCard({ opportunity, onFavoriteToggle }: OpportunityCardProps) {
  return (
    <article className="card hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 group overflow-hidden">
      {/* Top strip accent */}
      <div className={clsx('h-1', {
        'bg-brand-500': opportunity.type === 'vacancy',
        'bg-emerald-500': opportunity.type === 'internship',
        'bg-orange-500': opportunity.type === 'mentorship',
        'bg-slate-400': opportunity.type === 'event',
      })} />

      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1.5 flex-wrap">
              <span className={TYPE_COLORS[opportunity.type]}>{TYPE_LABELS[opportunity.type]}</span>
              <span className="badge-slate">{FORMAT_LABELS[opportunity.format]}</span>
              {opportunity.level !== 'any' && (
                <span className="badge-slate">{LEVEL_LABELS[opportunity.level]}</span>
              )}
            </div>
            <Link
              to={`/opportunities/${opportunity.id}`}
              className="font-display font-semibold text-slate-900 dark:text-white text-base leading-snug hover:text-brand-600 dark:hover:text-brand-400 transition-colors line-clamp-2"
            >
              {opportunity.title}
            </Link>
          </div>
          {onFavoriteToggle && (
            <button
              onClick={() => onFavoriteToggle(opportunity.id, !!opportunity.is_favorited)}
              className={clsx(
                'p-1.5 rounded-lg transition-colors shrink-0',
                opportunity.is_favorited
                  ? 'text-red-500 bg-red-50 dark:bg-red-950'
                  : 'text-slate-400 hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/50'
              )}
            >
              <Heart size={16} fill={opportunity.is_favorited ? 'currentColor' : 'none'} />
            </button>
          )}
        </div>

        {/* Company */}
        <div className="flex items-center gap-2 mb-3">
          {opportunity.company.logo_url ? (
            <img src={opportunity.company.logo_url} alt="" className="w-7 h-7 rounded-lg object-cover" />
          ) : (
            <div className="w-7 h-7 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
              <Briefcase size={14} className="text-slate-400" />
            </div>
          )}
          <div className="min-w-0">
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300 truncate block">
              {opportunity.company.name}
            </span>
            {opportunity.company.is_verified && (
              <span className="text-xs text-brand-600 dark:text-brand-400">✓ Верифицировано</span>
            )}
          </div>
        </div>

        {/* Salary */}
        <p className="text-sm font-semibold text-slate-900 dark:text-white mb-3">
          {formatSalary(opportunity.salary_from, opportunity.salary_to, opportunity.salary_currency)}
        </p>

        {/* Tags */}
        {opportunity.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-3">
            {opportunity.tags.slice(0, 4).map((tag) => (
              <span key={tag.id} className="text-xs px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-mono">
                {tag.name}
              </span>
            ))}
            {opportunity.tags.length > 4 && (
              <span className="text-xs px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-500">
                +{opportunity.tags.length - 4}
              </span>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-3">
            {opportunity.city && (
              <span className="flex items-center gap-1">
                <MapPin size={12} /> {opportunity.city}
              </span>
            )}
            <span className="flex items-center gap-1">
              <Eye size={12} /> {opportunity.views_count}
            </span>
            {opportunity.applications_count !== undefined && (
              <span className="flex items-center gap-1">
                <Users size={12} /> {opportunity.applications_count}
              </span>
            )}
          </div>
          <span className="flex items-center gap-1">
            <Clock size={12} />
            {new Date(opportunity.created_at).toLocaleDateString('ru-RU')}
          </span>
        </div>
      </div>
    </article>
  )
}
