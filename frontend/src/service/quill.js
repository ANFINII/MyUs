let editor = document.getElementById('comment_form_area');
let editorInput = document.getElementById('editor_input');
let quill = new Quill(editor, {
  modules: {
    toolbar: [
      [
        {'header': [1, 2, 3, 4, 5]},
        {'color': []}, {'background': []}, {'align': []},
        {'indent': '+1'}, {'indent': '-1'}, {'list': 'ordered'}, {'list': 'bullet'},
        'bold', 'underline', 'strike', 'formula', {'script': 'super'}, {'script': 'sub'},
        'code-block', 'blockquote', 'link', 'image',
      ],
    ]
  },
  placeholder: '',
  theme: 'snow'
});

quill.on('text-change', function() {
  let editorHtml = editor.querySelector('.ql-editor').innerHTML;
  const text = editorHtml.replace(/<p><br><\/p>/g, '')
  editorInput.value = editorHtml;
  if (!text || !text.match(/\S/g)) {
    // disabled属性を設定
    document.getElementById('comment_form_button').setAttribute('disabled', true);
  } else {
    // disabled属性を削除
    document.getElementById('comment_form_button').removeAttribute('disabled');
  }
  // ショートカット
  shortcut.add('Ctrl+Enter', function () {
    $('#comment_form_button').click();
  });
  shortcut.add('meta+Enter', function () {
    $('#comment_form_button').click();
  });
});


let replyEditor = document.getElementById('reply_form_area');
let replyEditorInput = document.getElementById('reply_editor_input');
let replyQuill = new Quill(replyEditor, {
  modules: {
    toolbar: [
      [
        {'header': [1, 2, 3, 4, 5]},
        {'color': []}, {'background': []}, {'align': []},
        {'indent': '+1'}, {'indent': '-1'}, {'list': 'ordered'}, {'list': 'bullet'},
        'bold', 'underline', 'strike', 'formula', {'script': 'super'}, {'script': 'sub'},
        'code-block', 'blockquote', 'link', 'image',
      ],
    ]
  },
  placeholder: '',
  theme: 'snow'
});


replyQuill.on('text-change', function() {
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
