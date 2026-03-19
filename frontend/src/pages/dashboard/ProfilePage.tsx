import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { useAuthStore } from '@/store/auth'
import api from '@/lib/api'
import { Save } from 'lucide-react'

interface ProfileFormData {
  full_name: string
  bio: string
  university: string
  study_year: number | undefined
  github_url: string
  portfolio_url: string
  resume_markdown: string
  resume_privacy: string
}

export default function ProfilePage() {
  const { user, refreshUser } = useAuthStore()

  const { register, handleSubmit, formState: { isDirty } } = useForm<ProfileFormData>({
    defaultValues: {
      full_name: user?.full_name || '',
      bio: user?.bio || '',
      university: user?.university || '',
      study_year: user?.study_year,
      github_url: user?.github_url || '',
      portfolio_url: user?.portfolio_url || '',
      resume_markdown: user?.resume_markdown || '',
      resume_privacy: user?.resume_privacy || 'public',
    },
  })

  const mutation = useMutation({
    mutationFn: async (data: ProfileFormData) => {
      await api.patch('/auth/me', data)
    },
    onSuccess: async () => {
      await refreshUser()
      toast.success('Профиль обновлён')
    },
    onError: () => toast.error('Ошибка при сохранении'),
  })

  return (
    <div className="max-w-2xl">
      <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white mb-6">Профиль</h1>

      <form onSubmit={handleSubmit((d) => mutation.mutate(d))} className="space-y-6">
        <div className="card p-6 space-y-4">
          <h2 className="font-display font-semibold text-slate-900 dark:text-white">Основная информация</h2>

          <div>
            <label className="label">Полное имя</label>
            <input type="text" {...register('full_name')} className="input" />
          </div>

          <div>
            <label className="label">О себе</label>
            <textarea rows={3} {...register('bio')} placeholder="Расскажите о себе..." className="input resize-none" />
          </div>

          {user?.role === 'soiskatel' && (
            <>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Университет</label>
                  <input type="text" {...register('university')} placeholder="КБТУ, НАУ..." className="input" />
                </div>
                <div>
                  <label className="label">Курс</label>
                  <input type="number" min={1} max={6} {...register('study_year', { valueAsNumber: true })} className="input" />
                </div>
              </div>

              <div>
                <label className="label">GitHub</label>
                <input type="url" {...register('github_url')} placeholder="https://github.com/username" className="input" />
              </div>

              <div>
                <label className="label">Портфолио</label>
                <input type="url" {...register('portfolio_url')} placeholder="https://your-portfolio.com" className="input" />
              </div>

              <div>
                <label className="label">Приватность резюме</label>
                <select {...register('resume_privacy')} className="input">
                  <option value="public">Видно всем</option>
                  <option value="contacts_only">Только контактам</option>
                  <option value="hidden">Скрыто</option>
                </select>
              </div>
            </>
          )}
        </div>

        {user?.role === 'soiskatel' && (
          <div className="card p-6">
            <h2 className="font-display font-semibold text-slate-900 dark:text-white mb-4">Резюме (Markdown)</h2>
            <textarea
              rows={12}
              {...register('resume_markdown')}
              placeholder="## Опыт&#10;&#10;### Компания ABC&#10;Разработчик, 2023–2024&#10;..."
              className="input resize-none font-mono text-sm"
            />
            <p className="text-xs text-slate-400 mt-2">Поддерживается Markdown-разметка</p>
          </div>
        )}

        <button
          type="submit"
          disabled={!isDirty || mutation.isPending}
          className="btn-primary"
        >
          {mutation.isPending ? (
            <div className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />
          ) : (
            <><Save size={16} /> Сохранить изменения</>
          )}
        </button>
      </form>
    </div>
  )
}
