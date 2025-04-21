/**
 * School Management System - Global JavaScript Functions
 */

// Toast notification system
class ToastManager {
    constructor() {
        this.successToast = null;
        this.errorToast = null;
        this.infoToast = null;
        this.initToasts();
    }

    initToasts() {
        // Initialize on document ready
        $(document).ready(() => {
            this.successToast = new bootstrap.Toast(document.getElementById('successToast'));
            this.errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
            this.infoToast = new bootstrap.Toast(document.getElementById('infoToast'));
        });
    }

    showSuccess(message) {
        $('#successToastMessage').text(message);
        this.successToast.show();
    }

    showError(message) {
        $('#errorToastMessage').text(message);
        this.errorToast.show();
    }

    showInfo(message) {
        $('#infoToastMessage').text(message);
        this.infoToast.show();
    }
}

// API request handler with error handling
class ApiService {
    constructor(toastManager) {
        this.toast = toastManager;
    }

    get(url, successCallback, errorCallback) {
        $.ajax({
            url: url,
            method: 'GET',
            success: (data) => {
                if (successCallback) successCallback(data);
            },
            error: (xhr) => {
                const errorMsg = xhr.responseJSON?.error || 'Unknown error occurred';
                if (this.toast) this.toast.showError(`Error: ${errorMsg}`);
                if (errorCallback) errorCallback(xhr);
            }
        });
    }

    post(url, data, successCallback, errorCallback) {
        $.ajax({
            url: url,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: (response) => {
                if (successCallback) successCallback(response);
            },
            error: (xhr) => {
                const errorMsg = xhr.responseJSON?.error || 'Unknown error occurred';
                if (this.toast) this.toast.showError(`Error: ${errorMsg}`);
                if (errorCallback) errorCallback(xhr);
            }
        });
    }

    delete(url, successCallback, errorCallback) {
        $.ajax({
            url: url,
            method: 'DELETE',
            success: (response) => {
                if (successCallback) successCallback(response);
            },
            error: (xhr) => {
                const errorMsg = xhr.responseJSON?.error || 'Unknown error occurred';
                if (this.toast) this.toast.showError(`Error: ${errorMsg}`);
                if (errorCallback) errorCallback(xhr);
            }
        });
    }

    put(url, data, successCallback, errorCallback) {
        $.ajax({
            url: url,
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: (response) => {
                if (successCallback) successCallback(response);
            },
            error: (xhr) => {
                const errorMsg = xhr.responseJSON?.error || 'Unknown error occurred';
                if (this.toast) this.toast.showError(`Error: ${errorMsg}`);
                if (errorCallback) errorCallback(xhr);
            }
        });
    }
}

// Page loader overlay
class PageLoader {
    constructor() {
        this.createLoaderElement();
    }

    createLoaderElement() {
        if (!$('#page-loader').length) {
            $('body').append(`
                <div id="page-loader" style="display:none">
                    <div class="loader-overlay"></div>
                    <div class="loader-content">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                        <p class="mt-2 text-white">Loading...</p>
                    </div>
                </div>
            `);

            // Add CSS for the loader
            $('head').append(`
                <style>
                    #page-loader {
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        z-index: 9999;
                    }
                    .loader-overlay {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-color: rgba(0, 0, 0, 0.7);
                    }
                    .loader-content {
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        text-align: center;
                    }
                </style>
            `);
        }
    }

    show(message = 'Loading...') {
        $('#page-loader').find('p').text(message);
        $('#page-loader').fadeIn(300);
    }

    hide() {
        $('#page-loader').fadeOut(300);
    }
}

// Search functionality for tables
function setupTableSearch(inputSelector, tableSelector) {
    $(inputSelector).on('keyup', function() {
        const value = $(this).val().toLowerCase();
        $(`${tableSelector} tbody tr`).filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
}

// Format date to a readable format
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Initialize global objects
const toastManager = new ToastManager();
const apiService = new ApiService(toastManager);
const pageLoader = new PageLoader();

// Mobile sidebar handler
class MobileSidebar {
    constructor() {
        this.init();
    }

    init() {
        $(document).ready(() => {
            // Initialize the offcanvas component
            this.sidebar = new bootstrap.Offcanvas(document.getElementById('mobileSidebar'));

            // Show sidebar button
            $('#showSidebar').on('click', () => {
                this.sidebar.show();
            });

            // Close sidebar when a menu item is clicked
            $('#mobileSidebar .list-group-item').on('click', () => {
                this.sidebar.hide();
                pageLoader.show('Loading page...');
            });
        });
    }

    show() {
        this.sidebar.show();
    }

    hide() {
        this.sidebar.hide();
    }
}

// Add event listeners for page navigation
$(document).ready(function() {
    // Initialize mobile sidebar
    const mobileSidebar = new MobileSidebar();

    // Add active class to current nav item
    const currentPath = window.location.pathname;
    $(`.list-group-item[href="${currentPath}"]`).addClass('active');

    // Show loading overlay when navigating
    $('a:not([data-bs-toggle])').on('click', function() {
        const href = $(this).attr('href');
        if (href && href !== '#' && !href.startsWith('javascript:') && !$(this).attr('target')) {
            pageLoader.show('Loading page...');
        }
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add animation to cards
    $('.card').addClass('fade-in');

    // Add responsive table classes
    $('.table').each(function() {
        if (!$(this).parent().hasClass('table-responsive')) {
            $(this).wrap('<div class="table-responsive"></div>');
        }
    });
});
