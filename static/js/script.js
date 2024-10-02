// This updates the avatar
const fileInput = document.querySelector('input[type="file"]');

fileInput.addEventListener('change', (event) => {
const file = event.target.files[0];
const image = document.querySelector('#avatar');

if (file && file.type.includes('image')) {
    const url = URL.createObjectURL(file);
    image.src = url;
}
});

// This updates the name
const display_nameInput = document.getElementById('id_displayname');
const display_nameOutput = document.getElementById('displayname');

display_nameInput.addEventListener('input', (event) => {
    display_nameOutput.innerText = event.target.value;
});