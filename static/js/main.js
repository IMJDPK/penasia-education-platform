// PenAsia Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeCarousel();
    initializeFormValidation();
    initializeSmoothScrolling();
    initializeImageLazyLoading();
    initializeLanguageSwitcher();
    initializeMultiStepApplication();
    initializeMobileMenu();
    initializeNavbarScroll();
    
    // Add fade-in animation to elements
    addFadeInAnimation();
});

// Multi-Step Application Form
function initializeMultiStepApplication() {
    const form = document.getElementById('applicationForm');
    if (!form) return;
    
    let currentStep = 1;
    const totalSteps = 3;
    
    // Program selection handling
    const programOptions = document.querySelectorAll('.program-option');
    const selectedProgramInput = document.getElementById('selectedProgram');
    
    programOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Prevent selection of disabled courses
            if (this.classList.contains('disabled') || this.dataset.active === 'false') {
                return;
            }
            
            // Remove previous selection
            programOptions.forEach(opt => opt.classList.remove('selected'));
            
            // Add selection to clicked option
            this.classList.add('selected');
            
            // Update hidden input
            selectedProgramInput.value = this.dataset.program;
            
            // Hide error message
            document.getElementById('program-error').style.display = 'none';
        });
    });
    
    // Step navigation functions
    window.nextStep = function() {
        if (validateCurrentStep(currentStep)) {
            hideStep(currentStep);
            currentStep++;
            showStep(currentStep);
            updateStepIndicator();
        }
    };
    
    window.prevStep = function() {
        hideStep(currentStep);
        currentStep--;
        showStep(currentStep);
        updateStepIndicator();
    };
    
    function validateCurrentStep(step) {
        if (step === 1) {
            // Validate program selection
            if (!selectedProgramInput.value) {
                document.getElementById('program-error').style.display = 'block';
                return false;
            }
        } else if (step === 2) {
            // Validate personal details
            const requiredFields = document.querySelectorAll('#step-2 [required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            return isValid;
        }
        return true;
    }
    
    function hideStep(step) {
        const stepElement = document.getElementById(`step-${step}`);
        if (stepElement) {
            stepElement.classList.remove('active');
        }
    }
    
    function showStep(step) {
        const stepElement = document.getElementById(`step-${step}`);
        if (stepElement) {
            stepElement.classList.add('active');
            stepElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    
    function updateStepIndicator() {
        for (let i = 1; i <= totalSteps; i++) {
            const indicator = document.getElementById(`step-${i}-indicator`);
            if (indicator) {
                indicator.classList.remove('active', 'completed');
                
                if (i < currentStep) {
                    indicator.classList.add('completed');
                } else if (i === currentStep) {
                    indicator.classList.add('active');
                }
            }
        }
    }
    
    // Form submission handling
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (currentStep === 3) {
            // Final validation and submission
            if (validateFinalStep()) {
                submitApplication();
            }
        }
    });
    
    function validateFinalStep() {
        const requiredCheckboxes = document.querySelectorAll('#step-3 [required][type="checkbox"]');
        let isValid = true;
        
        requiredCheckboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                checkbox.classList.add('is-invalid');
                isValid = false;
            } else {
                checkbox.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }
    
    function submitApplication() {
        // Show loading state
        const submitBtn = document.querySelector('#step-3 .btn-nav-success');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Submitting...';
        submitBtn.disabled = true;
        
        // Collect form data
        const formData = new FormData(form);
        
        // Submit via AJAX
        fetch(form.action || '/apply', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message
                showSuccessMessage();
            } else {
                // Show error message
                showErrorMessage(data.error || 'Application submission failed. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage('Network error. Please check your connection and try again.');
        })
        .finally(() => {
            // Restore button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    }
    
    function showSuccessMessage() {
        const successHtml = `
            <div class="text-center py-5">
                <i class="fas fa-check-circle text-success" style="font-size: 4rem; margin-bottom: 2rem;"></i>
                <h2 class="text-success mb-3">Application Submitted Successfully!</h2>
                <p class="lead mb-4">Thank you for applying to PenAsia. We will review your application and contact you within 2-3 business days.</p>
                <div class="alert alert-info">
                    <h6><i class="fas fa-info-circle me-2"></i>Next Steps:</h6>
                    <ul class="text-start">
                        <li>Check your email for a confirmation message</li>
                        <li>Prepare required documents for interview</li>
                        <li>Our admissions team will contact you soon</li>
                    </ul>
                </div>
                <div class="mt-4">
                    <a href="/" class="btn btn-primary me-3">Return to Homepage</a>
                    <a href="https://wa.me/85228936788?text=I%20just%20submitted%20my%20application%20and%20have%20questions" 
                       class="btn btn-success" target="_blank">
                        <i class="fab fa-whatsapp me-2"></i>WhatsApp Us
                    </a>
                </div>
            </div>
        `;
        
        document.querySelector('.form-content').innerHTML = successHtml;
    }
    
    function showErrorMessage(message) {
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger alert-dismissible fade show';
        errorAlert.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const formContent = document.querySelector('.form-content');
        formContent.insertBefore(errorAlert, formContent.firstChild);
        
        // Scroll to error
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Carousel initialization and controls
function initializeCarousel() {
    const carousel = document.querySelector('#heroCarousel');
    if (carousel) {
        // Auto-advance carousel every 5 seconds
        const carouselInstance = new bootstrap.Carousel(carousel, {
            interval: 5000,
            pause: 'hover'
        });
        
        // Pause video when carousel slides change
        carousel.addEventListener('slide.bs.carousel', function() {
            const videos = carousel.querySelectorAll('video');
            videos.forEach(video => {
                video.pause();
            });
        });
    }
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Real-time validation for specific fields
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', validateEmail);
    });
    
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', validatePhone);
    });
}

// Email validation
function validateEmail(event) {
    const email = event.target.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(email);
    
    if (email && !isValid) {
        event.target.setCustomValidity('Please enter a valid email address');
    } else {
        event.target.setCustomValidity('');
    }
}

// Phone validation (Hong Kong format)
function validatePhone(event) {
    const phone = event.target.value;
    const phoneRegex = /^[0-9+\-\s\(\)]{8,15}$/;
    const isValid = phoneRegex.test(phone);
    
    if (phone && !isValid) {
        event.target.setCustomValidity('Please enter a valid phone number');
    } else {
        event.target.setCustomValidity('');
    }
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                event.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Lazy loading for images
function initializeImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// Language switcher functionality
function initializeLanguageSwitcher() {
    const languageLinks = document.querySelectorAll('[href*="lang="]');
    
    languageLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // Store language preference
            const url = new URL(this.href);
            const lang = url.searchParams.get('lang');
            localStorage.setItem('preferred_language', lang);
            
            // Show loading indicator
            showLoadingIndicator();
        });
    });
    
    // Apply stored language preference
    const preferredLang = localStorage.getItem('preferred_language');
    if (preferredLang && !window.location.search.includes('lang=')) {
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('lang', preferredLang);
        window.location.href = currentUrl.toString();
    }
}

