var quill = new Quill('#quill_blog', {
  modules: {
    toolbar: [
      [{'header': [1, 2, 3, 4, 5]}, {'font': []}],
      [{'color': []}, {'background': []}, {'align': []}],
      [{'indent': '+1'}, {'indent': '-1'}, {'list': 'ordered'}, {'list': 'bullet'}],
      ['bold', 'underline', 'strike', 'formula', {'script': 'super'}, {'script': 'sub'}],
      ['code-block', 'blockquote', 'link', 'image'],
    ]
  },
  syntax: true,
  placeholder: '',
  theme: 'snow'
});

quill.on('text-change', function() {
  $('#delta').val(JSON.stringify(quill.getContents()));
  $('#richtext').val(quill.root.innerHTML);
});
