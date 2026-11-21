const COPY_ICON =
  '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16" width="14" height="14" data-icon="copy"><path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/></svg>'
const CHECK_ICON =
  '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16" width="14" height="14" data-icon="check"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0"/></svg>'

export const addCodeCopyButtons = (html: string, label: string): string => {
  const doc = new DOMParser().parseFromString(html, 'text/html')
  doc.body.querySelectorAll('pre').forEach((pre) => {
    const block = doc.createElement('div')
    block.setAttribute('data-code-block', '')
    const button = doc.createElement('button')
    button.type = 'button'
    button.title = label
    button.setAttribute('aria-label', label)
    button.setAttribute('data-code-copy', '')
    button.innerHTML = COPY_ICON + CHECK_ICON
    pre.replaceWith(block)
    block.append(button, pre)
  })
  return doc.body.innerHTML
}
