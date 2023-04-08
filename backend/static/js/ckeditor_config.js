CKEDITOR.on('dialogDefinition', function (ev) {
  let dialogName = ev.data.name
  let dialogDefinition = ev.data.definition

  if (dialogName === 'link') {
    var infoTab = dialogDefinition.getContents('info')
    if (infoTab) {
      var urlField = infoTab.get('url')
      urlField['default'] = 'www.example.com'
    }

    if (dialogDefinition.getContents('advanced')) dialogDefinition.removeContents('advanced')
  }

  if (dialogName === 'image') {
    var uploadTab = dialogDefinition.getContents('Upload')
    if (uploadTab) {
      var upload = uploadTab.get('upload')
      if (upload) upload.label = '画像を選択してください'

      var uploadButton = uploadTab.get('uploadButton')
      if (uploadButton) uploadButton.label = 'アップロード'
    }

    var infoTab = dialogDefinition.getContents('info')
    if (infoTab) {
      infoTab.remove('txtAlt')
      infoTab.get('txtUrl')['hidden'] = true
      infoTab.remove('txtHSpace')
      infoTab.remove('txtVSpace')
      infoTab.remove('txtBorder')
      infoTab.remove('cmbAlign')

      var browse = infoTab.get('browse')
      if (browse) browse.label = 'アップロード済みの画像を選択'
    }
    // remove unnecessary tabs
    if (dialogDefinition.getContents('Link')) dialogDefinition.removeContents('Link')
    if (dialogDefinition.getContents('advanced')) dialogDefinition.removeContents('advanced')
  }

  CKEDITOR.editorConfig = function (config) {
    // 画像のサイズ指定をstyleタグではなく，width,height属性で設定
    config.disallowedContent = 'img{width,height}'
    config.extraAllowedContent = 'img[width,height]'
  }

  const editor = ev.editor
  editor.on('fileUploadRequest', function (ev) {
    const fileLoader = ev.data.fileLoader
    // Notificationsをbindすることでメインの編集画面に通知が出るが、今回は別Dialogなのであまり意味がない。
    // CKEDITOR.fileTools.bindNotifications(fileLoader.editor, fileLoader)

    fileLoader.on("uploading", function () {
      console.log("アップロード開始")
    })

    fileLoader.on("uploaded", function () {
      console.log("アップロード完了")
    })

    fileLoader.on("error", function () {
      console.log("アップロードエラー")
    })

    fileLoader.on("abort", function () {
      console.log("アップロード失敗")
    })
  })
})
