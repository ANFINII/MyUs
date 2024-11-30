import { useRouter } from 'next/router'
import clsx from 'clsx'
import style from './Search.module.scss'

interface Props {
  value?: string
  className?: string
  onChange?: (value: string) => void
}

export default function Search(props: Props) {
  const { value, className, onChange } = props

  const router = useRouter()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => onChange && onChange(e.target.value)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && handleSearch()

  const handleSearch = () => {
    const { ...restQuery } = router.query
    const query = value ? { ...restQuery, search: value } : restQuery
    router.push({ pathname: router.pathname, query })
  }

  return (
    <div className={clsx(style.searchbar, className)}>
      <input type="search" name="search" placeholder="検索..." value={value} onChange={handleChange} onKeyDown={handleKeyDown} className={style.input} />
      <button onClick={handleSearch} className={style.icon}>
        <i className="fas fa-search"></i>
      </button>
    </div>
  )
}
