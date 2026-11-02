import { APP_VERSION } from 'lib/config'

const VERSION_URL = '/version.json'
const CHECK_INTERVAL_MS = 5 * 60 * 1000

let isLatest = true

const checkVersion = async (): Promise<void> => {
  try {
    const res = await fetch(VERSION_URL, { cache: 'no-store' })
    if (!res.ok) return
    const data: { version?: string } = await res.json()
    if (data.version !== undefined && data.version !== APP_VERSION) isLatest = false
  } catch {
    return
  }
}

export const isOutdated = (): boolean => !isLatest

export const watchVersion = (): void => {
  if (!import.meta.env.PROD) return
  window.setInterval(checkVersion, CHECK_INTERVAL_MS)
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') checkVersion()
  })
}

export const reloadOnPreloadError = (): void => {
  window.addEventListener('vite:preloadError', (event) => {
    const key = `vite_preload_reload:${event.payload.message}`
    if (sessionStorage.getItem(key) !== null) return
    sessionStorage.setItem(key, '1')
    event.preventDefault()
    window.location.reload()
  })
}
