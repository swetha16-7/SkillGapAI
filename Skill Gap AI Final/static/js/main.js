let analysisData = null;
let resumeMappingChart = null;
let jdMappingChart = null;
function setupFileUpload(boxId, inputId, nameId, overlayId) {
    const uploadBox = document.getElementById(boxId);
    const fileInput = document.getElementById(inputId);
    const fileNameDisplay = document.getElementById(nameId);
    const dragOverlay = document.getElementById(overlayId);

    // Prevent multiple rapid clicks from opening file picker multiple times
    let isFilePickerOpen = false;

    // Click to select file - only trigger if clicking on the upload box itself, not child elements
    uploadBox.addEventListener('click', (e) => {
        // Prevent triggering if clicking on buttons or other interactive elements
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            return;
        }
        // Prevent triggering if clicking on the file input itself
        if (e.target === fileInput) {
            return;
        }
        // Prevent triggering if clicking on elements with specific classes
        if (e.target.closest('.file-actions') || e.target.closest('.drag-overlay')) {
            return;
        }
        // Prevent multiple rapid clicks
        if (isFilePickerOpen) {
            return;
        }

        isFilePickerOpen = true;
        fileInput.click();

        // Reset the flag after a short delay
        setTimeout(() => {
            isFilePickerOpen = false;
        }, 1000);
    });

    // Prevent the file input from triggering the upload box click
    fileInput.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    // File input change
    fileInput.addEventListener('change', function(e) {
        isFilePickerOpen = false; // Reset the flag when file is selected
        handleFileSelection(e.target.files[0], fileNameDisplay);
    });

    // Drag and drop events
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('drag-over');
        dragOverlay.classList.add('active');
    });

    uploadBox.addEventListener('dragleave', (e) => {
        e.preventDefault();
        if (!uploadBox.contains(e.relatedTarget)) {
            uploadBox.classList.remove('drag-over');
            dragOverlay.classList.remove('active');
        }
    });

    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('drag-over');
        dragOverlay.classList.remove('active');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            // Only validate file type for drag and drop (basic validation)
            if (validateFileType(file)) {
                fileInput.files = files; // Set the file input
                handleFileSelection(file, fileNameDisplay);
            }
        }
    });
}

function handleFileSelection(file, fileNameDisplay) {
    const fileName = file ? file.name : 'No file selected';
    fileNameDisplay.textContent = fileName;
    fileNameDisplay.style.color = fileName !== 'No file selected' ? '#10b981' : '#64748b';

    // Show/hide preview buttons and enable/disable them
    const actionsContainer = fileNameDisplay.parentElement.querySelector('.file-actions');
    const previewBtn = actionsContainer ? actionsContainer.querySelector('.preview-btn') : null;

    if (actionsContainer) {
        actionsContainer.style.display = file ? 'block' : 'none';
        if (previewBtn) {
            previewBtn.disabled = !file;
            previewBtn.style.opacity = file ? '1' : '0.5';
        }
    }

    // Announce file selection to screen readers
    if (file) {
        announceToScreenReader(`File selected: ${file.name}`, 'assertive');
    }
}

function validateFileType(file) {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    return allowedTypes.includes(file.type);
}

function validateFile(file) {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);

    if (!allowedTypes.includes(file.type)) {
        const fileExtension = file.name.split('.').pop().toLowerCase();
        let suggestion = '';

        if (['doc', 'docx'].includes(fileExtension)) {
            suggestion = ' Try saving as .docx format.';
        } else if (fileExtension === 'rtf') {
            suggestion = ' Try converting to PDF or plain text.';
        } else {
            suggestion = ' Supported formats: PDF (.pdf), Word (.docx), and plain text (.txt).';
        }

        showError(`❌ Unsupported file format "${fileExtension}".${suggestion}`);
        return false;
    }

    if (file.size > maxSize) {
        showError(`❌ File "${file.name}" is too large (${fileSizeMB}MB). Maximum allowed size is 16MB. Try compressing the file or using a smaller version.`);
        return false;
    }

    if (file.size === 0) {
        showError(`❌ File "${file.name}" appears to be empty. Please check the file and try again.`);
        return false;
    }

    return true;
}

setupFileUpload('resume-upload-box', 'resume-upload', 'resume-name', 'resume-drag-overlay');
setupFileUpload('jd-upload-box', 'jd-upload', 'jd-name', 'jd-drag-overlay');

// Keyboard navigation and touch support
document.addEventListener('keydown', function(e) {
    // Enter or Space key on upload boxes
    if ((e.key === 'Enter' || e.key === ' ') && (e.target.id === 'resume-upload-box' || e.target.id === 'jd-upload-box')) {
        e.preventDefault();
        const inputId = e.target.id === 'resume-upload-box' ? 'resume-upload' : 'jd-upload';
        document.getElementById(inputId).click();
    }

    // Escape key to close modals
    if (e.key === 'Escape') {
        if (!document.getElementById('preview-modal').classList.contains('hidden')) {
            closePreviewModal();
        } else if (!document.getElementById('error-modal').classList.contains('hidden')) {
            closeErrorModal();
        }
    }
});

// Touch device optimizations
if ('ontouchstart' in window) {
    // Improve touch feedback for upload boxes
    document.querySelectorAll('.upload-box').forEach(box => {
        box.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });

        box.addEventListener('touchend', function() {
            this.style.transform = '';
        });
    });

    // Prevent double-tap zoom on buttons only
    document.querySelectorAll('button').forEach(element => {
        element.addEventListener('touchend', function(e) {
            e.preventDefault();
            this.click();
        }, { passive: false });
    });

    // For upload boxes, just prevent zoom without triggering additional clicks
    document.querySelectorAll('.upload-box').forEach(box => {
        box.addEventListener('touchend', function(e) {
            // Prevent zoom but don't call click() - the regular click handler will handle it
            e.preventDefault();
        }, { passive: false });
    });
}

// Mobile viewport height fix
function setMobileViewportHeight() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
}

if (window.innerWidth <= 768) {
    setMobileViewportHeight();
    window.addEventListener('resize', setMobileViewportHeight);
}

// Force modal scrollbar to top - simplified and more reliable
function forceModalScrollToTop(modal) {
    const modalBody = modal.querySelector('.modal-body');
    const previewContent = modal.querySelector('.preview-content');

    if (modalBody) {
        // Immediate scroll reset
        modalBody.scrollTop = 0;
        modalBody.scrollLeft = 0;

        // Force layout recalculation
        modalBody.offsetHeight;

        // Use multiple requestAnimationFrame calls to ensure it sticks
        requestAnimationFrame(() => {
            modalBody.scrollTop = 0;
            modalBody.scrollLeft = 0;

            requestAnimationFrame(() => {
                modalBody.scrollTop = 0;
                modalBody.scrollLeft = 0;

                // Also reset the preview content container if it exists
                if (previewContent) {
                    previewContent.scrollTop = 0;
                    previewContent.scrollLeft = 0;
                }
            });
        });
    }
}

// Ultra-aggressive scroll reset for preview modal
function forceModalScrollToTopAggressive(modal) {
    const modalBody = modal.querySelector('.modal-body');
    const previewContent = modal.querySelector('.preview-content');

    if (modalBody) {
        // Disable smooth scrolling temporarily
        modalBody.style.scrollBehavior = 'auto';

        // Force scroll reset multiple times immediately
        for (let i = 0; i < 5; i++) {
            modalBody.scrollTop = 0;
            modalBody.scrollLeft = 0;
        }

        // Force layout recalculation
        modalBody.offsetHeight;

        // Use requestAnimationFrame for additional resets
        requestAnimationFrame(() => {
            modalBody.scrollTop = 0;
            modalBody.scrollLeft = 0;

            requestAnimationFrame(() => {
                modalBody.scrollTop = 0;
                modalBody.scrollLeft = 0;

                // Reset preview content if it exists
                if (previewContent) {
                    previewContent.scrollTop = 0;
                    previewContent.scrollLeft = 0;
                    previewContent.style.scrollBehavior = 'auto';
                }

                // Re-enable smooth scrolling after a delay
                setTimeout(() => {
                    modalBody.style.scrollBehavior = '';
                    if (previewContent) {
                        previewContent.style.scrollBehavior = '';
                    }
                }, 100);
            });
        });

        // Additional reset using setTimeout for stubborn browsers
        setTimeout(() => {
            modalBody.scrollTop = 0;
            modalBody.scrollLeft = 0;
            if (previewContent) {
                previewContent.scrollTop = 0;
                previewContent.scrollLeft = 0;
            }
        }, 0);
    }
}

