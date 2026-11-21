import hljs from 'highlight.js/lib/core'
import bash from 'highlight.js/lib/languages/bash'
import css from 'highlight.js/lib/languages/css'
import go from 'highlight.js/lib/languages/go'
import javascript from 'highlight.js/lib/languages/javascript'
import json from 'highlight.js/lib/languages/json'
import python from 'highlight.js/lib/languages/python'
import sql from 'highlight.js/lib/languages/sql'
import typescript from 'highlight.js/lib/languages/typescript'
import xml from 'highlight.js/lib/languages/xml'
import yaml from 'highlight.js/lib/languages/yaml'
import { Option } from 'types/internal/other'

const COPY_ICON =
  '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16" width="14" height="14" data-icon="copy"><path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/></svg>'
const CHECK_ICON =
  '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16" width="14" height="14" data-icon="check"><path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0"/></svg>'
const LANGUAGE_PREFIX = 'language-'

export const CODE_LANGUAGES: Option[] = [
  { label: 'Python', value: 'python' },
  { label: 'TypeScript', value: 'typescript' },
  { label: 'JavaScript', value: 'javascript' },
  { label: 'HTML', value: 'xml' },
  { label: 'CSS', value: 'css' },
  { label: 'SQL', value: 'sql' },
  { label: 'Bash', value: 'bash' },
  { label: 'JSON', value: 'json' },
  { label: 'YAML', value: 'yaml' },
  { label: 'Go', value: 'go' },
]

hljs.registerLanguage('python', python)
hljs.registerLanguage('typescript', typescript)
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('xml', xml)
hljs.registerLanguage('css', css)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('bash', bash)
hljs.registerLanguage('json', json)
hljs.registerLanguage('yaml', yaml)
hljs.registerLanguage('go', go)

const highlightCode = (doc: Document, block: HTMLElement, code: Element) => {
  const language = [...code.classList].find((name) => name.startsWith(LANGUAGE_PREFIX))?.slice(LANGUAGE_PREFIX.length) ?? ''
  const option = CODE_LANGUAGES.find((item) => item.value === language)
  if (!option) return
  code.innerHTML = hljs.highlight(code.textContent ?? '', { language }).value
  const label = doc.createElement('span')
  label.setAttribute('data-code-lang', '')
  label.textContent = option.label
  block.setAttribute('data-has-lang', '')
  block.prepend(label)
}

export const decorateCodeBlocks = (html: string, copyLabel: string): string => {
  const doc = new DOMParser().parseFromString(html, 'text/html')
  doc.body.querySelectorAll('pre').forEach((pre) => {
    const block = doc.createElement('div')
    block.setAttribute('data-code-block', '')
    const button = doc.createElement('button')
    button.type = 'button'
    button.title = copyLabel
    button.setAttribute('aria-label', copyLabel)
    button.setAttribute('data-code-copy', '')
    button.innerHTML = COPY_ICON + CHECK_ICON
    pre.replaceWith(block)
    block.append(button, pre)
    const code = pre.querySelector('code')
    if (code) highlightCode(doc, block, code)
  })
  return doc.body.innerHTML
}

export const addHeadingLinks = (html: string, linkLabel: string): string => {
  const doc = new DOMParser().parseFromString(html, 'text/html')
  doc.body.querySelectorAll('h1[id], h2[id], h3[id]').forEach((heading) => {
    const button = doc.createElement('button')
    button.type = 'button'
    button.title = linkLabel
    button.setAttribute('aria-label', linkLabel)
    button.setAttribute('data-heading-link', '')
    button.innerHTML = '<span data-icon="hash">#</span>' + CHECK_ICON
    heading.append(button)
  })
  return doc.body.innerHTML
}
