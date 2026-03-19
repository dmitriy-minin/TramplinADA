import { useEffect, useRef } from 'react'
import type { Opportunity } from '@/types'

interface MapViewProps {
  opportunities: Opportunity[]
  onMarkerClick?: (id: string) => void
}

// Dynamic import to avoid SSR issues
let L: typeof import('leaflet') | null = null

export default function MapView({ opportunities, onMarkerClick }: MapViewProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<import('leaflet').Map | null>(null)
  const markersRef = useRef<import('leaflet').Marker[]>([])

  useEffect(() => {
    if (!containerRef.current) return

    // Lazy load Leaflet
    import('leaflet').then((leaflet) => {
      L = leaflet.default || leaflet

      if (mapRef.current) return // already initialized

      const map = L.map(containerRef.current!, {
        center: [48.0, 66.9],  // Kazakhstan center
        zoom: 5,
        zoomControl: true,
      })

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 19,
      }).addTo(map)

      mapRef.current = map
    })

    return () => {
      if (mapRef.current) {
        mapRef.current.remove()
        mapRef.current = null
      }
    }
  }, [])

  // Update markers when opportunities change
  useEffect(() => {
    if (!mapRef.current || !L) return

    // Clear existing markers
    markersRef.current.forEach((m) => m.remove())
    markersRef.current = []

    const withCoords = opportunities.filter((o) => o.latitude && o.longitude)
    if (withCoords.length === 0) return

    const TYPE_COLORS: Record<string, string> = {
      vacancy: '#3373ff',
      internship: '#10b981',
      mentorship: '#f97316',
      event: '#64748b',
    }

    withCoords.forEach((opp) => {
      const color = TYPE_COLORS[opp.type] || '#3373ff'

      const icon = L!.divIcon({
        html: `<div style="
          width: 32px; height: 32px;
          background: ${color};
          border: 3px solid white;
          border-radius: 50% 50% 50% 0;
          transform: rotate(-45deg);
          box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        "></div>`,
        className: '',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -36],
      })

      const salaryText = opp.salary_from
        ? `${opp.salary_from.toLocaleString('ru-RU')} – ${opp.salary_to?.toLocaleString('ru-RU') || '...'} ${opp.salary_currency}`
        : 'Зарплата не указана'

      const popupHtml = `
        <div style="min-width:220px; font-family: 'DM Sans', sans-serif;">
          <p style="font-weight:700; font-size:14px; margin:0 0 4px; color:#1e293b;">${opp.title}</p>
          <p style="font-size:12px; color:#64748b; margin:0 0 4px;">${opp.company.name}</p>
          <p style="font-size:12px; font-weight:600; color:#3373ff; margin:0 0 8px;">${salaryText}</p>
          <a href="/opportunities/${opp.id}" 
             style="display:inline-block; background:#3373ff; color:white; padding:5px 12px; border-radius:8px; font-size:12px; font-weight:600; text-decoration:none;">
            Подробнее →
          </a>
        </div>
      `

      const marker = L!.marker([opp.latitude!, opp.longitude!], { icon })
        .addTo(mapRef.current!)
        .bindPopup(popupHtml)

      if (onMarkerClick) {
        marker.on('click', () => onMarkerClick(opp.id))
      }

      markersRef.current.push(marker)
    })

    // Fit bounds if we have markers
    if (withCoords.length > 0) {
      const group = L.featureGroup(markersRef.current)
      mapRef.current.fitBounds(group.getBounds().pad(0.1), { maxZoom: 12 })
    }
  }, [opportunities, onMarkerClick])

  return (
    <div ref={containerRef} className="w-full h-full rounded-xl overflow-hidden" />
  )
}
