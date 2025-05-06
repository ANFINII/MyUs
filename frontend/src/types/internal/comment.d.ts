export interface Comment {
  id: number
  text: string
  created: Date
  updated: Date
  replys: Reply[]
  author: Author
}

export interface Reply {
  id: str
  text: str
  created: datetime
  updated: datetime
  author: Author
}