// Additional function to prevent scrolling away from top for a few seconds
function preventModalScrollAway(modal) {
    const modalBody = modal.querySelector('.modal-body');
    let scrollPreventionTimeout;
    let scrollCheckInterval;

    if (modalBody) {
        const preventScroll = (e) => {
            if (modalBody.scrollTop > 0) {
                modalBody.scrollTop = 0;
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        };

        // More aggressive scroll prevention
        const forceStayAtTop = () => {
            if (modalBody.scrollTop > 0) {
                modalBody.scrollTop = 0;
            }
        };

        // Add scroll prevention listeners
        modalBody.addEventListener('scroll', preventScroll, { passive: false, capture: true });
        modalBody.addEventListener('wheel', preventScroll, { passive: false, capture: true });
        modalBody.addEventListener('touchmove', preventScroll, { passive: false, capture: true });
        modalBody.addEventListener('keydown', (e) => {
            // Prevent page up/down keys
            if (e.key === 'PageDown' || e.key === 'PageUp' || e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                modalBody.scrollTop = 0;
            }
        }, { capture: true });

        // Continuous monitoring for 3 seconds
        scrollCheckInterval = setInterval(forceStayAtTop, 50); // Check every 50ms

        // Remove prevention after 3 seconds
        scrollPreventionTimeout = setTimeout(() => {
            modalBody.removeEventListener('scroll', preventScroll, true);
            modalBody.removeEventListener('wheel', preventScroll, true);
            modalBody.removeEventListener('touchmove', preventScroll, true);
            clearInterval(scrollCheckInterval);
        }, 3000);

        // Store timeouts on modal for cleanup
        modal._scrollPreventionTimeout = scrollPreventionTimeout;
        modal._scrollCheckInterval = scrollCheckInterval;
    }
}

// Focus management for screen readers
function announceToScreenReader(message, priority = 'polite') {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', priority);
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.style.width = '1px';
    announcement.style.height = '1px';
    announcement.style.overflow = 'hidden';

    document.body.appendChild(announcement);
    announcement.textContent = message;

    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

document.getElementById('analyze-btn').addEventListener('click', async () => {
    const resumeFile = document.getElementById('resume-upload').files[0];
    const jdFile = document.getElementById('jd-upload').files[0];

    // Enhanced validation with specific feedback
    if (!resumeFile && !jdFile) {
        showError('📄 No files uploaded. Please select both your resume and job description to get started with the analysis.');
        return;
    }

    if (!resumeFile) {
        showError('📄 Resume missing. Please upload your resume so we can analyze your skills.');
        return;
    }

    if (!jdFile) {
        showError('💼 Job description missing. Please upload the job posting you want to analyze.');
        return;
    }

    // Check if both files are the same
    if (resumeFile.name === jdFile.name &&
        resumeFile.size === jdFile.size &&
        resumeFile.lastModified === jdFile.lastModified) {
        showError('❌ Same file detected. Please upload different files for resume and job description. You cannot use the same file for both fields.');
        return;
    }

    // Validate file types and sizes
    if (!validateFile(resumeFile) || !validateFile(jdFile)) {
        return; // validateFile already shows error messages
    }

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jdFile);

    const loading = document.getElementById('loading');
    const uploadSection = document.getElementById('upload-section');
    const resultsSection = document.getElementById('results-section');
    const errorMessage = document.getElementById('error-message');

    loading.classList.remove('hidden');
    errorMessage.classList.add('hidden');

    // Reset progress
    resetProgress();

    try {
        // Step 1: Upload files (0-25%)
        updateProgress(0, 'Uploading files...', 'Sending your documents to our servers...');
        setStepActive('step-upload');

        await simulateDelay(500); // Simulate upload time

        // Step 2: Parse documents (25-50%)
        updateProgress(25, 'Parsing documents...', 'Reading and understanding your files...');
        setStepCompleted('step-upload');
        setStepActive('step-parse');

        await simulateDelay(1000);

        // Step 3: Extract skills (50-75%)
        updateProgress(50, 'Extracting skills...', 'Analyzing skills from your resume and job description...');
        setStepCompleted('step-parse');
        setStepActive('step-extract');

        await simulateDelay(1500);

        // Step 4: Analyze gaps (75-100%)
        updateProgress(75, 'Analyzing gaps...', 'Comparing skills and calculating your match score...');
        setStepCompleted('step-extract');
        setStepActive('step-analyze');

        // Add timestamp to prevent caching
        const timestamp = Date.now();
        const uploadUrl = `/upload?t=${timestamp}`;

        const response = await fetch(uploadUrl, {
            method: 'POST',
            body: formData,
            headers: {
                'Cache-Control': 'no-cache'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        updateProgress(100, 'Analysis complete!', 'Preparing your results...');
        setStepCompleted('step-analyze');

        await simulateDelay(500);

        analysisData = data;
        displayResults(data);

        // Save data for dashboard access
        saveAnalysisDataForDashboard(data);

        // Update chatbot with results-aware quick actions
        updateChatbotForResults(data);

        uploadSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        // Announce analysis completion to screen readers
        const matchPercentage = data.analysis.match_percentage;
        announceToScreenReader(`Analysis complete. Your match score is ${matchPercentage}%. ${data.analysis.summary.matched_count} skills match out of ${data.analysis.summary.total_jd_skills} required skills.`, 'assertive');

    } catch (error) {
        showError(error.message);
    } finally {
        loading.classList.add('hidden');
    }
});

function updateProgress(percentage, text, subtext) {
    const progressRing = document.getElementById('progress-ring');
    const progressPercentage = document.getElementById('progress-percentage');
    const loadingText = document.getElementById('loading-text');
    const loadingSubtext = document.getElementById('loading-subtext');

    // Update circular progress
    const circumference = 2 * Math.PI * 50; // 50 is the radius
    const offset = circumference - (percentage / 100) * circumference;
    progressRing.style.strokeDashoffset = offset;

    // Update text
    progressPercentage.textContent = `${percentage}%`;
    loadingText.textContent = text;
    loadingSubtext.textContent = subtext;
}

function setStepActive(stepId) {
    const step = document.getElementById(stepId);
    step.classList.add('active');
    step.classList.remove('completed');
}

function setStepCompleted(stepId) {
    const step = document.getElementById(stepId);
    step.classList.remove('active');
    step.classList.add('completed');
}

function resetProgress() {
    const steps = ['step-upload', 'step-parse', 'step-extract', 'step-analyze'];
    steps.forEach(stepId => {
        const step = document.getElementById(stepId);
        step.classList.remove('active', 'completed');
    });

    updateProgress(0, 'Reading your documents...', 'This usually takes 10-30 seconds');
}

function simulateDelay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Save analysis data for dashboard access
function saveAnalysisDataForDashboard(data) {
    try {
        localStorage.setItem('skillGapAnalysisData', JSON.stringify(data));
        sessionStorage.setItem('skillGapAnalysisData', JSON.stringify(data));
    } catch (e) {
        console.error('Error saving analysis data:', e);
    }
}

function displayResults(data) {
    const analysis = data.analysis;

    // Update summary cards with animations
    animateNumber('match-percentage', analysis.match_percentage, '%');
    animateNumber('total-resume-skills', analysis.summary.total_resume_skills, '');
    animateNumber('total-jd-skills', analysis.summary.total_jd_skills, '');
    animateNumber('matched-count', analysis.summary.matched_count, '');

    // Animate progress bars
    animateProgressBar('match-progress-bar', analysis.match_percentage);
    animateCircularProgress('match-score-ring', analysis.match_percentage);
    animateProgressBar('mini-matched-bar', (analysis.summary.matched_count / analysis.summary.total_jd_skills) * 100);

    // Update key insights
    updateKeyInsights(analysis);

    // Populate skill mapping visualization
    populateSkillMapping(data.resume_skills, data.jd_skills, analysis);

    // Display skills in detailed sections
    displaySkills('matched-technical', analysis.matched.technical, 'matched');
    displaySkills('matched-soft', analysis.matched.soft, 'matched');
    displaySkills('missing-technical', analysis.missing.technical, 'missing');
    displaySkills('missing-soft', analysis.missing.soft, 'missing');
    displaySkills('extra-technical', analysis.extra.technical, 'extra');
    displaySkills('extra-soft', analysis.extra.soft, 'extra');

    // Display partially matched skills
    displayPartiallyMatched(analysis.partially_matched);

    // Create action plan
    createActionPlan(analysis);

    // Create charts
    createMappingCharts(data.resume_skills, data.jd_skills);
}

function displaySkills(elementId, skills, type, analysis = null) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';

    if (skills.length === 0) {
        container.innerHTML = '<span style="color: #7f8c8d; font-style: italic;">No skills found in this category</span>';
        return;
    }

    skills.forEach(skill => {
        const tag = document.createElement('span');

        // Special handling for strengths-list and critical-skills-list to apply technical/soft colors
        if ((elementId === 'strengths-list' || elementId === 'critical-skills-list') && analysis) {
            if (elementId === 'strengths-list') {
                if (analysis.matched.technical.includes(skill)) {
                    tag.className = `skill-tag technical`;
                } else if (analysis.matched.soft.includes(skill)) {
                    tag.className = `skill-tag soft`;
                } else {
                    tag.className = `skill-tag ${type}`;
                }
            } else if (elementId === 'critical-skills-list') {
                if (analysis.missing.technical.includes(skill)) {
                    tag.className = `skill-tag technical`;
                } else if (analysis.missing.soft.includes(skill)) {
                    tag.className = `skill-tag soft`;
                } else {
                    tag.className = `skill-tag ${type}`;
                }
            }
        } else {
            tag.className = `skill-tag ${type}`;
        }

        tag.textContent = skill;
        container.appendChild(tag);
    });
}

function displayPartiallyMatched(partiallyMatched) {
    // Display technical partial matches
    const techContainer = document.getElementById('partially-matched-technical');
    if (techContainer) {
        techContainer.innerHTML = '';
        if (partiallyMatched.technical.length === 0) {
            techContainer.innerHTML = '<span style="color: #7f8c8d; font-style: italic;">No skills found in this category</span>';
        } else {
            partiallyMatched.technical.forEach(item => {
                const div = document.createElement('div');
                div.className = 'partial-match-item';
                div.innerHTML = `
                    <strong>${item.jd_skill}</strong> is similar to
                    <strong>${item.resume_skill}</strong>
                    (${(item.similarity * 100).toFixed(1)}% match)
                `;
                techContainer.appendChild(div);
            });
        }
    }

    // Display soft partial matches
    const softContainer = document.getElementById('partially-matched-soft');
    if (softContainer) {
        softContainer.innerHTML = '';
        if (partiallyMatched.soft.length === 0) {
            softContainer.innerHTML = '<span style="color: #7f8c8d; font-style: italic;">No skills found in this category</span>';
        } else {
            partiallyMatched.soft.forEach(item => {
                const div = document.createElement('div');
                div.className = 'partial-match-item';
                div.innerHTML = `
                    <strong>${item.jd_skill}</strong> is similar to
                    <strong>${item.resume_skill}</strong>
                    (${(item.similarity * 100).toFixed(1)}% match)
                `;
                softContainer.appendChild(div);
            });
        }
    }
}

// Animation functions
function animateNumber(elementId, targetValue, suffix = '') {
    const element = document.getElementById(elementId);
    const startValue = 0;
    const duration = 1500;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function for smooth animation
        const easeOutCubic = 1 - Math.pow(1 - progress, 3);
        const currentValue = Math.floor(startValue + (targetValue - startValue) * easeOutCubic);

        element.textContent = currentValue + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

function animateProgressBar(elementId, percentage) {
    const element = document.getElementById(elementId);
    element.style.width = '0%';

    // Update percentage text inside the main match progress bar
    if (elementId === 'match-progress-bar') {
        const percentageText = document.getElementById('progress-percentage-text');
        if (percentageText) {
            percentageText.textContent = Math.round(percentage) + '%';
        }
    }

    setTimeout(() => {
        element.style.transition = 'width 1.5s ease-out';
        element.style.width = percentage + '%';
    }, 500);
}

function animateCircularProgress(elementId, percentage) {
    const element = document.getElementById(elementId);
    if (!element) return;

    // Calculate circumference: 2 * π * radius (radius is 42)
    const circumference = 2 * Math.PI * 42;
    const offset = circumference - (percentage / 100) * circumference;

    // Reset to 0 first
    element.style.strokeDashoffset = circumference;

    // Animate to target percentage
    setTimeout(() => {
        element.style.strokeDashoffset = offset;
    }, 500);
}

// Key insights update function
function updateKeyInsights(analysis) {
    const matchPercent = analysis.match_percentage;
    const matchSummary = document.getElementById('match-summary');
    const matchDescription = document.getElementById('match-description');
    const priorityAction = document.getElementById('priority-action');

    if (!matchSummary || !matchDescription || !priorityAction) return;

    // Update match summary based on percentage
    if (matchPercent >= 80) {
        matchSummary.textContent = "Excellent Match! 🎉";
        matchDescription.textContent = "You're highly qualified for this position";
        priorityAction.textContent = "Tailor your resume and apply!";
    } else if (matchPercent >= 60) {
        matchSummary.textContent = "Good Match 👍";
        matchDescription.textContent = "You have solid qualifications with some gaps";
        priorityAction.textContent = "Address the most critical missing skills";
    } else if (matchPercent >= 40) {
        matchSummary.textContent = "Moderate Match 🤔";
        matchDescription.textContent = "You have potential but need skill development";
        priorityAction.textContent = "Focus on building core required skills";
    } else {
        matchSummary.textContent = "Limited Match ⚠️";
        matchDescription.textContent = "Significant skill gaps need to be addressed";
        priorityAction.textContent = "Consider building foundational skills first";
    }
}

// Skill mapping visualization
function populateSkillMapping(resumeSkills, jdSkills, analysis) {
    // Resume skills
    displaySkills('resume-technical-tags', resumeSkills.technical, 'resume');
    displaySkills('resume-soft-tags', resumeSkills.soft, 'resume');

    // Job skills
    displaySkills('job-technical-tags', jdSkills.technical, 'job');
    displaySkills('job-soft-tags', jdSkills.soft, 'job');

    // Update match indicator
    const matchCountEl = document.getElementById('mapping-match-count');
    if (matchCountEl) {
        matchCountEl.textContent = analysis.summary.matched_count;
    }
}

// Action plan creation
function createActionPlan(analysis) {
    const missingTechnical = analysis.missing.technical.slice(0, 3); // Top 3
    const missingSoft = analysis.missing.soft.slice(0, 2); // Top 2
    const criticalSkills = [...missingTechnical, ...missingSoft];

    // Combine partially matched technical and soft skills
    const partiallyMatched = [
        ...analysis.partially_matched.technical.slice(0, 2), // Top 2 technical
        ...analysis.partially_matched.soft.slice(0, 2)       // Top 2 soft
    ].slice(0, 3); // Take top 3 overall

    const matchedSkills = [...analysis.matched.technical.slice(0, 3), ...analysis.matched.soft.slice(0, 2)];

    // Step 1: Critical skills to learn
    const step1Title = document.getElementById('step-1-title');
    const step1Desc = document.getElementById('step-1-desc');
    if (criticalSkills.length > 0) {
        if (step1Title) step1Title.textContent = `Learn ${criticalSkills.length} Critical Skills`;
        if (step1Desc) step1Desc.textContent = 'These are the most important skills you\'re missing';
        displaySkills('critical-skills-list', criticalSkills, 'missing', analysis);
    } else {
        if (step1Title) step1Title.textContent = 'Start Learning Key Skills';
        if (step1Desc) step1Desc.textContent = 'Focus on high-demand skills relevant to your career goals';
        const criticalSkillsList = document.getElementById('critical-skills-list');
        if (criticalSkillsList) {
            criticalSkillsList.innerHTML = '<p style="color: #7f8c8d; font-style: italic;">All critical skills are already in your resume - great job!</p>';
        }
    }

    // Step 2: Strengthen similar skills
    const step2Title = document.getElementById('step-2-title');
    const step2Desc = document.getElementById('step-2-desc');
    if (partiallyMatched.length > 0) {
        if (step2Title) step2Title.textContent = 'Strengthen Similar Skills';
        if (step2Desc) step2Desc.textContent = 'Build on skills you partially have';
        displayPartialSkills('similar-skills-list', partiallyMatched);
    } else {
        if (step2Title) step2Title.textContent = 'Develop Related Skills';
        if (step2Desc) step2Desc.textContent = 'Consider learning skills related to your current expertise';
        const similarSkillsList = document.getElementById('similar-skills-list');
        if (similarSkillsList) {
            similarSkillsList.innerHTML = '<p style="color: #7f8c8d; font-style: italic;">No specific similar skills identified - focus on expanding your core competencies</p>';
        }
    }

    // Step 3: Highlight strengths
    const step3Title = document.getElementById('step-3-title');
    const step3Desc = document.getElementById('step-3-desc');
    if (matchedSkills.length > 0) {
        if (step3Title) step3Title.textContent = 'Highlight Your Strengths';
        if (step3Desc) step3Desc.textContent = 'Emphasize these matching skills in your resume';
        displaySkills('strengths-list', matchedSkills, 'matched', analysis);
    } else {
        if (step3Title) step3Title.textContent = 'Build Your Foundation';
        if (step3Desc) step3Desc.textContent = 'Focus on acquiring fundamental skills for your target role';
        const strengthsList = document.getElementById('strengths-list');
        if (strengthsList) {
            strengthsList.innerHTML = '<p style="color: #7f8c8d; font-style: italic;">Start by building core skills, then work on highlighting them effectively</p>';
        }
    }
}

function displayPartialSkills(containerId, partialSkills) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    partialSkills.forEach(item => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag partial';
        tag.textContent = `${item.resume_skill} → ${item.jd_skill}`;
        container.appendChild(tag);
    });
}

function createMappingCharts(resumeSkills, jdSkills) {
    // Resume Mapping Chart
    const resumeMappingCtx = document.getElementById('resume-mapping-chart');
    if (resumeMappingCtx) {
        const ctx = resumeMappingCtx.getContext('2d');
        if (resumeMappingChart) {
            resumeMappingChart.destroy();
        }

        const resumeTechCount = resumeSkills.technical.length;
        const resumeSoftCount = resumeSkills.soft.length;

        resumeMappingChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Technical', 'Soft'],
                datasets: [{
                    data: [resumeTechCount, resumeSoftCount],
                    backgroundColor: ['#6A5ACD', '#3EB489'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 10
                            }
                        }
                    }
                },
                layout: {
                    padding: 5
                }
            }
        });
    }

    // Job Description Mapping Chart
    const jdMappingCtx = document.getElementById('jd-mapping-chart');
    if (jdMappingCtx) {
        const ctx = jdMappingCtx.getContext('2d');
        if (jdMappingChart) {
            jdMappingChart.destroy();
        }

        const jdTechCount = jdSkills.technical.length;
        const jdSoftCount = jdSkills.soft.length;

        jdMappingChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Technical', 'Soft'],
                datasets: [{
                    data: [jdTechCount, jdSoftCount],
                    backgroundColor: ['#6A5ACD', '#3EB489'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 10
                            }
                        }
                    }
                },
                layout: {
                    padding: 5
                }
            }
        });
    }
}

