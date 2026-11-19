import { camelSnake } from 'utils/functions/convertCase'
import { isMeasurementId } from 'utils/functions/validation'

declare global {
  interface Window {
    userDataLayer?: unknown[]
    [key: `ga-disable-${string}`]: boolean | undefined
  }
}

const configured = new Set<string>()
let current = { ulid: '', measurementId: '' }

const gtag: (...args: unknown[]) => void = function() {
  window.userDataLayer?.push(arguments)
}

const loadGtag = (measurementId: string): void => {
  if (window.userDataLayer) return
  window.userDataLayer = []
  gtag('js', new Date())
  const script = document.createElement('script')
  script.async = true
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}&l=userDataLayer`
  document.head.appendChild(script)
}

export const trackUserPageView = (ulid: string, measurementId: string, title: string): void => {
  if (!import.meta.env.PROD || !isMeasurementId(measurementId)) return
  loadGtag(measurementId)
  if (!configured.has(measurementId)) {
    gtag('config', measurementId, camelSnake({ sendPageView: false }))
    configured.add(measurementId)
  }
  window[`ga-disable-${measurementId}`] = false
  current = { ulid, measurementId }
  gtag('event', 'page_view', camelSnake({ sendTo: measurementId, pageLocation: window.location.href, pageTitle: title }))
}

export const trackUserPageEvent = (name: string, params: Record<string, string>): void => {
  if (current.measurementId === '') return
  gtag('event', name, camelSnake({ ...params, sendTo: current.measurementId }))
}

export const leaveUserPage = (pathname: string): void => {
  if (current.measurementId === '' || pathname.endsWith(`/userpage/${current.ulid}`)) return
  window[`ga-disable-${current.measurementId}`] = true
  current = { ulid: '', measurementId: '' }
}
