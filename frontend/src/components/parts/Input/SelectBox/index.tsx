import { ChangeEvent } from 'react'
import { Option } from 'types/internal/other'
import cx from 'utils/functions/cx'
import Select from 'components/parts/Select'
import VStack from 'components/parts/Stack/Vertical'
import style from './SelectBox.module.scss'

interface Props {
  label?: string
  name?: string
  value: string
  options: Option[]
  placeholder?: string
  required?: boolean
  disabled?: boolean
  className?: string
  onChange?: (e: ChangeEvent<HTMLSelectElement>) => void
}

export default function SelectBox(props: Props): React.JSX.Element {
  const { label, value, required = false, className, ...rest } = props

  const isRequired = required && !value

  return (
    <VStack gap="2" className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <div className={style.select_box}>
        <Select {...rest} value={value} id={label} className={cx(style.select, isRequired && style.error)} />
      </div>
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
    </VStack>
  )
}
