    const sidebar = document.getElementById('sidebarMenu');
    const toggleBtn = document.getElementById('sidebarToggle');
    const navbar = document.getElementById('mainNavbar');

    // Toggle sidebar
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('translate-x-full');
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', (e) => {
      const isInsideSidebar = sidebar.contains(e.target);
      const isToggleBtn = toggleBtn.contains(e.target);
      if (!isInsideSidebar && !isToggleBtn && !sidebar.classList.contains('translate-x-full')) {
        sidebar.classList.add('translate-x-full');
      }
    });

    // Transparent navbar on scroll
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        navbar.classList.add('bg-black/30', 'backdrop-blur');
      } else {
        navbar.classList.remove('bg-black/30', 'backdrop-blur');
      }
    });








function openEditModal(id, name, type, category, description, deadline, notes, assignedTo) {
  document.getElementById("editModal").classList.remove("hidden");

  // Fill form
  document.getElementById("editProjectId").value = id;
  document.getElementById("editProjectName").value = name;
  document.getElementById("editProjectType").value = type;
  document.getElementById("editCategory").value = category;
  document.getElementById("editDescription").value = description;
  document.getElementById("editDeadline").value = deadline;
  document.getElementById("editNotes").value = notes;

  let assignedSelect = document.getElementById("editAssignedTo");
  for (let option of assignedSelect.options) {
    if (option.value == assignedTo) {
      option.selected = true;
    }
  }

  // Set form action dynamically
  document.getElementById("editForm").action = `/edit_assigned_project/${id}/`;
}

function closeEditModal() {
  document.getElementById("editModal").classList.add("hidden");
}

document.getElementById("editDepartment").addEventListener("change", function() {
    let deptId = this.value;
    let assignedToSelect = document.getElementById("editAssignedTo");
    assignedToSelect.innerHTML = "<option value=''>Loading...</option>";

    if (deptId) {
        fetch(`/ajax/get-team-members/?department_id=${deptId}`)
        .then(response => response.json())
        .then(data => {
            assignedToSelect.innerHTML = "";
            if (data.members.length > 0) {
                data.members.forEach(member => {
                    let opt = document.createElement("option");
                    opt.value = member.id;
                    opt.textContent = member.name;
                    assignedToSelect.appendChild(opt);
                });
            } else {
                assignedToSelect.innerHTML = "<option value=''>No members found</option>";
            }
        });
    } else {
        assignedToSelect.innerHTML = "<option value=''>Select department first</option>";
    }
});



function openDescriptionModal(description) {
    document.getElementById('descriptionContent').innerText = description;
    document.getElementById('descriptionModal').classList.remove('hidden');
    document.getElementById('descriptionModal').classList.add('flex');
  }

  function closeDescriptionModal() {
    document.getElementById('descriptionModal').classList.add('hidden');
    document.getElementById('descriptionModal').classList.remove('flex');
  }