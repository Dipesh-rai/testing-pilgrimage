// header
const header = document.querySelector('.site-header');
let isScrolled = false;

window.addEventListener('scroll', () => {
    if(window.scrollY > 50 && !isScrolled){
        header.classList.add('scrolled');
        isScrolled = true;
    } else if (window.scrollY < 10 && isScrolled) {
        header.classList.remove('scrolled');
        isScrolled = false;
    }
})


document.addEventListener('click', function (event) {
    const collapseIds = ['multiCollapseExample1','multiCollapseExample3'];

    collapseIds.forEach(id => {
        const collapse = document.getElementById(id);
        const trigger = document.querySelector(`[data-bs-toggle="collapse"][href="#${id}"]`);

        if (!collapse || !trigger) return;

        const isInsideCollapse = collapse.contains(event.target);
        const isInsideTrigger = trigger.contains(event.target);

        if (!isInsideCollapse && !isInsideTrigger && collapse.classList.contains('show')) {
            const collapseInstance = bootstrap.Collapse.getInstance(collapse);
            if (collapseInstance) {
                collapseInstance.hide();
            }
        }
    });
});

// subscribtion
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('subscription-form');
    const emailInput = document.getElementById('email-input');
    const messageDiv = document.getElementById('subscription-message') || createMessageDiv();
    
    function createMessageDiv() {
        const div = document.createElement('div');
        div.id = 'subscription-message';
        div.style.marginTop = '10px';
        form.parentNode.insertBefore(div, form.nextSibling);
        return div;
    }

    // Real-time email check
    emailInput.addEventListener('input', function() {
        const email = this.value.trim();
        if (email.length > 3 && email.includes('@')) {
            fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({email: email})
            })
            .then(handleResponse)
            .catch(handleError);
        }
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        
        fetch(window.location.pathname, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
        .then(handleResponse)
        .catch(handleError);
    });

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    function handleResponse(response) {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json().then(data => {
            if (data.exists !== undefined) {
                messageDiv.innerHTML = data.exists 
                    ? '<span style="color: orange;">Email already subscribed</span>'
                    : '<span style="color: green;">Email available</span>';
            } else {
                messageDiv.innerHTML = `<span style="color: ${data.status === 'success' ? 'green' : 'red'};">${data.message}</span>`;
                if (data.status === 'success') form.reset();
            }
        });
    }

    function handleError(error) {
        console.error('Error:', error);
        messageDiv.innerHTML = '<span style="color: red;">An error occurred. Please try again.</span>';
    }
});

// gallery
document.addEventListener('DOMContentLoaded', function() {
    const galleryItems = document.querySelectorAll('.gallery-items');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const imageInfo = document.getElementById('image-info');
    const closeBtn = document.querySelector('.close-btn');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    let currentImageIndex = 0;
    
    // Create image data array from HTML elements
    const images = Array.from(galleryItems).map(item => {
        const img = item.querySelector('.gallery-img');
        return {
            src: img.src,
            alt: img.alt,
            info: img.alt // Using alt text as info, you can add data-info attribute if needed
        };
    });

    // Add click event to each gallery item
    galleryItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            currentImageIndex = index;
            updateLightboxImage();
            lightbox.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    });

    // Close lightbox
    closeBtn.addEventListener('click', () => {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';
    });

    // Close when clicking outside the image
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Previous image
    prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        updateLightboxImage();
    });

    // Next image
    nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        currentImageIndex = (currentImageIndex + 1) % images.length;
        updateLightboxImage();
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (lightbox.style.display === 'block') {
            if (e.key === 'ArrowLeft') {
                currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
                updateLightboxImage();
            } else if (e.key === 'ArrowRight') {
                currentImageIndex = (currentImageIndex + 1) % images.length;
                updateLightboxImage();
            } else if (e.key === 'Escape') {
                lightbox.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        }
    });

    // Update lightbox image
    function updateLightboxImage() {
        const image = images[currentImageIndex];
        lightboxImg.src = image.src;
        lightboxImg.alt = image.alt;
        imageInfo.textContent = image.info;
    }
});

// contact
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const submitText = submitButton.querySelector('.submit-text');
            const spinner = submitButton.querySelector('.spinner');
            const formTitle = document.querySelector('.form-title'); // Get the heading element
            
            // Show loading state
            submitText.style.display = 'none';
            spinner.style.display = 'inline-block';
            submitButton.disabled = true;
            
            const formData = new FormData(contactForm);
            
            fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': contactForm.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Hide form elements
                    contactForm.style.display = 'none';
                    formTitle.style.display = 'none'; // Hide the heading
                    
                    // Show success message
                    document.getElementById('successMessage').style.display = 'block';
                    
                    // Optional animation
                    document.getElementById('successMessage').classList.add('animate-fade-in');
                } else {
                    // Error handling remains the same
                    document.querySelectorAll('.error-message').forEach(el => el.remove());
                    
                    if (data.errors) {
                        Object.entries(data.errors).forEach(([field, messages]) => {
                            const input = contactForm.querySelector(`[name="${field}"]`);
                            if (input) {
                                const errorDiv = document.createElement('div');
                                errorDiv.className = 'error-message text-danger mt-1 small';
                                errorDiv.textContent = messages[0];
                                input.closest('.form-group').appendChild(errorDiv);
                            }
                        });
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred. Please try again.', 'error');
            })
            .finally(() => {
                // Reset button state
                submitText.style.display = 'inline-block';
                spinner.style.display = 'none';
                submitButton.disabled = false;
            });
        });
    }
});

// Close Top Banner
const closeBanner = document.getElementById("closeBanner");

closeBanner.addEventListener("click", () => {
  noticeBanner.style.display = "none";
});