// Help Chatbot functionality
const chatbotButton = document.getElementById('chatbot-button');
const chatbotModal = document.getElementById('chatbot-modal');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotBody = document.getElementById('chatbot-body');
const quickQuestionsContainer = document.getElementById('quick-questions');
let quickBtns = document.querySelectorAll('.quick-btn');

// Function to update chatbot quick buttons when results are available
function updateChatbotForResults(data) {
    if (!data || !data.analysis) return;

    const quickQuestions = quickQuestionsContainer;
    const score = Math.round(data.analysis.match_percentage);
    quickQuestions.innerHTML = `
        <button class="quick-btn" data-question="explain-score">What does my ${score}% score mean?</button>
        <button class="quick-btn" data-question="missing-skills">What skills am I missing?</button>
        <button class="quick-btn" data-question="partial-skills">What are partially matching skills?</button>
        <button class="quick-btn" data-question="learn-first">What should I learn first?</button>
        <button class="quick-btn" data-question="resume-tips">How can I improve my resume?</button>
        <button class="quick-btn" data-question="general-help">General Help</button>
    `;

    // Update welcome message to be results-aware
    const welcomeMsg = document.getElementById('chatbot-welcome');
    if (welcomeMsg) {
        welcomeMsg.innerHTML = `<strong>👋 Hi! I'm here to help you understand your results!</strong><br>
        Your match score is <strong>${score}%</strong>. Click any question below to learn more about your analysis and how to improve!`;
    }

    // Re-attach event listeners
    quickBtns = document.querySelectorAll('.quick-btn');
    attachQuickButtonListeners();
}

