export const nowDate = (() => {
  const date = new Date()
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  return { year, month, day }
})()

export const selectDate = (() => {
  const years = Array.from({ length: new Date().getFullYear() - 1899 }, (_, index) => {
    const year = 1900 + index
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
})()

export const padZero = (num: number): string => (num < 10 ? `0${num}` : `${num}`)

export const formatDatetime = (datetime: string): string => {
  const date = new Date(datetime)
  const year = date.getFullYear()
  const month = padZero(date.getMonth() + 1)
  const day = padZero(date.getDate())
  const hours = padZero(date.getHours())
  const minutes = padZero(date.getMinutes())
  return `${year}/${month}/${day} ${hours}:${minutes}`
}
