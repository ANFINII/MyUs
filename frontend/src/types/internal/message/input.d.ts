export interface MessageCreateIn {
  chatUlid: string
  text: string
  parentUlid?: string
}

export interface MessageUpdateIn {
  chatUlid: string
  text: string
}
