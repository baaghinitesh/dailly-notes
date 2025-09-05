// Open java files in a new tab when clicked
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('a[href$=".java"]').forEach(link => {
        link.setAttribute('target', '_blank');
    });
});
