function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');
  const itemsContainer = document.getElementById('itemsContainer');
  const discountSelect = document.getElementById('discountSelect');
  
  let servicesList = [];
  let clothesList  = [];
  let extraServicesList = [];
  let discountsList = [];
  
  
  async function fetchAllData(){
    const res = await fetch('/items/orderpagedata/');
    const data = await res.json();
  
    servicesList = data.services || [];
    clothesList  = data.clothes || [];
    extraServicesList = data.extraservice || [];
    discountsList = data.discount || [];
  
    discountsList.forEach(d=>{
      const opt = document.createElement('option');
      opt.value = d.percent;
      opt.textContent = `${d.name} - ${d.percent}%`;
      discountSelect.appendChild(opt);
    });
  }
  
  function updateGrandTotal() {
    const rows = itemsContainer.querySelectorAll('.item');
    let total = 0;
    rows.forEach(r => {
        const val = parseFloat(r.querySelector('.totalPrice').value);
        total += isNaN(val) ? 0 : val;
    });
  
    const discount = parseFloat(discountSelect.value) || 0;
    const discountedTotal = total * (1 - discount / 100);
  
    document.getElementById('grandTotal').value = discountedTotal.toFixed(0); 
  }
  
  function addItem() {
    if (!servicesList.length || !clothesList.length || !extraServicesList.length) return;
    const div = document.createElement('div');
    div.classList.add('item');
  
    const serviceOptions = servicesList.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    const clothOptions   = clothesList.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    const extraOptions   = extraServicesList.map(e => 
        `<label><input type="checkbox" class="extraService" value="${e.id}" data-price="${e.extra_fee}"> ${e.name}</label>`
    ).join('<br>');
    div.innerHTML = `
      <!-- خط اول -->
      <div class="line1">
        <div class="right-group">
          <div>لباس: <select class="clothId">${clothOptions}</select></div>
          <div>خدمت: <select class="serviceId">${serviceOptions}</select></div>
          <div>تعداد: <input type="number" class="quantity" value="1" min="1"></div>
        </div>
        <div class="left-group">
          قیمت واحد: <input type="number" class="unitPrice" readonly>
        </div>
      </div>
  
      <!-- خط دوم -->
      <div class="line2">
        <div class="extraServices">
          خدمات اضافی:<br>
          ${extraOptions}
        </div>
        <div class="totalPriceBox">
          قیمت کل: <input type="number" class="totalPrice" readonly>
        </div>
      </div>
          <!-- خط سوم -->
      <div class="line3">
        <label>
          <input type="checkbox" class="isExpress">
          کار عجله‌ای
        </label>
      </div>
  
      <!-- دکمه حذف -->
      <button type="button" class="removeBtn">❌ حذف</button>
    `;
  
  
    const serviceEl   = div.querySelector('.serviceId');
    const clothEl     = div.querySelector('.clothId');
    const quantityEl  = div.querySelector('.quantity');
    const unitPriceEl = div.querySelector('.unitPrice');
    const totalPriceEl= div.querySelector('.totalPrice');
    const extraEls    = div.querySelectorAll('.extraService');
  
    function updatePrice(){
      const quantity  = parseInt(quantityEl.value) || 1;
    
      const service = servicesList.find(x => x.id == serviceEl.value);
      const cloth   = clothesList.find(x => x.id == clothEl.value);
    
      const basePrice = (service ? service.price_modifier : 0) * (cloth ? cloth.base_price : 0);
      
      let extrasPrice = 0;
      extraEls.forEach(chk=>{
        if(chk.checked) extrasPrice += parseInt(chk.dataset.price);
      });
    
      let unit = basePrice + extrasPrice;
      const isExpressEl = div.querySelector('.isExpress');
      if(isExpressEl.checked){
        unit += unit * 0.3;  
      }
  
      unitPriceEl.value = unit;
      totalPriceEl.value = unit * quantity;
  
      updateGrandTotal();
      updateInvoice();
    }
  
    serviceEl.addEventListener('change', updatePrice);
    clothEl.addEventListener('change', updatePrice);
    quantityEl.addEventListener('input', updatePrice);
    extraEls.forEach(chk=>chk.addEventListener('change', updatePrice));
    const isExpressEl = div.querySelector('.isExpress');
    isExpressEl.addEventListener('change', updatePrice);
  
    div.querySelector('.removeBtn').addEventListener('click', ()=>{
      div.remove();
      updateGrandTotal();
      updateInvoice();
    });
  
    updatePrice();
    itemsContainer.appendChild(div);
  }
  
  async function createOrder(e){
    e.preventDefault();


    const phone = e.target.phone?.value.trim() || "";
    const fullname = e.target.fullname?.value.trim() || "";
    


    console.log('fullname (from form):', fullname);
    const rows = itemsContainer.querySelectorAll('.item');
    if (!rows.length) { 
      showPopup("حداقل یک آیتم لازم است.", "error"); 
      return; 
  }
  
  
    const items = Array.from(rows).map(r=>{
      const extras = Array.from(r.querySelectorAll('.extraService:checked')).map(x=>parseInt(x.value));
      const isExpress = r.querySelector('.isExpress').checked;
      return {
        service: parseInt(r.querySelector('.serviceId').value),
        cloth: parseInt(r.querySelector('.clothId').value),
        extra_services_ids: extras,
        quantity: parseInt(r.querySelector('.quantity').value),
        is_express: isExpress
      }
    });
  
    const discount = parseFloat(discountSelect.value) || 0;
    const res = await fetch('/orders/ordercreate/', {
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
      body: JSON.stringify({phone, fullname, items, discount_amount: discount})
    });
    const data = await res.json();
    if(res.ok){
      const customerName = data.fullname_display; 
      showPopup(`سفارش شماره "${data.id}" برای مشتری "${customerName}" ثبت شد.`, "success");
      e.target.reset();
      itemsContainer.innerHTML="";
      addItem();
      updateGrandTotal();
      updateInvoice();
    } else {
      showPopup("خطا در ثبت سفارش: " + JSON.stringify(data), "error");
    }
  }

