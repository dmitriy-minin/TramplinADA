import { Link } from 'react-router-dom'
import { ArrowRight, Map, Filter, Users, Shield, Zap, Star, TrendingUp, Globe, Award } from 'lucide-react'
import Navbar from '@/components/common/Navbar'

const FEATURES = [
  {
    icon: Map,
    title: 'Интерактивная карта',
    desc: 'Все возможности на карте — видно расположение офисов, формат работы и ближайшие мероприятия.',
    color: 'text-brand-500 bg-brand-50 dark:bg-brand-950',
  },
  {
    icon: Filter,
    title: 'Умные фильтры',
    desc: 'Фильтруй по стеку технологий, уровню, зарплате и формату. Находи только то, что нужно тебе.',
    color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-950',
  },
  {
    icon: Users,
    title: 'Нетворкинг',
    desc: 'Связывайся с коллегами, делись рекомендациями, строй профессиональные связи ещё в вузе.',
    color: 'text-orange-500 bg-orange-50 dark:bg-orange-950',
  },
  {
    icon: Shield,
    title: 'Верифицированные компании',
    desc: 'Все работодатели проходят проверку кураторами. Только реальные вакансии и честные условия.',
    color: 'text-purple-500 bg-purple-50 dark:bg-purple-950',
  },
  {
    icon: TrendingUp,
    title: 'Карьерный трекинг',
    desc: 'Отслеживай статусы откликов, собирай портфолио и управляй своей карьерной историей.',
    color: 'text-sky-500 bg-sky-50 dark:bg-sky-950',
  },
  {
    icon: Globe,
    title: 'Три роли, один аккаунт',
    desc: 'Соискатель, работодатель или куратор — у каждого свой кабинет и инструменты.',
    color: 'text-rose-500 bg-rose-50 dark:bg-rose-950',
  },
]

const STATS = [
  { value: '500+', label: 'Вакансий и стажировок' },
  { value: '120+', label: 'Верифицированных компаний' },
  { value: '3 000+', label: 'Студентов и выпускников' },
  { value: '95%', label: 'Довольных работодателей' },
]

