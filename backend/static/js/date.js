const time = new Date();
const year = time.getFullYear();

for (let i = year; i >= 1900; i--) {
  createOptionElements(i, 'year');
}

for (let i = 1; i <= 12; i++) {
  createOptionElements(i, 'month');
}

for (let i = 1; i <= 31; i++) {
  createOptionElements(i, 'day');
}

function createOptionElements(num, parentId) {
  const doc = document.createElement('option');
  doc.value = doc.innerHTML = num;
  document.getElementById(parentId).appendChild(doc);
}
