const form = document.getElementById("edit-profile-form");

form.addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(form);
    fetch("{% url 'edit_profile' %}", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Profile updated successfully!");
        } else {
            alert("An error occurred while updating your profile.");
        }
    })
    .catch(error => {
        console.log(error);
        alert("An error occurred while updating your profile.");
    });
});
