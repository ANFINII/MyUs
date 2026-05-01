import { ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { Option } from 'types/internal/other'
import Button from 'components/parts/Button'
import SelectBox from 'components/parts/Input/SelectBox'
import style from './Header.module.scss'

interface Props {
  count: number
  ulid: string
  options: Option[]
  onDelete: () => void
  onChange: (e: ChangeEvent<HTMLSelectElement>) => void
}

export default function ManageHeader(props: Props): React.JSX.Element {
  const { count, ulid, options, onDelete, onChange } = props

  const router = useRouter()

  return (
    <div className={style.header}>
      {count > 0 && (
        <>
          <span className={style.count}>{count}件選択</span>
          <Button color="red" size="s" name="一括削除" onClick={onDelete} />
        </>
      )}
      <Button color="blue" size="s" name="投稿管理" onClick={() => router.push('/manage')} />
      <SelectBox value={ulid} options={options} className={style.filter} onChange={onChange} />
    </div>
  )
}
