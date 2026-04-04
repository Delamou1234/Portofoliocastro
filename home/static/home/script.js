// Mobile navigation toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const navHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = target.offsetTop - navHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Active link on scroll
window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section');
    const navHeight = document.querySelector('.navbar').offsetHeight;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - navHeight - 100;
        const sectionHeight = section.clientHeight;
        
        if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
});

// Hamburger animation
const style = document.createElement('style');
style.textContent = `
    .hamburger.active span:nth-child(2) {
        opacity: 0;
    }
    
    .hamburger.active span:nth-child(1) {
        transform: translateY(8px) rotate(45deg);
    }
    
    .hamburger.active span:nth-child(3) {
        transform: translateY(-8px) rotate(-45deg);
    }
    
    @media (max-width: 768px) {
        .hamburger {
            display: flex;
        }
        
        .nav-menu {
            position: fixed;
            left: -100%;
            top: 80px;
            flex-direction: column;
            background: white;
            width: 100%;
            text-align: center;
            transition: 0.3s;
            box-shadow: 0 10px 27px rgba(0, 0, 0, 0.05);
            padding: 20px 0;
        }
        
        .nav-menu.active {
            left: 0;
        }
        
        .nav-menu ul {
            flex-direction: column;
            gap: 20px;
        }
    }
`;
document.head.appendChild(style);

// Counter Animation
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const updateCounter = () => {
        start += increment;
        if (start < target) {
            element.textContent = Math.ceil(start) + '+';
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target + '+';
        }
    };
    
    updateCounter();
}

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            
            // Animate counters when visible
            if (entry.target.classList.contains('stat-item')) {
                const counterNumber = entry.target.querySelector('.counter-number');
                if (counterNumber && !counterNumber.classList.contains('animated')) {
                    counterNumber.classList.add('animated');
                    const target = parseInt(counterNumber.textContent);
                    animateCounter(counterNumber, target);
                }
            }
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.stat-item, .skill-category, .project-card');
    animateElements.forEach(el => observer.observe(el));
});

// Form Validation and Submission
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        const name = contactForm.querySelector('input[name="name"]').value;
        const email = contactForm.querySelector('input[name="email"]').value;
        const subject = contactForm.querySelector('input[name="subject"]').value;
        const message = contactForm.querySelector('textarea[name="message"]').value;

        if (!name || !email || !subject || !message) {
            e.preventDefault();
            showNotification('Veuillez remplir tous les champs', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            e.preventDefault();
            showNotification('Veuillez entrer une adresse email valide', 'error');
            return;
        }

        // Leave the form submission to Django so the contact message is stored and email can be envoyé.
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Notification System
function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    switch (type) {
        case 'success':
            notification.style.background = '#28a745';
            break;
        case 'error':
            notification.style.background = '#dc3545';
            break;
        default:
            notification.style.background = '#4A90E2';
    }
    
    document.body.appendChild(notification);
    
    requestAnimationFrame(() => {
        notification.style.transform = 'translateX(0)';
    });
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.addEventListener('transitionend', () => notification.remove());
    }, 3000);
}

// Chat widget logic
const chatToggle = document.getElementById('chat-toggle');
const chatClose = document.getElementById('chat-close');
const chatPanel = document.getElementById('chat-panel');
const chatForm = document.getElementById('chat-form');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatWidget = document.getElementById('chat-widget');

// Draggable chat widget
let isDragging = false;
let dragOffsetX = 0;
let dragOffsetY = 0;

