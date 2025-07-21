/**
 * Test cases for the ProductManager frontend class
 * 
 * Tests the main functionality of the insurance products
 * frontend application including API interactions and UI updates.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { JSDOM } from 'jsdom';

// Setup DOM environment
const dom = new JSDOM(`
<!DOCTYPE html>
<html>
<body>
    <div id="productsContainer"></div>
    <div id="productDetails"></div>
    <div id="alertToast">
        <div id="toastMessage"></div>
    </div>
    <div id="productModal">
        <div id="modalTitle"></div>
        <form id="productForm">
            <input id="productName" required>
            <textarea id="productDescription" required></textarea>
            <input id="productPrice" type="number" required>
            <input id="productCoverage" required>
            <input id="productDeductible" type="number">
        </form>
        <button id="saveProductBtn"></button>
    </div>
</body>
</html>
`);

global.document = dom.window.document;
global.window = dom.window;

// Import the ProductManager after setting up DOM
const { ProductManager } = await import('../src/frontend/app.js');

describe('ProductManager', () => {
    let productManager;
    const mockProducts = [
        {
            id: 1,
            name: 'Auto Insurance',
            description: 'Comprehensive car coverage',
            price: 125.99,
            coverage: 'Full Coverage',
            deductible: 500,
            formatted_price: '$125.99'
        },
        {
            id: 2,
            name: 'Home Insurance',
            description: 'Protect your home',
            price: 89.50,
            coverage: 'Property & Contents',
            deductible: 1000,
            formatted_price: '$89.50'
        }
    ];

    beforeEach(() => {
        // Reset DOM
        document.getElementById('productsContainer').innerHTML = '';
        document.getElementById('productDetails').innerHTML = '';
        
        // Mock successful API response
        fetch.mockResolvedValue({
            ok: true,
            json: () => Promise.resolve(mockProducts)
        });
        
        productManager = new ProductManager();
    });

    describe('loadProducts', () => {
        it('should load products from API successfully', async () => {
            await productManager.loadProducts();
            
            expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/products');
            expect(productManager.products).toEqual(mockProducts);
        });

        it('should handle API errors gracefully', async () => {
            fetch.mockResolvedValue({
                ok: false,
                statusText: 'Server Error'
            });

            await productManager.loadProducts();
            
            expect(productManager.products).toEqual([]);
        });
    });

    describe('renderProducts', () => {
        beforeEach(async () => {
            await productManager.loadProducts();
        });

        it('should render product cards correctly', () => {
            productManager.renderProducts();
            
            const container = document.getElementById('productsContainer');
            expect(container.innerHTML).toContain('Auto Insurance');
            expect(container.innerHTML).toContain('Home Insurance');
            expect(container.innerHTML).toContain('$125.99');
            expect(container.innerHTML).toContain('$89.50');
        });

        it('should render empty state when no products', () => {
            productManager.products = [];
            productManager.renderProducts();
            
            const container = document.getElementById('productsContainer');
            expect(container.innerHTML).toContain('No Products Available');
        });
    });

    describe('createProductCard', () => {
        it('should create properly formatted product card HTML', () => {
            const product = mockProducts[0];
            const cardHtml = productManager.createProductCard(product);
            
            expect(cardHtml).toContain('Auto Insurance');
            expect(cardHtml).toContain('$125.99');
            expect(cardHtml).toContain('Comprehensive car coverage');
            expect(cardHtml).toContain('Full Coverage');
            expect(cardHtml).toContain('data-product-id="1"');
        });

        it('should handle products without deductible', () => {
            const productWithoutDeductible = { ...mockProducts[0], deductible: 0 };
            const cardHtml = productManager.createProductCard(productWithoutDeductible);
            
            expect(cardHtml).not.toContain('deductible-info');
        });
    });

    describe('selectProduct', () => {
        beforeEach(async () => {
            await productManager.loadProducts();
            productManager.renderProducts();
        });

        it('should select product and update details', () => {
            productManager.selectProduct(1);
            
            expect(productManager.selectedProduct).toEqual(mockProducts[0]);
            
            const detailsContainer = document.getElementById('productDetails');
            expect(detailsContainer.innerHTML).toContain('Auto Insurance');
            expect(detailsContainer.innerHTML).toContain('$125.99');
        });

        it('should clear previous selection', () => {
            // Add a mock selected card to DOM
            const mockCard = document.createElement('div');
            mockCard.classList.add('product-card', 'selected');
            mockCard.setAttribute('data-product-id', '2');
            document.getElementById('productsContainer').appendChild(mockCard);
            
            productManager.selectProduct(1);
            
            expect(mockCard.classList.contains('selected')).toBe(false);
        });
    });

    describe('saveProduct', () => {
        beforeEach(() => {
            // Setup form values
            document.getElementById('productName').value = 'New Insurance';
            document.getElementById('productDescription').value = 'New description';
            document.getElementById('productPrice').value = '199.99';
            document.getElementById('productCoverage').value = 'Premium Coverage';
            document.getElementById('productDeductible').value = '250';
        });

        it('should create new product successfully', async () => {
            const newProduct = {
                id: 3,
                name: 'New Insurance',
                description: 'New description',
                price: 199.99,
                coverage: 'Premium Coverage',
                deductible: 250,
                formatted_price: '$199.99'
            };

            fetch.mockResolvedValue({
                ok: true,
                json: () => Promise.resolve(newProduct)
            });

            await productManager.saveProduct();

            expect(fetch).toHaveBeenCalledWith(
                'http://localhost:5000/api/products',
                expect.objectContaining({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: 'New Insurance',
                        description: 'New description',
                        price: 199.99,
                        coverage: 'Premium Coverage',
                        deductible: 250
                    })
                })
            );
        });

        it('should update existing product when editing', async () => {
            productManager.editingProductId = 1;
            
            const updatedProduct = { ...mockProducts[0], name: 'Updated Insurance' };
            fetch.mockResolvedValue({
                ok: true,
                json: () => Promise.resolve(updatedProduct)
            });

            await productManager.saveProduct();

            expect(fetch).toHaveBeenCalledWith(
                'http://localhost:5000/api/products/1',
                expect.objectContaining({
                    method: 'PUT'
                })
            );
        });

        it('should handle API errors during save', async () => {
            fetch.mockResolvedValue({
                ok: false,
                json: () => Promise.resolve({ error: 'Validation failed' })
            });

            await productManager.saveProduct();
            
            // Should not add product to local array on error
            expect(productManager.products).toHaveLength(2);
        });
    });

    describe('deleteProduct', () => {
        beforeEach(async () => {
            await productManager.loadProducts();
            // Mock window.confirm
            global.confirm = vi.fn(() => true);
        });

        it('should delete product successfully', async () => {
            fetch.mockResolvedValue({
                ok: true,
                json: () => Promise.resolve({ message: 'Product deleted successfully' })
            });

            await productManager.deleteProduct(1);

            expect(fetch).toHaveBeenCalledWith(
                'http://localhost:5000/api/products/1',
                expect.objectContaining({ method: 'DELETE' })
            );
            
            expect(productManager.products).toHaveLength(1);
            expect(productManager.products.find(p => p.id === 1)).toBeUndefined();
        });

        it('should not delete when user cancels confirmation', async () => {
            global.confirm = vi.fn(() => false);

            await productManager.deleteProduct(1);

            expect(fetch).not.toHaveBeenCalled();
            expect(productManager.products).toHaveLength(2);
        });
    });

    describe('utility methods', () => {
        it('should escape HTML correctly', () => {
            const maliciousInput = '<script>alert("xss")</script>';
            const escaped = productManager.escapeHtml(maliciousInput);
            
            expect(escaped).toBe('&lt;script&gt;alert("xss")&lt;/script&gt;');
        });

        it('should show toast messages', () => {
            productManager.showToast('Test message', 'success');
            
            const toastMessage = document.getElementById('toastMessage');
            expect(toastMessage.textContent).toBe('Test message');
        });
    });
});
