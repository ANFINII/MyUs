function handleInputFileChange(inputSelector, displaySelector) {
  $(inputSelector).change(function () {
    const fileNames = []
    for (let i = 0; i < this.files.length; i++) {
      fileNames.push(this.files[i].name)
    }
    $(displaySelector).val(fileNames.join(', '))
  })
}

handleInputFileChange('.file_1', '#file_1');
handleInputFileChange('.file_2', '#file_2');
