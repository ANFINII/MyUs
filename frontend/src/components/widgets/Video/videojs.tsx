import { useRef, useEffect, useState } from 'react'
import videojs from 'video.js'
import { PLAYBACK_RATES, MENU_DELAY_MS, SPEED_MENU, QUALITY_MENU, STANDARD_SPEED, MENU_UPDATE_DELAY_MS, AUTO_QUALITY } from './constants'
import { PlayerOptions, Player, ExtendedPlayer, Component } from './type'
import 'videojs-contrib-quality-levels'
import 'videojs-hls-quality-selector'

interface Props {
  options: PlayerOptions
  onReady?: (player: Player) => void
}

export default function VideoJS(props: Props): React.JSX.Element {
  const { options, onReady } = props

  const videoRef = useRef<HTMLDivElement>(null)
  const playerRef = useRef<Player | null>(null)
  const [settingsMenu, setSettingsMenu] = useState<boolean>(false)

  useEffect(() => {
    // Video.jsプレーヤーが一度だけ初期化されることを確認
    // React 18 Strict ModeのためにVideo.jsプレーヤーはコンポーネントelの内部に必要
    if (!playerRef.current && videoRef.current) {
      const videoElement = document.createElement('video-js')
      videoElement.classList.add('vjs-big-play-centered')
      videoRef.current.appendChild(videoElement)

      // オプションが適切な構造を持つことを確認
      const playerOptions = { controls: true, fluid: true, ...options }
      if ('src' in playerOptions && !playerOptions.sources) {
        const src = playerOptions.src as string
        playerOptions.sources = [
          {
            src,
            type: src.includes('.m3u8') ? 'application/x-mpegURL' : 'video/mp4',
          },
        ]
        delete (playerOptions as Record<string, unknown>).src
      }

      const player = (playerRef.current = videojs(videoElement, playerOptions, () => {
        const extendedPlayer = player as unknown as ExtendedPlayer
        const playerWithOptions = player as unknown as { options_: { playbackRates?: number[] } }
        playerWithOptions.options_.playbackRates = PLAYBACK_RATES
        extendedPlayer.hlsQualitySelector({ displayCurrentQuality: false })
        setTimeout(() => {
          if (!settingsMenu) {
            createSettingsMenu(player as unknown as ExtendedPlayer)
            setSettingsMenu(true)
          }
        }, MENU_DELAY_MS)
        onReady?.(player)
      }))

      // prop変更時に既存のプレーヤーを更新
    } else if (playerRef.current) {
      const player = playerRef.current
      if (options.autoplay !== undefined) player.autoplay(options.autoplay)
      if (options.sources) player.src(options.sources)
    }
  }, [options, onReady, settingsMenu])

  // カスタム設定メニューを作成する関数
  const createSettingsMenu = (player: ExtendedPlayer): void => {
    const controlBar = player.controlBar
    const playerEl = player.el()

    // 既存の品質セレクターと再生速度ボタンを非表示
    const hideElement = (selector: string): void => {
      const element = playerEl.querySelector(selector) as HTMLElement | null
      if (element) {
        element.style.display = 'none'
      }
    }

    hideElement('.vjs-quality-selector')
    hideElement('.vjs-playback-rate')
    const Button = videojs.getComponent('Button')
    const Menu = videojs.getComponent('Menu')
    const Component = videojs.getComponent('Component')
    if (!Button || !Menu || !Component) {
      return
    }

    // 設定メニューボタンクラス
    class SettingsButton extends (Button as unknown as new (player: Player, options?: Record<string, unknown>) => Component) {
      constructor(player: Player, options?: Record<string, unknown>) {
        super(player, options)
        const thisComponent = this as unknown as Component & { controlText: (text: string) => void }
        thisComponent.controlText('Settings')
        const thisAsComponent = this as unknown as Component
        thisAsComponent.addClass('vjs-settings-button')

        // ギアアイコンを設定
        const buttonEl = (this as unknown as Component).el()
        const iconPlaceholder = buttonEl.querySelector('.vjs-icon-placeholder')
        if (iconPlaceholder) {
          iconPlaceholder.className = 'vjs-icon-placeholder vjs-icon-cog'
        }
      }

      handleClick(): void {
        const playerEl = (this as unknown as { player: () => Player }).player().el()
        const mainMenu = playerEl.querySelector('.vjs-settings-menu')
        const submenus = playerEl.querySelectorAll('.vjs-speed-submenu, .vjs-quality-submenu')
        const isSubmenuOpen = Array.from(submenus).some((submenu) => !submenu.classList.contains('vjs-hidden'))
        if (isSubmenuOpen) {
          submenus.forEach((submenu) => submenu.classList.add('vjs-hidden'))
          if (mainMenu) mainMenu.classList.add('vjs-hidden')
        } else {
          if (mainMenu) mainMenu.classList.toggle('vjs-hidden')
        }
      }
    }

    // メインメニューを作成
    const createMainMenu = (): HTMLElement => {
      const menuEl = document.createElement('div')
      menuEl.className = 'vjs-settings-menu vjs-hidden'
      const menuContent = document.createElement('div')
      menuContent.className = 'vjs-settings-menu-content'

      // 再生速度メニューアイテム
      const speedItem = createMenuItem(SPEED_MENU, getCurrentSpeedLabel(), () => showSubmenu('speed'))
      menuContent.appendChild(speedItem)

      // 画質メニューアイテム
      const qualityItem = createMenuItem(QUALITY_MENU, getCurrentQualityLabel(), () => showSubmenu('quality'))
      menuContent.appendChild(qualityItem)
      menuEl.appendChild(menuContent)
      return menuEl
    }

    // サブメニューを作成
    const createSubmenu = (type: 'speed' | 'quality'): HTMLElement => {
      const submenuEl = document.createElement('div')
      submenuEl.className = `vjs-${type}-submenu vjs-hidden`
      submenuEl.dataset.type = type
      const submenuContent = document.createElement('div')
      submenuContent.className = 'vjs-settings-menu-content'
      const backItem = document.createElement('div')
      backItem.className = 'vjs-settings-menu-item vjs-back-button'
      backItem.innerHTML = '<span class="vjs-back-arrow">←</span>戻る'
      backItem.addEventListener('click', () => hideSubmenu(type))
      submenuContent.appendChild(backItem)

      if (type === 'speed') {
        const currentSpeed = player.playbackRate()
        PLAYBACK_RATES.forEach((speed) => {
          const item = document.createElement('div')
          item.className = 'vjs-settings-menu-item'
          const label = speed === 1 ? STANDARD_SPEED : `${speed}`
          item.innerHTML = `<span class="vjs-menu-label">${label}</span>`
          item.dataset.speed = String(speed)

          if (currentSpeed === speed) {
            item.innerHTML += '<span class="vjs-menu-checkmark">✓</span>'
          }

          item.addEventListener('click', () => {
            player.playbackRate(speed)
            setTimeout(() => {
              updateSubmenuSelection(type)
              updateMainMenuLabel()
            }, MENU_UPDATE_DELAY_MS)
            hideSubmenu(type)
          })
          submenuContent.appendChild(item)
        })
      } else if (type === 'quality') {
        const qualityLevels = player.qualityLevels()
        const isAuto = Array.from({ length: qualityLevels.length }).every((_, i) => {
          const level = qualityLevels[i]
          return level ? level.enabled : true
        })

        // 各解像度オプション
        const qualityOptions: Array<{ height: number; index: number }> = []
        for (let i = 0; i < qualityLevels.length; i++) {
          const level = qualityLevels[i]
          if (level && level.height) {
            if (!qualityOptions.find((opt) => opt.height === level.height)) {
              qualityOptions.push({ height: level.height, index: i })
            }
          }
        }

        // 高画質から低画質の順にソート
        qualityOptions.sort((a, b) => b.height - a.height)
        qualityOptions.forEach((option) => {
          const item = document.createElement('div')
          item.className = 'vjs-settings-menu-item'
          item.innerHTML = `<span class="vjs-menu-label">${option.height}p</span>`
          const level = qualityLevels[option.index]
          if (level && level.enabled && !isAuto) {
            item.innerHTML += '<span class="vjs-menu-checkmark">✓</span>'
          }
          item.addEventListener('click', () => {
            for (let i = 0; i < qualityLevels.length; i++) {
              const level = qualityLevels[i]
              if (level) {
                level.enabled = level.height === option.height
              }
            }
            updateSubmenuSelection(type)
            updateMainMenuLabel()
            hideSubmenu(type)
          })
          submenuContent.appendChild(item)
        })

        // Auto オプションを一番下に追加
        const autoItem = document.createElement('div')
        autoItem.className = 'vjs-settings-menu-item'
        autoItem.innerHTML = `<span class="vjs-menu-label">${AUTO_QUALITY}</span>`

        if (isAuto) {
          autoItem.innerHTML += '<span class="vjs-menu-checkmark">✓</span>'
        }

        autoItem.addEventListener('click', () => {
          for (let i = 0; i < qualityLevels.length; i++) {
            const level = qualityLevels[i]
            if (level) level.enabled = true
          }
          updateSubmenuSelection(type)
          updateMainMenuLabel()
          hideSubmenu(type)
        })
        submenuContent.appendChild(autoItem)
      }
      submenuEl.appendChild(submenuContent)
      return submenuEl
    }

    // メニューアイテムを作成
    const createMenuItem = (label: string, value: string, onClick: () => void): HTMLElement => {
      const item = document.createElement('div')
      item.className = 'vjs-settings-menu-item'
      item.innerHTML = `<span class="vjs-menu-label">${label}</span><span class="vjs-menu-value">${value}</span>`
      item.addEventListener('click', onClick)
      return item
    }

    // 現在の速度ラベルを取得
    const getCurrentSpeedLabel = (): string => {
      const speed = player.playbackRate()
      return speed === 1 ? STANDARD_SPEED : `${speed}`
    }

    // 現在の画質ラベルを取得
    const getCurrentQualityLabel = (): string => {
      const qualityLevels = player.qualityLevels()
      const enabledLevels: number[] = []
      for (let i = 0; i < qualityLevels.length; i++) {
        const level = qualityLevels[i]
        if (level && level.enabled) {
          enabledLevels.push(level.height)
        }
      }
      if (enabledLevels.length === qualityLevels.length || enabledLevels.length === 0) {
        return AUTO_QUALITY
      }
      const maxHeight = Math.max(...enabledLevels)
      return `${maxHeight}p`
    }

    // メニューの表示切り替えヘルパー
    const toggleMenuVisibility = (element: Element | null, show: boolean): void => {
      if (!element) return
      if (show) {
        element.classList.remove('vjs-hidden')
      } else {
        element.classList.add('vjs-hidden')
      }
    }

    // サブメニューを表示
    const showSubmenu = (type: 'speed' | 'quality'): void => {
      const mainMenu = playerEl.querySelector('.vjs-settings-menu')
      const submenu = playerEl.querySelector(`[data-type="${type}"]`)
      toggleMenuVisibility(mainMenu, false)
      toggleMenuVisibility(submenu, true)
    }

    // サブメニューを非表示
    const hideSubmenu = (type: 'speed' | 'quality'): void => {
      const mainMenu = playerEl.querySelector('.vjs-settings-menu')
      const submenu = playerEl.querySelector(`[data-type="${type}"]`)
      toggleMenuVisibility(submenu, false)
      toggleMenuVisibility(mainMenu, true)
    }

    // サブメニューの選択状態を更新
    const updateSubmenuSelection = (type: 'speed' | 'quality'): void => {
      const submenu = playerEl.querySelector(`[data-type="${type}"]`)
      if (!submenu) return
      const items = submenu.querySelectorAll('.vjs-settings-menu-item')
      const clearCheckmarks = (): void => {
        items.forEach((item, index) => {
          if (index === 0) return
          const itemEl = item as HTMLElement
          const lastSpan = itemEl.querySelector('.vjs-menu-checkmark')
          if (lastSpan) lastSpan.remove()
        })
      }
      clearCheckmarks()

      if (type === 'speed') {
        const currentSpeed = player.playbackRate()
        items.forEach((item, index) => {
          if (index === 0) return
          const itemEl = item as HTMLElement
          const storedSpeed = parseFloat(itemEl.dataset.speed || '0')
          if (storedSpeed === currentSpeed) {
            const checkmark = document.createElement('span')
            checkmark.className = 'vjs-menu-checkmark'
            checkmark.textContent = '✓'
            itemEl.appendChild(checkmark)
          }
        })
      }
    }

    // メインメニューのラベルを更新
    const updateMainMenuLabel = (): void => {
      const mainMenu = playerEl.querySelector('.vjs-settings-menu')
      if (!mainMenu) return
      const updateMenuItem = (labelText: string, newValue: string): void => {
        const items = mainMenu.querySelectorAll('.vjs-settings-menu-item')
        items.forEach((item) => {
          const itemEl = item as HTMLElement
          const labelSpan = itemEl.querySelector('.vjs-menu-label')
          const valueSpan = itemEl.querySelector('.vjs-menu-value')
          if (labelSpan?.textContent === labelText && valueSpan) {
            valueSpan.textContent = newValue
          }
        })
      }
      updateMenuItem(SPEED_MENU, getCurrentSpeedLabel())
      updateMenuItem(QUALITY_MENU, getCurrentQualityLabel())
    }

    // コンポーネントを登録
    videojs.registerComponent('SettingsButton', SettingsButton as unknown as ReturnType<typeof videojs.getComponent>)
    const settingsButton = controlBar.addChild('SettingsButton', {})

    // メニューを追加
    const menus = [createMainMenu(), createSubmenu('speed'), createSubmenu('quality')]
    menus.forEach((menu) => playerEl.appendChild(menu))

    // フルスクリーンボタンの前に配置
    const fullscreenToggle = controlBar.getChild('fullscreenToggle') as Component | undefined
    if (fullscreenToggle) {
      const fullscreenEl = fullscreenToggle.el()
      const settingsEl = (settingsButton as Component).el()
      if (fullscreenEl && fullscreenEl.parentNode && settingsEl) {
        fullscreenEl.parentNode.insertBefore(settingsEl, fullscreenEl)
      }
    }

    // クリック外側でメニューを閉じる
    const handleOutsideClick = (e: MouseEvent): void => {
      const target = e.target as HTMLElement
      const settingsBtn = playerEl.querySelector('.vjs-settings-button')
      const menus = playerEl.querySelectorAll('.vjs-settings-menu, .vjs-speed-submenu, .vjs-quality-submenu')
      const isClickInside = (settingsBtn && settingsBtn.contains(target)) || Array.from(menus).some((menu) => menu.contains(target))
      if (!isClickInside) {
        menus.forEach((menu) => menu.classList.add('vjs-hidden'))
      }
    }
    document.addEventListener('click', handleOutsideClick)
  }

  // 関数コンポーネントのアンマウント時にVideo.jsプレーヤーを破棄
  useEffect(() => {
    const player = playerRef.current
    return () => {
      if (player && !player.isDisposed()) {
        player.dispose()
        playerRef.current = null
      }
    }
  }, [])

  return (
    <div data-vjs-player>
      <div ref={videoRef} />
    </div>
  )
}
