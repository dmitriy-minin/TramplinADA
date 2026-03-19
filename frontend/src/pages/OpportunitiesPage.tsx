import { useState, useCallback } from 'react'
import { useQuery } from '@tanstack/react-query'
import { LayoutList, Map, ChevronLeft, ChevronRight } from 'lucide-react'
import Navbar from '@/components/common/Navbar'
import OpportunityCard from '@/components/opportunities/OpportunityCard'
import OpportunityFilters from '@/components/opportunities/OpportunityFilters'
import type { OpportunityFilters as Filters, OpportunityListResponse } from '@/types'
import api from '@/lib/api'
import { lazy, Suspense } from 'react'

const MapView = lazy(() => import('@/components/map/MapView'))

const DEFAULT_FILTERS: Filters = { page: 1, per_page: 20 }

export default function OpportunitiesPage() {
  const [view, setView] = useState<'list' | 'map'>('list')
  const [filters, setFilters] = useState<Filters>(DEFAULT_FILTERS)

  const { data, isLoading } = useQuery<OpportunityListResponse>({
    queryKey: ['opportunities', filters],
    queryFn: async () => {
      const params = Object.fromEntries(
        Object.entries(filters).filter(([, v]) => v !== undefined && v !== '')
      )
      const { data } = await api.get('/opportunities', { params })
      return data
    },
  })

  const updateFilters = useCallback((update: Partial<Filters>) => {
    setFilters((prev) => ({ ...prev, ...update, page: 1 }))
  }, [])

  const resetFilters = useCallback(() => {
    setFilters(DEFAULT_FILTERS)
  }, [])

  const opportunities = data?.items || []

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <Navbar />
      <div className="pt-16">
        <div className="max-w-7xl mx-auto px-4 py-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="font-display font-bold text-2xl text-slate-900 dark:text-white">
                Возможности
              </h1>
              {data && (
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                  Найдено: {data.total.toLocaleString('ru-RU')}
                </p>
              )}
            </div>

            {/* View toggle */}
            <div className="flex items-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-1 gap-1">
              <button
                onClick={() => setView('list')}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  view === 'list'
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200'
                }`}
              >
                <LayoutList size={16} /> Лента
              </button>
              <button
                onClick={() => setView('map')}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  view === 'map'
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200'
                }`}
              >
                <Map size={16} /> Карта
              </button>
            </div>
          </div>

          <div className="flex gap-6">
            {/* Sidebar filters */}
            <aside className="hidden lg:block w-72 shrink-0">
              <div className="sticky top-20">
                <OpportunityFilters filters={filters} onChange={updateFilters} onReset={resetFilters} />
              </div>
            </aside>

            {/* Main content */}
            <div className="flex-1 min-w-0">
              {/* Mobile filters */}
              <div className="lg:hidden mb-4">
                <OpportunityFilters filters={filters} onChange={updateFilters} onReset={resetFilters} />
              </div>

              {view === 'list' ? (
                <>
                  {isLoading ? (
                    <div className="grid sm:grid-cols-2 gap-4">
                      {[...Array(6)].map((_, i) => (
                        <div key={i} className="card h-48 animate-pulse bg-slate-100 dark:bg-slate-800" />
                      ))}
                    </div>
                  ) : opportunities.length === 0 ? (
                    <div className="text-center py-20 text-slate-400">
                      <Map size={40} className="mx-auto mb-3 opacity-30" />
                      <p className="font-display font-semibold text-lg">Ничего не найдено</p>
                      <p className="text-sm mt-1">Попробуйте изменить фильтры</p>
                    </div>
                  ) : (
                    <>
                      <div className="grid sm:grid-cols-2 gap-4 animate-stagger">
                        {opportunities.map((opp) => (
                          <OpportunityCard key={opp.id} opportunity={opp} />
                        ))}
                      </div>

                      {/* Pagination */}
                      {data && data.pages > 1 && (
                        <div className="flex items-center justify-center gap-3 mt-8">
                          <button
                            onClick={() => updateFilters({ page: (filters.page || 1) - 1 })}
                            disabled={(filters.page || 1) <= 1}
                            className="btn-secondary px-3 py-2 disabled:opacity-40"
                          >
                            <ChevronLeft size={16} />
                          </button>
                          <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">
                            {filters.page || 1} / {data.pages}
                          </span>
                          <button
                            onClick={() => updateFilters({ page: (filters.page || 1) + 1 })}
                            disabled={(filters.page || 1) >= data.pages}
                            className="btn-secondary px-3 py-2 disabled:opacity-40"
                          >
                            <ChevronRight size={16} />
                          </button>
                        </div>
                      )}
                    </>
                  )}
                </>
              ) : (
                <div className="h-[calc(100vh-180px)] rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-700 shadow-sm">
                  <Suspense fallback={
                    <div className="w-full h-full flex items-center justify-center bg-slate-100 dark:bg-slate-800">
                      <div className="text-slate-400">Загрузка карты...</div>
                    </div>
                  }>
                    <MapView opportunities={opportunities} />
                  </Suspense>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
