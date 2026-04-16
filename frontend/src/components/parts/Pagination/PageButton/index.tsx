import cx from 'utils/functions/cx'
import style from './PageButton.module.scss'

interface Props {
  page: number
  isActive: boolean
  onClick: () => void
}

export default function PageButton(props: Props): React.JSX.Element {
  const { page, isActive, onClick } = props

  return (
    <button type="button" className={cx(style.button, isActive && style.active)} onClick={onClick}>
      {page}
    </button>
  )
}
