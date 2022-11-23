var quillBlog = new Quill('#quill_blog', {
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

quillBlog.on('text-change', function() {
  $('#delta').val(JSON.stringify(quillBlog.getContents()));
  $('#richtext').val(quillBlog.root.innerHTML);
});