// Loading indicator
function showLoadingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'loading-indicator';
    indicator.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="sr-only">Loading...</span></div>';
    indicator.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 9999;
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 8px;
    `;
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.remove();
    }, 3000);
}

// Fade-in animations
function addFadeInAnimation() {
    const animatedElements = document.querySelectorAll('.card, .stat-item, .testimonial-card');
    
    if ('IntersectionObserver' in window) {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    animationObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        
        animatedElements.forEach(element => {
            animationObserver.observe(element);
        });
    }
}

// Course application form handling
function handleCourseApplication(courseId) {
    const form = document.getElementById('applicationForm');
    if (form) {
        const courseInput = form.querySelector('input[name="course"]');
        if (courseInput) {
            courseInput.value = courseId;
        }
        
        // Scroll to form
        form.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        
        // Focus on first input
        const firstInput = form.querySelector('input, select, textarea');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 500);
        }
    }
}

// Image gallery functionality
function initializeImageGallery() {
    const galleryImages = document.querySelectorAll('.gallery-img');
    
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            openImageModal(this.src, this.alt);
        });
    });
}

// Image modal
function openImageModal(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeImageModal()">
            <div class="modal-content">
                <img src="${src}" alt="${alt}" class="modal-image">
                <button class="modal-close" onclick="closeImageModal()">&times;</button>
            </div>
        </div>
    `;
    
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
}

