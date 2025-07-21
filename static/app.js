// Product Editor Frontend
const API_URL = '/api/products';

function fetchProducts() {
  return fetch(API_URL).then(res => res.json());
}

function renderTable(products) {
  const tbody = document.querySelector('#products-table tbody');
  tbody.innerHTML = '';
  products.forEach(product => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${product.name}</td>
      <td>${product.description}</td>
      <td>$${product.price.toFixed(2)}</td>
      <td>${product.coverage}</td>
      <td>${product.deductible}</td>
      <td>
        <button onclick="editProduct(${product.id})">Edit</button>
        <button onclick="deleteProduct(${product.id})">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function showForm(product = null) {
  document.getElementById('product-form-modal').classList.remove('hidden');
  document.getElementById('form-title').textContent = product ? 'Edit Product' : 'Add Product';
  document.getElementById('product-id').value = product ? product.id : '';
  document.getElementById('product-name').value = product ? product.name : '';
  document.getElementById('product-description').value = product ? product.description : '';
  document.getElementById('product-price').value = product ? product.price : '';
  document.getElementById('product-coverage').value = product ? product.coverage : '';
  document.getElementById('product-deductible').value = product ? product.deductible : '';
}

function hideForm() {
  document.getElementById('product-form-modal').classList.add('hidden');
}

window.editProduct = function(id) {
  fetch(`${API_URL}`).then(res => res.json()).then(products => {
    const product = products.find(p => p.id === id);
    showForm(product);
  });
};

window.deleteProduct = function(id) {
  if (!confirm('Delete this product?')) return;
  fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    .then(() => loadAndRender());
};

document.getElementById('add-product-btn').onclick = () => showForm();
document.getElementById('cancel-btn').onclick = hideForm;

document.getElementById('product-form').onsubmit = function(e) {
  e.preventDefault();
  const id = document.getElementById('product-id').value;
  const product = {
    name: document.getElementById('product-name').value,
    description: document.getElementById('product-description').value,
    price: parseFloat(document.getElementById('product-price').value),
    coverage: document.getElementById('product-coverage').value,
    deductible: parseInt(document.getElementById('product-deductible').value, 10)
  };
  if (id) {
    // Edit
    product.id = parseInt(id, 10);
    fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product)
    }).then(() => {
      hideForm();
      loadAndRender();
    });
  } else {
    // Add
    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product)
    }).then(() => {
      hideForm();
      loadAndRender();
    });
  }
};

function loadAndRender() {
  fetchProducts().then(renderTable);
}

loadAndRender();
