// VoipFit Admin Panel JavaScript

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initAdminPanel();
    initDataTables();
    initModals();
    initFormValidation();
    initFileUploads();
    initConfirmDialogs();
});

// Main admin panel initialization
function initAdminPanel() {
    initSidebar();
    initTooltips();
    initAutoRefresh();
    updateTimestamps();
}

// Sidebar functionality
function initSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const toggleBtn = document.querySelector('.sidebar-toggle');
    
    // Mobile sidebar toggle
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            document.body.classList.toggle('sidebar-open');
        });
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !e.target.matches('.sidebar-toggle')) {
                sidebar.classList.remove('show');
                document.body.classList.remove('sidebar-open');
            }
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('show');
            document.body.classList.remove('sidebar-open');
        }
    });
    
    // Active nav item highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Data tables enhancement
function initDataTables() {
    const tables = document.querySelectorAll('.table');
    
    tables.forEach(table => {
        // Add search functionality
        addTableSearch(table);
        
        // Add sorting functionality
        addTableSorting(table);
        
        // Add row highlighting
        addRowHighlighting(table);
    });
}

function addTableSearch(table) {
    const tableContainer = table.closest('.admin-card');
    if (!tableContainer) return;
    
    const cardHeader = tableContainer.querySelector('.card-header');
    if (!cardHeader) return;
    
    // Create search input
    const searchContainer = document.createElement('div');
    searchContainer.className = 'table-search';
    searchContainer.innerHTML = `
        <div class="input-group input-group-sm" style="width: 250px;">
            <input type="text" class="form-control" placeholder="Search..." id="search-${table.id || 'table'}">
            <span class="input-group-text">
                <i class="fas fa-search"></i>
            </span>
        </div>
    `;
    
    cardHeader.appendChild(searchContainer);
    
    const searchInput = searchContainer.querySelector('input');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
}

function addTableSorting(table) {
    const headers = table.querySelectorAll('th');
    
    headers.forEach((header, index) => {
        if (header.textContent.trim() === '' || header.querySelector('input, button')) {
            return; // Skip empty headers or action columns
        }
        
        header.style.cursor = 'pointer';
        header.innerHTML += ' <i class="fas fa-sort text-muted"></i>';
        
        header.addEventListener('click', function() {
            sortTable(table, index, header);
        });
    });
}

function sortTable(table, columnIndex, header) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAscending = header.dataset.sortOrder !== 'asc';
    
    // Reset all sort icons
    table.querySelectorAll('th i').forEach(icon => {
        icon.className = 'fas fa-sort text-muted';
    });
    
    // Set current sort icon
    const icon = header.querySelector('i');
    icon.className = isAscending ? 'fas fa-sort-up' : 'fas fa-sort-down';
    header.dataset.sortOrder = isAscending ? 'asc' : 'desc';
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try to parse as numbers
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }
        
        // String comparison
        return isAscending ? 
            aValue.localeCompare(bValue) : 
            bValue.localeCompare(aValue);
    });
    
    // Reorder rows
    rows.forEach(row => tbody.appendChild(row));
}

function addRowHighlighting(table) {
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(99, 102, 241, 0.1)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
}

// Modal enhancements
function initModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        // Auto-focus first input when modal opens
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = modal.querySelector('input, textarea, select');
            if (firstInput) {
                firstInput.focus();
            }
        });
        
        // Clear form when modal closes
        modal.addEventListener('hidden.bs.modal', function() {
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
                clearFormErrors(form);
            }
        });
    });
}

// Form validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Please fix the errors in the form.', 'danger');
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    
    // Clear previous errors
    clearFieldError(field);
    
    // Required validation
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required.');
        isValid = false;
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(value)) {
            showFieldError(field, 'Please enter a valid email address.');
            isValid = false;
        }
    }
    
    // URL validation
    if (field.type === 'url' && value) {
        try {
            new URL(value);
        } catch {
            showFieldError(field, 'Please enter a valid URL.');
            isValid = false;
        }
    }
    
    // Password confirmation
    if (field.name === 'confirm_password') {
        const passwordField = document.querySelector('input[name="new_password"]');
        if (passwordField && value !== passwordField.value) {
            showFieldError(field, 'Passwords do not match.');
            isValid = false;
        }
    }
    
    // Minimum length
    const minLength = field.getAttribute('minlength');
    if (minLength && value.length < parseInt(minLength)) {
        showFieldError(field, `Minimum length is ${minLength} characters.`);
        isValid = false;
    }
    
    return isValid;
}

function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function clearFormErrors(form) {
    const errorDivs = form.querySelectorAll('.invalid-feedback');
    const invalidFields = form.querySelectorAll('.is-invalid');
    
    errorDivs.forEach(div => div.remove());
    invalidFields.forEach(field => field.classList.remove('is-invalid'));
}

// File upload handling
function initFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            handleFileUpload(this);
        });
    });
}

function handleFileUpload(input) {
    const files = input.files;
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    
    for (let file of files) {
        if (file.size > maxSize) {
            showAlert('File size must be less than 16MB.', 'danger');
            input.value = '';
            return;
        }
        
        if (!allowedTypes.includes(file.type)) {
            showAlert('Only image files are allowed.', 'danger');
            input.value = '';
            return;
        }
    }
    
    // Show preview for images
    if (files.length > 0 && files[0].type.startsWith('image/')) {
        showImagePreview(input, files[0]);
    }
}

