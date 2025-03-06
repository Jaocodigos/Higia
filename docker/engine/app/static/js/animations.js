

// Left SideBar
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const menuToggle = document.querySelector('.menu-toggle');
const sidebarClose = document.getElementById('sidebar-close');

menuToggle.addEventListener('click', () => {
   sidebar.classList.toggle('-translate-x-full');
   sidebar.classList.toggle('z-50');
   menuToggle.classList.toggle('z-50');
   overlay.classList.toggle('block');
});



// Right SideBar
const secondSidebarToggle = document.getElementById('second-sidebar-toggle');
const secondSidebar = document.getElementById('second-sidebar');
const secondSidebarClose = document.getElementById('second-sidebar-close');

secondSidebarToggle.addEventListener('click', () => {
   secondSidebar.classList.toggle('translate-x-full');
   secondSidebar.classList.toggle('z-50');
   secondSidebarToggle.classList.toggle('z-50');
   overlay.classList.toggle('block');
});


// Sidebars Overlay
overlay.addEventListener('click', () => {

    if (sidebar.classList.contains('-translate-x-full')){
        secondSidebar.classList.toggle('translate-x-full');
        secondSidebar.classList.toggle('z-50');
        overlay.classList.toggle('block');
    }
    else if (secondSidebar.classList.contains('translate-x-full')){
        sidebar.classList.toggle('-translate-x-full');
        sidebar.classList.toggle('z-50');
        overlay.classList.toggle('block');
    }

});

// Close Sidebar Button
secondSidebarClose.addEventListener('click', () => {
    secondSidebar.classList.toggle('translate-x-full');
    overlay.classList.toggle('block');
    secondSidebar.classList.toggle('z-50');
    secondSidebarToggle.classList.toggle('z-50');
});

// Close Sidebar Button
sidebarClose.addEventListener('click', () => {
    sidebar.classList.toggle('-translate-x-full');
    sidebar.classList.toggle('z-50');
    menuToggle.classList.toggle('z-50');
    overlay.classList.toggle('block');
});
