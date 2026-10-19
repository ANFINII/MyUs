const VOLUME_KEY = 'media_volume'
const DEFAULT_VOLUME = 0.5

export const getVolume = (): number => {
  try {
    const value = localStorage.getItem(VOLUME_KEY)
    if (value === null) return DEFAULT_VOLUME
    const volume = Number(value)
    return Number.isFinite(volume) && volume >= 0 && volume <= 1 ? volume : DEFAULT_VOLUME
  } catch {
    return DEFAULT_VOLUME
  }
}

export const saveVolume = (volume: number): void => {
  try {
    localStorage.setItem(VOLUME_KEY, String(volume))
  } catch {
    return
  }
}
