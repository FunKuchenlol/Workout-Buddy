document.addEventListener("DOMContentLoaded", () => {
    const editDeviceModal = document.getElementById('editDeviceModal');
    const editDropZone = document.getElementById("edit-drop-zone");
    const editFileInput = document.getElementById("editFileUpload");
    const editPreviewImage = document.getElementById("edit-preview-image");
    const editDeviceForm = document.getElementById("editDeviceForm");

    editDeviceModal.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget; 
        const deviceId = button.getAttribute('data-device-id');
        const deviceName = button.getAttribute('data-device-name');
        const deviceRepetitions = button.getAttribute('data-device-repetitions');
        const deviceBreakTime = button.getAttribute('data-device-breaktime');
        const deviceSets = button.getAttribute('data-device-sets');
        const deviceWeight = button.getAttribute('data-device-weight');
        const devicePicture = button.getAttribute('data-device-picture');

        document.getElementById('editDeviceId').value = deviceId;
        document.getElementById('editName').value = deviceName;
        document.getElementById('editRepetitions').value = deviceRepetitions;
        document.getElementById('editBreakTime').value = deviceBreakTime;
        document.getElementById('editSets').value = deviceSets;
        document.getElementById('editWeight').value = deviceWeight;

        if (devicePicture && devicePicture !== 'None') { 
            editPreviewImage.src = devicePicture;
            editPreviewImage.classList.remove('d-none');
            editPreviewImage.classList.add('d-block');
        } else {
            editPreviewImage.src = "";
            editPreviewImage.classList.remove('d-block');
            editPreviewImage.classList.add('d-none');
        }

        editDeviceForm.action = `/edit_device/${deviceId}`;
        editFileInput.value = ''; 
    });

    addDeviceModal.addEventListener('hidden.bs.modal', event => {
        const form = event.target.querySelector('form');
        form.reset(); 
        addPreviewImage.src = ""; 
        addPreviewImage.classList.remove('d-block');
        addPreviewImage.classList.add('d-none');
    });

    editDeviceModal.addEventListener('hidden.bs.modal', event => {
        const form = event.target.querySelector('form');
        form.reset(); 
        editPreviewImage.src = ""; 
        editPreviewImage.classList.remove('d-block');
        editPreviewImage.classList.add('d-none');
    });

    if (editDropZone && editFileInput && editPreviewImage) {
        editDropZone.addEventListener("click", () => editFileInput.click());
        editDropZone.addEventListener("dragover", (e) => { e.preventDefault(); editDropZone.classList.add("drag-over"); });
        editDropZone.addEventListener("dragleave", () => { editDropZone.classList.remove("drag-over"); });
        editDropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            editDropZone.classList.remove("drag-over");
            const file = e.dataTransfer.files[0];
            editFileInput.files = e.dataTransfer.files;
            updatePreview(file, editPreviewImage);
        });
        editFileInput.addEventListener("change", () => {
            const file = editFileInput.files[0];
            updatePreview(file, editPreviewImage);
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
});