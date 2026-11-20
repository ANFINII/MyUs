import { AudioHires } from 'types/internal/media/output'

const FLAC_HEADER_SIZE = 42
const HIRES_BIT_DEPTH = 24
const HIRES_SAMPLE_RATE_MIN = 48000
const HIRES_SAMPLE_RATE_MAX = 192000
const HIRES_PRICE_MIN = 300
const HIRES_PRICE_MAX = 600

export const flacHires = async (file: File): Promise<AudioHires | null> => {
  const bytes = new Uint8Array(await file.slice(0, FLAC_HEADER_SIZE).arrayBuffer())
  if (bytes.length < FLAC_HEADER_SIZE) return null
  if (new TextDecoder().decode(bytes.slice(0, 4)) !== 'fLaC') return null
  const [b18 = 0, b19 = 0, b20 = 0, b21 = 0] = bytes.slice(18, 22)
  const sampleRate = (b18 << 12) | (b19 << 4) | (b20 >> 4)
  const bitDepth = (((b20 & 0x01) << 4) | (b21 >> 4)) + 1
  return { sampleRate, bitDepth }
}

export const hiresLabel = (hires: AudioHires): string => `${hires.bitDepth}bit / ${hires.sampleRate / 1000}kHz`

export const hiresError = (hires: AudioHires | null, price: number): string => {
  if (hires === null || hires.bitDepth !== HIRES_BIT_DEPTH) return 'error.hiresInvalid'
  if (hires.sampleRate < HIRES_SAMPLE_RATE_MIN || hires.sampleRate > HIRES_SAMPLE_RATE_MAX) return 'error.hiresInvalid'
  if (price < HIRES_PRICE_MIN || price > HIRES_PRICE_MAX) return 'error.hiresPriceRange'
  return ''
}
