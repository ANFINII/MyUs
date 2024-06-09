import { useRef, useCallback, SetStateAction } from 'react'
import { debounce } from 'lodash'

type ValueType = 'string' | 'number'

interface OutProps<V> {
  debounceChange: (onChange: (v: V) => void, value: V, id?: number) => void
}

interface Props<V> {
  setValues: React.Dispatch<SetStateAction<{ [id: number]: V }>>
  delay?: number
  type?: ValueType
}

export function useDebounce<V>(Props: Props<V>): OutProps<V> {
  const { setValues, delay = 800, type = 'string' } = Props

  const debouncedRef = useRef(debounce((id: number, value: V) => setValues({ [id]: value }), delay)).current

  const debounceChange = useCallback(
    (onChange: (v: V) => void, value: V, id?: number) => {
      if (type === 'string') {
        onChange(value)
        debouncedRef(id || 0, value)
      } else if (type === 'number') {
        const intValue = Number(value)
        onChange(intValue as V)
        debouncedRef(id || 0, intValue as V)
      }
    },
    [type, debouncedRef],
  )

  return { debounceChange }
}
