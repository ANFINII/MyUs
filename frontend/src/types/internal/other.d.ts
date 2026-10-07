export interface ErrorOut {
  message: string
}

export interface UrlSearch {
  search?: string
  page?: string
  channel?: string
  token?: string
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
  isError?: boolean
  isToast?: boolean
  setIsToast?: React.Dispatch<React.SetStateAction<boolean>>
}
