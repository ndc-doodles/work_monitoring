



  document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".menu-toggle"); 
  const sidebar = document.getElementById("sidebar");

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      sidebar.classList.toggle("-translate-x-full");
    });
  });
});



function openProjectModal(button) {
    const modal = document.getElementById("assignProjectModal");
    modal.classList.remove("hidden");

    // Scope all selectors to modal only
    modal.querySelector("input[name='work_name']").value = button.dataset.work_name || "";
    modal.querySelector("input[name='work_type']").value = button.dataset.work_type || "";
    modal.querySelector("input[name='category']").value = button.dataset.category || "";
    modal.querySelector("textarea[name='description']").value = button.dataset.description || "";
    modal.querySelector("input[name='deadline']").value = button.dataset.deadline || "";
    modal.querySelector("textarea[name='additional_notes']").value = button.dataset.additional_notes || "";
    modal.querySelector("input[name='color_preference']").value = button.dataset.color_preference || "";
    modal.querySelector("input[name='priority']").value = button.dataset.priority || "";
    modal.querySelector("textarea[name='content_example']").value = button.dataset.content_example || "";

    // Handle multiple files
    let filesContainer = modal.querySelector("#existing-files-list");
    filesContainer.innerHTML = "";
    if (button.dataset.files) {
        let files = button.dataset.files.split(",");
        files.forEach(url => {
            if (url.trim() !== "") {
                let link = document.createElement("a");
                link.href = url;
                link.target = "_blank";
                link.className = "text-blue-400 hover:underline block";
                link.textContent = "📄 View File";
                filesContainer.appendChild(link);
            }
        });
    }

    // Handle multiple images
    let imagesContainer = modal.querySelector("#existing-images-list");
    imagesContainer.innerHTML = "";
    if (button.dataset.images) {
        let images = button.dataset.images.split(",");
        images.forEach(url => {
            if (url.trim() !== "") {
                let img = document.createElement("img");
                img.src = url;
                img.className = "w-32 h-32 object-cover rounded border";
                imagesContainer.appendChild(img);
            }
        });
    }
}

