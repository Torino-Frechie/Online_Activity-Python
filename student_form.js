document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.editBtn');
    const form = document.getElementById('studentForm');
    const idnoField = document.getElementById('idno');
    const lastnameField = document.getElementById('lastname');
    const firstnameField = document.getElementById('firstname');
    const courseField = document.getElementById('course');
    const levelField = document.getElementById('level');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');

    // Get references for image functionality
    const imagePicker = document.getElementById('imagePicker');
    // const imageLogo = document.getElementById('imagePickerLogo'); // <-- Remove or comment this
    const studentImage = document.getElementById('studentImage');

    // --- 1. EDIT BUTTON LOGIC ---
    editButtons.forEach(button => {
        button.addEventListener('click', function(e){
            e.preventDefault();
            idnoField.value = this.dataset.idno;
            idnoField.disabled = true;
            lastnameField.value = this.dataset.lastname;
            firstnameField.value = this.dataset.firstname;
            courseField.value = this.dataset.course;
            levelField.value = this.dataset.level;
            
            // Set form action for update
            form.action = "/update_student/" + this.dataset.idno; 

            // Update profile image preview
            // Use the student's image if available, otherwise use default
            const imageUrl = this.dataset.image 
                             ? "/static/images/" + this.dataset.image 
                             : "/static/images/default.png";
            studentImage.src = imageUrl;

            submitBtn.value = "UPDATE";
        });
    });

    // --- 2. CANCEL BUTTON LOGIC ---
    if(cancelBtn){
        cancelBtn.addEventListener('click', function(){
            form.action = "/add_student";
            submitBtn.value = "SAVE";
            idnoField.disabled = false;
            form.reset();

            // Reset image preview to default.png
            studentImage.src = "/static/images/default.png";
        });
    }

    // --- 3. IMAGE PICKER FUNCTIONALITY (Modified) ---
    // Make the profile image itself clickable
    studentImage.addEventListener('click', function(){
        imagePicker.click();
    });

    // Handle file selection and display preview
    imagePicker.addEventListener('change', function(){
        if(this.files && this.files[0]){
            const reader = new FileReader();
            reader.onload = function(e){
                studentImage.src = e.target.result; // preview the selected image
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
});