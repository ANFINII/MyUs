import { ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { useAppRouter } from 'components/hooks/useAppRouter'
import IconSearch from 'components/parts/Icon/Search'
import style from './Search.module.scss'

interface Props {
  value?: string
  className?: string
  onChange?: (e: ChangeEvent<HTMLInputElement>) => void
}

export default function Search(props: Props): React.JSX.Element {
  const { value, className, onChange } = props

  const router = useAppRouter()
  const { t } = useTranslation()

  const handleSearch = () => {
    const query = value ? { search: value } : {}
    router.push({ pathname: router.pathname, query })
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSearch()
  }

  return (
    <div className={cx(style.searchbar, className)}>
      <input type="search" name="search" placeholder={t('input.search')} value={value} onChange={onChange} onKeyDown={handleKeyDown} className={style.input} />
      <button onClick={handleSearch} className={style.icon}>
        <IconSearch size="16" />
      </button>
    </div>
  )
}
