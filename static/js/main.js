// UrbanEase - Main JavaScript File

// Global variables
let currentUser = null;
let websocket = null;
let notifications = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadUserData();
    setupWebSocket();
});

// Initialize the main application
function initializeApp() {
    console.log('UrbanEase app initializing...');
    
    // Add loading animation
    addLoadingAnimation();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize charts if they exist
    initializeCharts();
    
    // Setup real-time updates
    setupRealTimeUpdates();
    
    // Remove loading animation after initialization
    setTimeout(() => {
        removeLoadingAnimation();
    }, 1000);
}

// Setup event listeners
function setupEventListeners() {
    // Form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
    
    // Search functionality
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(handleSearch, 300));
    });
    
    // Modal events
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', handleModalShow);
        modal.addEventListener('hidden.bs.modal', handleModalHide);
    });
    
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', handleNavClick);
    });
    
    // Scroll events
    window.addEventListener('scroll', debounce(handleScroll, 100));
    
    // Resize events
    window.addEventListener('resize', debounce(handleResize, 250));
}

// Load user data
function loadUserData() {
    const userData = localStorage.getItem('urbanEaseUser');
    if (userData) {
        currentUser = JSON.parse(userData);
        updateUserInterface();
    }
}

// Setup WebSocket connection
function setupWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/updates/`;
    
    try {
        websocket = new WebSocket(wsUrl);
        
        websocket.onopen = function(e) {
            console.log('WebSocket connected');
            sendWebSocketMessage({
                type: 'subscribe',
                user_id: currentUser?.id || 'anonymous'
            });
        };
        
        websocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            handleWebSocketMessage(data);
        };
        
        websocket.onclose = function(e) {
            console.log('WebSocket disconnected');
            // Attempt to reconnect after 5 seconds
            setTimeout(setupWebSocket, 5000);
        };
        
        websocket.onerror = function(e) {
            console.error('WebSocket error:', e);
        };
    } catch (error) {
        console.error('WebSocket setup failed:', error);
    }
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'transport_update':
            updateTransportInfo(data.payload);
            break;
        case 'traffic_alert':
            showTrafficAlert(data.payload);
            break;
        case 'emergency_alert':
            showEmergencyAlert(data.payload);
            break;
        case 'notification':
            showNotification(data.payload);
            break;
        default:
            console.log('Unknown WebSocket message type:', data.type);
    }
}

// Send WebSocket message
function sendWebSocketMessage(message) {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify(message));
    }
}

// API Functions
const API = {
    baseUrl: '/api/v1/',
    
    // Generic API call
    async call(endpoint, options = {}) {
        const url = this.baseUrl + endpoint;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    },
    
    // GET request
    async get(endpoint) {
        return this.call(endpoint, { method: 'GET' });
    },
    
    // POST request
    async post(endpoint, data) {
        return this.call(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    // PUT request
    async put(endpoint, data) {
        return this.call(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    // DELETE request
    async delete(endpoint) {
        return this.call(endpoint, { method: 'DELETE' });
    }
};

// Transport Functions
const TransportAPI = {
    async searchRoutes(from, to) {
        return API.post('mobility/routes/search/', { from, to });
    },
    
    async getLiveUpdates() {
        return API.get('mobility/live-updates/');
    },
    
    async findParking(location, radius) {
        return API.post('mobility/parking/search/', { location, radius });
    },
    
    async findChargingStations(chargerType) {
        return API.post('mobility/charging/search/', { charger_type: chargerType });
    }
};

// Health Functions
const HealthAPI = {
    async getHealthMetrics() {
        return API.get('health/metrics/');
    },
    
    async bookAppointment(data) {
        return API.post('health/appointments/', data);
    },
    
    async getEmergencyServices() {
        return API.get('health/emergency-services/');
    }
};

// Safety Functions
const SafetyAPI = {
    async getAlerts() {
        return API.get('safety/alerts/');
    },
    
    async reportIncident(data) {
        return API.post('safety/incidents/', data);
    },
    
    async getSafetyChecks() {
        return API.get('safety/checks/');
    }
};

// Services Functions
const ServicesAPI = {
    async getServices() {
        return API.get('services/list/');
    },
    
    async requestService(data) {
        return API.post('services/requests/', data);
    },
    
    async getEcoPoints() {
        return API.get('services/eco-points/');
    }
};

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function getCSRFToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border text-primary';
    spinner.setAttribute('role', 'status');
    spinner.innerHTML = '<span class="visually-hidden">Loading...</span>';
    
    element.appendChild(spinner);
    element.style.opacity = '0.6';
}

function hideLoading(element) {
    const spinner = element.querySelector('.spinner-border');
    if (spinner) {
        spinner.remove();
    }
    element.style.opacity = '1';
}

function addLoadingAnimation() {
    const loader = document.createElement('div');
    loader.id = 'app-loader';
    loader.className = 'position-fixed w-100 h-100 d-flex justify-content-center align-items-center bg-white';
    loader.style.cssText = 'top: 0; left: 0; z-index: 9999;';
    loader.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h5>Loading UrbanEase...</h5>
        </div>
    `;
    
    document.body.appendChild(loader);
}

function removeLoadingAnimation() {
    const loader = document.getElementById('app-loader');
    if (loader) {
        loader.remove();
    }
}

// Event Handlers
function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
        showLoading(submitBtn);
    }
    
    // Handle form submission based on form ID or action
    const formId = form.id || form.action;
    
    switch (formId) {
        case 'route-search-form':
            handleRouteSearch(form);
            break;
        case 'parking-search-form':
            handleParkingSearch(form);
            break;
        case 'health-appointment-form':
            handleHealthAppointment(form);
            break;
        case 'safety-report-form':
            handleSafetyReport(form);
            break;
        default:
            console.log('Unknown form:', formId);
    }
}

