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

  const orderElement = document.getElementById('orderData');
  const orderIdFromUrl = orderElement ? orderElement.dataset.orderId : null;
  
  if (!orderIdFromUrl) {
    console.error("❌ order_id پیدا نشد. مطمئن شو در HTML تگ <div id='orderData' data-order-id='...'></div> وجود دارد.");
  }
  
  const itemsContainer = document.getElementById('itemsContainer');
  const messageDiv = document.getElementById('message');
  const discountSelect = document.getElementById('discountSelect');
  
  let servicesList = [], clothesList = [], extraServicesList = [], discountsList = [];

  async function fetchOrderPageData(){
    const res = await fetch('/items/orderpagedata/');
    const data = await res.json();
    servicesList = data.services || [];
    clothesList  = data.clothes || [];
    extraServicesList = data.extraservice || [];
    discountsList = data.discount || [];
  
    discountSelect.innerHTML = `<option value="0">بدون تخفیف</option>`;
    discountsList.forEach(d=>{
      discountSelect.innerHTML += `<option value="${d.percent}">${d.name} (${d.percent}%)</option>`;
    });
  }

  function addItem(item = null) {
    const div = document.createElement('div');
    div.classList.add('item');
  
    const serviceOptions = servicesList.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    const clothOptions   = clothesList.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    const extraOptions   = extraServicesList.map(e => 
      `<label><input type="checkbox" class="extraService" value="${e.id}" data-price="${e.extra_fee}"> ${e.name}</label>`
    ).join('');
  
    div.innerHTML = `
      <div class="line1">
        <div>لباس: <select class="clothId">${clothOptions}</select></div>
        <div>خدمت: <select class="serviceId">${serviceOptions}</select></div>
        <div>تعداد: <input type="number" class="quantity" value="1" min="1"></div>
        <div>قیمت واحد: <input type="number" class="unitPrice" readonly></div>
      </div>
      <div class="line2">
        <div class="extraServices">خدمات اضافی: ${extraOptions}</div>
        <div>قیمت کل: <input type="number" class="totalPrice" readonly></div>
      </div>
      <button type="button" class="removeBtn">❌ حذف</button>
    `;
  
    const serviceEl = div.querySelector('.serviceId');
    const clothEl   = div.querySelector('.clothId');
    const quantityEl= div.querySelector('.quantity');
    const unitPriceEl = div.querySelector('.unitPrice');
    const totalPriceEl= div.querySelector('.totalPrice');
    const extraEls  = div.querySelectorAll('.extraService');
  
    function updatePrice(){
      const service = servicesList.find(s=>s.id == serviceEl.value);
      const cloth   = clothesList.find(c=>c.id == clothEl.value);
      const qty     = parseInt(quantityEl.value) || 1;
      let extrasTotal = 0;
      extraEls.forEach(chk=>{ if(chk.checked) extrasTotal += parseInt(chk.dataset.price); });
  
      const base = (cloth ? cloth.base_price : 0) * (service ? service.price_modifier : 0);
      const unit = base + extrasTotal;
      unitPriceEl.value = unit;
      totalPriceEl.value = unit * qty;
  
      updateGrandTotal();
    }
    
    serviceEl.addEventListener('change', updatePrice);
    clothEl.addEventListener('change', updatePrice);
    quantityEl.addEventListener('input', updatePrice);
    extraEls.forEach(chk=>chk.addEventListener('change', updatePrice));
    div.querySelector('.removeBtn').addEventListener('click', ()=>{ div.remove(); updateGrandTotal(); });
  
    if(item){
      serviceEl.value = item.service;
      clothEl.value   = item.cloth;
      quantityEl.value= item.quantity || 1;
      if(item.extra_services){
        const extraIds = item.extra_services.map(es=>typeof es === 'object'? es.id: es);
        extraEls.forEach(chk=>{ if(extraIds.includes(parseInt(chk.value))) chk.checked = true; });
      }
      if(item.id) div.dataset.itemId = item.id;
    }
  
    updatePrice();
    itemsContainer.appendChild(div);
  }

  function updateGrandTotal(){
    let total = 0;
    itemsContainer.querySelectorAll('.totalPrice').forEach(inp=>{
      total += parseInt(inp.value) || 0;
    });
    const discount = parseFloat(discountSelect.value) || 0;
    document.getElementById('grandTotal').value = Math.round(total * (1 - discount/100));
  }

  async function updateOrder(e){
    e.preventDefault();
    const rows = itemsContainer.querySelectorAll('.item');
    if(!rows.length){ showPopup("حداقل یک آیتم لازم است.", "error");
      return; }
  
    let computedTotal = 0;
    const order_items = Array.from(rows).map(r=>{
      const service = parseInt(r.querySelector('.serviceId').value);
      const cloth   = parseInt(r.querySelector('.clothId').value);
      const qty     = parseInt(r.querySelector('.quantity').value) || 1;
      const extras  = Array.from(r.querySelectorAll('.extraService:checked')).map(chk=>parseInt(chk.value));
      const totalP  = parseInt(r.querySelector('.totalPrice').value) || 0;
      computedTotal += totalP;
  
      const payload = {service, cloth, quantity: qty, extra_services: extras, total_price: totalP};
      if(r.dataset.itemId) payload.id = parseInt(r.dataset.itemId);
      return payload;
    });
  
    const discount_amount = parseFloat(discountSelect.value) || 0;
  
    const res = await fetch(`/orders/ordermanagment/${orderIdFromUrl}/`, {
      method:'PATCH',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
      body: JSON.stringify({
        total_amount: computedTotal,
        discount_amount: discount_amount,
        order_items: order_items
      })
    });
    const data = await res.json();
    if(res.ok){ showPopup("سفارش با موفقیت ویرایش شد.", "success"); }
    else { showPopup("خطا: " + JSON.stringify(data), "error"); }
  }

  async function editOrder(){
    const res = await fetch(`/orders/ordermanagment/${orderIdFromUrl}/`);
    if(!res.ok){ showPopup("خطا در دریافت سفارش.", "error"); return; }
    const order = await res.json();
  
    discountSelect.value = order.discount_amount || 0;
    document.getElementById('orderInfo').innerHTML = `
      🆔 سفارش: ${order.id} <br>
      👤 مشتری: ${order.customer_name} <br>
      📞 تلفن: ${order.customer_phone} <br>
      📅 تاریخ: ${order.order_date_shamsi}
    `;
  
    itemsContainer.innerHTML="";
    if(order.order_items.length){
      order.order_items.forEach(it=>{
        addItem({
          id: it.id,
          service: it.service,
          cloth: it.cloth,
          quantity: it.quantity,
          extra_services: it.extra_services
        });
      });
    } else {
      addItem();
    }
    updateGrandTotal();
  }

  async function init(){
    await fetchOrderPageData();
    await editOrder();
    document.getElementById('updateOrderForm').addEventListener('submit', updateOrder);
    document.getElementById('addItemBtn').addEventListener('click', ()=>addItem());
  }
  document.addEventListener('DOMContentLoaded', init);