function closeImageModal() {
    const modal = document.querySelector('.image-modal');
    if (modal) {
        modal.remove();
        document.body.style.overflow = '';
    }
}

// Utility functions
function formatCurrency(amount, currency = 'HKD') {
    return new Intl.NumberFormat('en-HK', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(date, locale = 'en-HK') {
    return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput && searchResults) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
            }
        });
    }
}

function performSearch(query) {
    // This would typically make an AJAX request to the server
    // For now, we'll simulate a search
    const results = [
        { title: 'Hotel Culinary Management', url: '/course/169', type: 'Course' },
        { title: 'BTEC Business Management', url: '/course/btec', type: 'Course' },
        { title: 'Western Bakery Certificate', url: '/course/171', type: 'Course' },
        { title: 'Admissions Requirements', url: '/admissions', type: 'Page' }
    ].filter(item => 
        item.title.toLowerCase().includes(query.toLowerCase())
    );
    
    displaySearchResults(results);
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    
    if (results.length > 0) {
        searchResults.innerHTML = results.map(result => `
            <div class="search-result-item">
                <a href="${result.url}" class="search-result-link">
                    <strong>${result.title}</strong>
                    <small class="text-muted">${result.type}</small>
                </a>
            </div>
        `).join('');
        searchResults.style.display = 'block';
    } else {
        searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
        searchResults.style.display = 'block';
    }
}

// Export functions for global access
window.handleCourseApplication = handleCourseApplication;
window.closeImageModal = closeImageModal;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;

// CEF Calculator Function
function calculateCEF() {
    const courseFeeElement = document.getElementById('course-fee');
    const cefStatusElement = document.getElementById('cef-status');
    const maxReimbursementElement = document.getElementById('max-reimbursement');
    const actualReimbursementElement = document.getElementById('actual-reimbursement');
    const netCostElement = document.getElementById('net-cost');
    
    if (!courseFeeElement || !cefStatusElement) return;
    
    const courseFee = parseInt(courseFeeElement.getAttribute('data-fee'));
    const cefStatus = cefStatusElement.value;
    
    // Calculate reimbursement rate
    const reimbursementRate = cefStatus === 'first' ? 0.8 : 0.6; // 80% for first-time, 60% for returning
    const maxReimbursement = 25000; // HK$25,000 maximum
    
    // Calculate actual reimbursement
    const calculatedReimbursement = courseFee * reimbursementRate;
    const actualReimbursement = Math.min(calculatedReimbursement, maxReimbursement);
    
    // Calculate net cost
    const netCost = courseFee - actualReimbursement;
    
    // Update display
    actualReimbursementElement.textContent = actualReimbursement.toLocaleString();
    netCostElement.textContent = netCost.toLocaleString();
    
    // Update maximum reimbursement display
    maxReimbursementElement.textContent = maxReimbursement.toLocaleString();
}

// Initialize CEF calculator on page load
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('cef-status')) {
        calculateCEF(); // Calculate initial values
    }
});

// Make calculateCEF globally available
window.calculateCEF = calculateCEF;

// Mobile Menu Toggle
function initializeMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (!mobileToggle || !navbarMenu) return;
    
    // Toggle mobile menu
    mobileToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        navbarMenu.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (navbarMenu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });
    
    // Close menu when clicking on nav links
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                mobileToggle.classList.remove('active');
                navbarMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!mobileToggle.contains(e.target) && !navbarMenu.contains(e.target)) {
            mobileToggle.classList.remove('active');
            navbarMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            mobileToggle.classList.remove('active');
            navbarMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// Navbar Scroll Effect
function initializeNavbarScroll() {
    const navbar = document.querySelector('.navbar-premium');
    const logo = document.querySelector('.navbar-brand-premium img');
    
    if (!navbar || !logo) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
            logo.style.height = '70px';
        } else {
            navbar.classList.remove('scrolled');
            logo.style.height = '150px';
        }
    });
}
