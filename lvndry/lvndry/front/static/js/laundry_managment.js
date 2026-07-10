document.addEventListener('DOMContentLoaded', () => {

    const messageDiv = document.getElementById("message");
    const servicesList = document.getElementById("servicesList");
    const clothesList = document.getElementById("clothesList");
    const extraservicesList = document.getElementById("extraservicesList");
    
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
    
    async function fetchAllData(){
      try {
        const res = await fetch('/items/orderpagedata/');
        const data = await res.json();
    
        const services = data.services;
        if(servicesList) servicesList.innerHTML = ""; 
        document.getElementById("servicesListTitle").innerHTML = "<h4>لیست خدمات:</h4>";
        const serviceSelect = document.getElementById('serviceSelect');
        if(serviceSelect) serviceSelect.innerHTML = '';
        services.forEach(s => {
          if(servicesList){
            const div = document.createElement("div");
            div.classList.add("itemDiv");
            div.textContent = `ID: ${s.id} | نام: ${s.name} | ضریب قیمت: ${s.price_modifier}`;
            servicesList.appendChild(div);
          }
          if(serviceSelect){
            const option = document.createElement('option');
            option.value = s.id;
            option.textContent = `${s.name} (ID: ${s.id})`;
            serviceSelect.appendChild(option);
          }
        });
        
        const clothes = data.clothes;
        if(clothesList) clothesList.innerHTML = ""; 
        document.getElementById("clothesListTitle").innerHTML = "<h4>لیست لباس‌ها:</h4>";
        const clothSelect = document.getElementById('clothSelect');
        if(clothSelect) clothSelect.innerHTML = '';
        clothes.forEach(c => {
          if(clothesList){
            const div = document.createElement("div");
            div.classList.add("itemDiv");
            div.textContent = `ID: ${c.id} | نام: ${c.name} | قیمت: ${c.base_price}`;
            clothesList.appendChild(div);
          }
          if(clothSelect){
            const option = document.createElement('option');
            option.value = c.id;
            option.textContent = `${c.name} (ID: ${c.id})`;
            clothSelect.appendChild(option);
          }
        });
    
        const extraServices = data.extraservice;
        if(extraservicesList) extraservicesList.innerHTML = ""; 
        document.getElementById("extraservicesListTitle").innerHTML = "<h4>لیست خدمات اضافی:</h4>";
        extraServices.forEach(service => {
          if(extraservicesList){
            const div = document.createElement("div");
            div.classList.add("itemDiv");
            div.textContent = `ID: ${service.id} | نام: ${service.name} | قیمت: ${service.extra_fee}`;
            extraservicesList.appendChild(div);
          }
        });

        const discounts = data.discount;
        const discountsList = document.getElementById("discountsList");
        if(discountsList) discountsList.innerHTML = "";
        document.getElementById("discountsListTitle").innerHTML = "<h4>لیست تخفیف ها:</h4>";
        discounts.forEach(d => {
          if(discountsList){
            const div = document.createElement("div");
            div.classList.add("itemDiv");
            div.textContent = `ID: ${d.id}  |  نام: ${d.name}  |  درصد: ${d.percent}%`;
            discountsList.appendChild(div); 
          }
        });
    
      } catch(err){ console.error(err); }
    }
    
    const showDeletedBtn = document.getElementById("showDeletedBtn");
    const deletedItemsContainer = document.getElementById("deletedItemsContainer");
    
    let isVisible = false;
    
    function getItemUrl(type, id) {
      const urls = {
        service: `/items/services/${id}/`,
        clothes: `/items/clothes/${id}/`,
        extraservice: `/items/extraservices/${id}/`,
        discount: `/items/discounts/${id}/`
      };
      return urls[type];
    }
    
    const typeNamesFa = {
      service: "خدمت",
      extraservice: "خدمت اضافی",
      clothes: "لباس",
      discount: "تخفیف"
    };
    
    async function fetchDeletedItems() {
      try {
        const res = await fetch("/items/deleteditems/");
        const data = await res.json();
    
        deletedItemsContainer.innerHTML = "";
    
        const allItems = [
          ...(data.services || []).map(i => ({ ...i, type: 'service' })),
          ...(data.clothes || []).map(i => ({ ...i, type: 'clothes' })),
          ...(data.extras || []).map(i => ({ ...i, type: 'extraservice' })),
          ...(data.discounts || []).map(i => ({ ...i, type: 'discount' }))
        ];
    
        if (allItems.length === 0) {
          deletedItemsContainer.innerHTML = "<p>هیچ آیتم حذف شده‌ای وجود ندارد</p>";
          return;
        }
    
        allItems.forEach(item => {
          const card = document.createElement("div");
          card.classList.add("itemCard");
          card.innerHTML = `
            <p><strong>نوع: ${typeNamesFa[item.type]}</strong></p>
            <p>نام: ${item.name}</p>
            <p>ایدی : ${item.id}</p>
            ${item.price_modifier ? `<p>ضریب قیمت: ${item.price_modifier}</p>` : ''}
            ${item.price ? `<p>قیمت: ${item.price}</p>` : ''}
            ${item.percent ? `<p>درصد: ${item.percent}</p>` : ''}
            ${item.base_price ? `<p>قیمت پایه: ${item.base_price}</p>` : ''}
            ${item.extra_fee ? `<p>هزینه اضافی: ${item.extra_fee}</p>` : ''}
            <button class="restoreBtn">🔄 بازگردانی</button>
          `;
    
          card.querySelector(".restoreBtn").addEventListener("click", async () => {
            const url = getItemUrl(item.type, item.id);
            try {
              const res = await fetch(url, {
                method: "PATCH",
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify({ is_active: true })
              });
    
              if (res.ok) {
                alert(`✅ آیتم "${item.name}" بازگردانی شد`);
                fetchDeletedItems();
              } else {
                const errorData = await res.json();
                alert(`❌ خطا در بازگردانی "${item.name}"`);
              }
            } catch (err) {
              console.error(err);
              alert(`❌ خطا در بازگردانی "${item.name}"`);
            }
          });
    
          deletedItemsContainer.appendChild(card);
        });
    
      } catch (err) {
        deletedItemsContainer.innerHTML = "❌ خطا در دریافت آیتم‌ها";
        console.error(err);
      }
    }
    
    showDeletedBtn.addEventListener("click", async () => {
      if (!isVisible) {
        await fetchDeletedItems();
        deletedItemsContainer.style.display = "grid"; 
        showDeletedBtn.textContent = "❌ پنهان کردن آیتم‌های حذف شده";
      } else {
        deletedItemsContainer.style.display = "none";
        showDeletedBtn.textContent = "🗑 نمایش آیتم‌های حذف شده";
      }
      isVisible = !isVisible;
    });
    
    const addServiceForm = document.getElementById("addServiceForm");
    if(addServiceForm){
      addServiceForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const payload = Object.fromEntries(new FormData(e.target).entries());
        const res = await fetch('/items/services/', {
          method:"POST",
          headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
          body: JSON.stringify(payload)
        });
        if(res.ok){ 
          showPopup("خدمت با موفقیت اضافه شد.", "success");
          e.target.reset(); 
          fetchAllData(); 
        }
        else showPopup("خطا در افزودن خدمت.", "error");
        });
    }

    const editServiceForm = document.getElementById("editServiceForm");
    if(editServiceForm){
      editServiceForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const fd = new FormData(e.target);
        const serviceId = fd.get("id");
    
        const payload = {};
        for (const [key, value] of fd.entries()) {
          if (key !== "id" && value.trim() !== "") {
            payload[key] = key === "price_modifier" ? Number(value) : value;
          }
        }
    
        const res = await fetch(`/items/services/${serviceId}/`, {
          method:"PATCH",
          headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
          body: JSON.stringify(payload)
        });
    
        if(res.ok){ showPopup("ویرایش خدمت انجام شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در ویرایش خدمت.", "error");
      });
    }
    
    const deleteServiceForm = document.getElementById("deleteServiceForm");
    if(deleteServiceForm){
      deleteServiceForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const serviceId = new FormData(e.target).get("id");
    
        const res = await fetch(`/items/services/${serviceId}/`, {
          method:"DELETE",
          headers:{'X-CSRFToken':csrftoken}
        });
    
        if(res.ok){ showPopup("خدمت با موفقیت حذف شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در حذف خدمت.", "error");
      });
    }
    
    const addClothForm = document.getElementById("addClothForm");
    if(addClothForm){
      addClothForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const payload = Object.fromEntries(new FormData(e.target).entries());
        const res = await fetch('/items/clothes/', {
          method:"POST",
          headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
          body: JSON.stringify(payload)
        });
        if(res.ok){ showPopup("لباس جدید ثبت شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در افزودن لباس.", "error");
      });
    }

    const editClothForm = document.getElementById("editClothForm");
    if(editClothForm){
      editClothForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const fd = new FormData(e.target);
        const clothId = fd.get("id");
    
        const payload = {};
        for (const [key, value] of fd.entries()) {
          if (key !== "id" && value.trim() !== "") {
            payload[key] = key === "base_price" ? Number(value) : value;
          }
        }
        
        const res = await fetch(`/items/clothes/${clothId}/`, {
          method:"PATCH",
          headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
          body: JSON.stringify(payload)
        });
    
        if(res.ok){ showPopup("ویرایش لباس انجام شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در ویرایش لباس.", "error");

      });
    }
    
    const deleteClothForm = document.getElementById("deleteClothForm");
    if(deleteClothForm){
      deleteClothForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const clothId = new FormData(e.target).get("id");
    
        const res = await fetch(`/items/clothes/${clothId}/`, {
          method:"DELETE",
          headers:{'X-CSRFToken':csrftoken}
        });
    
        if(res.ok){ showPopup("لباس حذف شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در حذف لباس.", "error");

      });
    }

    const addExtraServicesForm = document.getElementById("addExtraServicesForm");
    if(addExtraServicesForm){
      addExtraServicesForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const payload = Object.fromEntries(new FormData(e.target).entries());
        const res = await fetch('/items/extraservices/', {
          method:"POST", headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
          body: JSON.stringify(payload)
        });
        if(res.ok){ showPopup("خدمت اضافی جدید اضافه شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در افزودن خدمت اضافی.", "error");
      });
    }
    
    const editExtraServicesForm = document.getElementById("editExtraServicesForm");
    if(editExtraServicesForm){
      editExtraServicesForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const fd = new FormData(e.target);
        const serviceId = fd.get("id");
    
        const payload = {};
        for (const [key, value] of fd.entries()) {
          if (key !== "id" && value.trim() !== "") {
            payload[key] = key === "extra_fee" ? Number(value) : value;
          }
        }
    
        const res = await fetch(`/items/extraservices/${serviceId}/`, {
          method:"PATCH",
          headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
          body: JSON.stringify(payload)
        });
    
        if(res.ok){ showPopup("ویرایش خدمت اضافی انجام شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در ویرایش خدمت اضافی.", "error");
      });
    }
    
    const deleteExtraServicesForm = document.getElementById("deleteExtraServicesForm");
    if(deleteExtraServicesForm){
      deleteExtraServicesForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const serviceId = new FormData(e.target).get("id"); 
    
        const res = await fetch(`/items/extraservices/${serviceId}/`, {
          method:"DELETE",
          headers:{'X-CSRFToken':csrftoken}
        });
    
        if(res.ok){ showPopup("خدمت اضافی حذف شد.", "success");
          e.target.reset(); fetchAllData(); }
        else showPopup("خطا در حذف خدمت اضافی.", "error");
      });
    }
    
    const addDiscountForm = document.getElementById("addDiscountForm");
    if(addDiscountForm){
      addDiscountForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const payload = Object.fromEntries(new FormData(e.target).entries());
        const res = await fetch('/items/discounts/', {
          method:"POST",
          headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},
          body: JSON.stringify(payload)
        });
        if(res.ok){ 
          showPopup("تخفیف جدید ثبت شد.", "success"); 
          e.target.reset(); 
          fetchAllData(); 
        }
        else showPopup("خطا در افزودن تخفیف.", "error");
      });
    }
    const editDiscountForm = document.getElementById("editDiscountForm");
    if(editDiscountForm){
      editDiscountForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const fd = new FormData(e.target);
        const discountId = fd.get("id");
    
        const payload = {};
        for (const [key, value] of fd.entries()) {
          if (value.trim() !== "" && key !== "id") {  
            payload[key] = key === "percent" ? Number(value) : value;
          }
        }
    
        const res = await fetch(`/items/discounts/${discountId}/`, {
          method: "PATCH",
          headers: {'Content-Type':'application/json','X-CSRFToken': csrftoken},
          body: JSON.stringify(payload)
        });
    
        if(res.ok){
          showPopup("ویرایش تخفیف انجام شد.", "success");
          e.target.reset();
          fetchAllData();
        } else {
          showPopup("خطا در ویرایش تخفیف.", "error");
        }
      });
    }

    const deleteDiscountForm = document.getElementById("deleteDiscountForm");
    if(deleteDiscountForm){
      deleteDiscountForm.addEventListener("submit", async e=>{
        e.preventDefault();
        const discountId = new FormData(e.target).get("id"); 
    
        const res = await fetch(`/items/discounts/${discountId}/`, {
          method:"DELETE",
          headers:{'X-CSRFToken':csrftoken}
        });
    
        if(res.ok){ 
          showPopup("تخفیف حذف شد.", "success"); 
          e.target.reset(); 
          fetchAllData(); 
        }
        showPopup("خطا در حذف تخفیف.", "error");
      });
    }

    const createOrderForm = document.getElementById('createOrderForm');
    if(createOrderForm){
      createOrderForm.addEventListener('submit', async e => {
        e.preventDefault();
    
        const service = document.getElementById('serviceSelect')?.value || "";
        const cloth = document.getElementById('clothSelect')?.value || "";
    
        const extrasSelect = document.getElementById('extraservicesSelect');
        const extras = extrasSelect ? Array.from(extrasSelect.selectedOptions).map(o => o.value) : [];
    
        const payload = { service, cloth, extras };
    
        const res = await fetch('/orders/ordercreate/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify(payload)
        });
    
        if(res.ok) showPopup("سفارش با موفقیت ثبت شد.", "success");
        else showPopup("خطا در ثبت سفارش.", "error");
      });
    }
  
window.scrollToSection = function(sectionId) {
  const section = document.getElementById(sectionId);
  if(section) {
    section.scrollIntoView({ behavior: 'smooth' });
  }
};
    fetchAllData();
    });