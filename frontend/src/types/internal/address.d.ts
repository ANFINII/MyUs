export interface AddressResult {
  zipcode: string
  prefcode: string
  address1: string
  address2: string
  address3: string
  kana1: string
  kana2: string
  kana3: string
}

export interface Address {
  status: number
  message: string
  results: AddressResult[]
}
