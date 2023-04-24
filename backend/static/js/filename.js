function handleInputFileChange(inputSelector, displaySelector) {
  $(inputSelector).change(function () {
    $(displaySelector).val($(this).val().replace('C:\\fakepath\\', ''))
  })
}

handleInputFileChange('.file_1', '#file_1')
handleInputFileChange('.file_2', '#file_2')
