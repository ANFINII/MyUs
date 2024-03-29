// textareaのdisabled判定

// 検索タグショートカット
$(document).on('focus', '.searchtag_3', function (event) {
  event.preventDefault()

  // focus時にそれ以外のtextareaを無効化する
  const targetElem = document.querySelectorAll('.form_button')
  const targetCount = targetElem.length
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].setAttribute('disabled', true)
  }

  const text = $(this).val()
  if (text || text.match(/\S/g)) {
    // disabled属性を削除
    document.querySelector('.searchtag_2').removeAttribute('disabled')
  }

  $(document).on('input', '.searchtag_3', function (event) {
    event.preventDefault()
    const text = $(this).val()
    if (!text || !text.match(/\S/g)) {
      // disabled属性を設定
      document.querySelector('.searchtag_2').setAttribute('disabled', true)
    } else {
      // disabled属性を削除
      document.querySelector('.searchtag_2').removeAttribute('disabled')

      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('.searchtag_2').click()
      })
      shortcut.add('meta+Enter', function () {
        $('.searchtag_2').click()
      })
    }
  })
})


// commentショートカット
$(document).on('focus', '#comment_area', function (event) {
  event.preventDefault()

  // focus時にそれ以外のtextareaを無効化する
  const targetElem = document.querySelectorAll('.form_button')
  const targetCount = targetElem.length
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].setAttribute('disabled', true)
  }

  const text = $(this).val()
  if (text || text.match(/\S/g)) {
    // disabled属性を削除
    document.getElementById('comment_button').removeAttribute('disabled')
  }

  $(document).on('input', '#comment_area', function (event) {
    event.preventDefault()
    const text = $(this).val()
    if (!text || !text.match(/\S/g)) {
      // disabled属性を設定
      document.getElementById('comment_button').setAttribute('disabled', true)
    } else {
      // disabled属性を削除
      document.getElementById('comment_button').removeAttribute('disabled')

      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#comment_button').click()
      })
      shortcut.add('meta+Enter', function () {
        $('#comment_button').click()
      })
    }
  })
})


// updateショートカット
$(document).on('focus', '.update_area', function (event) {
  event.preventDefault()
  const commentId = $(this).closest('form').attr('comment-id')

  // focus時にそれ以外のtextareaを無効化する
  const targetElem = document.querySelectorAll('.form_button')
  const targetCount = targetElem.length
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].setAttribute('disabled', true)
  }

  const text = $(this).val()
  if (text || text.match(/\S/g)) {
    // disabled属性を削除
    document.getElementById('update_button_' + commentId).removeAttribute('disabled')
  }

  // ショートカット
  shortcut.add('Ctrl+Enter', function () {
    $('#update_button_' + commentId).click()
  })
  shortcut.add('meta+Enter', function () {
    $('#update_button_' + commentId).click()
  })

  $(document).on('input', '#comment_update_' + commentId, function (event) {
    event.preventDefault()
    const text = $(this).val()
    if (!text || !text.match(/\S/g)) {
      // disabled属性を設定
      document.getElementById('update_button_' + commentId).setAttribute('disabled', true)
    } else {
      // disabled属性を削除
      document.getElementById('update_button_' + commentId).removeAttribute('disabled')

      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#update_button_' + commentId).click()
      })
      shortcut.add('meta+Enter', function () {
        $('#update_button_' + commentId).click()
      })
    }
  })
})
