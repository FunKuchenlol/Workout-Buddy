document.addEventListener("DOMContentLoaded", () => {
    const addDropZone = document.getElementById("add-drop-zone");
    const addFileInput = document.getElementById("addFileUpload");
    const addPreviewImage = document.getElementById("add-preview-image");

        if (addDropZone && addFileInput && addPreviewImage) {
            addDropZone.addEventListener("click", () => addFileInput.click());
            addDropZone.addEventListener("dragover", (e) => { e.preventDefault(); addDropZone.classList.add("drag-over"); });
            addDropZone.addEventListener("dragleave", () => { addDropZone.classList.remove("drag-over"); });
            addDropZone.addEventListener("drop", (e) => {
                e.preventDefault();
                addDropZone.classList.remove("drag-over");
                const file = e.dataTransfer.files[0];
                addFileInput.files = e.dataTransfer.files;
                updatePreview(file, addPreviewImage);
            });
            addFileInput.addEventListener("change", () => {
                const file = addFileInput.files[0];
                updatePreview(file, addPreviewImage);
            });
        }

    function updatePreview(file, previewImgElement) {
        if (!file || !file.type.startsWith("image/")) {
            previewImgElement.src = "";
            previewImgElement.classList.remove('d-block');
            previewImgElement.classList.add('d-none');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            previewImgElement.src = e.target.result;
            previewImgElement.classList.remove('d-none');
            previewImgElement.classList.add('d-block');
        };
        reader.readAsDataURL(file);
    }
        
        }
);