



  document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".menu-toggle"); 
  const sidebar = document.getElementById("sidebar");

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      sidebar.classList.toggle("-translate-x-full");
    });
  });
});



function openProjectModal(projectId) {
  const modal = document.getElementById('assignProjectModal');
  const projectData = document.getElementById(`project-data-${projectId}`);
  if (!projectData) return;

  // Populate text inputs and textareas
  const fields = projectData.querySelectorAll('input, textarea');
  fields.forEach(field => {
    const name = field.getAttribute('name');
    const modalField = modal.querySelector(`[name="${name}"]`);
    if (modalField) {
      if (modalField.tagName.toLowerCase() === 'textarea') {
        modalField.textContent = field.value || '';
      } else {
        modalField.value = field.value || '';
      }
    }
  });

  // Populate selects
  const selectNames = ['work_type','priority'];
  selectNames.forEach(name => {
    const hiddenField = projectData.querySelector(`[name="${name}"]`);
    const modalSelect = modal.querySelector(`[name="${name}"]`);
    if (hiddenField && modalSelect) {
      const optionExists = Array.from(modalSelect.options).some(o => o.value == hiddenField.value);
      if(optionExists) modalSelect.value = hiddenField.value;
    }
  });

  // File/Image previews
  const fileUrl = projectData.querySelector('[name="upload_file"]')?.value;
  const imageUrl = projectData.querySelector('[name="upload_image"]')?.value;

  const fileLink = modal.querySelector('#existing-file-link');
  const imagePreview = modal.querySelector('#existing-image-preview');

  if (fileLink) fileLink.href = fileUrl || '#';
  if (imagePreview) imagePreview.src = imageUrl || '';

  // Show modal
  modal.classList.remove('hidden');
}