// Function to reset chatbot to default when starting new analysis
function resetChatbotToDefault() {
    const quickQuestions = quickQuestionsContainer;
    quickQuestions.innerHTML = `
        <button class="quick-btn" data-question="upload">How to upload files?</button>
        <button class="quick-btn" data-question="analyze">How does analysis work?</button>
        <button class="quick-btn" data-question="results">Understanding results</button>
        <button class="quick-btn" data-question="export">How to export reports?</button>
    `;

    // Re-attach event listeners
    quickBtns = document.querySelectorAll('.quick-btn');
    attachQuickButtonListeners();

    // Reset welcome message
    const welcomeMsg = document.getElementById('chatbot-welcome');
    if (welcomeMsg) {
        welcomeMsg.innerHTML = `<strong>👋 Welcome to SkillGap AI!</strong><br>
        I'm your personal assistant for understanding how to get the most out of our skill analysis tool. Click any of the questions below or ask me anything about using the platform!`;
    }
}

// Chatbot responses with multiple variations for more natural conversation
const chatbotResponses = {
    upload: [
        {
            title: "📤 File Upload Guide",
            content: `Uploading files is simple! Here's what you need to know:

• <strong>Resume</strong>: Click the resume upload area and select your CV/resume file
• <strong>Job Description</strong>: Do the same for the job posting you want to analyze
• <strong>Formats</strong>: We support PDF, Word (.docx), and plain text files
• <strong>Tip</strong>: Keep files under 10MB for fastest processing

Once uploaded, a preview button will appear so you can check the content!`
        },
        {
            title: "📤 Getting Your Files Ready",
            content: `Let's get those files uploaded:

1. <strong>Find your resume</strong> - Look for your most recent CV in PDF, Word, or text format
2. <strong>Locate the job posting</strong> - Copy-paste the job description into a text file, or upload the original PDF
3. <strong>Click the upload areas</strong> - Drop your files or click to browse
4. <strong>Check the preview</strong> - Use the preview button to verify the content was read correctly

Pro tip: Make sure your resume includes your most recent skills and experiences!`
        }
    ],
    analyze: [
        {
            title: "🔍 How Our AI Analysis Works",
            content: `Our AI is pretty smart! Here's what happens behind the scenes:

• <strong>Text Processing</strong>: We extract and clean text from both documents
• <strong>Skill Detection</strong>: Advanced algorithms identify technical and soft skills in your resume
• <strong>Requirements Analysis</strong>: We analyze what the job posting is looking for
• <strong>Matching Engine</strong>: We compare your skills against job requirements
• <strong>Insights Generation</strong>: Create personalized recommendations just for you

Usually takes 10-30 seconds. The more detailed your documents, the better the analysis!`
        },
        {
            title: "🔍 The Analysis Process",
            content: `Curious about our AI magic? Here's how we analyze your documents:

1. <strong>Reading Phase</strong>: We carefully read through both your resume and the job description
2. <strong>Skill Extraction</strong>: Our AI identifies all the skills mentioned in both documents
3. <strong>Comparison</strong>: We match your skills against what's needed for the job
4. <strong>Categorization</strong>: Skills are sorted into matching, partially matching, missing, and bonus categories
5. <strong>Recommendations</strong>: We suggest specific steps to improve your fit for the role

The whole process is automated and takes just seconds to complete!`
        }
    ],
    results: [
        {
            title: "📊 Making Sense of Your Results",
            content: `Your results are organized to make it super easy to understand:

<strong>🟢 Matching Skills</strong>: Perfect matches between your resume and the job requirements
<strong>🟡 Partially Matching Skills</strong>: Related skills that could be helpful
<strong>🔴 Missing Skills</strong>: Key skills you'll want to develop or highlight
<strong>💎 Bonus Skills</strong>: Extra skills that make you stand out

The action plan at the bottom gives you a clear roadmap for improvement!`
        },
        {
            title: "📊 Understanding What the Colors Mean",
            content: `Let's break down what each section of your results means:

• <strong>Matching Skills</strong> (green): These are your strongest selling points!
• <strong>Partially Matching Skills</strong> (yellow): Skills that are related but not exact matches
• <strong>Missing Skills</strong> (red): Areas where you might want to upskill or gain experience
• <strong>Bonus Skills</strong> (blue): Skills you have that weren't required but could be a plus

Don't worry if you have some missing skills - that's what the action plan is for!`
        }
    ],
    export: [
        {
            title: "💾 Saving Your Analysis",
            content: `Ready to save your results? You have two great options:

<strong>📄 PDF Report</strong>: A beautifully formatted document perfect for sharing or printing
• Includes charts, recommendations, and detailed analysis
• Great for job applications or keeping records

<strong>📊 Excel Spreadsheet</strong>: Raw data for further analysis
• All your skills data in spreadsheet format
• Perfect if you want to do your own analysis

Both formats include all your analysis data and are ready to download instantly!`
        },
        {
            title: "💾 Export Options Explained",
            content: `We give you two ways to save your work:

1. <strong>PDF Format</strong>: Professional-looking report with:
   - Visual charts and graphs
   - Clear recommendations
   - Easy to share with recruiters or mentors

2. <strong>Excel Format</strong>: Data-focused export with:
   - All skills in spreadsheet format
   - Easy to sort and filter
   - Great for tracking your progress over time

Choose whichever format works best for your needs!`
        }
    ],
    'explain-score': [],
    'missing-skills': [],
    'partial-skills': [],
    'learn-first': [],
    'resume-tips': [],
    'general-help': []
};

