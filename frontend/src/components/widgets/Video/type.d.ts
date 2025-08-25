import videojs from 'video.js'

export type Player = ReturnType<typeof videojs>
export type PlayerOptions = Parameters<typeof videojs>[1]
export type Component = ReturnType<typeof videojs.getComponent> & VideoJSComponent

export interface VideoJSComponent {
  el(): HTMLElement
  addClass(className: string): void
  removeClass(className: string): void
  on(event: string, handler: () => void): void
  show(): void
  hide(): void
}

export interface QualityLevel {
  enabled: boolean
  height: number
  width: number
  bitrate: number
}

export interface QualityLevels {
  length: number
  selectedIndex: number
  [index: number]: QualityLevel
  on(event: string, callback: () => void): void
}

export interface ExtendedPlayer extends Player {
  qualityLevels(): QualityLevels
  hlsQualitySelector(options?: { displayCurrentQuality?: boolean }): void
  controlBar: {
    addChild(name: string, options?: Record<string, unknown>): Component
    getChild(name: string): Component | undefined
  }
}
