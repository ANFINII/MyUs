export default function Footer() {
  const today = new Date()
  const year = today.getFullYear()
  return (
    <footer className="footer">
      <small>© {year} MyUs Co.,Ltd</small>
    </footer>
  )
}
