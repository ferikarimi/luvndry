let filterMode = 'all';
let orderStatus = "";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.startsWith(name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

async function deleteOrder(orderId, customerName) {
  if (!confirm(`آیا از حذف سفارش ${customerName} مطمئن هستید؟`)) return;

  try {
    const res = await fetch(`/orders/ordermanagment/${orderId}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    });
    if (res.ok) {
      showPopup("سفارش با موفقیت حذف شد.", "success");
      fetchRecentOrders();
    } else {
      showPopup("خطا در حذف سفارش.", "error");
    }
  } catch(err) {
    showPopup("خطای ارتباط با سرور هنگام حذف.", "error");
  }
}

async function fetchRecentOrders(page=1){
  let url = `/orders/allactiveorderslist/?page=${page}&page_size=30`;

  const name = document.getElementById('searchName')?.value || '';
  const code = document.getElementById('searchCode')?.value || '';
  const order = document.getElementById('searchOrder')?.value || '';
  const date = document.getElementById('searchDate')?.value || '';

  if (name) url += `&customer_name=${encodeURIComponent(name)}`;
  if (code) url += `&customer_code=${encodeURIComponent(code)}`;
  if (order) url += `&order_id=${encodeURIComponent(order)}`;
  if (date) url += `&order_date=${encodeURIComponent(date)}`;
  if(filterMode === 'express') url += '&is_express=true';
  if (orderStatus) {
      url += '&delivered=true';
  }

  try {
    const res = await fetch(url);
    const data = await res.json();
    const container = document.getElementById('recentOrders');
    container.innerHTML = "";

    if (!data.results || data.results.length === 0) {
      container.innerHTML = "<p>هیچ سفارشی یافت نشد.</p>";
      return;
    }

    const ordersByDate = {};
    data.results.forEach(order => {
        const orderDate = order.order_date;
        if (!ordersByDate[orderDate]) ordersByDate[orderDate] = [];
        ordersByDate[orderDate].push(order);
    });
    const sortedDates = Object.keys(ordersByDate).sort((a, b) => {
        const [y1,m1,d1] = a.split('/').map(Number);
        const [y2,m2,d2] = b.split('/').map(Number);
        if(y1!==y2) return y2-y1;
        if(m1!==m2) return m2-m1;
        return d2-d1;
    });

    for(const orderDate of sortedDates){
        const dateHeader = document.createElement('h3');
        dateHeader.textContent = `تاریخ: ${orderDate}`;
        dateHeader.style.marginTop = '15px';
        dateHeader.style.fontSize = '20px';
        container.appendChild(dateHeader);

        ordersByDate[orderDate].forEach(item => {
            const div = document.createElement('div');
            div.classList.add('orderRow');
            const mainOrderId = item.order_id || item.id;
            div.innerHTML = `
                <div class="order-info" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                <div style="text-align:right; line-height:2;">
                    <div>
                        <b>شماره سفارش:</b> ${mainOrderId} |
                        <b>مشتری:</b> ${item.customer_name}

                        ${item.customer_level ? `
                            <span style="
                                display:inline-block;
                                margin:0 6px;
                                padding:2px 8px;
                                border-radius:12px;
                                font-size:12px;
                                font-weight:bold;
                                color:white;
                                background:${
                                    item.customer_level === 'طلایی' ? '#FFD700' :
                                    item.customer_level === 'نقره‌ای' ? '#9E9E9E' :
                                    item.customer_level === 'برنزی' ? '#CD7F32' :
                                    '#6c757d'
                                };
                            ">
                                ${item.customer_level}
                            </span>
                        ` : ''}

                        (${item.customer_code}) |
                        <b>تلفن:</b> ${item.customer_phone}
                    </div>

                    <div>
                        <b>تاریخ ثبت سفارش:</b> ${item.order_date} |
                        <b>تعداد سفارش‌های تحویل داده شده:</b> ${item.delivered_orders_count} |
                        <b>مبلغ قابل پرداخت:</b> ${item.final_amount}
                    </div>
                </div>

                ${orderStatus ? '' : `
                <div style="display:flex; gap:10px; align-items:center;">
                    <label>
                    <input type="checkbox"
                            class="status-ready-checkbox"
                            ${item.status === 'Completed' ? 'checked' : ''}
                            onchange="toggleReadyStatus(${mainOrderId}, this)">
                    آماده تحویل
                    </label>

                    <label>
                    <input type="checkbox"
                            class="status-delivered-checkbox"
                            onchange="markAsDelivered(${mainOrderId}, this)">
                    تحویل داده شد
                    </label>
                </div>
                `}
                </div>

                <div class="order-actions" style="margin-top:5px; display:flex; justify-content:space-between; align-items:center;">
                ${orderStatus ? '' : `
                <div class="left-buttons">
                    <button class="delete-btn" onclick="deleteOrder(${mainOrderId}, '${item.customer_name}')">
                    🗑️ حذف
                    </button>

                    <button class="edit-btn" onclick="window.location.href='/order_edit/${mainOrderId}/'">
                    ✏️ ویرایش
                    </button>
                </div>
                `}

                <button onclick="showOrderDetails(${mainOrderId})">
                    🔍 جزئیات
                </button>
                </div>
            `;
            container.appendChild(div);
        });
    }

    const pagDiv = document.getElementById('pagination');
    pagDiv.innerHTML = "";
    if(data.previous){
      const prevBtn = document.createElement('button');
      prevBtn.textContent=" ➡ صفحه قبل";
      prevBtn.onclick = ()=>fetchRecentOrders(page-1);
      pagDiv.appendChild(prevBtn);
    }
    if(data.next){
      const nextBtn = document.createElement('button');
      nextBtn.textContent="صفحه بعد ⬅";
      nextBtn.onclick = ()=>fetchRecentOrders(page+1);
      pagDiv.appendChild(nextBtn);
    }
    
  } catch(err){
    showPopup("خطا در دریافت لیست سفارش‌ها.", "error");
  }
}


async function toggleReadyStatus(orderId, checkbox){
  const newStatus = checkbox.checked ? 'Completed' : 'In progress';
  try {
    const res = await fetch(`/orders/orderstatusupdate/${orderId}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type':'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({status: newStatus})
    });
    if(res.ok){
      fetchRecentOrders();
    } else {
      const errData = await res.json();
      showPopup("خطا در تغییر وضعیت سفارش.", "error");

      checkbox.checked = !checkbox.checked;
    }
  } catch(err){
    showPopup("خطای ارتباط با سرور هنگام تغییر وضعیت.", "error");
    checkbox.checked = !checkbox.checked;
  }
}

