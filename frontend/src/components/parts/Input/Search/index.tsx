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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    onChange && onChange(value)
  }

  const handleClick = () => {
    if (value) {
      const pathname = router.pathname
      const query = { ...router.query, search: value }
      router.push({ pathname, query })
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleClick()
  }

  return (
    <div className={clsx(style.searchbar, className)}>
      <input type="search" name="search" placeholder="検索..." value={value} onChange={handleChange} onKeyDown={handleKeyDown} className={style.input} />
      <button onClick={handleClick} className={style.icon}>
        <i className="fas fa-search"></i>
      </button>
    </div>
  )
}
