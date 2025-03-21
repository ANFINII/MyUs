import { useRouter } from 'next/router'
import clsx from 'clsx'
import style from './Search.module.scss'

interface Props {
  value?: string
  className?: string
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
}

export default function Search(props: Props): JSX.Element {
  const { value, className, onChange } = props

  const router = useRouter()
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && handleSearch()

  const handleSearch = (): void => {
    const query = value ? { search: value } : ''
    router.push({ pathname: router.pathname, query })
  }

  return (
    <div className={clsx(style.searchbar, className)}>
      <input type="search" name="search" placeholder="検索..." value={value} onChange={onChange} onKeyDown={handleKeyDown} className={style.input} />
      <button onClick={handleSearch} className={style.icon}>
        <i className="fas fa-search"></i>
      </button>
    </div>
  )
}
