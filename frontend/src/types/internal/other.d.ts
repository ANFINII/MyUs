export interface MessageOut {
  message: string
}

export interface SearchTag {
  id: number
  name: string
}

export interface Option {
  label: string
  value: string
}

export interface MetaType {
  description?: string
  url?: string
  locale?: string
  siteName?: string
  canonical?: string
}

export interface ToastType {
  content?: string
  error?: boolean
  toast?: boolean
  setToast?: React.Dispatch<React.SetStateAction<boolean>>
}