async function markAsDelivered(orderId, checkbox){
  if(!confirm("آیا مطمئن هستید این سفارش به صاحب بازگردانده شود و از لیست حذف شود؟")){
    checkbox.checked = false;
    return;
  }
  try {
    const res = await fetch(`/orders/orderstatusupdate/${orderId}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type':'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({status: 'Delivered'})
    });
    if(res.ok){
      fetchRecentOrders();
    } else {
      const errData = await res.json();
      showPopup("خطا در تغییر وضعیت سفارش.", "error");
      checkbox.checked = false;
    }
  } catch(err){
    showPopup("خطای سرور هنگام تغییر وضعیت.", "error");
    checkbox.checked = false;
  }
}

async function showOrderDetails(orderId){
  try{
    const res = await fetch(`/orders/detail/${orderId}/`);
    if(!res.ok) throw new Error("خطا در دریافت جزئیات سفارش");
    const data = await res.json();

    const itemsHtml = data.items.map(it=>{
      const extras = Array.isArray(it.extra_services) ? it.extra_services.map(es=>es.name) : [];
      return `
      <div style="background:#f7faff;border:1px solid #e0e7ff;border-radius:10px;padding:12px;margin-bottom:10px;">
        <div style="font-weight:bold;font-size:15px;">
          ${it.cloth_name} <span style="color:#444;font-weight:bold;">—> ${it.service_name}</span>
        </div>
        <div style="font-size:14px;margin-top:4px;">
          تعداد: ${it.quantity} عدد<br>
          مبلغ: ${it.total_price.toLocaleString()} تومان
        </div>
        ${extras.length>0 ? `<div style="margin-top:6px;font-size:13px;color:#444;">خدمات اضافه: ${extras.join(', ')}</div>` : ''}
        ${it.is_express ? `<div style="margin-top:6px;"><span style="background:#ffe6e6;color:#c00;font-size:12px;padding:3px 8px;border-radius:6px;font-weight:bold;">کار عجله‌ای</span></div>` : ''}
      </div>`;
    }).join('');

    document.getElementById('orderDetailContent').innerHTML = itemsHtml || '<p style="text-align:center;color:#999;">هیچ آیتمی برای این سفارش ثبت نشده است.</p>';

    const overlay = document.getElementById('modalOverlay');
    const modal = document.getElementById('orderDetailModal');
    overlay.style.display='block';
    modal.style.display='block';
    setTimeout(()=>{ modal.style.opacity='1'; modal.style.transform='translate(-50%,-50%) scale(1)'; },10);
  } catch(err){
    showPopup("خطا در نمایش جزئیات سفارش.", "error");
  }
}

function closeModal(){
  const overlay = document.getElementById('modalOverlay');
  const modal = document.getElementById('orderDetailModal');
  modal.style.opacity='0';
  modal.style.transform='translate(-50%,-50%) scale(0.95)';
  setTimeout(()=>{
    overlay.style.display='none';
    modal.style.display='none';
  },200);
}

document.getElementById('modalOverlay').addEventListener('click', closeModal);

document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('showAllBtn').addEventListener('click', () => {
        filterMode = 'all';
        orderStatus = "";
        fetchRecentOrders(1);
    });

    document.getElementById('showExpressBtn').addEventListener('click', () => {
        filterMode = 'express';
        orderStatus = "";
        fetchRecentOrders(1);
    });

    document.getElementById('showDeliveredBtn').addEventListener('click', () => {
        filterMode = 'all';
        orderStatus = "true";
        fetchRecentOrders(1);
    });

    document.getElementById('searchBtn').addEventListener('click', () => fetchRecentOrders(1));

    document.getElementById('resetBtn').addEventListener('click', () => {
        ['searchName', 'searchCode', 'searchOrder', 'searchDate'].forEach(id => {
            document.getElementById(id).value = '';
        });
        fetchRecentOrders(1);
    });

    ['searchName', 'searchCode', 'searchOrder', 'searchDate'].forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('keypress', e => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    fetchRecentOrders(1);
                }
            });
        }
    });

    fetchRecentOrders(1);
});