function showImagePreview(input, file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        let preview = input.parentNode.querySelector('.image-preview');
        
        if (!preview) {
            preview = document.createElement('div');
            preview.className = 'image-preview mt-2';
            input.parentNode.appendChild(preview);
        }
        
        preview.innerHTML = `
            <img src="${e.target.result}" alt="Preview" style="max-width: 200px; max-height: 200px; border-radius: 4px;">
            <button type="button" class="btn btn-sm btn-outline-danger ms-2" onclick="clearImagePreview(this)">
                <i class="fas fa-times"></i>
            </button>
        `;
    };
    
    reader.readAsDataURL(file);
}

function clearImagePreview(button) {
    const preview = button.closest('.image-preview');
    const input = preview.previousElementSibling;
    
    input.value = '';
    preview.remove();
}

// Confirmation dialogs
function initConfirmDialogs() {
    const deleteLinks = document.querySelectorAll('a[href*="/delete/"], a[onclick*="confirm"]');
    
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const message = this.getAttribute('data-confirm') || 'Are you sure you want to delete this item?';
            
            showConfirmDialog(message, () => {
                window.location.href = this.href;
            });
        });
    });
}

function showConfirmDialog(message, onConfirm) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Action</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" id="confirmBtn">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    modal.querySelector('#confirmBtn').addEventListener('click', function() {
        bsModal.hide();
        onConfirm();
    });
    
    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

// Alert system
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.querySelector('.flash-messages') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // Auto-remove
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, duration);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1050;
        max-width: 400px;
    `;
    document.body.appendChild(container);
    return container;
}

// Auto-refresh functionality
function initAutoRefresh() {
    const refreshInterval = 5 * 60 * 1000; // 5 minutes
    const dashboardPath = '/admin/dashboard';
    
    if (window.location.pathname === dashboardPath) {
        setInterval(() => {
            // Only refresh if user is active
            if (document.visibilityState === 'visible') {
                refreshDashboardStats();
            }
        }, refreshInterval);
    }
}

function refreshDashboardStats() {
    // This would typically make an AJAX request to get updated stats
    // For now, just reload the page if user hasn't interacted recently
    const lastActivity = parseInt(localStorage.getItem('lastActivity') || '0');
    const now = Date.now();
    
    if (now - lastActivity > 10 * 60 * 1000) { // 10 minutes of inactivity
        window.location.reload();
    }
}

// Track user activity
let activityTimer;
function trackActivity() {
    localStorage.setItem('lastActivity', Date.now().toString());
    
    clearTimeout(activityTimer);
    activityTimer = setTimeout(() => {
        // Show session timeout warning
        showSessionWarning();
    }, 25 * 60 * 1000); // 25 minutes
}

function showSessionWarning() {
    showAlert('Your session will expire soon. Please save your work.', 'warning', 10000);
}

// Initialize activity tracking
document.addEventListener('mousemove', trackActivity);
document.addEventListener('keypress', trackActivity);
document.addEventListener('click', trackActivity);
trackActivity(); // Initial call

// Update timestamps
function updateTimestamps() {
    const timestamps = document.querySelectorAll('[data-timestamp]');
    
    timestamps.forEach(element => {
        const timestamp = new Date(element.dataset.timestamp);
        const now = new Date();
        const diff = now - timestamp;
        
        let relative;
        if (diff < 60000) { // Less than 1 minute
            relative = 'Just now';
        } else if (diff < 3600000) { // Less than 1 hour
            relative = Math.floor(diff / 60000) + ' minutes ago';
        } else if (diff < 86400000) { // Less than 1 day
            relative = Math.floor(diff / 3600000) + ' hours ago';
        } else {
            relative = Math.floor(diff / 86400000) + ' days ago';
        }
        
        element.textContent = relative;
        element.title = timestamp.toLocaleString();
    });
}

// Content management helpers
function previewContent(content, type) {
    let preview;
    
    switch (type) {
        case 'html':
            preview = content.substring(0, 100) + (content.length > 100 ? '...' : '');
            break;
        case 'image_url':
            preview = `<img src="${content}" alt="Preview" style="max-width: 50px; max-height: 50px;">`;
            break;
        default:
            preview = content.substring(0, 100) + (content.length > 100 ? '...' : '');
    }
    
    return preview;
}

// Bulk actions
function initBulkActions() {
    const selectAllCheckbox = document.querySelector('#selectAll');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const bulkActionBtn = document.querySelector('#bulkActionBtn');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            
            updateBulkActionBtn();
        });
    }
    
    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkActionBtn);
    });
    
    function updateBulkActionBtn() {
        const checkedCount = document.querySelectorAll('.item-checkbox:checked').length;
        
        if (bulkActionBtn) {
            bulkActionBtn.style.display = checkedCount > 0 ? 'block' : 'none';
            bulkActionBtn.textContent = `Actions (${checkedCount} selected)`;
        }
    }
}

// Keyboard shortcuts
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const saveBtn = document.querySelector('button[type="submit"]');
            if (saveBtn) {
                saveBtn.click();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
}

// Initialize all admin features
document.addEventListener('DOMContentLoaded', function() {
    initBulkActions();
    initKeyboardShortcuts();
});

// Export functions for global access
window.AdminPanel = {
    showAlert,
    showConfirmDialog,
    validateField,
    clearFormErrors,
    updateTimestamps,
    previewContent
};

// CSS additions for admin enhancements
const adminStyle = document.createElement('style');
adminStyle.textContent = `
    .table-search {
        margin-left: auto;
    }
    
    .image-preview {
        margin-top: 0.5rem;
    }
    
    .is-invalid {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
    }
    
    .invalid-feedback {
        display: block;
        color: #dc3545;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }
    
    .sidebar-toggle {
        display: none;
    }
    
    @media (max-width: 768px) {
        .sidebar-toggle {
            display: block;
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 1100;
            background: var(--admin-primary);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem;
            cursor: pointer;
        }
        
        .main-content {
            padding-top: 60px;
        }
    }
`;
document.head.appendChild(adminStyle);
