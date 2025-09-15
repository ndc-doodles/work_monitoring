document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".menu-toggle"); 
  const sidebar = document.getElementById("sidebar");

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      sidebar.classList.toggle("-translate-x-full");
    });
  });
});








// admin side user details edit modal




function openAdminUserEditModal(button) {
  document.getElementById("edit_id").value = button.dataset.id;
  document.getElementById("edit_emp_id").value = button.dataset.empid;
  document.getElementById("edit_name").value = button.dataset.name;
  document.getElementById("edit_email").value = button.dataset.email;
  document.getElementById("edit_phone").value = button.dataset.phone;
  document.getElementById("edit_department").value = button.dataset.department;
  document.getElementById("edit_team").value = button.dataset.team;
  document.getElementById("edit_designation").value = button.dataset.designation;
  document.getElementById("edit_job_position").value = button.dataset.job_position; // fixed
  document.getElementById("edit_work_location").value = button.dataset.worklocation;
let joiningDate = button.dataset.joining;
  if (joiningDate) {
    let formatted = new Date(joiningDate).toISOString().split("T")[0];
    document.getElementById("edit_joining_date").value = formatted;
  } else {
    document.getElementById("edit_joining_date").value = "";
  }  document.getElementById("edit_username").value = button.dataset.username;
  document.getElementById("edit_status").value = button.dataset.status;

  let imgSrc = button.dataset.profile;
  document.getElementById("edit_profile_image").src = imgSrc ? imgSrc : "";

  document.getElementById("editModal").classList.remove("hidden");
}


function closeModal() {
  document.getElementById("editModal").classList.add("hidden");
}




const passwordInput = document.getElementById('password');
  const toggleBtn = document.getElementById('togglePassword');
  const eyeIcon = document.getElementById('eyeIcon');

  toggleBtn.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      // Replace with eye-off icon
      eyeIcon.innerHTML = `
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.964 9.964 0 012.489-4.043M6.62 6.62l10.76 10.76M12 5c4.477 0 8.268 2.943 9.542 7a9.964 9.964 0 01-1.536 2.823M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>`;
    } else {
      passwordInput.type = 'password';
      // Restore eye icon
      eyeIcon.innerHTML = `
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>`;
    }
  });