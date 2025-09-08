import { render, screen, RenderResult } from '@testing-library/react'
import { ErrorBoundary } from '.'

// 正常画面のコンポーネント
const NormalScreen = (): React.JSX.Element => <div>正常画面</div>

// エラー画面のコンポーネント
const ErrorScreen = <div>エラー画面</div>

// エラーを発生させるコンポーネント
const Bomb = (): React.JSX.Element => {
  throw new Error('Boom!')
}

describe('ErrorBoundary', (): void => {
  beforeEach((): void => {
    jest.spyOn(console, 'error').mockImplementation(jest.fn())
  })

  afterEach((): void => {
    jest.restoreAllMocks()
  })

  it('子コンポーネントを正常に表示する', (): void => {
    render(
      <ErrorBoundary>
        <NormalScreen />
      </ErrorBoundary>,
    )
    expect(screen.getByText('正常画面')).toBeTruthy()
  })

  it('エラー発生時に fallback UI が表示される', (): void => {
    render(
      <ErrorBoundary fallback={ErrorScreen}>
        <Bomb />
      </ErrorBoundary>,
    )
    expect(screen.getByText('エラー画面')).toBeTruthy()
  })

  it('resetKeys が変更されたらエラー状態をリセットする', (): void => {
    const { rerender }: RenderResult = render(
      <ErrorBoundary fallback={ErrorScreen} resetKeys={['a']}>
        <Bomb />
      </ErrorBoundary>,
    )
    expect(screen.getByText('エラー画面')).toBeTruthy()

    rerender(
      <ErrorBoundary fallback={ErrorScreen} resetKeys={['b']}>
        <NormalScreen />
      </ErrorBoundary>,
    )
    expect(screen.getByText('正常画面')).toBeTruthy()
  })
})
