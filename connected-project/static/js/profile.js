// const input = document.getElementById('exampleFormControlFile1');
// const btn = document.querySelector('button');

// input.addEventListener('change', function() {
//   btn.innerHTML = input.files[0].name;
// });

// const input = document.getElementById('uploadFile');
// const label = document.querySelector('.custom-file-label');

// input.addEventListener('change', e => {
//   const fileName = e.target.files[0].name;
//   label.textContent = fileName;
// });

// const uploadBtn = document.getElementById('upload-btn');
// const uploadDropdown = document.getElementById('upload-dropdown');

// uploadBtn.addEventListener('click', () => {
//   uploadDropdown.classList.toggle('expanded');
// });

const likeButton = document.querySelector('.like-button');
likeButton.addEventListener('click', toggleLike);

function toggleLike() {
  likeButton.classList.toggle('liked');
}

