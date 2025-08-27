document.addEventListener("DOMContentLoaded", () => {
  const header = document.getElementById("mainHeader");
  const menuToggle = document.getElementById("menuToggle");
  const menuSidebar = document.getElementById("menuSidebar");
  const closeMenu = document.getElementById("closeMenu");

  // Scroll effect
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header.classList.add("bg-black/30", "backdrop-blur-md", "shadow-md");
    } else {
      header.classList.remove("bg-black/30", "backdrop-blur-md", "shadow-md");
    }
  });

  // Sidebar toggle
  menuToggle.addEventListener("click", () => {
    menuSidebar.classList.remove("translate-x-full");
    menuSidebar.classList.add("translate-x-0");
  });

  closeMenu.addEventListener("click", () => {
    menuSidebar.classList.add("translate-x-full");
    menuSidebar.classList.remove("translate-x-0");
  });

  // Close sidebar when clicking outside
  document.addEventListener("click", (e) => {
    if (!menuSidebar.contains(e.target) && !menuToggle.contains(e.target)) {
      menuSidebar.classList.add("translate-x-full");
      menuSidebar.classList.remove("translate-x-0");
    }
  });
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