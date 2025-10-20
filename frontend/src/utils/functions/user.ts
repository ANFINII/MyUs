export const getFullName = (lastName: string, firstName: string): string => {
  return lastName + ' ' + firstName
}

export const getAge = (year: number, month: number, day: number): number => {
  const birthDate = new Date(year, month - 1, day)
  const today = new Date()
  const DAYS_IN_YEAR = 365.2425
  const diffTime = today.getTime() - birthDate.getTime()
  const diffDays = diffTime / (1000 * 60 * 60 * 24)
  return Math.floor(diffDays / DAYS_IN_YEAR)
}
