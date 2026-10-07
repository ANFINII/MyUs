import { ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { Option } from 'types/internal/other'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Button from 'components/parts/Button'
import SelectBox from 'components/parts/Input/SelectBox'
import style from './Header.module.scss'

interface Props {
  count: number
  ulid: string
  options: Option[]
  onModal: () => void
  onChange: (e: ChangeEvent<HTMLSelectElement>) => void
}

export default function ManageHeader(props: Props): React.JSX.Element {
  const { count, ulid, options, onModal, onChange } = props

  const router = useAppRouter()
  const { t } = useTranslation()

  return (
    <div className={style.header}>
      {count > 0 && (
        <>
          <span className={style.count}>{t('manage.header.selected', { count })}</span>
          <Button color="red" size="s" name={t('manage.header.bulkDelete')} onClick={onModal} />
        </>
      )}
      <Button color="blue" size="s" name={t('manage.title')} onClick={() => router.push('/manage')} />
      <SelectBox value={ulid} options={options} className={style.select_box} onChange={onChange} />
    </div>
  )
}
