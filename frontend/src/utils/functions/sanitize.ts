import DOMPurify from 'isomorphic-dompurify'

export const sanitizeHtml = (html: string): string => {
  return DOMPurify.sanitize(html)
}
