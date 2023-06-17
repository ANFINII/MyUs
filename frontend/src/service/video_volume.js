$(function () {
  function getCookie() {
    let cookie = []
    if (document.cookie != '') {
      cookie_list = document.cookie.split(';')
      for (let item of cookie_list) {
        [key, value] = item.split('=')
        cookie[key.replace(' ', '')] = decodeURIComponent(value)
      }
    }
    return cookie
  }

  function saveCookie(_key, _value) {
    document.cookie = _key + '=' + encodeURIComponent(_value) + '; max-age=31536000; path=/'
  }

  $(document).ready(function () {
    cookie = getCookie()
    if (cookie['volume']) {
      $('#video_html5_api').get(0).volume = cookie['volume']
    }
  })

  $('#video_html5_api').on('volumechange', function () {
    saveCookie('volume', $('#video_html5_api').get(0).volume)
  })
})