// Additional conversational responses for more natural interaction
const conversationalResponses = [
    "That's a great question! Let me help you with that.",
    "I'm happy to explain that in more detail.",
    "Let me walk you through this step by step.",
    "That's an important aspect to understand.",
    "Great timing - this is a common question!",
    "I'm glad you asked about that.",
    "Let me break this down for you clearly.",
    "That's a smart question to ask!",
    "I'm glad you asked about that.",
    "This is one of the most important features!"
];

function openChatbot() {
    chatbotModal.classList.remove('hidden');
    announceToScreenReader('Help chatbot opened');
}

function closeChatbot() {
    chatbotModal.classList.add('hidden');
    announceToScreenReader('Help chatbot closed');
}

function addChatbotMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message ${isUser ? 'user' : 'bot'}`;

    const contentDiv = document.createElement('div');
    messageDiv.className = 'message-content';
    contentDiv.innerHTML = content;

    messageDiv.appendChild(contentDiv);
    chatbotBody.appendChild(messageDiv);
    chatbotBody.scrollTop = chatbotBody.scrollHeight;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chatbot-message bot typing';
    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatbotBody.appendChild(typingDiv);
    chatbotBody.scrollTop = chatbotBody.scrollHeight;
    return typingDiv;
}

function hideTypingIndicator(typingDiv) {
    if (typingDiv && typingDiv.parentNode) {
        typingDiv.remove();
    }
}

function handleQuickQuestion(questionType, questionText) {
    // Display the user's question first
    if (questionText) {
        addChatbotMessage(questionText, true);
    }

    // Handle results-specific questions
    if (['explain-score', 'missing-skills', 'partial-skills', 'learn-first', 'resume-tips'].includes(questionType)) {
        if (!analysisData || !analysisData.analysis) {
            setTimeout(() => {
                addChatbotMessage("⚠️ <strong>No results available</strong><br>Please run an analysis first to get personalized explanations about your match score and skills.");
            }, 300);
            return;
        }
        handleResultsQuestion(questionType);
        return;
    }

    // Handle general help
    if (questionType === 'general-help') {
        setTimeout(() => {
            resetChatbotToDefault();
            addChatbotMessage("💡 <strong>Switched to General Help</strong><br>You can now ask about uploading files, how analysis works, understanding results, or exporting reports!");
        }, 300);
        return;
    }

    // Handle standard questions
    const responses = chatbotResponses[questionType];
    if (responses && responses.length > 0) {
        // Randomly select one of the response variations
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];

        // Show typing indicator
        const typingDiv = showTypingIndicator();

        setTimeout(() => {
            hideTypingIndicator(typingDiv);

            // Add a conversational opener sometimes
            const addConversationalOpener = Math.random() > 0.5;
            if (addConversationalOpener) {
                const opener = conversationalResponses[Math.floor(Math.random() * conversationalResponses.length)];
                addChatbotMessage(opener);

                setTimeout(() => {
                    addChatbotMessage(`<strong>${randomResponse.title}</strong>`);
                    setTimeout(() => {
                        addChatbotMessage(randomResponse.content);
                        addFollowUpSuggestions(questionType);
                    }, 600);
                }, 800);
            } else {
                addChatbotMessage(`<strong>${randomResponse.title}</strong>`);
                setTimeout(() => {
                    addChatbotMessage(randomResponse.content);
                    addFollowUpSuggestions(questionType);
                }, 500);
            }
        }, 1000 + Math.random() * 1000); // Random delay between 1-2 seconds
    }
}

// Handle results-specific questions
function handleResultsQuestion(questionType) {
    const analysis = analysisData.analysis;
    const typingDiv = showTypingIndicator();

    setTimeout(() => {
        hideTypingIndicator(typingDiv);

        let response = '';

        switch(questionType) {
            case 'explain-score':
                response = explainMatchScore(analysis);
                break;
            case 'missing-skills':
                response = explainMissingSkills(analysis);
                break;
            case 'partial-skills':
                response = explainPartialSkills(analysis);
                break;
            case 'learn-first':
                response = suggestLearningPriorities(analysis);
                break;
            case 'resume-tips':
                response = provideResumeTips(analysis);
                break;
        }

        if (response) {
            addChatbotMessage(response);
        }
    }, 800 + Math.random() * 500);
}

// Explain match score in simple terms
function explainMatchScore(analysis) {
    const score = Math.round(analysis.match_percentage);
    const matched = analysis.summary.matched_count;
    const total = analysis.summary.total_jd_skills;

    let explanation = `<strong>📊 Your ${score}% Match Score Explained</strong><br><br>`;

    if (score >= 80) {
        explanation += `🎉 <strong>Excellent!</strong> You have a very strong match with this job.<br><br>`;
        explanation += `You have <strong>${matched} out of ${total}</strong> required skills. This means you're highly qualified!<br><br>`;
        explanation += `💡 <strong>What this means:</strong> You're a great fit! Focus on highlighting your matching skills in your application and interview.`;
    } else if (score >= 60) {
        explanation += `👍 <strong>Good Match!</strong> You're well-qualified with some room to grow.<br><br>`;
        explanation += `You have <strong>${matched} out of ${total}</strong> required skills. You're missing some, but you have a solid foundation.<br><br>`;
        explanation += `💡 <strong>What this means:</strong> You're competitive! Consider learning a few of the missing skills to strengthen your application.`;
    } else if (score >= 40) {
        explanation += `🤔 <strong>Moderate Match</strong> - You have potential but need skill development.<br><br>`;
        explanation += `You have <strong>${matched} out of ${total}</strong> required skills. There are some gaps, but you're on the right track.<br><br>`;
        explanation += `💡 <strong>What this means:</strong> Focus on building the most critical missing skills. Your existing skills are a good starting point!`;
    } else {
        explanation += `⚠️ <strong>Limited Match</strong> - Significant skill gaps need attention.<br><br>`;
        explanation += `You have <strong>${matched} out of ${total}</strong> required skills. This job requires skills you don't have yet.<br><br>`;
        explanation += `💡 <strong>What this means:</strong> Don't worry! Use the "What should I learn first?" option to see which skills to prioritize.`;
    }

    return explanation;
}

