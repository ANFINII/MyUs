import { camelSnake, snakeCamel } from './convertCase'

describe('camelSnake', (): void => {
  it('ネストしたオブジェクトと配列のキーを snake_case に変換する', (): void => {
    const input = { channelUlid: 'a', mediaUser: { isLike: true }, hashtags: [{ jpName: 'x' }], tags: ['fooBar'] }
    expect(camelSnake(input)).toEqual({ channel_ulid: 'a', media_user: { is_like: true }, hashtags: [{ jp_name: 'x' }], tags: ['fooBar'] })
  })

  it('File と null はそのまま残す', (): void => {
    const file = new File(['x'], 'a.png')
    const result = camelSnake({ imageFile: file, deletedAt: null }) as Record<string, unknown>
    expect(result.image_file).toBe(file)
    expect(result.deleted_at).toBeNull()
  })
})

describe('snakeCamel', (): void => {
  it('ネストしたオブジェクトと配列のキーを camelCase に変換する', (): void => {
    const input = { items: [{ media_user: { is_like: false } }], total: 2, channel_ulid: 'b' }
    expect(snakeCamel(input)).toEqual({ items: [{ mediaUser: { isLike: false } }], total: 2, channelUlid: 'b' })
  })

  it('プリミティブ値と null はそのまま返す', (): void => {
    expect(snakeCamel('text')).toBe('text')
    expect(snakeCamel(1)).toBe(1)
    expect(snakeCamel(null)).toBeNull()
  })
})
