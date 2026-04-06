type ClassValue = string | number | boolean | undefined | null | Record<string, boolean | undefined | null> | ClassValue[]

export default function cx(...args: ClassValue[]): string {
  let result = ''

  for (let i = 0; i < args.length; i++) {
    const arg = args[i]
    if (!arg) continue

    if (typeof arg === 'string') {
      result = result ? result + ' ' + arg : arg
    } else if (typeof arg === 'number') {
      result = result ? result + ' ' + arg : '' + arg
    } else if (Array.isArray(arg)) {
      const inner = cx(...arg)
      if (inner) result = result ? result + ' ' + inner : inner
    } else {
      for (const key in arg) {
        if (arg[key]) result = result ? result + ' ' + key : key
      }
    }
  }

  return result
}