// Explain missing skills clearly
function explainMissingSkills(analysis) {
    const missingTech = analysis.missing.technical;
    const missingSoft = analysis.missing.soft;
    const totalMissing = missingTech.length + missingSoft.length;

    if (totalMissing === 0) {
        return `<strong>✅ No Missing Skills!</strong><br><br>🎉 Amazing! You have all the required skills for this job. Your resume covers everything the job needs!`;
    }

    let explanation = `<strong>❌ Missing Skills (${totalMissing} total)</strong><br><br>`;
    explanation += `These are skills the job requires but aren't in your resume:<br><br>`;

    if (missingTech.length > 0) {
        explanation += `<strong>💻 Technical Skills (${missingTech.length}):</strong><br>`;
        explanation += missingTech.slice(0, 5).map(skill => `• ${skill}`).join('<br>');
        if (missingTech.length > 5) {
            explanation += `<br>... and ${missingTech.length - 5} more`;
        }
        explanation += `<br><br>`;
    }

    if (missingSoft.length > 0) {
        explanation += `<strong>🤝 Soft Skills (${missingSoft.length}):</strong><br>`;
        explanation += missingSoft.slice(0, 5).map(skill => `• ${skill}`).join('<br>');
        if (missingSoft.length > 5) {
            explanation += `<br>... and ${missingSoft.length - 5} more`;
        }
        explanation += `<br><br>`;
    }

    explanation += `💡 <strong>Don't worry!</strong> Missing skills are opportunities to grow. Check "What should I learn first?" for prioritized recommendations.`;

    return explanation;
}

// Explain partially matching skills
function explainPartialSkills(analysis) {
    const partialTech = analysis.partially_matched.technical;
    const partialSoft = analysis.partially_matched.soft;
    const totalPartial = partialTech.length + partialSoft.length;

    if (totalPartial === 0) {
        return `<strong>⚠️ No Partially Matching Skills</strong><br><br>This means your skills either match exactly or are completely different. That's okay - focus on the missing skills to improve your match!`;
    }

    let explanation = `<strong>⚠️ Partially Matching Skills (${totalPartial} total)</strong><br><br>`;
    explanation += `These are skills you have that are <strong>similar</strong> to what the job needs, but not exact matches:<br><br>`;

    const allPartial = [...partialTech, ...partialSoft].slice(0, 5);

    allPartial.forEach(item => {
        const similarity = Math.round(item.similarity * 100);
        explanation += `• <strong>${item.resume_skill}</strong> → similar to <strong>${item.jd_skill}</strong> (${similarity}% match)<br>`;
    });

    if (totalPartial > 5) {
        explanation += `<br>... and ${totalPartial - 5} more similar skills<br>`;
    }

    explanation += `<br>💡 <strong>What this means:</strong> You're close! These skills show you have related experience. Consider learning the exact skills or highlighting how your similar skills apply.`;

    return explanation;
}

// Suggest what to learn first
function suggestLearningPriorities(analysis) {
    const missingTech = analysis.missing.technical;
    const missingSoft = analysis.missing.soft;
    const partialTech = analysis.partially_matched.technical;
    const partialSoft = analysis.partially_matched.soft;

    const totalMissing = missingTech.length + missingSoft.length;

    if (totalMissing === 0) {
        return `<strong>🎯 Learning Recommendations</strong><br><br>🎉 Great news! You have all required skills. Consider:<br><br>• Building deeper expertise in your existing skills<br>• Learning bonus skills that could make you stand out<br>• Getting certifications to validate your skills`;
    }

    let explanation = `<strong>🎯 What to Learn First - Priority Guide</strong><br><br>`;

    // Prioritize: missing technical skills first (usually more critical)
    if (missingTech.length > 0) {
        explanation += `<strong>🔥 HIGH PRIORITY - Technical Skills (${missingTech.length}):</strong><br>`;
        explanation += `Start with these - they're often the most important:<br>`;
        missingTech.slice(0, 3).forEach((skill, idx) => {
            explanation += `${idx + 1}. <strong>${skill}</strong><br>`;
        });
        explanation += `<br>`;
    }

    // Then missing soft skills
    if (missingSoft.length > 0) {
        explanation += `<strong>⭐ MEDIUM PRIORITY - Soft Skills (${missingSoft.length}):</strong><br>`;
        explanation += `These are important for teamwork and communication:<br>`;
        missingSoft.slice(0, 2).forEach((skill, idx) => {
            explanation += `${idx + 1}. <strong>${skill}</strong><br>`;
        });
        explanation += `<br>`;
    }

    // Partially matched skills - easier to build on
    if (partialTech.length > 0 || partialSoft.length > 0) {
        explanation += `<strong>💡 EASIER WINS - Build on Similar Skills:</strong><br>`;
        explanation += `You already have related skills, so these might be faster to learn:<br>`;
        const topPartial = [...partialTech, ...partialSoft]
            .sort((a, b) => b.similarity - a.similarity)
            .slice(0, 2);
        topPartial.forEach((item, idx) => {
            explanation += `${idx + 1}. Learn <strong>${item.jd_skill}</strong> (you already know ${item.resume_skill})<br>`;
        });
        explanation += `<br>`;
    }

    explanation += `💡 <strong>Tip:</strong> Focus on 2-3 skills at a time. Master them before moving to the next ones!`;

    return explanation;
}

// Provide resume improvement tips
function provideResumeTips(analysis) {
    const matched = analysis.matched;
    const extra = analysis.extra;
    const missing = analysis.missing;
    const score = Math.round(analysis.match_percentage);

    let explanation = `<strong>📝 Resume Improvement Tips</strong><br><br>`;

    // Tips based on match score
    if (score >= 80) {
        explanation += `<strong>🎯 You're already strong! Here's how to shine:</strong><br><br>`;
        explanation += `✅ <strong>Highlight your strengths:</strong> Make sure your matching skills are prominent in your resume summary and experience sections.<br><br>`;
        explanation += `✅ <strong>Use your bonus skills:</strong> You have ${extra.technical.length + extra.soft.length} extra skills - mention these to stand out!<br><br>`;
        explanation += `✅ <strong>Quantify achievements:</strong> Add numbers and results to show how you've used these skills successfully.`;
    } else if (score >= 60) {
        explanation += `<strong>💪 Build on your foundation:</strong><br><br>`;
        explanation += `✅ <strong>Emphasize matching skills:</strong> Put your ${matched.technical.length + matched.soft.length} matching skills at the top of your skills section.<br><br>`;
        explanation += `✅ <strong>Show growth:</strong> If you're learning missing skills, mention "Currently learning..." to show initiative.<br><br>`;
        explanation += `✅ <strong>Use action verbs:</strong> Describe how you've used your skills with strong action words (e.g., "Developed", "Implemented", "Led").`;
    } else {
        explanation += `<strong>🚀 Strategic improvements:</strong><br><br>`;
        explanation += `✅ <strong>Reorganize your resume:</strong> Put your matching skills first, even if you have fewer of them.<br><br>`;
        explanation += `✅ <strong>Add relevant projects:</strong> If you're learning missing skills, include personal projects or coursework that demonstrates them.<br><br>`;
        explanation += `✅ <strong>Focus on transferable skills:</strong> Your ${matched.technical.length + matched.soft.length} matching skills are valuable - explain how they apply to this role.<br><br>`;
        explanation += `✅ <strong>Be honest but positive:</strong> Don't claim skills you don't have, but highlight your willingness to learn.`;
    }

    // General tips
    explanation += `<br><br><strong>💡 Universal Tips:</strong><br>`;
    explanation += `• Use keywords from the job description naturally in your resume<br>`;
    explanation += `• Show impact: "Improved X by Y%" is better than "Worked on X"<br>`;
    explanation += `• Keep it concise: Aim for 1-2 pages maximum<br>`;
    explanation += `• Proofread carefully: Typos can hurt your chances`;

    return explanation;
}

