import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'
import api from '@/lib/api'

interface AuthState {
  user: User | null
  isLoading: boolean
  setUser: (user: User | null) => void
  login: (access_token: string, refresh_token: string) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isLoading: false,

      setUser: (user) => set({ user }),

      login: async (access_token, refresh_token) => {
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        await get().refreshUser()
      },

      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null })
      },

      refreshUser: async () => {
        set({ isLoading: true })
        try {
          const { data } = await api.get('/auth/me')
          set({ user: data })
        } catch {
          set({ user: null })
        } finally {
          set({ isLoading: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user }),
    }
  )
)
