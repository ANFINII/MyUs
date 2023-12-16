export const selectDate = () => {
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
}
