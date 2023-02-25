function handleSearchtag() {
  const searchtag_n = document.querySelector('.searchtag_n')
  const searchtag_1 = document.querySelector('.searchtag_1')
  const searchtag_2 = document.querySelector('.searchtag_2')
  const searchtag_3 = document.querySelector('.searchtag_3')
  const searchtag_4 = document.querySelector('.searchtag_4')
  if (searchtag_n.classList.contains('active')) {
    searchtag_n.classList.remove('active')
    searchtag_1.classList.remove('active')
    searchtag_2.classList.remove('active')
    searchtag_3.classList.remove('active')
    searchtag_4.classList.remove('active')
  } else {
    searchtag_n.classList.add("active")
    searchtag_1.classList.add("active")
    searchtag_2.classList.add("active")
    searchtag_3.classList.add("active")
    searchtag_4.classList.add("active")
  }
}
