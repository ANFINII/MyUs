import { ChangeEvent } from 'react'
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

  return (
    <div className={style.header}>
      {count > 0 && (
        <>
          <span className={style.count}>{count}件選択</span>
          <Button color="red" size="s" name="一括削除" onClick={onModal} />
        </>
      )}
      <Button color="blue" size="s" name="投稿管理" onClick={() => router.push('/manage')} />
      <SelectBox value={ulid} options={options} className={style.select_box} onChange={onChange} />
    </div>
  )
}