function addFollowUpSuggestions(questionType) {
    const suggestions = {
        upload: ["Now try uploading your resume!", "Don't forget to upload the job description too."],
        analyze: ["Ready to run your analysis?", "Make sure both files are uploaded first."],
        results: ["Check out your action plan for next steps!", "You can export your results to save them."],
        export: ["Your reports are ready to download!", "Share these with recruiters or mentors."]
    };

    if (suggestions[questionType] && Math.random() > 0.6) { // Only show sometimes for natural feel
        setTimeout(() => {
            const suggestion = suggestions[questionType][Math.floor(Math.random() * suggestions[questionType].length)];
            addChatbotMessage(`💡 <em>${suggestion}</em>`);
        }, 1500);
    }
}

function clearChat() {
    // Keep only the welcome message
    const welcomeMessage = chatbotBody.querySelector('.chatbot-message.bot');
    chatbotBody.innerHTML = '';
    if (welcomeMessage) {
        chatbotBody.appendChild(welcomeMessage);
    } else {
        // Recreate welcome message if it was cleared
        addChatbotMessage('<strong>👋 Welcome back to SkillGap AI!</strong><br>I\'m here to help you with any questions about using our skill analysis tool!');
    }
}

// Chatbot event listeners
chatbotButton.addEventListener('click', openChatbot);
chatbotClose.addEventListener('click', closeChatbot);

chatbotModal.addEventListener('click', (e) => {
    if (e.target.classList.contains('chatbot-overlay')) {
        closeChatbot();
    }
});

// Attach event listeners to quick buttons
function attachQuickButtonListeners() {
    // Remove old listeners by cloning and replacing
    const newBtns = document.querySelectorAll('.quick-btn');
    newBtns.forEach(btn => {
        // Remove any existing listeners by cloning
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);

        // Add fresh listener
        newBtn.addEventListener('click', () => {
            const questionType = newBtn.getAttribute('data-question');
            const questionText = newBtn.textContent.trim();
            handleQuickQuestion(questionType, questionText);
        });
    });

    // Update quickBtns reference
    quickBtns = document.querySelectorAll('.quick-btn');
}

// Initial attachment
attachQuickButtonListeners();

// Clear chat functionality
const clearChatBtn = document.getElementById('clear-chat');
if (clearChatBtn) {
    clearChatBtn.addEventListener('click', clearChat);
}

function showError(message, type = 'error') {
    const errorModal = document.getElementById('error-modal');
    const errorTitle = document.getElementById('error-title');
    const errorMessage = document.getElementById('error-message');
    const icon = type === 'success' ? '✅' : '❌';
    const title = type === 'success' ? 'Success' : 'Error';

    errorTitle.textContent = title;
    errorMessage.innerHTML = `
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 1.5em;">${icon}</span>
            <div>
                <span style="font-size: 1em;">${message}</span>
            </div>
        </div>
    `;

    // Add appropriate class for styling
    errorModal.classList.remove('success', 'error');
    errorModal.classList.add(type);

    // Show modal
    errorModal.classList.remove('hidden');

    // Focus on close button
    const closeButton = errorModal.querySelector('.modal-close');
    if (closeButton) {
        closeButton.focus();
    }

    // Announce to screen readers
    announceToScreenReader(`${title}: ${message}`, type === 'error' ? 'assertive' : 'polite');

    // Auto-hide success messages faster
    if (type === 'success') {
        setTimeout(() => {
            closeErrorModal();
        }, 3000);
    }
}

function closeErrorModal() {
    const errorModal = document.getElementById('error-modal');
    errorModal.classList.add('hidden');
    errorModal.classList.remove('success', 'error');
    announceToScreenReader('Error modal closed');
}

// Dashboard functionality
document.getElementById('view-dashboard').addEventListener('click', () => {
    if (!analysisData) {
        showError('No analysis data available. Please run an analysis first.');
        return;
    }
    window.open('/dashboard', '_blank');
});

// Export functionality
document.getElementById('export-pdf').addEventListener('click', async () => {
    if (!analysisData) return;

    try {
        const response = await fetch('/export_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...analysisData,
                type: 'pdf'
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'skill_gap_report.pdf';
            a.click();
            showError('✅ PDF report downloaded successfully!', 'success');
        } else {
            const error = await response.json();
            showError('❌ Could not download PDF. Please try again.');
        }
    } catch (error) {
        showError('❌ Could not download PDF. Please check your connection and try again.');
    }
});

document.getElementById('export-csv').addEventListener('click', async () => {
    if (!analysisData) return;

    try {
        const response = await fetch('/export_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...analysisData,
                type: 'csv'
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'skill_gap_report.csv';
            a.click();
            showError('✅ Excel report downloaded successfully!', 'success');
        } else {
            const error = await response.json();
            showError('❌ Could not download Excel file. Please try again.');
        }
    } catch (error) {
        showError('❌ Could not download Excel file. Please check your connection and try again.');
    }
});

