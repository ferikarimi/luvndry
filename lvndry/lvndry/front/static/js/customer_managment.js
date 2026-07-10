let currentPage = 1;
let nextUrl = null;
let prevUrl = null;

async function fetchCustomers(url = `/customers/allcustomers/?page=${currentPage}`) {
  try {
    const res = await fetch(url);
    const data = await res.json();
    nextUrl = data.next;
    prevUrl = data.previous;
    const listDiv = document.getElementById('customersList');
    listDiv.innerHTML = "";
    if (!data.results || data.results.length === 0) {
      showPopup("هیچ مشتری یافت نشد.", "warning");
      return;
    }
    data.results.forEach(c => {
      const div = document.createElement('div');
      div.className = "col-md-4 mb-3";
      div.innerHTML = `
        <div class="card p-3 shadow-sm">
          <h5 class="mb-2">${c.fullname || '---'}</h5>
          <p class="mb-1"><b>کد مشتری:</b> ${c.code}</p>
          <p class="mb-1"><b>شماره:</b> ${c.phone}</p>
          <p class="mb-2"><b>آدرس:</b> ${c.address || '---'}</p>
          <div class="d-flex justify-content-between">
            <a href="/customer_edit/?code=${c.code}" class="btn btn-warning btn-sm">ویرایش</a>
            <a href="/customer_order/?customer_id=${c.id}" class="btn btn-warning btn-sm">سفارشات</a>
            <button class="btn btn-danger btn-sm" onclick="deleteCustomer(${c.code}, '${c.fullname || ''}')">حذف</button>
          </div>
        </div>
      `;
      listDiv.appendChild(div);
    });
  } catch (err) {
    showPopup("خطا در بارگذاری لیست مشتری‌ها.", "error");
  }
}
async function deleteCustomer(code, name) {
  if (!confirm(`آیا مطمئنید می‌خواهید مشتری "${name}" با کد ${code} حذف شود؟`)) return;
  try {
    const res = await fetch(`/customers/delete/${code}/`, {
      method: "DELETE",
      headers: { "X-CSRFToken": getCookie('csrftoken') }
    });

    if (res.ok) {
      showPopup("مشتری با موفقیت حذف شد.", "success");
      fetchCustomers();
    } else {
      showPopup("خطا در حذف مشتری.", "error");
    }

  } catch {
    showPopup("مشکل در اتصال به سرور هنگام حذف.", "error");
  }
}
document.getElementById('nextPage').addEventListener('click', () => {
  if (nextUrl) {
    currentPage++;
    fetchCustomers(nextUrl);
  }
});
document.getElementById('prevPage').addEventListener('click', () => {
  if (prevUrl) {
    currentPage--;
    fetchCustomers(prevUrl);
  }
});
document.getElementById('searchBtn').addEventListener('click', () => {
  const val = document.getElementById('searchInput').value.trim();
  let url = `/customers/allcustomers/?page=1`;
  if (val) url += `&search=${encodeURIComponent(val)}`;
  fetchCustomers(url);
});
document.getElementById('searchInput').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    document.getElementById('searchBtn').click();
  }
});
document.getElementById('resetBtn').addEventListener('click', () => {
  document.getElementById('searchInput').value = "";
  fetchCustomers();
});
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
document.addEventListener('DOMContentLoaded', () => fetchCustomers());