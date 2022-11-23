var quill_blog = new Quill('#quill_blog', {
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

quill_blog.on('text-change', function() {
  $('#delta').val(JSON.stringify(quill_blog.getContents()));
  $('#richtext').val(quill_blog.root.innerHTML);
});
