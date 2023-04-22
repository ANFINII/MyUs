if (document.querySelector('.video') != null) {
  $('.video').hover(playVideo, hideVideo)
}

// ホバーすると再生開始
function playVideo(e) {
  $('video', this).get(0).play()
  const videos = document.querySelectorAll('video')
  for (const i = 0; i < videos.length; i++) {
    if (videos[i].closest('.video_auto')) {
      videos[i].playbackRate = 2.0
    }
  }
}

// ホバーアウトするとサムネイル表示
function hideVideo(e) {
  $('video', this).get(0).load()
}