if (chatWidget) {
    // Charger la position sauvegardee
    const savedPosition = localStorage.getItem('chatWidgetPosition');
    if (savedPosition) {
        try {
            const pos = JSON.parse(savedPosition);
            chatWidget.style.right = 'auto';
            chatWidget.style.bottom = 'auto';
            chatWidget.style.left = pos.left + 'px';
            chatWidget.style.top = pos.top + 'px';
        } catch (e) {
            // Ignorer les erreurs de parsing
        }
    }

    // Fonction pour demarrer le drag
    function startDrag(e) {
        // Ne pas draguer si on clique sur le bouton toggle ou le panel
        if (e.target.closest('.chat-toggle') || e.target.closest('.chat-panel')) {
            return;
        }
        
        isDragging = true;
        chatWidget.classList.add('dragging');
        
        const rect = chatWidget.getBoundingClientRect();
        dragOffsetX = e.clientX - rect.left;
        dragOffsetY = e.clientY - rect.top;
        
        e.preventDefault();
    }

    // Fonction pour demarrer le drag sur mobile
    function startDragTouch(e) {
        if (e.target.closest('.chat-toggle') || e.target.closest('.chat-panel')) {
            return;
        }
        
        isDragging = true;
        chatWidget.classList.add('dragging');
        
        const touch = e.touches[0];
        const rect = chatWidget.getBoundingClientRect();
        dragOffsetX = touch.clientX - rect.left;
        dragOffsetY = touch.clientY - rect.top;
        
        e.preventDefault();
    }

    // Fonction pour effectuer le drag
    function doDrag(e) {
        if (!isDragging) return;
        
        const newX = e.clientX - dragOffsetX;
        const newY = e.clientY - dragOffsetY;
        
        // Limiter aux bords de la fenetre
        const maxX = window.innerWidth - chatWidget.offsetWidth;
        const maxY = window.innerHeight - chatWidget.offsetHeight;
        
        const clampedX = Math.max(0, Math.min(newX, maxX));
        const clampedY = Math.max(0, Math.min(newY, maxY));
        
        chatWidget.style.right = 'auto';
        chatWidget.style.bottom = 'auto';
        chatWidget.style.left = clampedX + 'px';
        chatWidget.style.top = clampedY + 'px';
    }

    // Fonction pour effectuer le drag sur mobile
    function doDragTouch(e) {
        if (!isDragging) return;
        
        const touch = e.touches[0];
        const newX = touch.clientX - dragOffsetX;
        const newY = touch.clientY - dragOffsetY;
        
        const maxX = window.innerWidth - chatWidget.offsetWidth;
        const maxY = window.innerHeight - chatWidget.offsetHeight;
        
        const clampedX = Math.max(0, Math.min(newX, maxX));
        const clampedY = Math.max(0, Math.min(newY, maxY));
        
        chatWidget.style.right = 'auto';
        chatWidget.style.bottom = 'auto';
        chatWidget.style.left = clampedX + 'px';
        chatWidget.style.top = clampedY + 'px';
    }

    // Fonction pour arreter le drag
    function stopDrag() {
        if (isDragging) {
            isDragging = false;
            chatWidget.classList.remove('dragging');
            
            // Sauvegarder la position
            const rect = chatWidget.getBoundingClientRect();
            localStorage.setItem('chatWidgetPosition', JSON.stringify({
                left: rect.left,
                top: rect.top
            }));
        }
    }

    // Evenements souris
    chatWidget.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', doDrag);
    document.addEventListener('mouseup', stopDrag);

    // Evenements tactiles
    chatWidget.addEventListener('touchstart', startDragTouch, { passive: false });
    document.addEventListener('touchmove', doDragTouch, { passive: false });
    document.addEventListener('touchend', stopDrag);
}

if (chatToggle && chatPanel) {
    chatToggle.addEventListener('click', () => {
        chatPanel.classList.toggle('open');
        chatPanel.setAttribute('aria-hidden', chatPanel.classList.contains('open') ? 'false' : 'true');
        if (chatPanel.classList.contains('open')) {
            chatInput.focus();
        }
    });
}

if (chatClose && chatPanel) {
    chatClose.addEventListener('click', () => {
        chatPanel.classList.remove('open');
        chatPanel.setAttribute('aria-hidden', 'true');
    });
}

function addChatMessage(text, type) {
    const messageElement = document.createElement('div');
    messageElement.className = `chat-message ${type}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    const now = new Date();
    timeSpan.textContent = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeSpan);
    messageElement.appendChild(contentDiv);
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageElement;
}

async function sendChatMessage(message) {
    try {
        const csrfInput = document.querySelector('#chat-csrf-form [name="csrfmiddlewaretoken"]');
        const csrfToken = csrfInput ? csrfInput.value : '';

        const response = await fetch(window.chatApiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erreur de communication avec le serveur.');
        }

        return data;
    } catch (error) {
        console.error('Chat Error:', error);
        throw error;
    }
}

if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) {
            showNotification('Écris une question avant d\'envoyer.', 'error');
            return;
        }

        addChatMessage(message, 'visitor');
        chatInput.value = '';
        const loadingMessage = addChatMessage('...', 'bot');

        try {
            const data = await sendChatMessage(message);
            loadingMessage.remove();
            if (data.answer) {
                addChatMessage(data.answer, 'bot');
            } else {
                addChatMessage('Désolé, je n\'ai pas pu récupérer de réponse.', 'bot');
            }
        } catch (error) {
            loadingMessage.remove();
            addChatMessage('Impossible de contacter le service de chat pour le moment.', 'bot');
            console.error(error);
        }
    });
}
