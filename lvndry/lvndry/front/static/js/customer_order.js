const weekDaysMap = {
    'Saturday': 'شنبه',
    'Sunday': 'یکشنبه',
    'Monday': 'دوشنبه',
    'Tuesday': 'سه‌شنبه',
    'Wednesday': 'چهارشنبه',
    'Thursday': 'پنج‌شنبه',
    'Friday': 'جمعه'
  };
  function formatOrderTime(orderTimeJalali) {
    if (!orderTimeJalali) return '---';
    const parts = orderTimeJalali.split(' ');
    if (parts.length < 2) return orderTimeJalali;
    const dayEn = parts[0];
    const datePart = parts.slice(1).join(' ');
    const dayFa = weekDaysMap[dayEn] || dayEn;
    return `${dayFa} ${datePart}`;
  }
  
  const urlParams = new URLSearchParams(window.location.search);
  const customerId = urlParams.get("customer_id");
  
  async function fetchOrders() {
    if (!customerId) {
      showPopup("کد مشتری معتبر نیست.", "error");
      return;
    }
    try {
      const response = await fetch(`/orders/customerorders/${customerId}/`);
      if (!response.ok) {
        showPopup("خطا در دریافت سفارشات مشتری.", "error");
        return;
      }
      
      const data = await response.json();
      let html = "";
      if (data.customer) {
        html += `
          <div class="mb-4 p-3 bg-info bg-opacity-10 border border-info rounded">
            <h4>اطلاعات مشتری</h4>
            <p><strong>نام:</strong> ${data.customer.fullname || '---'}</p>
            <p><strong>کد مشتری:</strong> ${data.customer.code || '---'}</p>
            <p><strong>شماره تلفن:</strong> ${data.customer.phone || '---'}</p>
            <p><strong>آدرس:</strong> ${data.customer.address || '---'}</p>
            <p>
              <strong>کل سفارشات:</strong>
              ${data.customer.order_count || '---'} 
              (<strong>سفارشات تکمیل شده:</strong> ${data.customer.delivered_order_count || '---'})
            </p>
          </div>
        `;
      }
  
      const orders = data.orders;
      if (!orders || orders.length === 0) {
        showPopup("برای این مشتری هیچ سفارشی ثبت نشده.", "warning");
        document.getElementById("ordersList").innerHTML = html;
        attachDeliveredButtonHandlers();
        return;
      }

      let pendingItemsHtml = '';
      let deliveredItemsHtml = '';
  
      orders.forEach(order => {
        const itemsRows = order.order_items.map(item => {
          const extraServices = (item.extra_services && item.extra_services.length > 0)
              ? item.extra_services.map(s => s.name || s).join(', ')
              : '---';
          return `
            <tr>
              <td>${item.service_name || '---'}</td>
              <td>${item.cloth_name || '---'}</td>
              <td>${extraServices}</td>
              <td>${item.quantity}</td>
              <td>${item.unit_price}</td>
              <td>${item.total_price}</td>
            </tr>
          `;
        }).join('');
  
        if (order.is_delivered) {
          deliveredItemsHtml += `
            <li class="list-group-item bg-success bg-opacity-10 border border-success rounded p-3 mb-3">
              <h5 class="text-success">✅ فاکتور سفارش ${order.id}</h5>
              <strong>زمان سفارش:</strong> ${formatOrderTime(order.order_time_jalali)} <br>
              <strong>زمان تحویل:</strong> ${formatOrderTime(order.delivery_time_jalali)} <br>
              <table class="table table-bordered mt-2">
                <thead class="table-success">
                  <tr>
                    <th>سرویس</th>
                    <th>لباس</th>
                    <th>خدمات اضافی</th>
                    <th>تعداد</th>
                    <th>قیمت واحد</th>
                    <th>جمع آیتم</th>
                  </tr>
                </thead>
                <tbody>
                  ${itemsRows}
                </tbody>
              </table>
              <p class="text-end"><strong>مبلغ کل:</strong> ${order.total_amount} تومان</p>
              <p class="text-end"><strong>تخفیف:</strong> ${order.discount_amount}%</p>
              <p class="text-end"><strong>مبلغ نهایی:</strong> <span class="fw-bold">${order.final_amount}</span></p>
            </li>
          `;
        } else {
          pendingItemsHtml += `
            <li class="list-group-item bg-warning bg-opacity-10 border border-warning rounded p-3 mb-3">
              <strong>کد سفارش:</strong> ${order.id} <br>
              <strong>مبلغ کل:</strong> ${order.total_amount} <br>
              <strong>مبلغ نهایی:</strong> ${order.final_amount} <br>
              <strong>وضعیت:</strong> ${order.status_display} <br>
              <strong>زمان سفارش:</strong> ${formatOrderTime(order.order_time_jalali)} <br>
              <button class="btn btn-sm btn-warning mt-2" onclick="goToEditOrder(${order.id})">✏️ ویرایش سفارش</button>
            </li>
          `;
        }
      });
  
      html += `
        <div id="pendingSection">
          <h4>سفارشات در حال انجام</h4>
          <ul id="pendingOrders" class="list-group mb-4">
            ${pendingItemsHtml || `<li class="list-group-item text-muted">سفارشی در حال انجام وجود ندارد.</li>`}
          </ul>
        </div>
  
        <div id="deliveredSection">
          <h4 id="deliveredHeader">سفارشات تحویل شده</h4>
          <ul id="deliveredOrders" class="list-group mb-4">
            ${deliveredItemsHtml || `<li class="list-group-item text-muted">سفارشی تحویل شده وجود ندارد.</li>`}
          </ul>
        </div>
      `;
  
      document.getElementById("ordersList").innerHTML = html;
  
      attachDeliveredButtonHandlers();
  
    } catch (err) {
      console.error(err);
      showPopup("مشکل در اتصال به سرور.", "error");
      attachDeliveredButtonHandlers();
    }
  }
  
  function attachDeliveredButtonHandlers(){
    const gotoBtn = document.getElementById('gotoDeliveredBtn');
    if (gotoBtn) {
      gotoBtn.onclick = function() {
        const el = document.getElementById('deliveredHeader');
        if (el && document.getElementById('deliveredOrders').children.length > 0) {
          el.scrollIntoView({behavior:'smooth', block:'start'});
          el.classList.add('border', 'border-success', 'p-2', 'rounded');
          setTimeout(()=> el.classList.remove('border','border-success','p-2','rounded'), 1600);
        } else {
          showPopup("هیچ سفارش تحویل‌شده‌ای برای نمایش وجود ندارد.", "warning");
        }
      };
    }
  
    const filterBtn = document.getElementById('filterDeliveredBtn');
    const showAllBtn = document.getElementById('showAllBtn');
    if (filterBtn) {
      filterBtn.onclick = function() {
        const pending = document.getElementById('pendingSection');
        if (pending) pending.style.display = 'none';
        const delivered = document.getElementById('deliveredSection');
        if (delivered) delivered.style.display = 'block';
        filterBtn.classList.add('d-none');
        if (showAllBtn) showAllBtn.classList.remove('d-none');
        const el = document.getElementById('deliveredHeader');
        if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
      };
    }
    if (showAllBtn) {
      showAllBtn.onclick = function() {
        const pending = document.getElementById('pendingSection');
        if (pending) pending.style.display = 'block';
        const delivered = document.getElementById('deliveredSection');
        if (delivered) delivered.style.display = 'block';
        showAllBtn.classList.add('d-none');
        if (filterBtn) filterBtn.classList.remove('d-none');
      };
    }
  }
  document.addEventListener("DOMContentLoaded", fetchOrders);
  function goToEditOrder(orderId){
    window.location.href = `/order_edit/${orderId}/`;
  }