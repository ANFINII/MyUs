export const selectDate = () => {
  const years = []
  for (let i = 1900; i <= new Date().getFullYear(); i++) {
    years.push({ value: i, label: i.toString() })
  }

  const months = []
  for (let i = 1; i <= 12; i++) {
    months.push({ value: i, label: i.toString() })
  }

  const days = []
  for (let i = 1; i <= 31; i++) {
    days.push({ value: i, label: i.toString() })
  }
  return { years, months, days }
}
