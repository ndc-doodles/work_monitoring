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
