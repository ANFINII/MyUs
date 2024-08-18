import { Option } from 'types/internal/other'

export const priority: Option[] = [
  { label: '高', value: 'danger' },
  { label: '普通', value: 'success' },
  { label: '低', value: 'info' },
]

export const progress: Option[] = [
  { label: '未着手', value: '0' },
  { label: '進行中', value: '1' },
  { label: '完了', value: '2' },
]
