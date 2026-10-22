import DOMPurify from 'isomorphic-dompurify'

DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node.tagName !== 'A' || !/^https?:\/\//.test(node.getAttribute('href') ?? '')) return
  node.setAttribute('target', '_blank')
  node.setAttribute('rel', 'noopener noreferrer nofollow')
})

export const sanitizeHtml = (html: string): string => {
  return DOMPurify.sanitize(html)
}
