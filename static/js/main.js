$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#mainListDiv").toggleClass("show_list");
    $("#mainListDiv").fadeIn();
});


// Photo Formset Management
const imageForm = document.getElementsByClassName("image-form");
const mainForm = document.querySelector("#post_form");
const addImageFormBtn = document.querySelector("#add-image-form");
// const submitFormBtn = document.querySelector('[type="submit"]');
const endOfForm = document.querySelector("#form-end-hidden")
const totalForms = document.querySelector("#id_post_photos-TOTAL_FORMS");

let formCount = imageForm.length - 1;

function updateForms() {
    let count = 0;
    for (let form of imageForm) {
        const formRegex = RegExp(`post_photos-(\\d){1}-`, 'g');
        form.innerHTML = form.innerHTML.replace(formRegex, `post_photos-${count++}-`)
    }
}

addImageFormBtn.addEventListener("click", function (event) {
    event.preventDefault();

    const newImageForm = imageForm[0].cloneNode(true);
    const formRegex = RegExp(`post_photos-(\\d){1}-`, 'g');

    formCount++;

    newImageForm.innerHTML = newImageForm.innerHTML.replace(formRegex, `post_photos-${formCount}-`);
    mainForm.insertBefore(newImageForm, endOfForm);
    totalForms.setAttribute('value', `${formCount + 1}`);
});

mainForm.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-image-form")) {
        event.preventDefault();
        event.target.parentElement.parentElement.parentElement.remove();
        formCount--;
        updateForms();
        totalForms.setAttribute('value', `${formCount + 1}`);
    }
});