document.getElementById('new-analysis').addEventListener('click', () => {
    // Hide results and show upload section
    document.getElementById('upload-section').classList.remove('hidden');
    document.getElementById('results-section').classList.add('hidden');

    // Clear all file inputs
    document.getElementById('resume-upload').value = '';
    document.getElementById('jd-upload').value = '';

    // Clear file name displays
    document.getElementById('resume-name').textContent = 'No file selected';
    document.getElementById('jd-name').textContent = 'No file selected';
    document.getElementById('resume-name').style.color = '#64748b';
    document.getElementById('jd-name').style.color = '#64748b';

    // Hide preview buttons
    const resumeActions = document.getElementById('resume-actions');
    const jdActions = document.getElementById('jd-actions');
    if (resumeActions) resumeActions.style.display = 'none';
    if (jdActions) jdActions.style.display = 'none';

    // Clear analysis data
    analysisData = null;

    // Reset chatbot to default
    resetChatbotToDefault();

    // Destroy existing charts
    if (resumeChart) {
        resumeChart.destroy();
        resumeChart = null;
    }
    if (jdChart) {
        jdChart.destroy();
        jdChart = null;
    }

    // Clear all result displays
    clearAllResults();

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

function clearAllResults() {
    // Clear summary cards
    document.getElementById('match-percentage').textContent = '0%';
    document.getElementById('total-resume-skills').textContent = '0';
    document.getElementById('total-jd-skills').textContent = '0';
    document.getElementById('matched-count').textContent = '0';

    // Reset circular progress ring
    const matchScoreRing = document.getElementById('match-score-ring');
    if (matchScoreRing) {
        const circumference = 2 * Math.PI * 42;
        matchScoreRing.style.strokeDashoffset = circumference;
    }

    // Clear skills displays
    const skillContainers = [
        'matched-technical', 'matched-soft', 'missing-technical', 'missing-soft',
        'extra-technical', 'extra-soft', 'partially-matched'
    ];

    skillContainers.forEach(id => {
        const container = document.getElementById(id);
        if (container) {
            container.innerHTML = '';
        }
    });
}

// File preview functionality
const resumePreviewBtn = document.getElementById('preview-resume');
const jdPreviewBtn = document.getElementById('preview-jd');

// Store scroll position for each preview type
let savedScrollPositions = {
    resume: 0,
    jd: 0
};
let lastPreviewType = null;

if (resumePreviewBtn) {
    resumePreviewBtn.addEventListener('click', () => {
        // Save current scroll position before opening modal
        savedScrollPositions.resume = window.pageYOffset || document.documentElement.scrollTop;
        lastPreviewType = 'resume';
        // Scroll to top of page when preview is clicked
        window.scrollTo({ top: 0, behavior: 'smooth' });
        previewFile('resume-upload', 'Resume Preview');
    });
}

if (jdPreviewBtn) {
    jdPreviewBtn.addEventListener('click', () => {
        // Save current scroll position before opening modal
        savedScrollPositions.jd = window.pageYOffset || document.documentElement.scrollTop;
        lastPreviewType = 'jd';
        // Scroll to top of page when preview is clicked
        window.scrollTo({ top: 0, behavior: 'smooth' });
        previewFile('jd-upload', 'Job Description Preview');
    });
}

document.getElementById('close-preview').addEventListener('click', () => {
    closePreviewModal();
});

document.getElementById('preview-modal').addEventListener('click', (e) => {
    if (e.target.id === 'preview-modal') {
        closePreviewModal();
    }
});

// Error modal event listeners
document.getElementById('close-error').addEventListener('click', () => {
    closeErrorModal();
});

document.getElementById('error-modal').addEventListener('click', (e) => {
    if (e.target.id === 'error-modal') {
        closeErrorModal();
    }
});

function closePreviewModal() {
    const modal = document.getElementById('preview-modal');

    // Clear any scroll prevention timeout and interval
    if (modal._scrollPreventionTimeout) {
        clearTimeout(modal._scrollPreventionTimeout);
        modal._scrollPreventionTimeout = null;
    }
    if (modal._scrollCheckInterval) {
        clearInterval(modal._scrollCheckInterval);
        modal._scrollCheckInterval = null;
    }
    if (modal._modalObserver) {
        modal._modalObserver.disconnect();
        modal._modalObserver = null;
    }

    // Hide the modal
    modal.classList.add('hidden');

    // Small delay to ensure modal is fully hidden before restoring scroll
    setTimeout(() => {
        // Restore the saved scroll position for the last preview type
        if (lastPreviewType && savedScrollPositions[lastPreviewType] !== undefined) {
            const restorePos = savedScrollPositions[lastPreviewType];
            window.scrollTo({ top: restorePos, behavior: 'instant' });
        }
    }, 100);

    announceToScreenReader('File preview modal closed');
}

async function previewFile(inputId, title) {
    const fileInput = document.getElementById(inputId);
    const file = fileInput.files[0];

    if (!file) {
        showError(`❌ No ${title.toLowerCase()} file selected to preview. Please select a file first.`);
        return;
    }

    const modal = document.getElementById('preview-modal');
    const modalTitle = document.getElementById('preview-title');
    const previewContent = document.getElementById('preview-content');

    modalTitle.textContent = title;
    modal.setAttribute('aria-label', `${title} Modal`);
    previewContent.innerHTML = `
        <div class="preview-loading">
            <div class="spinner"></div>
            <p>Loading file contents...</p>
        </div>
    `;

    // Force modal to stay at top BEFORE showing it - ultra aggressive approach
    forceModalScrollToTopAggressive(modal);

    // Temporarily disable smooth scrolling on body to prevent conflicts
    document.body.style.scrollBehavior = 'auto';

    // Show modal
    modal.classList.remove('hidden');

    // Ultimate scroll-to-top solution: combine all techniques
    const ensureTopScroll = () => {
        // Method 1: Direct scroll reset
        const modalBody = modal.querySelector('.modal-body');
        if (modalBody) {
            modalBody.scrollTop = 0;
            modalBody.scrollLeft = 0;
        }

        // Method 2: Scroll window to top to ensure modal is visible from top
        window.scrollTo(0, 0);

        // Method 3: Force modal header into view
        const modalHeader = modal.querySelector('.modal-header');
        if (modalHeader) {
            modalHeader.scrollIntoView({ behavior: 'auto', block: 'start', inline: 'nearest' });
        }
    };

    // Execute immediately
    ensureTopScroll();

    // Execute after animation
    setTimeout(ensureTopScroll, 50);
    setTimeout(ensureTopScroll, 150);
    setTimeout(ensureTopScroll, 300);

    // Continuous monitoring for 3 seconds
    let monitorCount = 0;
    const monitorInterval = setInterval(() => {
        ensureTopScroll();
        monitorCount++;
        if (monitorCount >= 60) { // 60 * 50ms = 3 seconds
            clearInterval(monitorInterval);
        }
    }, 50);

    // Set up MutationObserver to watch for content changes and force scroll to top
    const modalObserver = new MutationObserver(() => {
        ensureTopScroll();
    });

    // Observe changes to the modal body and content
    modalObserver.observe(modal, { childList: true, subtree: true });
    modalObserver.observe(previewContent, { childList: true, subtree: true, attributes: true });

    // Store observer on modal for cleanup
    modal._modalObserver = modalObserver;

    // Multiple aggressive resets with different timing
    setTimeout(() => forceModalScrollToTopAggressive(modal), 0);
    setTimeout(() => forceModalScrollToTopAggressive(modal), 1);
    setTimeout(() => forceModalScrollToTopAggressive(modal), 5);
    setTimeout(() => forceModalScrollToTopAggressive(modal), 10);
    setTimeout(() => forceModalScrollToTopAggressive(modal), 25);
    setTimeout(() => forceModalScrollToTopAggressive(modal), 50);

    // Restore smooth scrolling after modal is stable
    setTimeout(() => {
        document.body.style.scrollBehavior = '';
    }, 100);

    // Focus management for modal - set focus on close button to avoid scrolling
    const closeButton = modal.querySelector('.modal-close');
    if (closeButton) {
        closeButton.focus({ preventScroll: true });
    }

    announceToScreenReader(`Opening ${title} preview modal`);

    try {
        // Send file to backend for proper text extraction
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/preview', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to load preview');
        }

        // Display the extracted content
        const content = data.content;
        const filename = data.filename;
        const fileSize = data.file_size;

        previewContent.innerHTML = `
            <div class="preview-header">
                <h4>📄 ${filename}</h4>
                <p class="preview-meta">Extracted ${fileSize} characters of text content</p>
            </div>
            <div class="preview-text">${content.replace(/\n/g, '<br>')}</div>
        `;

        // Force modal to stay at top after content loads - multiple approaches
        const forceTopAfterLoad = () => {
            const modalBody = modal.querySelector('.modal-body');
            if (modalBody) {
                modalBody.scrollTop = 0;
                modalBody.scrollLeft = 0;
            }
        };

        forceTopAfterLoad();
        setTimeout(forceTopAfterLoad, 1);
        setTimeout(forceTopAfterLoad, 5);
        setTimeout(forceTopAfterLoad, 10);
        setTimeout(forceTopAfterLoad, 50);
        setTimeout(() => forceModalScrollToTopAggressive(modal), 25);
        setTimeout(() => forceModalScrollToTopAggressive(modal), 50);

        // Final reset after content has fully rendered and browser has settled
        setTimeout(() => {
            forceModalScrollToTopAggressive(modal);
        }, 100);

        announceToScreenReader(`File preview loaded for ${filename}`);

    } catch (error) {
        previewContent.innerHTML = `
            <div class="preview-error">
                <h4>❌ Preview Error</h4>
                <p>Unable to load preview for this file.</p>
                <p><strong>Error:</strong> ${error.message}</p>
                <p><em>The file will still be analyzed properly when you click "Analyze Now".</em></p>
            </div>
        `;
        announceToScreenReader(`Error loading file preview: ${error.message}`);
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}