function updateInvoice() {
  const rows = itemsContainer.querySelectorAll('.item');
  const tbody = document.getElementById('invoiceItems');
  tbody.innerHTML = '';

  let total = 0;

  rows.forEach((row, index) => {
    const clothName = row.querySelector('.clothId option:checked').textContent;
    const serviceName = row.querySelector('.serviceId option:checked').textContent;
    const quantity = parseInt(row.querySelector('.quantity').value) || 1;
    const totalPrice = parseFloat(row.querySelector('.totalPrice').value) || 0;
    const unitPrice = parseFloat(row.querySelector('.unitPrice').value) || 0;

    const extras = Array.from(row.querySelectorAll('.extraService:checked'))
                        .map(x => x.parentElement.textContent.trim())
                        .join(', ') || '-';

    total += totalPrice;

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${clothName}</td>
      <td>${serviceName}</td>
      <td>${extras}</td>
      <td>${quantity}</td>
      <td>${unitPrice}</td>

    `;
    tbody.appendChild(tr);
  });

  document.getElementById('invoiceBeforeDiscount').textContent = total.toFixed(0);
  const discountPercent = parseFloat(discountSelect.value) || 0;
  document.getElementById('invoiceDiscount').textContent = discountPercent ? discountPercent + '%' : 'بدون تخفیف';

  const discountedTotal = total * (1 - discountPercent / 100);
  document.getElementById('invoiceGrandTotal').textContent = discountedTotal.toFixed(0);
}
  


const registerCustomerForm = document.getElementById("registerCustomerForm");

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

registerCustomerForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(registerCustomerForm);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch("/customers/customerregister/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken, 
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (response.status === 201) {
      showPopup(`مشتری با موفقیت ثبت شد. کد مشتری: ${result.code}`, "success");
      registerCustomerForm.reset();
    } else if (response.status === 400) {
      showPopup("خطا در ثبت مشتری: " + JSON.stringify(result), "error");
    } else {
      showPopup("خطای غیرمنتظره!", "error");
    }
  } catch (error) {
    console.error("خطای ثبت مشتری:", error);
    showPopup("خطا در اتصال به سرور!", "error");

  }
});

  async function init(){
    await fetchAllData();
    addItem();
    document.getElementById('createOrderForm').addEventListener('submit', createOrder);
    document.getElementById('addItemBtn').addEventListener('click', ()=>addItem());
    discountSelect.addEventListener('change', () => {
      updateGrandTotal();
      updateInvoice();
  });
  }
  document.addEventListener('DOMContentLoaded', init);

  window.addEventListener('scroll', () => {
    const invoice = document.getElementById('invoiceContainer');
    const customerSection = document.getElementById('registerCustomerForm');
  
    if (!invoice || !customerSection) return;
  
    const invoiceBottom = invoice.getBoundingClientRect().bottom;
    const customerTop = customerSection.getBoundingClientRect().top;
  
    if (invoiceBottom >= customerTop - 20) {
      invoice.style.position = 'absolute';
      invoice.style.top = (window.scrollY + customerTop - invoice.offsetHeight - 20) + 'px';
    } else {
      invoice.style.position = 'sticky';
      invoice.style.top = '20px';
    }
  });

// -----------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {

  const checkBtn = document.getElementById("checkCustomerBtn");
  const phoneInput = document.querySelector("#createOrderForm input[name='phone']");
  const fullnameInput = document.querySelector("#createOrderForm input[name='fullname']");
  const addressInput = document.querySelector("#createOrderForm input[name='address']");

  let originalCustomerData = null;

  checkBtn.addEventListener("click", function () {
      const phone = phoneInput.value.trim();
      if (!phone) {
          showPopup("لطفاً شماره تلفن را وارد کنید!", "error");
          return;
      }
      fetch(`orders/checkcustomer/?phone=${phone}`)
          .then(res => res.json())
          .then(data => {
              if (data.exists === true) {
                  fullnameInput.value = data.customer.fullname || "";
                  addressInput.value = data.customer.address || "";
                  originalCustomerData = {
                      fullname: data.customer.fullname || "",
                      address: data.customer.address || ""
                  };
                  showPopup("مشتری پیدا شد!", "success");
              } else {
                  fullnameInput.value = "";
                  addressInput.value = "";
                  originalCustomerData = null;
                  showPopup("مشتری با این شماره وجود ندارد!", "warning");
              }
          })
          .catch(err => {
              console.log("Error checking customer:", err);
              showPopup("خطا در ارتباط با سرور!", "error");
          });
  });
  const form = document.getElementById("createOrderForm");
  form.addEventListener("submit", function (e) {
      if (originalCustomerData) {
          if (fullnameInput.value === originalCustomerData.fullname) {
            fullnameInput.value = ""; 
          }
          if (addressInput.value === originalCustomerData.address) {
              addressInput.value = "";
          }
        
      }
  });
});