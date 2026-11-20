import { ChangeEvent } from 'react'
import IconArrow from 'components/parts/Icon/Arrow'
import Search from 'components/parts/Input/Search'
import style from './SearchBar.module.scss'

interface Props {
  value: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
  onClose: () => void
}

export default function SearchBar(props: Props): React.JSX.Element {
  const { value, onChange, onClose } = props

  return (
    <div className={style.search_bar}>
      <button type="button" className={style.back} onClick={onClose}>
        <IconArrow size="20" type="left" />
      </button>
      <Search value={value} isFull autoFocus onChange={onChange} onSearch={onClose} />
    </div>
  )
}
