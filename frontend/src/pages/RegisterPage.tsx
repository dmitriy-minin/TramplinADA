import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Eye, EyeOff, Zap, ArrowRight, GraduationCap, Building2 } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '@/lib/api'
import { useAuthStore } from '@/store/auth'
import { clsx } from 'clsx'

const baseSchema = z.object({
  email: z.string().email('Введите корректный email'),
  password: z.string()
    .min(8, 'Минимум 8 символов')
    .regex(/[A-Z]/, 'Нужна хотя бы одна заглавная буква')
    .regex(/[0-9]/, 'Нужна хотя бы одна цифра'),
  full_name: z.string().min(2, 'Минимум 2 символа'),
})

const soiskatelSchema = baseSchema.extend({
  role: z.literal('soiskatel'),
  university: z.string().optional(),
  study_year: z.preprocess(
    (v) => (v === '' || v === null || v === undefined || Number.isNaN(v) ? undefined : Number(v)),
    z.number().int().min(1).max(6).optional()
  ),
  company_name: z.string().optional(),
  inn: z.string().optional(),
})

const employerSchema = baseSchema.extend({
  role: z.literal('employer'),
  company_name: z.string().min(1, 'Укажите название компании'),
  inn: z.string().optional(),
  university: z.string().optional(),
  study_year: z.number().optional(),
})

type SoiskatelData = z.infer<typeof soiskatelSchema>
type EmployerData = z.infer<typeof employerSchema>
type FormData = SoiskatelData | EmployerData

export default function RegisterPage() {
  const navigate = useNavigate()
  const { login } = useAuthStore()
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [role, setRole] = useState<'soiskatel' | 'employer'>('soiskatel')

  const currentSchema = role === 'soiskatel' ? soiskatelSchema : employerSchema

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(currentSchema),
    defaultValues: { role: 'soiskatel' },
  })

  const handleRoleChange = (r: 'soiskatel' | 'employer') => {
    setRole(r)
    reset({ role: r } as FormData)
  }

  const onSubmit = async (data: FormData) => {
    setLoading(true)
    try {
      await api.post('/auth/register', data)
      const res = await api.post('/auth/login', { email: data.email, password: data.password })
      await login(res.data.access_token, res.data.refresh_token)
      toast.success('Аккаунт создан!')
      navigate('/dashboard')
    } catch (err: unknown) {
      const message = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Ошибка регистрации'
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  const e = errors as Record<string, { message?: string }>

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950 px-4 py-12">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-brand-300/10 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-1/4 w-80 h-80 bg-purple-300/10 rounded-full blur-3xl" />
      </div>

      <div className="w-full max-w-md animate-slide-up">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2">
            <div className="w-10 h-10 bg-brand-600 rounded-xl flex items-center justify-center shadow-lg shadow-brand-500/30">
              <Zap size={20} className="text-white" />
            </div>
            <span className="font-display font-bold text-xl text-slate-900 dark:text-white">Трамплин</span>
          </Link>
        </div>

        <div className="card p-8">
          <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white mb-1">
            Создать аккаунт
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mb-6">
            Уже есть аккаунт?{' '}
            <Link to="/login" className="text-brand-600 dark:text-brand-400 font-semibold hover:underline">Войти</Link>
          </p>

          <div className="grid grid-cols-2 gap-3 mb-6">
            {[
              { value: 'soiskatel', label: 'Студент / Выпускник', icon: GraduationCap },
              { value: 'employer', label: 'Работодатель', icon: Building2 },
            ].map(({ value, label, icon: Icon }) => (
              <button
                key={value}
                type="button"
                onClick={() => handleRoleChange(value as 'soiskatel' | 'employer')}
                className={clsx(
                  'flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all text-sm font-semibold',
                  role === value
                    ? 'border-brand-500 bg-brand-50 dark:bg-brand-950 text-brand-700 dark:text-brand-300'
                    : 'border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:border-brand-300'
                )}
              >
                <Icon size={22} />
                {label}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <input type="hidden" value={role} {...register('role')} />

            <div>
              <label className="label">Полное имя</label>
              <input type="text" placeholder="Иван Иванов" {...register('full_name')} className="input" />
              {e.full_name && <p className="text-xs text-red-500 mt-1">{e.full_name.message}</p>}
            </div>

            <div>
              <label className="label">Email</label>
              <input type="email" placeholder="you@example.com" {...register('email')} className="input" />
              {e.email && <p className="text-xs text-red-500 mt-1">{e.email.message}</p>}
            </div>

            <div>
              <label className="label">Пароль</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Минимум 8 символов, заглавная, цифра"
                  {...register('password')}
                  className="input pr-10"
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              {e.password && <p className="text-xs text-red-500 mt-1">{e.password.message}</p>}
            </div>

            {role === 'soiskatel' && (
              <>
                <div>
                  <label className="label">Университет (необязательно)</label>
                  <input type="text" placeholder="НАУ, КТУ, КБТУ..." {...register('university')} className="input" />
                </div>
                <div>
                  <label className="label">Курс (необязательно)</label>
                  <input type="number" placeholder="1–6" min={1} max={6} {...register('study_year')} className="input" />
                  {e.study_year && <p className="text-xs text-red-500 mt-1">{e.study_year.message}</p>}
                </div>
              </>
            )}

            {role === 'employer' && (
              <>
                <div>
                  <label className="label">Название компании *</label>
                  <input type="text" placeholder="ООО «Технологии»" {...register('company_name')} className="input" />
                  {e.company_name && <p className="text-xs text-red-500 mt-1">{e.company_name.message}</p>}
                </div>
                <div>
                  <label className="label">БИН / ИНН (необязательно)</label>
                  <input type="text" placeholder="123456789012" {...register('inn')} className="input" />
                </div>
              </>
            )}

            <button type="submit" disabled={loading} className="btn-primary w-full justify-center py-3 mt-2">
              {loading
                ? <div className="w-5 h-5 border-2 border-white/40 border-t-white rounded-full animate-spin" />
                : <>Зарегистрироваться <ArrowRight size={16} /></>
              }
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
