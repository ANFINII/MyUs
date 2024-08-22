export interface AnyObject {
  [key: string]: any
}

export interface MessageOut {
  error: boolean
  message: string
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
  toastContent?: string
  isError?: boolean
  isToast?: boolean
  setIsToast?: React.Dispatch<React.SetStateAction<boolean>>
}
