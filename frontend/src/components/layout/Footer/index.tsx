import { nowDate } from 'utils/functions/datetime'

export default function Footer(): React.JSX.Element {
  return (
    <footer className="footer">
      <small>© {nowDate.year} MyUs Co.,Ltd</small>
    </footer>
  )
}
