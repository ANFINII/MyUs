export const nowDate = (() => {
  const date = new Date()
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return { year, month, day }
})()

export const selectDate = () => {
  const date = new Date()
  const currentYear = date.getFullYear()
  const baseYear = currentYear - 130

  const years = Array.from({ length: currentYear - baseYear + 1 }, (_, index) => {
    const year = baseYear + index
    return { label: year.toString(), value: year.toString() }
  })

  const months = Array.from({ length: 12 }, (_, index) => {
    const month = index + 1
    return { label: month.toString(), value: month.toString() }
  })

  const days = Array.from({ length: 31 }, (_, index) => {
    const day = index + 1
    return { label: day.toString(), value: day.toString() }
  })

  return { years, months, days }
}

export const formatDatetime = (datetime: Date): string => {
  return new Date(datetime).toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  })
}

export const formatTimeAgo = (datetime: Date): string => {
  const now = new Date()
  const date = new Date(datetime)
  const diff = (now.getFullYear() - date.getFullYear()) * 12 + (now.getMonth() - date.getMonth())
  const year = Math.floor(diff / 12)
  const month = diff % 12
  const yearText = year > 0 ? `${year}年` : ''
  const monthText = month > 0 ? `${month}ヶ月` : ''
  return `${yearText}${monthText}前`
}
