const TIME_TAG = /\[(\d{1,2}):(\d{2})(?:[.:](\d{1,3}))?\]/g
const TIME_INPUT = /^\[?(\d{1,2}):([0-5]\d)(?:[.:](\d{1,3}))?\]?$/

export interface LyricLine {
  time: number
  text: string
}

export interface ParsedLyric {
  isSynced: boolean
  lines: LyricLine[]
}

const toSeconds = (minutes: string, seconds: string, fraction: string | undefined): number => Number(minutes) * 60 + Number(seconds) + (fraction ? Number(`0.${fraction}`) : 0)

export const parseLyric = (lyric: string): ParsedLyric => {
  const rows = lyric.split(/\r?\n/)
  const synced = rows.flatMap((row) => {
    const text = row.replace(TIME_TAG, '').trim()
    return [...row.matchAll(TIME_TAG)].map((m) => ({ time: toSeconds(m[1] ?? '0', m[2] ?? '0', m[3]), text }))
  })
  if (synced.length === 0) return { isSynced: false, lines: rows.map((text) => ({ time: -1, text })) }
  return { isSynced: true, lines: synced.sort((a, b) => a.time - b.time) }
}

export const activeLyricIndex = (lines: LyricLine[], currentTime: number): number => {
  let index = -1
  lines.forEach((line, i) => {
    if (line.time <= currentTime) index = i
  })
  return index
}

export const toLyricRows = (lyric: string): LyricLine[] =>
  lyric.split(/\r?\n/).map((row) => {
    const tag = [...row.matchAll(TIME_TAG)][0]
    const time = tag ? toSeconds(tag[1] ?? '0', tag[2] ?? '0', tag[3]) : -1
    return { time, text: row.replace(TIME_TAG, '').trim() }
  })

export const formatLyricTime = (time: number): string => {
  const minutes = Math.floor(time / 60)
  const seconds = time - minutes * 60
  return `${String(minutes).padStart(2, '0')}:${seconds.toFixed(2).padStart(5, '0')}`
}

export const parseLyricTime = (value: string): number | undefined => {
  const m = value.trim().match(TIME_INPUT)
  return m ? toSeconds(m[1] ?? '0', m[2] ?? '0', m[3]) : undefined
}

export const buildLyric = (rows: LyricLine[]): string => rows.map((row) => (row.time >= 0 ? `[${formatLyricTime(row.time)}]${row.text}` : row.text)).join('\n')
