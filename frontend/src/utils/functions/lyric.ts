const TIME_TAG = /\[(\d{1,2}):(\d{2})(?:[.:](\d{1,3}))?\]/g

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
