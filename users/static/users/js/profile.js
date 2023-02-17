
function fillProfileFormInput() {
    let nameInput = document.getElementById("form-name");
    let surnameInput = document.getElementById("form-surname");
    let ageInput = document.getElementById("form-age");
    let githubInput = document.getElementById("form-github");

    nameInput.value = nameInput.dataset.value;
    surnameInput.value = surnameInput.dataset.value;
    ageInput.value = ageInput.dataset.value;
    githubInput.value = githubInput.dataset.value;

    alert("Profil bilgileri dolduruldu!");

}