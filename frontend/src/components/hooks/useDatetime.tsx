import { useTranslation } from 'react-i18next'

interface OutProps {
  formatDatetime: (datetime: Date) => string
  formatDate: (datetime: Date) => string
  formatTimeAgo: (datetime: Date) => string
}

export const useDatetime = (): OutProps => {
  const { t, i18n } = useTranslation()
  const locale = i18n.language

  const formatDatetime = (datetime: Date): string => {
    return new Date(datetime).toLocaleString(locale, {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    })
  }

  const formatDate = (datetime: Date): string => {
    const date = new Date(datetime)
    const today = new Date()
    if (date.toDateString() === today.toDateString()) return t('datetime.today')
    return date.toLocaleDateString(locale, { year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' })
  }

  const formatTimeAgo = (datetime: Date): string => {
    const now = new Date()
    const date = new Date(datetime)
    const diff = (now.getFullYear() - date.getFullYear()) * 12 + (now.getMonth() - date.getMonth())
    const year = Math.floor(diff / 12)
    const month = diff % 12
    const yearText = year > 0 ? t('datetime.year', { count: year }) : ''
    const monthText = month > 0 ? t('datetime.month', { count: month }) : ''
    const time = [yearText, monthText].filter(Boolean).join(t('datetime.separator'))
    return t('datetime.ago', { time })
  }

  return { formatDatetime, formatDate, formatTimeAgo }
}
