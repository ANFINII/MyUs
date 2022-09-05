export default function Footer() {
  const today = new Date();
  const year = today.getFullYear();
  return (
    <footer className="footer-myus" style={{textAlign: "center"}}>
      <small>© {year} MyUs Co.,Ltd</small>
    </footer>
  )
}