function handleSearch(event) {
    const query = event.target.value;
    const searchType = event.target.dataset.searchType;
    
    if (query.length < 2) return;
    
    // Implement search functionality based on type
    switch (searchType) {
        case 'routes':
            searchRoutes(query);
            break;
        case 'parking':
            searchParking(query);
            break;
        case 'services':
            searchServices(query);
            break;
    }
}

function handleModalShow(event) {
    const modal = event.target;
    const modalId = modal.id;
    
    // Load modal content based on type
    switch (modalId) {
        case 'liveUpdatesModal':
            loadLiveUpdates();
            break;
        case 'parkingModal':
            loadParkingOptions();
            break;
    }
}

function handleModalHide(event) {
    const modal = event.target;
    const modalId = modal.id;
    
    // Clean up modal data
    console.log('Modal hidden:', modalId);
}

function handleNavClick(event) {
    const link = event.target;
    const href = link.getAttribute('href');
    
    // Track navigation
    if (typeof gtag !== 'undefined') {
        gtag('event', 'navigation', {
            'event_category': 'navigation',
            'event_label': href
        });
    }
}

function handleScroll(event) {
    // Implement scroll-based animations
    const scrolled = window.pageYOffset;
    const parallax = document.querySelectorAll('.parallax');
    
    parallax.forEach(element => {
        const speed = element.dataset.speed || 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
}

function handleResize(event) {
    // Handle responsive design adjustments
    const width = window.innerWidth;
    
    if (width < 768) {
        // Mobile adjustments
        document.body.classList.add('mobile-view');
    } else {
        document.body.classList.remove('mobile-view');
    }
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize charts
function initializeCharts() {
    const chartElements = document.querySelectorAll('canvas[data-chart]');
    
    chartElements.forEach(canvas => {
        const chartType = canvas.dataset.chart;
        const chartData = JSON.parse(canvas.dataset.chartData || '{}');
        
        createChart(canvas, chartType, chartData);
    });
}

// Create chart
function createChart(canvas, type, data) {
    const ctx = canvas.getContext('2d');
    
    const config = {
        type: type,
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Setup real-time updates
function setupRealTimeUpdates() {
    // Update every 30 seconds
    setInterval(() => {
        updateLiveData();
    }, 30000);
}

// Update live data
async function updateLiveData() {
    try {
        const updates = await API.get('live-updates/');
        updateDashboard(updates);
    } catch (error) {
        console.error('Failed to update live data:', error);
    }
}

// Update dashboard with live data
function updateDashboard(data) {
    // Update transport info
    if (data.transport) {
        updateTransportInfo(data.transport);
    }
    
    // Update safety alerts
    if (data.alerts) {
        updateSafetyAlerts(data.alerts);
    }
    
    // Update health metrics
    if (data.health) {
        updateHealthMetrics(data.health);
    }
}

// Update transport information
function updateTransportInfo(data) {
    const transportElements = document.querySelectorAll('[data-transport-id]');
    
    transportElements.forEach(element => {
        const transportId = element.dataset.transportId;
        const transportData = data.find(t => t.id === transportId);
        
        if (transportData) {
            element.querySelector('.status').textContent = transportData.status;
            element.querySelector('.eta').textContent = transportData.eta;
        }
    });
}

// Show traffic alert
function showTrafficAlert(alert) {
    const alertContainer = document.getElementById('trafficAlerts');
    if (alertContainer) {
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${alert.severity} mb-2`;
        alertElement.innerHTML = `
            <small><strong>${alert.title}</strong><br>${alert.message}</small>
        `;
        
        alertContainer.insertBefore(alertElement, alertContainer.firstChild);
        
        // Remove after 5 minutes
        setTimeout(() => {
            alertElement.remove();
        }, 300000);
    }
}

// Show emergency alert
function showEmergencyAlert(alert) {
    const modal = new bootstrap.Modal(document.getElementById('emergencyModal'));
    const modalBody = document.getElementById('emergencyModalBody');
    
    modalBody.innerHTML = `
        <div class="alert alert-danger">
            <h5><i class="fas fa-exclamation-triangle me-2"></i>Emergency Alert</h5>
            <p><strong>${alert.title}</strong></p>
            <p>${alert.message}</p>
            <p><small>Location: ${alert.location}</small></p>
        </div>
    `;
    
    modal.show();
}

// Update user interface
function updateUserInterface() {
    if (currentUser) {
        // Update user-specific elements
        const userElements = document.querySelectorAll('[data-user-field]');
        
        userElements.forEach(element => {
            const field = element.dataset.userField;
            if (currentUser[field]) {
                element.textContent = currentUser[field];
            }
        });
        
        // Update eco points
        updateEcoPoints();
    }
}

// Update eco points display
async function updateEcoPoints() {
    try {
        const ecoPoints = await ServicesAPI.getEcoPoints();
        const pointsElement = document.getElementById('ecoPoints');
        if (pointsElement) {
            pointsElement.textContent = ecoPoints.total_points;
        }
    } catch (error) {
        console.error('Failed to update eco points:', error);
    }
}

// Export functions for use in templates
window.UrbanEase = {
    API,
    TransportAPI,
    HealthAPI,
    SafetyAPI,
    ServicesAPI,
    showNotification,
    showLoading,
    hideLoading,
    debounce
}; 