import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { Send } from 'lucide-react'
import api from '@/lib/api'
import type { Tag } from '@/types'

const schema = z.object({
  title: z.string().min(3, 'Минимум 3 символа'),
  description: z.string().min(20, 'Минимум 20 символов'),
  type: z.enum(['vacancy', 'internship', 'mentorship', 'event']),
  format: z.enum(['office', 'remote', 'hybrid']),
  level: z.enum(['junior', 'middle', 'senior', 'any']).default('any'),
  salary_from: z.number().optional(),
  salary_to: z.number().optional(),
  salary_currency: z.string().default('KZT'),
  address: z.string().optional(),
  city: z.string().optional(),
  tag_ids: z.array(z.string()).default([]),
})

type FormData = z.infer<typeof schema>

export default function CreateOpportunity() {
  const navigate = useNavigate()
  const qc = useQueryClient()

  const { data: tags } = useQuery<Tag[]>({
    queryKey: ['tags'],
    queryFn: async () => { const { data } = await api.get('/tags'); return data },
  })

  const { register, handleSubmit, control, watch, setValue, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { type: 'vacancy', format: 'office', level: 'any', salary_currency: 'KZT', tag_ids: [] },
  })

  const selectedTags = watch('tag_ids')

  const mutation = useMutation({
    mutationFn: (data: FormData) => api.post('/opportunities', data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['my-opportunities'] })
      toast.success('Вакансия создана и отправлена на модерацию')
      navigate('/dashboard/opportunities')
    },
    onError: (err: unknown) => {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Ошибка'
      toast.error(msg)
    },
  })

  const toggleTag = (id: string) => {
    const next = selectedTags.includes(id)
      ? selectedTags.filter((t) => t !== id)
      : [...selectedTags, id]
    setValue('tag_ids', next)
  }

  return (
    <div className="max-w-2xl">
      <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white mb-6">Создать вакансию</h1>

      <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className="space-y-6">
        <div className="card p-6 space-y-4">
          <h2 className="font-display font-semibold text-slate-900 dark:text-white">Основное</h2>

          <div>
            <label className="label">Название *</label>
            <input type="text" {...register('title')} placeholder="Frontend Developer" className="input" />
            {errors.title && <p className="text-xs text-red-500 mt-1">{errors.title.message}</p>}
          </div>

          <div>
            <label className="label">Описание *</label>
            <textarea rows={6} {...register('description')} placeholder="Опишите задачи, требования, условия..." className="input resize-none" />
            {errors.description && <p className="text-xs text-red-500 mt-1">{errors.description.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Тип *</label>
              <select {...register('type')} className="input">
                <option value="vacancy">Вакансия</option>
                <option value="internship">Стажировка</option>
                <option value="mentorship">Менторство</option>
                <option value="event">Мероприятие</option>
              </select>
            </div>
            <div>
              <label className="label">Формат *</label>
              <select {...register('format')} className="input">
                <option value="office">Офис</option>
                <option value="remote">Удалёнка</option>
                <option value="hybrid">Гибрид</option>
              </select>
            </div>
          </div>

          <div>
            <label className="label">Уровень</label>
            <select {...register('level')} className="input">
              <option value="any">Любой</option>
              <option value="junior">Junior</option>
              <option value="middle">Middle</option>
              <option value="senior">Senior</option>
            </select>
          </div>
        </div>

        <div className="card p-6 space-y-4">
          <h2 className="font-display font-semibold text-slate-900 dark:text-white">Зарплата</h2>
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="label">От</label>
              <input type="number" {...register('salary_from', { valueAsNumber: true })} placeholder="300000" className="input" />
            </div>
            <div>
              <label className="label">До</label>
              <input type="number" {...register('salary_to', { valueAsNumber: true })} placeholder="600000" className="input" />
            </div>
            <div>
              <label className="label">Валюта</label>
              <select {...register('salary_currency')} className="input">
                <option value="KZT">KZT</option>
                <option value="USD">USD</option>
                <option value="RUB">RUB</option>
              </select>
            </div>
          </div>
        </div>

        <div className="card p-6 space-y-4">
          <h2 className="font-display font-semibold text-slate-900 dark:text-white">Местоположение</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Город</label>
              <input type="text" {...register('city')} placeholder="Алматы" className="input" />
            </div>
            <div>
              <label className="label">Адрес</label>
              <input type="text" {...register('address')} placeholder="ул. Абая 123" className="input" />
            </div>
          </div>
        </div>

        {tags && tags.length > 0 && (
          <div className="card p-6">
            <h2 className="font-display font-semibold text-slate-900 dark:text-white mb-4">Технологии</h2>
            <div className="flex flex-wrap gap-2">
              {tags.filter((t) => t.category === 'tech').map((tag) => (
                <button
                  key={tag.id}
                  type="button"
                  onClick={() => toggleTag(tag.id)}
                  className={`text-xs px-3 py-1.5 rounded-lg font-mono transition-colors ${
                    selectedTags.includes(tag.id)
                      ? 'bg-brand-600 text-white'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-brand-50'
                  }`}
                >
                  {tag.name}
                </button>
              ))}
            </div>
          </div>
        )}

        <button type="submit" disabled={mutation.isPending} className="btn-primary">
          {mutation.isPending ? (
            <div className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
          ) : (
            <><Send size={16} /> Отправить на модерацию</>
          )}
        </button>
      </form>
    </div>
  )
}
