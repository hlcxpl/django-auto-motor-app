/**
 * AUTOELITE CORE UTILITIES
 * Funciones JavaScript modulares y reutilizables
 */

const AutoElite = {
    // Configuración global
    config: {
        loadingDelay: 300,
        animationDuration: 300,
        apiTimeout: 10000
    },

    // Utilidades DOM
    DOM: {
        /**
         * Selecciona un elemento del DOM
         */
        select(selector) {
            return document.querySelector(selector);
        },

        /**
         * Selecciona múltiples elementos del DOM
         */
        selectAll(selector) {
            return document.querySelectorAll(selector);
        },

        /**
         * Crear un elemento con clases y atributos
         */
        create(tag, classes = [], attributes = {}) {
            const element = document.createElement(tag);

            if (classes.length) {
                element.classList.add(...classes);
            }

            Object.entries(attributes).forEach(([key, value]) => {
                element.setAttribute(key, value);
            });

            return element;
        },

        /**
         * Mostrar/Ocultar elementos con animación
         */
        toggle(element, show = null) {
            if (!element) return;

            const isVisible = !element.classList.contains('hidden');
            const shouldShow = show !== null ? show : !isVisible;

            if (shouldShow) {
                element.classList.remove('hidden');
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';

                requestAnimationFrame(() => {
                    element.style.transition = `all ${AutoElite.config.animationDuration}ms ease`;
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                });
            } else {
                element.style.transition = `all ${AutoElite.config.animationDuration}ms ease`;
                element.style.opacity = '0';
                element.style.transform = 'translateY(-20px)';

                setTimeout(() => {
                    element.classList.add('hidden');
                }, AutoElite.config.animationDuration);
            }
        }
    },

    // Utilidades de carga
    Loading: {
        /**
         * Muestra un indicador de carga
         */
        show(container, message = 'Cargando...') {
            const loadingEl = AutoElite.DOM.create('div', ['loading'], {
                'data-loading': 'true'
            });

            loadingEl.innerHTML = `
                <div class="d-flex align-items-center">
                    <i class="fas fa-spinner fa-spin me-2"></i>
                    <span>${message}</span>
                </div>
            `;

            if (typeof container === 'string') {
                container = AutoElite.DOM.select(container);
            }

            if (container) {
                container.appendChild(loadingEl);
            }

            return loadingEl;
        },

        /**
         * Oculta el indicador de carga
         */
        hide(container) {
            if (typeof container === 'string') {
                container = AutoElite.DOM.select(container);
            }

            if (container) {
                const loadingEl = container.querySelector('[data-loading="true"]');
                if (loadingEl) {
                    loadingEl.remove();
                }
            }
        }
    },

    // Utilidades de formularios
    Form: {
        /**
         * Serializa un formulario a objeto JavaScript
         */
        serialize(form) {
            if (typeof form === 'string') {
                form = AutoElite.DOM.select(form);
            }

            const formData = new FormData(form);
            const data = {};

            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }

            return data;
        },

        /**
         * Valida un formulario
         */
        validate(form) {
            if (typeof form === 'string') {
                form = AutoElite.DOM.select(form);
            }

            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    AutoElite.Form.showFieldError(field, 'Este campo es obligatorio');
                    isValid = false;
                } else {
                    AutoElite.Form.clearFieldError(field);
                }
            });

            return isValid;
        },

        /**
         * Muestra error en un campo
         */
        showFieldError(field, message) {
            AutoElite.Form.clearFieldError(field);

            const errorEl = AutoElite.DOM.create('div', ['invalid-feedback']);
            errorEl.textContent = message;

            field.classList.add('is-invalid');
            field.parentNode.appendChild(errorEl);
        },

        /**
         * Limpia errores de un campo
         */
        clearFieldError(field) {
            field.classList.remove('is-invalid');
            const errorEl = field.parentNode.querySelector('.invalid-feedback');
            if (errorEl) {
                errorEl.remove();
            }
        }
    },

    // Utilidades de notificaciones
    Notification: {
        /**
         * Muestra una notificación
         */
        show(message, type = 'info', duration = 5000) {
            const notificationEl = AutoElite.DOM.create('div', [
                'alert',
                `alert-${type}`,
                'alert-dismissible',
                'fade',
                'show',
                'position-fixed'
            ], {
                'style': 'top: 20px; right: 20px; z-index: 1060; max-width: 400px;'
            });

            notificationEl.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            document.body.appendChild(notificationEl);

            // Auto-remover después del tiempo especificado
            if (duration > 0) {
                setTimeout(() => {
                    if (notificationEl.parentNode) {
                        notificationEl.remove();
                    }
                }, duration);
            }

            return notificationEl;
        }
    },

    // Utilidades AJAX
    API: {
        /**
         * Realiza una petición GET
         */
        async get(url, params = {}) {
            const queryString = new URLSearchParams(params).toString();
            const fullUrl = queryString ? `${url}?${queryString}` : url;

            try {
                const response = await fetch(fullUrl, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error('Error en petición GET:', error);
                throw error;
            }
        },

        /**
         * Realiza una petición POST
         */
        async post(url, data = {}) {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': AutoElite.Utils.getCSRFToken()
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error('Error en petición POST:', error);
                throw error;
            }
        }
    },

    // Utilidades generales
    Utils: {
        /**
         * Obtiene el token CSRF de Django
         */
        getCSRFToken() {
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        },

        /**
         * Debounce function para limitar ejecuciones
         */
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        /**
         * Formatea números como moneda
         */
        formatCurrency(amount, currency = 'USD') {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: currency
            }).format(amount);
        },

        /**
         * Capitaliza la primera letra de cada palabra
         */
        capitalizeWords(str) {
            return str.replace(/\w\S*/g, (txt) =>
                txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
            );
        }
    }
};

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function () {
    console.log('AutoElite Core Utils initialized');

    // Configurar CSRF para todas las peticiones AJAX
    const csrfToken = AutoElite.Utils.getCSRFToken();
    if (csrfToken) {
        // Configurar headers por defecto para fetch
        const originalFetch = window.fetch;
        window.fetch = function (...args) {
            const [url, config] = args;
            if (config && config.method && config.method.toUpperCase() !== 'GET') {
                config.headers = config.headers || {};
                config.headers['X-CSRFToken'] = csrfToken;
            }
            return originalFetch.apply(this, args);
        };
    }
});

// Exportar para uso global
window.AutoElite = AutoElite;