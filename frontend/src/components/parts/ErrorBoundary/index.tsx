/* eslint-disable no-console */
import { Component, ErrorInfo, ReactNode } from 'react'
import { ENV } from 'lib/config'

interface ErrorBoundaryProps {
  fallback?: ReactNode
  resetKeys?: string[]
  children: ReactNode
}

interface ErrorBoundaryState {
  hasError: boolean
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    logErrorToMyService(error, errorInfo)
  }

  componentDidUpdate(prev: ErrorBoundaryProps): void {
    const prevKeys = prev.resetKeys || []
    const currentKeys = this.props.resetKeys || []
    const isDiffLength = prevKeys.length !== currentKeys.length
    const isDiffKeys = JSON.stringify(prevKeys) !== JSON.stringify(currentKeys)
    const isChanged = isDiffLength || isDiffKeys
    if (isChanged && this.state.hasError) {
      this.setState({ hasError: false })
    }
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return this.props.fallback
    }
    return this.props.children
  }
}

const logErrorToMyService = (error: Error, errorInfo: ErrorInfo): void => {
  if (ENV === 'http://127.0.0.1') {
    console.group()
    console.log('%c========== Error Boundary Start ==========', 'color: red;')
    console.error(error, errorInfo)
    console.log('%c========== Error Boundary End ==========', 'color: red;')
    console.groupEnd()
  }
}
