import { nowDate } from 'utils/functions/datetime'
import style from './Footer.module.scss'

export default function Footer(): React.JSX.Element {
  return (
    <footer className={style.footer}>
      <small>© {nowDate.year} MyUs Co.,Ltd</small>
    </footer>
  )
}
