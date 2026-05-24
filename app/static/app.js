document.addEventListener("DOMContentLoaded", () => {
    // State management
    let selectedFile = null;
    let conversionStartTime = 0;
    let timerInterval = null;
    let convertedMarkdown = "";

    // DOM Elements
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const fileInfo = document.getElementById("file-info");
    const fileInfoName = fileInfo.querySelector(".file-name");
    const removeFileBtn = document.getElementById("remove-file-btn");
    
    const urlInput = document.getElementById("url-input");
    const convertBtn = document.getElementById("convert-btn");
    
    const ocrToggle = document.getElementById("ocr-toggle");
    const imagesToggle = document.getElementById("images-toggle");
    
    const processingContainer = document.getElementById("processing-container");
    const stepOcr = document.getElementById("step-ocr");
    const stepMarkdown = document.getElementById("step-markdown");
    const elapsedTime = document.getElementById("elapsed-time");
    
    const metricsBar = document.getElementById("metrics-bar");
    const metricPages = document.getElementById("metric-pages");
    const metricSpeed = document.getElementById("metric-speed");
    const metricTitle = document.getElementById("metric-title");
    
    const previewDisplay = document.getElementById("preview-display");
    const codeDisplay = document.getElementById("code-display");
    
    const copyBtn = document.getElementById("copy-btn");
    const downloadBtn = document.getElementById("download-btn");
    const notifications = document.getElementById("notifications");

    // Initialize marked option
    marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: true
    });

    // -------------------------------------------------------------
    // INPUT TAB SWITCHING
    // -------------------------------------------------------------
    document.querySelectorAll(".input-tabs .tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".input-tabs .tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll("#upload-tab, #url-tab").forEach(pane => pane.classList.remove("active"));
            
            btn.classList.add("active");
            const targetPane = document.getElementById(btn.dataset.tab);
            targetPane.classList.add("active");
            
            // Clear selections when switching tabs
            if (btn.dataset.tab === "upload-tab") {
                urlInput.value = "";
            } else {
                clearSelectedFile();
            }
        });
    });

    // -------------------------------------------------------------
    // OUTPUT TAB SWITCHING
    // -------------------------------------------------------------
    document.querySelectorAll(".output-tabs .tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".output-tabs .tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll("#preview-tab, #code-tab").forEach(pane => pane.classList.remove("active"));
            
            btn.classList.add("active");
            const targetPane = document.getElementById(btn.dataset.tab);
            targetPane.classList.add("active");
        });
    });

    // -------------------------------------------------------------
    // FILE DRAG AND DROP HANDLERS
    // -------------------------------------------------------------
    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    ["dragleave", "dragend"].forEach(type => {
        dropZone.addEventListener(type, () => {
            dropZone.classList.remove("dragover");
        });
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (fileInput.files.length) {
            handleFileSelect(fileInput.files[0]);
        }
    });

    removeFileBtn.addEventListener("click", (e) => {
        e.stopPropagation(); // Avoid triggering file selection
        clearSelectedFile();
    });

    function handleFileSelect(file) {
        selectedFile = file;
        fileInfoName.textContent = file.name;
        fileInfo.classList.remove("hidden");
        showNotification(`Selected file: ${file.name}`, "info");
    }

    function clearSelectedFile() {
        selectedFile = null;
        fileInput.value = "";
        fileInfo.classList.add("hidden");
    }

    // -------------------------------------------------------------
    // CONVERSION HANDLER
    // -------------------------------------------------------------
    convertBtn.addEventListener("click", async () => {
        const isUploadTab = document.querySelector(".input-tabs .tab-btn[data-tab='upload-tab']").classList.contains("active");
        
        if (isUploadTab && !selectedFile) {
            showNotification("Please select or drag a file to convert.", "error");
            return;
        }
        
        if (!isUploadTab && !urlInput.value.trim()) {
            showNotification("Please enter a valid document URL.", "error");
            return;
        }

        // Start UI progress
        startTimer();
        setStepState("step-ocr", "active");
        setStepState("step-markdown", "pending");
        processingContainer.classList.remove("hidden");
        convertBtn.disabled = true;

        try {
            let result;
            if (isUploadTab) {
                result = await performFileUploadConversion();
            } else {
                result = await performUrlConversion();
            }

            if (result.success) {
                // Success phase
                setStepState("step-ocr", "done");
                setStepState("step-markdown", "done");
                
                convertedMarkdown = result.markdown;
                
                // Display markdown
                previewDisplay.innerHTML = marked.parse(result.markdown);
                codeDisplay.textContent = result.markdown;
                
                // Show Metrics
                metricPages.textContent = result.metrics.pages_processed || 1;
                metricSpeed.textContent = `${result.metrics.execution_time_sec}s`;
                metricTitle.textContent = result.metadata.title || "Untitled Document";
                metricsBar.classList.remove("hidden");
                
                showNotification("Conversion completed successfully!", "success");
            } else {
                throw new Error(result.error || "Failed to convert document.");
            }
        } catch (error) {
            console.error(error);
            showNotification(error.message, "error");
        } finally {
            stopTimer();
            processingContainer.classList.add("hidden");
            convertBtn.disabled = false;
        }
    });

    async function performFileUploadConversion() {
        const formData = new FormData();
        formData.append("file", selectedFile);
        formData.append("enable_ocr", ocrToggle.checked);
        formData.append("generate_images", imagesToggle.checked);
        
        const response = await fetch("/api/convert/file", {
            method: "POST",
            body: formData
        });
        
        return await response.json();
    }

    async function performUrlConversion() {
        const payload = {
            url: urlInput.value.trim(),
            enable_ocr: ocrToggle.checked,
            generate_images: imagesToggle.checked
        };
        
        const response = await fetch("/api/convert/url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        
        return await response.json();
    }

    // -------------------------------------------------------------
    // PROGRESS TIMER & BADGES
    // -------------------------------------------------------------
    function startTimer() {
        conversionStartTime = Date.now();
        elapsedTime.textContent = "0.0";
        clearInterval(timerInterval);
        
        timerInterval = setInterval(() => {
            const elapsed = ((Date.now() - conversionStartTime) / 1000).toFixed(1);
            elapsedTime.textContent = elapsed;
            
            // Dynamically push progress stages based on timer
            if (elapsed > 4) {
                setStepState("step-ocr", "done");
                setStepState("step-markdown", "active");
            }
        }, 100);
    }

    function stopTimer() {
        clearInterval(timerInterval);
    }

    function setStepState(stepId, state) {
        const step = document.getElementById(stepId);
        if (!step) return;
        
        step.classList.remove("active", "done");
        if (state === "active") {
            step.classList.add("active");
        } else if (state === "done") {
            step.classList.add("done");
        }
    }

    // -------------------------------------------------------------
    // EXPORTS (COPY & DOWNLOAD)
    // -------------------------------------------------------------
    copyBtn.addEventListener("click", () => {
        if (!convertedMarkdown) {
            showNotification("No converted content to copy.", "error");
            return;
        }
        
        navigator.clipboard.writeText(convertedMarkdown).then(() => {
            showNotification("Markdown copied to clipboard!", "success");
            
            // Visual feedback on button
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = "✓ Copied";
            copyBtn.style.borderColor = "var(--accent-success)";
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.style.borderColor = "";
            }, 2000);
        }).catch(err => {
            showNotification("Failed to copy text.", "error");
        });
    });

    downloadBtn.addEventListener("click", () => {
        if (!convertedMarkdown) {
            showNotification("No converted content to download.", "error");
            return;
        }
        
        const blob = new Blob([convertedMarkdown], { type: "text/markdown;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement("a");
        a.href = url;
        
        // Define clean file name
        let filename = "converted_document.md";
        if (selectedFile) {
            const nameWithoutExt = selectedFile.name.substring(0, selectedFile.name.lastIndexOf('.')) || selectedFile.name;
            filename = `${nameWithoutExt}.md`;
        } else if (urlInput.value) {
            try {
                const parsedUrl = new URL(urlInput.value);
                const pathParts = parsedUrl.pathname.split('/');
                const lastPart = pathParts[pathParts.length - 1];
                if (lastPart && lastPart.includes('.')) {
                    filename = lastPart.substring(0, lastPart.lastIndexOf('.')) + ".md";
                }
            } catch (e) {}
        }
        
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification(`Downloading ${filename}`, "success");
    });

    // -------------------------------------------------------------
    // TOAST NOTIFICATIONS
    // -------------------------------------------------------------
    function showNotification(message, type = "info") {
        const toast = document.createElement("div");
        toast.className = `notification ${type}`;
        
        let iconMarkup = "";
        if (type === "success") iconMarkup = "✓";
        else if (type === "error") iconMarkup = "✗";
        else iconMarkup = "ℹ";
        
        toast.innerHTML = `
            <span class="notification-icon">${iconMarkup}</span>
            <span class="notification-msg">${message}</span>
        `;
        
        notifications.appendChild(toast);
        
        // Auto remove
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(50px)";
            toast.style.transition = "all 0.3s ease";
            setTimeout(() => {
                notifications.removeChild(toast);
            }, 300);
        }, 3500);
    }
});
