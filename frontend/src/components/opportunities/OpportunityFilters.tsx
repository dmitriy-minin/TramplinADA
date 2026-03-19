import { useState } from 'react'
import { Search, SlidersHorizontal, X } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import type { OpportunityFilters, Tag } from '@/types'
import api from '@/lib/api'

interface FiltersProps {
  filters: OpportunityFilters
  onChange: (f: Partial<OpportunityFilters>) => void
  onReset: () => void
}

const TYPES = [
  { value: 'vacancy', label: 'Вакансия' },
  { value: 'internship', label: 'Стажировка' },
  { value: 'mentorship', label: 'Менторство' },
  { value: 'event', label: 'Мероприятие' },
]

const FORMATS = [
  { value: 'office', label: 'Офис' },
  { value: 'remote', label: 'Удалёнка' },
  { value: 'hybrid', label: 'Гибрид' },
]

const LEVELS = [
  { value: 'junior', label: 'Junior' },
  { value: 'middle', label: 'Middle' },
  { value: 'senior', label: 'Senior' },
]

export default function OpportunityFilters({ filters, onChange, onReset }: FiltersProps) {
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedTags, setSelectedTags] = useState<string[]>(
    filters.tag_ids ? filters.tag_ids.split(',') : []
  )

  const { data: tags } = useQuery<Tag[]>({
    queryKey: ['tags'],
    queryFn: async () => {
      const { data } = await api.get('/tags')
      return data
    },
  })

  const handleTagToggle = (tagId: string) => {
    const next = selectedTags.includes(tagId)
      ? selectedTags.filter((t) => t !== tagId)
      : [...selectedTags, tagId]
    setSelectedTags(next)
    onChange({ tag_ids: next.length ? next.join(',') : undefined })
  }

  const hasActiveFilters = filters.search || filters.type || filters.format || filters.level ||
    filters.salary_from || filters.salary_to || selectedTags.length > 0

  return (
    <div className="card p-4 space-y-4">
      {/* Search */}
      <div className="relative">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          type="text"
          placeholder="Поиск по вакансиям, компаниям..."
          value={filters.search || ''}
          onChange={(e) => onChange({ search: e.target.value || undefined })}
          className="input pl-9 pr-4"
        />
      </div>

      {/* Quick filters */}
      <div className="flex flex-wrap gap-2">
        {TYPES.map((t) => (
          <button
            key={t.value}
            onClick={() => onChange({ type: filters.type === t.value ? undefined : t.value as never })}
            className={`text-xs px-3 py-1.5 rounded-lg border font-medium transition-colors ${
              filters.type === t.value
                ? 'bg-brand-600 border-brand-600 text-white'
                : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:border-brand-400'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Toggle advanced */}
      <button
        onClick={() => setShowAdvanced(!showAdvanced)}
        className="flex items-center gap-2 text-sm text-brand-600 dark:text-brand-400 font-medium hover:underline"
      >
        <SlidersHorizontal size={14} />
        {showAdvanced ? 'Скрыть фильтры' : 'Расширенные фильтры'}
      </button>

      {showAdvanced && (
        <div className="space-y-4 pt-2 border-t border-slate-100 dark:border-slate-800">
          {/* Format */}
          <div>
            <p className="label">Формат</p>
            <div className="flex flex-wrap gap-2">
              {FORMATS.map((f) => (
                <button
                  key={f.value}
                  onClick={() => onChange({ format: filters.format === f.value ? undefined : f.value as never })}
                  className={`text-xs px-3 py-1.5 rounded-lg border font-medium transition-colors ${
                    filters.format === f.value
                      ? 'bg-brand-600 border-brand-600 text-white'
                      : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:border-brand-400'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {/* Level */}
          <div>
            <p className="label">Уровень</p>
            <div className="flex flex-wrap gap-2">
              {LEVELS.map((l) => (
                <button
                  key={l.value}
                  onClick={() => onChange({ level: filters.level === l.value ? undefined : l.value as never })}
                  className={`text-xs px-3 py-1.5 rounded-lg border font-medium transition-colors ${
                    filters.level === l.value
                      ? 'bg-brand-600 border-brand-600 text-white'
                      : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:border-brand-400'
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          </div>

          {/* Salary */}
          <div>
            <p className="label">Зарплата (KZT)</p>
            <div className="flex gap-2">
              <input
                type="number"
                placeholder="От"
                value={filters.salary_from || ''}
                onChange={(e) => onChange({ salary_from: e.target.value ? Number(e.target.value) : undefined })}
                className="input text-sm"
              />
              <input
                type="number"
                placeholder="До"
                value={filters.salary_to || ''}
                onChange={(e) => onChange({ salary_to: e.target.value ? Number(e.target.value) : undefined })}
                className="input text-sm"
              />
            </div>
          </div>

          {/* Tags */}
          {tags && tags.length > 0 && (
            <div>
              <p className="label">Технологии</p>
              <div className="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
                {tags
                  .filter((t) => t.category === 'tech')
                  .map((tag) => (
                    <button
                      key={tag.id}
                      onClick={() => handleTagToggle(tag.id)}
                      className={`text-xs px-2.5 py-1 rounded-md font-mono transition-colors ${
                        selectedTags.includes(tag.id)
                          ? 'bg-brand-600 text-white'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-brand-50 dark:hover:bg-brand-950'
                      }`}
                    >
                      {tag.name}
                    </button>
                  ))}
              </div>
            </div>
          )}

          {/* City */}
          <div>
            <p className="label">Город</p>
            <input
              type="text"
              placeholder="Алматы, Астана..."
              value={filters.city || ''}
              onChange={(e) => onChange({ city: e.target.value || undefined })}
              className="input text-sm"
            />
          </div>
        </div>
      )}

      {/* Reset */}
      {hasActiveFilters && (
        <button
          onClick={() => {
            setSelectedTags([])
            onReset()
          }}
          className="flex items-center gap-1.5 text-xs text-red-500 hover:text-red-600 font-medium"
        >
          <X size={12} /> Сбросить фильтры
        </button>
      )}
    </div>
  )
}
