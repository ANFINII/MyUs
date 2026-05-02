import { useEffect, useMemo, useRef, useState } from 'react'
import { useRouter } from 'next/router'
import cx from 'utils/functions/cx'
import IconCalendar from 'components/parts/Icon/Calendar'
import style from './DatePicker.module.scss'

interface DayCell {
  date: Date
  isDisabled: boolean
}

const PLACEHOLDER_MAP: Record<string, string> = {
  ja: '日付を選択',
  en: 'Select a date',
}

const toIsoDate = (date: Date): string => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

const fromIsoDate = (iso?: string): Date | undefined => {
  if (!iso) return undefined
  const [y, m, d] = iso.split('-').map(Number)
  if (!y || !m || !d) return undefined
  return new Date(y, m - 1, d)
}

const isSameDate = (a: Date, b: Date): boolean => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()

const buildMonthGrid = (year: number, month: number, min?: Date, max?: Date): (DayCell | null)[] => {
  const startDay = new Date(year, month, 1).getDay()
  const lastDay = new Date(year, month + 1, 0).getDate()
  const isDisabled = (d: Date): boolean => {
    if (min && d < min) return true
    if (max && d > max) return true
    return false
  }
  const cells: (DayCell | null)[] = []
  for (let i = 0; i < startDay; i++) cells.push(null)
  for (let i = 1; i <= lastDay; i++) {
    const d = new Date(year, month, i)
    cells.push({ date: d, isDisabled: isDisabled(d) })
  }
  while (cells.length < 42) cells.push(null)
  return cells
}

interface Props {
  label?: string
  value?: string
  name?: string
  placeholder?: string
  error?: string
  className?: string
  required?: boolean
  minDate?: string
  maxDate?: string
  onChange?: (date: string) => void
}

export default function DatePicker(props: Props): React.JSX.Element {
  const { label, value, placeholder, error, className, required = false, minDate, maxDate, onChange } = props

  const router = useRouter()
  const locale = router.locale ?? 'ja'

  const boxRef = useRef<HTMLDivElement>(null)
  const today = useMemo(() => new Date(), [])
  const min = useMemo(() => fromIsoDate(minDate), [minDate])
  const max = useMemo(() => fromIsoDate(maxDate), [maxDate])
  const selected = useMemo(() => fromIsoDate(value), [value])

  const displayFormat = useMemo(() => new Intl.DateTimeFormat(locale, { year: 'numeric', month: 'long', day: 'numeric' }), [locale])
  const titleFormat = useMemo(() => new Intl.DateTimeFormat(locale, { year: 'numeric', month: 'long' }), [locale])
  const weekdays = useMemo(() => {
    const fmt = new Intl.DateTimeFormat(locale, { weekday: 'short' })
    return Array.from({ length: 7 }, (_, i) => fmt.format(new Date(2024, 0, 7 + i)))
  }, [locale])
  const placeholderText = placeholder ?? PLACEHOLDER_MAP[locale] ?? PLACEHOLDER_MAP.ja

  const [isOpen, setIsOpen] = useState<boolean>(false)
  const [viewYear, setViewYear] = useState<number>((selected ?? today).getFullYear())
  const [viewMonth, setViewMonth] = useState<number>((selected ?? today).getMonth())

  const isError = !!error || (error === '' && required && !selected)
  const cells = useMemo(() => buildMonthGrid(viewYear, viewMonth, min, max), [viewYear, viewMonth, min, max])

  useEffect(() => {
    if (!selected) return
    setViewYear(selected.getFullYear())
    setViewMonth(selected.getMonth())
  }, [selected])

  useEffect(() => {
    if (!isOpen) return
    const handleClickOutside = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setIsOpen(false)
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isOpen])

  const handleToggle = () => setIsOpen((prev) => !prev)

  const handlePrev = () => {
    const d = new Date(viewYear, viewMonth - 1, 1)
    setViewYear(d.getFullYear())
    setViewMonth(d.getMonth())
  }

  const handleNext = () => {
    const d = new Date(viewYear, viewMonth + 1, 1)
    setViewYear(d.getFullYear())
    setViewMonth(d.getMonth())
  }

  const handleSelect = (cell: DayCell) => {
    if (cell.isDisabled) return
    onChange?.(toIsoDate(cell.date))
    setIsOpen(false)
  }

  return (
    <div ref={boxRef} className={cx(style.box, className)}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
          {required && <span className={style.required}>*</span>}
        </label>
      )}
      <div className={style.field}>
        <button id={label} type="button" onClick={handleToggle} className={cx(style.input, !selected && style.placeholder, isOpen && style.active, isError && style.error)}>
          {selected ? (locale === 'ja' ? toIsoDate(selected) : displayFormat.format(selected)) : placeholderText}
        </button>
        <IconCalendar size="16" className={style.icon} />
        {isOpen && (
          <div className={style.calendar}>
            <div className={style.nav}>
              <button type="button" onClick={handlePrev} className={style.nav_button}>
                ‹
              </button>
              <span className={style.title}>{titleFormat.format(new Date(viewYear, viewMonth, 1))}</span>
              <button type="button" onClick={handleNext} className={style.nav_button}>
                ›
              </button>
            </div>
            <div className={style.weekdays}>
              {weekdays.map((w, i) => (
                <span key={w} className={cx(style.weekday, i === 0 && style.sunday, i === 6 && style.saturday)}>
                  {w}
                </span>
              ))}
            </div>
            <div className={style.grid}>
              {cells.map((cell, i) => {
                if (!cell) return <span key={i} className={style.empty} />
                const day = cell.date.getDay()
                const isToday = isSameDate(cell.date, today)
                const isSelected = !!selected && isSameDate(cell.date, selected)
                return (
                  <button
                    key={i}
                    type="button"
                    disabled={cell.isDisabled}
                    onClick={() => handleSelect(cell)}
                    className={cx(
                      style.day,
                      isToday && style.today,
                      isSelected && style.selected,
                      cell.isDisabled && style.disabled,
                      !cell.isDisabled && !isSelected && day === 0 && style.sunday,
                      !cell.isDisabled && !isSelected && day === 6 && style.saturday,
                    )}
                  >
                    {cell.date.getDate()}
                  </button>
                )
              })}
            </div>
          </div>
        )}
      </div>
      {error && <p className={style.error_text}>{error}</p>}
    </div>
  )
}
