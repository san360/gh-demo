/**
 * Insurance Products Frontend Application
 * 
 * Handles product display, creation, editing, and deletion
 * with Bootstrap UI components and REST API integration.
 */

const API_BASE_URL = 'http://localhost:5000/api';

class ProductManager {
    constructor() {
        this.products = [];
        this.selectedProduct = undefined;
        this.editingProductId = undefined;
        this.init();
    }

    async init() {
        await this.loadProducts();
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('saveProductBtn').addEventListener('click', () => this.saveProduct());
        document.getElementById('productForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveProduct();
        });

        const modal = document.getElementById('productModal');
        modal.addEventListener('show.bs.modal', () => this.prepareModal());
        modal.addEventListener('hidden.bs.modal', () => this.resetModal());
    }

    async loadProducts() {
        try {
            this.showLoading();
            const response = await fetch(`${API_BASE_URL}/products`);
            
            if (!response.ok) {
                throw new Error(`Failed to load products: ${response.statusText}`);
            }
            
            this.products = await response.json();
            this.renderProducts();
        } catch (error) {
            console.error('Error loading products:', error);
            this.showToast('Failed to load products', 'error');
            this.renderEmptyState();
        }
    }

    renderProducts() {
        const container = document.getElementById('productsContainer');
        
        if (this.products.length === 0) {
            this.renderEmptyState();
            return;
        }

        container.innerHTML = this.products.map(product => this.createProductCard(product)).join('');
        
        // Add event listeners to product cards
        document.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('.product-actions')) {
                    this.selectProduct(parseInt(card.dataset.productId));
                }
            });
        });

        // Add event listeners to action buttons
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.editProduct(parseInt(btn.dataset.productId));
            });
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.deleteProduct(parseInt(btn.dataset.productId));
            });
        });
    }

    createProductCard(product) {
        return `
            <div class="col-md-6 mb-3">
                <div class="card product-card fade-in-up" data-product-id="${product.id}">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">${this.escapeHtml(product.name)}</h6>
                        <span class="badge bg-success price-badge">${product.formatted_price}</span>
                    </div>
                    <div class="card-body">
                        <p class="card-text text-muted mb-2">${this.escapeHtml(product.description)}</p>
                        <div class="coverage-info">
                            <small><strong>Coverage:</strong> ${this.escapeHtml(product.coverage)}</small>
                        </div>
                        ${product.deductible > 0 ? `
                            <div class="deductible-info">
                                <small><strong>Deductible:</strong> $${product.deductible.toFixed(2)}</small>
                            </div>
                        ` : ''}
                        <div class="product-actions mt-2">
                            <div class="btn-group btn-group-sm" role="group">
                                <button type="button" class="btn btn-outline-primary edit-btn" data-product-id="${product.id}">
                                    Edit
                                </button>
                                <button type="button" class="btn btn-outline-danger delete-btn" data-product-id="${product.id}">
                                    Delete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    selectProduct(productId) {
        // Remove previous selection
        document.querySelectorAll('.product-card').forEach(card => {
            card.classList.remove('selected');
        });

        // Add selection to current card
        const selectedCard = document.querySelector(`[data-product-id="${productId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }

        this.selectedProduct = this.products.find(p => p.id === productId);
        this.renderProductDetails();
    }

    renderProductDetails() {
        const container = document.getElementById('productDetails');
        
        if (!this.selectedProduct) {
            container.innerHTML = '<p class="text-muted">Select a product to view details</p>';
            return;
        }

        const product = this.selectedProduct;
        container.innerHTML = `
            <div class="product-details">
                <h6 class="text-primary">${this.escapeHtml(product.name)}</h6>
                <p class="mb-3">${this.escapeHtml(product.description)}</p>
                
                <div class="row mb-2">
                    <div class="col-4"><strong>Price:</strong></div>
                    <div class="col-8">${product.formatted_price}</div>
                </div>
                
                <div class="row mb-2">
                    <div class="col-4"><strong>Coverage:</strong></div>
                    <div class="col-8">${this.escapeHtml(product.coverage)}</div>
                </div>
                
                <div class="row mb-2">
                    <div class="col-4"><strong>Deductible:</strong></div>
                    <div class="col-8">$${product.deductible.toFixed(2)}</div>
                </div>
                
                <div class="mt-3">
                    <button class="btn btn-sm btn-primary me-2" onclick="productManager.editProduct(${product.id})">
                        Edit Product
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="productManager.deleteProduct(${product.id})">
                        Delete Product
                    </button>
                </div>
            </div>
        `;
    }

    prepareModal() {
        const modalTitle = document.getElementById('modalTitle');
        const saveBtn = document.getElementById('saveProductBtn');

        if (this.editingProductId) {
            modalTitle.textContent = 'Edit Product';
            saveBtn.textContent = 'Update Product';
            this.populateForm();
        } else {
            modalTitle.textContent = 'Add New Product';
            saveBtn.textContent = 'Save Product';
        }
    }

    populateForm() {
        const product = this.products.find(p => p.id === this.editingProductId);
        if (!product) return;

        document.getElementById('productName').value = product.name;
        document.getElementById('productDescription').value = product.description;
        document.getElementById('productPrice').value = product.price;
        document.getElementById('productCoverage').value = product.coverage;
        document.getElementById('productDeductible').value = product.deductible;
    }

    resetModal() {
        document.getElementById('productForm').reset();
        this.editingProductId = undefined;
    }

    async saveProduct() {
        const form = document.getElementById('productForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const productData = {
            name: document.getElementById('productName').value.trim(),
            description: document.getElementById('productDescription').value.trim(),
            price: parseFloat(document.getElementById('productPrice').value),
            coverage: document.getElementById('productCoverage').value.trim(),
            deductible: parseFloat(document.getElementById('productDeductible').value) || 0
        };

        try {
            const url = this.editingProductId 
                ? `${API_BASE_URL}/products/${this.editingProductId}`
                : `${API_BASE_URL}/products`;
            
            const method = this.editingProductId ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to save product');
            }

            const savedProduct = await response.json();
            
            if (this.editingProductId) {
                const index = this.products.findIndex(p => p.id === this.editingProductId);
                if (index !== -1) {
                    this.products[index] = savedProduct;
                }
                this.showToast('Product updated successfully', 'success');
            } else {
                this.products.push(savedProduct);
                this.showToast('Product created successfully', 'success');
            }

            this.renderProducts();
            bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();

        } catch (error) {
            console.error('Error saving product:', error);
            this.showToast(error.message, 'error');
        }
    }

    editProduct(productId) {
        this.editingProductId = productId;
        const modal = new bootstrap.Modal(document.getElementById('productModal'));
        modal.show();
    }

    async deleteProduct(productId) {
        const product = this.products.find(p => p.id === productId);
        if (!product) return;

        if (!confirm(`Are you sure you want to delete "${product.name}"?`)) {
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete product');
            }

            this.products = this.products.filter(p => p.id !== productId);
            
            if (this.selectedProduct && this.selectedProduct.id === productId) {
                this.selectedProduct = undefined;
            }

            this.renderProducts();
            this.renderProductDetails();
            this.showToast('Product deleted successfully', 'success');

        } catch (error) {
            console.error('Error deleting product:', error);
            this.showToast('Failed to delete product', 'error');
        }
    }

    showLoading() {
        const container = document.getElementById('productsContainer');
        container.innerHTML = `
            <div class="col-12">
                <div class="spinner-container">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </div>
        `;
    }

    renderEmptyState() {
        const container = document.getElementById('productsContainer');
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <i class="bi bi-inbox"></i>
                    <h5>No Products Available</h5>
                    <p class="text-muted">Start by adding your first insurance product.</p>
                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#productModal">
                        Add First Product
                    </button>
                </div>
            </div>
        `;
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('alertToast');
        const toastMessage = document.getElementById('toastMessage');
        
        toastMessage.textContent = message;
        
        // Remove existing type classes
        toast.classList.remove('text-bg-success', 'text-bg-danger', 'text-bg-info');
        
        // Add appropriate type class
        switch (type) {
            case 'success':
                toast.classList.add('text-bg-success');
                break;
            case 'error':
                toast.classList.add('text-bg-danger');
                break;
            default:
                toast.classList.add('text-bg-info');
        }

        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application
const productManager = new ProductManager();

// Make it globally available for inline event handlers
window.productManager = productManager;
