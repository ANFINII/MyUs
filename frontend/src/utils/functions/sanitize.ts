import DOMPurify from 'isomorphic-dompurify'

const EXTERNAL_LINK = 'a[href^="http://"], a[href^="https://"]'

export const sanitizeHtml = (html: string, isSponsored: boolean = false): string => {
  const fragment = DOMPurify.sanitize(html, { RETURN_DOM_FRAGMENT: true })
  fragment.querySelectorAll(EXTERNAL_LINK).forEach((link) => {
    link.setAttribute('target', '_blank')
    link.setAttribute('rel', isSponsored ? 'sponsored noopener noreferrer nofollow' : 'noopener noreferrer nofollow')
  })
  const container = document.createElement('div')
  container.appendChild(fragment)
  return container.innerHTML
}
