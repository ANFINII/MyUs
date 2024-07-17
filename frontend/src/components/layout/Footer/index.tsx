export default function Footer() {
  const today = new Date()
  return (
    <footer className="footer">
      <small>© {today.getFullYear()} MyUs Co.,Ltd</small>
    </footer>
  )
}
