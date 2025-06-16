// Dein JavaScript bleibt größtenteils gleich, es ist schon gut so!
document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-upload");
    const previewImage = document.getElementById("preview-image");

    if (!dropZone || !fileInput || !previewImage) return;

    const updatePreview = (file) => {
        if (!file || !file.type.startsWith("image/")) {
            previewImage.style.display = "none"; // Hide preview if no file or not an image
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    };

    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("drag-over");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("drag-over");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("drag-over");
        const file = e.dataTransfer.files[0];
        // Das ist der wichtige Teil: Die Datei wird dem fileInput zugewiesen
        // und somit beim Formular-Submit mitgesendet.
        fileInput.files = e.dataTransfer.files;
        updatePreview(file);
    });

    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        updatePreview(file);
    });
});