var quillChat = new Quill('#quill_chat', {
  modules: {
    toolbar: [
      ['bold', 'underline', 'strike'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      ['code-block', 'blockquote', 'link', 'image'],
    ]
  },
  placeholder: '',
  theme: 'snow'
});

// messageショートカット
quillChat.on('text-change', function() {
  // const text = editorHtml.replace(/<p><br><\/p>/g, '')
  const message = $('#text').val(quillChat.root.innerHTML);
  console.log(message)

  // focus時にそれ以外のtextareaを無効化する
  const targetElem = document.querySelectorAll('.form_button');
  const targetCount = targetElem.length;
  if (targetElem) {
    for (let i = 0; i < targetCount; i++)
      targetElem[i].setAttribute('disabled', true);
  }

  if (message) {
    // disabled属性を削除
    document.getElementById('message_form_button').removeAttribute('disabled');
  }

  $(document).on('input', message, function (event) {
    event.preventDefault();
    if (!message) {
      // disabled属性を設定
      document.getElementById('message_form_button').setAttribute('disabled', true);
    } else {
      // disabled属性を削除
      document.getElementById('message_form_button').removeAttribute('disabled');
      // ショートカット
      shortcut.add('Ctrl+Enter', function () {
        $('#message_form_button').click();
      });
      shortcut.add('meta+Enter', function () {
        $('#message_form_button').click();
      });
    }
  });
});


let replyEditorInput = document.getElementById('reply_editor_input');
let quillChatReply = new Quill('reply_form_area', {
  modules: {
    toolbar: [
      ['bold', 'underline', 'strike'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      ['code-block', 'blockquote', 'link', 'image'],
    ]
  },
  placeholder: '',
  theme: 'snow'
});

quillChatReply.on('text-change', function() {
  let editorHtml = editor.querySelector('.ql-editor').innerHTML;
  const text = editorHtml.replace(/<p><br><\/p>/g, '')
  replyEditorInput.value = editorHtml;
  if (!text || !text.match(/\S/g)) {
    // disabled属性を設定
    document.getElementById('reply_form_button').setAttribute('disabled', true);
  } else {
    // disabled属性を削除
    document.getElementById('reply_form_button').removeAttribute('disabled');
  }
  // ショートカット
  shortcut.add('Ctrl+Enter', function () {
    $('#reply_form_button').click();
  });
  shortcut.add('meta+Enter', function () {
    $('#reply_form_button').click();
  });
});
