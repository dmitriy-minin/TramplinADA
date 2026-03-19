export type UserRole = 'soiskatel' | 'employer' | 'curator'
export type PrivacyLevel = 'public' | 'contacts_only' | 'hidden'
export type OpportunityType = 'vacancy' | 'internship' | 'mentorship' | 'event'
export type WorkFormat = 'office' | 'remote' | 'hybrid'
export type ExperienceLevel = 'junior' | 'middle' | 'senior' | 'any'
export type OpportunityStatus = 'pending' | 'active' | 'rejected' | 'closed'
export type ApplicationStatus = 'pending' | 'accepted' | 'rejected' | 'reserve'

export interface User {
  id: string
  email: string
  full_name: string
  role: UserRole
  is_verified: boolean
  avatar_url?: string
  university?: string
  study_year?: number
  bio?: string
  resume_markdown?: string
  github_url?: string
  portfolio_url?: string
  resume_privacy?: PrivacyLevel
  created_at: string
}

export interface Tag {
  id: string
  name: string
  category: string
}

export interface CompanyShort {
  id: string
  name: string
  logo_url?: string
  city?: string
  is_verified: boolean
}

export interface Opportunity {
  id: string
  title: string
  description: string
  type: OpportunityType
  format: WorkFormat
  level: ExperienceLevel
  status: OpportunityStatus
  salary_from?: number
  salary_to?: number
  salary_currency: string
  address?: string
  city?: string
  latitude?: number
  longitude?: number
  views_count: number
  tags: Tag[]
  company: CompanyShort
  created_at: string
  expires_at?: string
  applications_count?: number
  is_favorited?: boolean
}

export interface OpportunityListResponse {
  items: Opportunity[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface Application {
  id: string
  opportunity_id: string
  status: ApplicationStatus
  cover_letter?: string
  created_at: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface OpportunityFilters {
  search?: string
  type?: OpportunityType
  format?: WorkFormat
  level?: ExperienceLevel
  salary_from?: number
  salary_to?: number
  tag_ids?: string
  city?: string
  page?: number
  per_page?: number
}
