(function ($) {
  var player = videojs('video')
  var status = {
    current: 'buffering',
    oldstate: 'none'
  }

  player.on(['play', 'pause'], function (e) {
    GetPlayerStatus()
    /* 一番最初の再生は buffering => play のステータス変化から判定する */
    if (status.current == 'play' && status.oldstate == 'buffering') {
      /* 5秒後にスキップボタンを表示 */
      $.wait(5000).done(function () {
        $('.skip').css('display', 'block')
      })
    }
  })

  /* スキップボタンが押された時の処理 */
  $('.skip').on('click', function (e) {
    $('.skip').css('display', 'none')
    player.paused()
    player.src({ type: 'application/x-mpegURL', src: 'video.m3u8' })
    player.load()
    player.play()
  })

  /* プロモーション動画が再生終了した時の処理 */
  player.on('ended', function () {
    var promotion = player.currentSrc().match(/promotion\.mp4/)
    if (promotion != null) {
      $('.skip').css('display', 'none')
      player.src({ type: 'application/x-mpegURL', src: 'video.m3u8' })
      player.play()
    }
  })

  $.wait = function (msec) {
    var d = new $.Deferred
    setTimeout(function () { d.resolve(msec) }, msec)
    return d.promise()
  }

  function GetPlayerStatus() {
    var is = {
      Play: !player.paused(),
      Paused: player.paused(),
      Seeking: player.seeking()
    }
    status.oldstate = status.current
    if (is.Seeking) {
      status.current = 'seeking'
    } else if (is.Play) {
      status.current = 'play'
    } else if (is.Paused) {
      status.current = 'paused'
    } else {
      status.current = 'unknown'
    }
    return
  }
})(jQuery)
