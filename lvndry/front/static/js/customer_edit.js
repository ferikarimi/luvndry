const urlParams = new URLSearchParams(window.location.search);
const customerCode = urlParams.get("code"); 

if (!customerCode) {
  showPopup("کد مشتری یافت نشد.", "error");
} else {
  fetch(`/customers/customerupdateprofile/?code=${customerCode}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById('code').value = data.code;
      document.getElementById('fullname').value = data.fullname || '';
      document.getElementById('phone').value = data.phone || '';
      document.getElementById('address').value = data.address || '';
    })
    .catch(err => {
      showPopup("خطا در دریافت اطلاعات مشتری.", "error");
    });
}

document.getElementById('saveBtn').addEventListener('click', async ()=>{
  const payload = {
    code: document.getElementById('code').value 
  };
  const fullname = document.getElementById('fullname').value.trim();
  const phone = document.getElementById('phone').value.trim();
  const address = document.getElementById('address').value.trim();

  if(fullname) payload.fullname = fullname;
  if(phone) payload.phone = phone;
  if(address) payload.address = address;

  const res = await fetch(`/customers/customerupdateprofile/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie('csrftoken')
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  if (res.ok) {
    showPopup("اطلاعات با موفقیت ذخیره شد.", "success");
  } else {
    const text = typeof data === "object" ? JSON.stringify(data) : "خطای ناشناخته";
    showPopup(text, "error");
  }
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
