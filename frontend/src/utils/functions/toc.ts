const HEADING = 'h1, h2, h3'

export interface TocHeading {
  id: string
  level: number
  text: string
}

export interface TocArticle {
  richtext: string
  paidText: string
  headings: TocHeading[]
}

export const buildToc = (richtext: string, paidText: string): TocArticle => {
  const headings: TocHeading[] = []
  const parser = new DOMParser()

  const addHeadingIds = (html: string): string => {
    const doc = parser.parseFromString(html, 'text/html')
    doc.body.querySelectorAll(HEADING).forEach((element) => {
      const text = element.textContent?.trim() ?? ''
      if (text === '') return
      const id = `section-${headings.length + 1}`
      element.id = id
      headings.push({ id, level: Number(element.tagName.slice(1)), text })
    })
    return doc.body.innerHTML
  }

  return { richtext: addHeadingIds(richtext), paidText: addHeadingIds(paidText), headings }
}