const OPPORTUNITY_TYPES = [
  { label: 'Вакансии', color: 'bg-brand-500', desc: 'Полноценная работа с зарплатой' },
  { label: 'Стажировки', color: 'bg-emerald-500', desc: 'Практика во время учёбы' },
  { label: 'Менторство', color: 'bg-orange-500', desc: 'Развитие с опытным наставником' },
  { label: 'Мероприятия', color: 'bg-purple-500', desc: 'Хакатоны, митапы, конференции' },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <Navbar transparent />

      {/* Hero */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-400/20 rounded-full blur-3xl animate-pulse-slow" />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-400/15 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-accent-400/10 rounded-full blur-2xl animate-pulse-slow" style={{ animationDelay: '2s' }} />
          {/* Grid pattern */}
          <div
            className="absolute inset-0 opacity-[0.03] dark:opacity-[0.05]"
            style={{
              backgroundImage: 'linear-gradient(#3373ff 1px, transparent 1px), linear-gradient(90deg, #3373ff 1px, transparent 1px)',
              backgroundSize: '60px 60px',
            }}
          />
        </div>

        <div className="max-w-5xl mx-auto px-4 text-center animate-fade-in">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-brand-50 dark:bg-brand-950/60 border border-brand-200 dark:border-brand-800 text-brand-700 dark:text-brand-300 text-sm font-semibold px-4 py-2 rounded-full mb-8">
            <Zap size={14} className="fill-current" />
            Платформа для IT-карьеры в Казахстане
          </div>

          {/* Headline */}
          <h1 className="font-display font-black text-5xl sm:text-6xl lg:text-7xl text-slate-900 dark:text-white leading-[1.05] mb-6">
            Твой старт в
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-500 via-brand-400 to-purple-500">
              IT-карьере
            </span>
            <br />
            начинается здесь
          </h1>

          <p className="text-lg sm:text-xl text-slate-500 dark:text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Трамплин объединяет студентов IT-вузов с работодателями. Вакансии, стажировки, менторство и карьерные мероприятия — всё на одной платформе с интерактивной картой.
          </p>

          {/* CTA */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/register" className="btn-primary text-base px-8 py-3.5 shadow-xl shadow-brand-500/25">
              Начать бесплатно
              <ArrowRight size={18} />
            </Link>
            <Link to="/opportunities" className="btn-secondary text-base px-8 py-3.5">
              Смотреть вакансии
            </Link>
          </div>

          {/* Opportunity type pills */}
          <div className="flex flex-wrap items-center justify-center gap-3 mt-12">
            {OPPORTUNITY_TYPES.map((t) => (
              <div key={t.label} className="flex items-center gap-2 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 px-3 py-1.5 rounded-full text-sm shadow-sm">
                <div className={`w-2 h-2 rounded-full ${t.color}`} />
                <span className="font-medium text-slate-700 dark:text-slate-300">{t.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-bounce">
          <div className="w-px h-12 bg-gradient-to-b from-transparent to-slate-300 dark:to-slate-600" />
          <div className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600" />
        </div>
      </section>

      {/* Stats */}
      <section className="py-20 bg-white dark:bg-slate-900 border-y border-slate-100 dark:border-slate-800">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 animate-stagger">
            {STATS.map((s) => (
              <div key={s.label} className="text-center">
                <div className="font-display font-black text-4xl text-brand-600 dark:text-brand-400 mb-2">{s.value}</div>
                <div className="text-sm text-slate-500 dark:text-slate-400 font-medium">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-display font-bold text-4xl text-slate-900 dark:text-white mb-4">
              Всё что нужно для старта
            </h2>
            <p className="text-slate-500 dark:text-slate-400 text-lg max-w-xl mx-auto">
              Трамплин создан с учётом реальных потребностей студентов и работодателей.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 animate-stagger">
            {FEATURES.map((f) => (
              <div key={f.title} className="card p-6 hover:shadow-md transition-shadow">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${f.color}`}>
                  <f.icon size={22} />
                </div>
                <h3 className="font-display font-semibold text-lg text-slate-900 dark:text-white mb-2">
                  {f.title}
                </h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">
                  {f.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-24 bg-white dark:bg-slate-900 border-y border-slate-100 dark:border-slate-800 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="font-display font-bold text-4xl text-slate-900 dark:text-white mb-4">
              Как это работает
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { step: '01', title: 'Регистрируйся', desc: 'Создай аккаунт как студент или работодатель. Всего несколько минут.' },
              { step: '02', title: 'Находи', desc: 'Просматривай карту, применяй фильтры, добавляй в избранное.' },
              { step: '03', title: 'Действуй', desc: 'Откликайся на вакансии, общайся напрямую, строй карьеру.' },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="font-display font-black text-6xl text-brand-100 dark:text-brand-900 mb-4">{item.step}</div>
                <h3 className="font-display font-bold text-xl text-slate-900 dark:text-white mb-2">{item.title}</h3>
                <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA section */}
      <section className="py-24 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <div className="flex items-center justify-center gap-1 mb-6">
            {[...Array(5)].map((_, i) => (
              <Star key={i} size={20} className="text-amber-400 fill-amber-400" />
            ))}
          </div>
          <h2 className="font-display font-black text-4xl sm:text-5xl text-slate-900 dark:text-white mb-6">
            Готов сделать прыжок?
          </h2>
          <p className="text-slate-500 dark:text-slate-400 text-lg mb-8">
            Присоединяйся к тысячам студентов, которые уже нашли свою первую IT-работу через Трамплин.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/register" className="btn-primary text-base px-8 py-3.5 shadow-xl shadow-brand-500/25">
              Создать аккаунт бесплатно
              <ArrowRight size={18} />
            </Link>
            <Link to="/opportunities" className="btn-ghost text-base">
              Просмотр без регистрации →
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-100 dark:border-slate-800 py-12 px-4">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-brand-600 rounded-lg flex items-center justify-center">
              <Zap size={16} className="text-white" />
            </div>
            <span className="font-display font-bold text-slate-900 dark:text-white">Трамплин</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-slate-500">
            <Link to="/opportunities" className="hover:text-brand-600 transition-colors">Вакансии</Link>
            <Link to="/register" className="hover:text-brand-600 transition-colors">Регистрация</Link>
            <Link to="/login" className="hover:text-brand-600 transition-colors">Вход</Link>
          </div>
          <p className="text-sm text-slate-400">© 2024 Трамплин. Все права защищены.</p>
        </div>
      </footer>
    </div>
  )
}
