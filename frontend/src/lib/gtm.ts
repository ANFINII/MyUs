import { GTM_ID } from 'lib/config'

declare global {
  interface Window {
    dataLayer?: unknown[]
  }
}

export const loadGtm = (): void => {
  if (!import.meta.env.PROD || GTM_ID === '') return
  const dataLayer = window.dataLayer ?? []
  window.dataLayer = dataLayer
  dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' })
  const script = document.createElement('script')
  script.async = true
  script.src = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(GTM_ID)}`
  document.head.appendChild(script)
}
