/**
 * AUTOELITE VEHICLE COMPONENTS
 * Componentes específicos para manejo de vehículos
 */

AutoElite.Vehicle = {

    // Filtros de vehículos
    Filters: {
        init() {
            this.bindEvents();
            this.loadSavedFilters();
        },

        bindEvents() {
            const filterForm = AutoElite.DOM.select('#filter-form');
            if (!filterForm) return;

            // Aplicar filtros en tiempo real
            const filterInputs = filterForm.querySelectorAll('select, input');
            filterInputs.forEach(input => {
                input.addEventListener('change',
                    AutoElite.Utils.debounce(() => {
                        this.applyFilters();
                    }, 500)
                );
            });

            // Botón de reset
            const resetBtn = AutoElite.DOM.select('.btn-reset-filters');
            if (resetBtn) {
                resetBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.resetFilters();
                });
            }
        },

        async applyFilters() {
            const form = AutoElite.DOM.select('#filter-form');
            if (!form) return;

            const formData = AutoElite.Form.serialize(form);
            const resultsContainer = AutoElite.DOM.select('#vehicles-results');

            // Mostrar loading
            const loading = AutoElite.Loading.show(resultsContainer, 'Filtrando vehículos...');

            try {
                const response = await AutoElite.API.get('/vehiculo/api/', formData);

                if (response.success) {
                    this.renderVehicles(response.vehiculos, resultsContainer);
                    this.updateResultsCount(response.total_count);
                    this.saveFilters(formData);
                } else {
                    AutoElite.Notification.show(
                        response.error || 'Error al cargar vehículos',
                        'danger'
                    );
                }
            } catch (error) {
                console.error('Error aplicando filtros:', error);
                AutoElite.Notification.show('Error de conexión', 'danger');
            } finally {
                AutoElite.Loading.hide(resultsContainer);
            }
        },

        renderVehicles(vehicles, container) {
            const resultsDiv = container.querySelector('.vehicles-grid') ||
                AutoElite.DOM.create('div', ['vehicles-grid']);

            if (!vehicles.length) {
                resultsDiv.innerHTML = `
                    <div class="no-results text-center py-5">
                        <i class="fas fa-car fa-4x text-muted mb-3"></i>
                        <h3>No se encontraron vehículos</h3>
                        <p class="text-muted">Intenta ajustar los filtros de búsqueda</p>
                    </div>
                `;
                return;
            }

            resultsDiv.innerHTML = vehicles.map(vehicle => `
                <div class="card-modern" data-vehicle-id="${vehicle.id}">
                    <div class="card-modern__header">
                        <h5 class="mb-0">${vehicle.marca} ${vehicle.modelo}</h5>
                        <span class="badge bg-primary">${vehicle.categoria}</span>
                    </div>
                    <div class="card-modern__body">
                        <p class="text-muted">Año: ${vehicle.año}</p>
                        <p class="h5 text-success">${AutoElite.Utils.formatCurrency(vehicle.precio)}</p>
                    </div>
                    <div class="card-modern__footer">
                        <button class="btn btn-accent-modern" onclick="AutoElite.Vehicle.viewDetails(${vehicle.id})">
                            Ver Detalles
                        </button>
                    </div>
                </div>
            `).join('');

            if (!container.contains(resultsDiv)) {
                container.appendChild(resultsDiv);
            }
        },

        updateResultsCount(count) {
            const countEl = AutoElite.DOM.select('.results-count');
            if (countEl) {
                countEl.textContent = `${count} vehículo${count !== 1 ? 's' : ''} encontrado${count !== 1 ? 's' : ''}`;
            }
        },

        resetFilters() {
            const form = AutoElite.DOM.select('#filter-form');
            if (form) {
                form.reset();
                this.applyFilters();
                this.clearSavedFilters();
            }
        },

        saveFilters(filters) {
            localStorage.setItem('autoelite_filters', JSON.stringify(filters));
        },

        loadSavedFilters() {
            try {
                const saved = localStorage.getItem('autoelite_filters');
                if (saved) {
                    const filters = JSON.parse(saved);
                    const form = AutoElite.DOM.select('#filter-form');

                    Object.entries(filters).forEach(([key, value]) => {
                        const input = form.querySelector(`[name="${key}"]`);
                        if (input && value) {
                            input.value = value;
                        }
                    });
                }
            } catch (error) {
                console.warn('Error loading saved filters:', error);
            }
        },

        clearSavedFilters() {
            localStorage.removeItem('autoelite_filters');
        }
    },

    // Manejo de formularios de vehículos
    Form: {
        init() {
            this.bindEvents();
            this.setupValidation();
        },

        bindEvents() {
            const form = AutoElite.DOM.select('#vehicle-form');
            if (!form) return;

            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitForm();
            });

            // Auto-calcular precio estimado basado en otros campos
            const precioInput = form.querySelector('[name="precio"]');
            const marcaSelect = form.querySelector('[name="marca"]');
            const añoInput = form.querySelector('[name="año"]');

            if (precioInput && marcaSelect && añoInput) {
                [marcaSelect, añoInput].forEach(input => {
                    input.addEventListener('change', () => {
                        this.calculateEstimatedPrice();
                    });
                });
            }
        },

        setupValidation() {
            const form = AutoElite.DOM.select('#vehicle-form');
            if (!form) return;

            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
            });
        },

        validateField(field) {
            AutoElite.Form.clearFieldError(field);

            // Validaciones específicas para vehículos
            if (field.name === 'año') {
                const año = parseInt(field.value);
                if (año < 1900 || año > 2030) {
                    AutoElite.Form.showFieldError(field, 'El año debe estar entre 1900 y 2030');
                    return false;
                }
            }

            if (field.name === 'precio') {
                const precio = parseFloat(field.value);
                if (precio <= 0) {
                    AutoElite.Form.showFieldError(field, 'El precio debe ser mayor a 0');
                    return false;
                }
            }

            if (field.name === 'kilometraje') {
                const km = parseFloat(field.value);
                if (km < 0) {
                    AutoElite.Form.showFieldError(field, 'El kilometraje no puede ser negativo');
                    return false;
                }
            }

            return true;
        },

        async submitForm() {
            const form = AutoElite.DOM.select('#vehicle-form');
            if (!form) return;

            // Validar formulario completo
            if (!AutoElite.Form.validate(form)) {
                AutoElite.Notification.show('Por favor corrige los errores en el formulario', 'warning');
                return;
            }

            const submitBtn = form.querySelector('[type="submit"]');
            const originalText = submitBtn.textContent;

            // Deshabilitar botón y mostrar loading
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';

            try {
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': AutoElite.Utils.getCSRFToken()
                    }
                });

                if (response.ok) {
                    AutoElite.Notification.show('Vehículo guardado exitosamente', 'success');
                    // Redirigir después de un momento
                    setTimeout(() => {
                        window.location.href = '/vehiculo/lista/';
                    }, 1500);
                } else {
                    throw new Error('Error al guardar el vehículo');
                }
            } catch (error) {
                console.error('Error submitting form:', error);
                AutoElite.Notification.show('Error al guardar el vehículo', 'danger');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        },

        calculateEstimatedPrice() {
            const form = AutoElite.DOM.select('#vehicle-form');
            if (!form) return;

            const marca = form.querySelector('[name="marca"]')?.value;
            const año = parseInt(form.querySelector('[name="año"]')?.value);

            if (!marca || !año) return;

            // Estimación básica basada en marca y año
            const baseValues = {
                'Toyota': 25000,
                'Honda': 23000,
                'BMW': 45000,
                'Mercedes-Benz': 50000,
                'Audi': 42000,
                'Ford': 22000,
                'Volkswagen': 26000
            };

            const basePrice = baseValues[marca] || 20000;
            const currentYear = new Date().getFullYear();
            const depreciation = Math.max(0, (currentYear - año) * 0.1);
            const estimatedPrice = Math.round(basePrice * (1 - depreciation));

            const priceInput = form.querySelector('[name="precio"]');
            if (priceInput && !priceInput.value) {
                priceInput.value = estimatedPrice;

                // Mostrar sugerencia
                const suggestion = AutoElite.DOM.create('small', ['text-muted']);
                suggestion.textContent = `Precio estimado basado en marca y año: $${estimatedPrice.toLocaleString()}`;

                const existingSuggestion = priceInput.parentNode.querySelector('.price-suggestion');
                if (existingSuggestion) {
                    existingSuggestion.remove();
                }

                suggestion.classList.add('price-suggestion');
                priceInput.parentNode.appendChild(suggestion);
            }
        }
    },

    // Funciones de utilidad para vehículos
    Utils: {
        viewDetails(vehicleId) {
            // Implementar modal o navegación a detalles
            console.log('Viewing details for vehicle:', vehicleId);
            // window.location.href = `/vehiculo/${vehicleId}/`;
        },

        shareVehicle(vehicleId) {
            const url = `${window.location.origin}/vehiculo/${vehicleId}/`;

            if (navigator.share) {
                navigator.share({
                    title: 'Vehículo en AutoElite',
                    url: url
                });
            } else {
                // Fallback: copiar al clipboard
                navigator.clipboard.writeText(url).then(() => {
                    AutoElite.Notification.show('Enlace copiado al portapapeles', 'success');
                });
            }
        },

        favoriteVehicle(vehicleId) {
            // Implementar sistema de favoritos
            console.log('Adding to favorites:', vehicleId);
        }
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#filter-form')) {
        AutoElite.Vehicle.Filters.init();
    }

    if (document.querySelector('#vehicle-form')) {
        AutoElite.Vehicle.Form.init();
    }
});