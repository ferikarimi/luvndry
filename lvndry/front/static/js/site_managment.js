const csrftoken = document.querySelector('[name=csrf-token]').content;
const commentsList = document.getElementById('commentsList');
const galleryList = document.getElementById('galleryList');
const galleryForm = document.getElementById('galleryForm');


async function loadComments(page = 1) {

    try {
        const response = await fetch(`/customers/admincommentlist/?page=${page}`);
        const data = await response.json();

        commentsList.innerHTML = "";

        if (!data.results || data.results.length === 0) {
            showPopup("هیچ نظری ثبت نشده است.", "warning");
            return;
        }

        data.results.forEach(comment => {
            const div = document.createElement('div');
            div.classList.add('comment-card');
            div.innerHTML = `
                <p><strong>${comment.customer} (${comment.customer_phone})</strong> گفت:</p>
                <p>${comment.text}</p>
                <p>تاریخ: ${comment.created_at ? new Date(comment.created_at).toLocaleString('fa-IR') : ''}</p>
                <p>
                    وضعیت:
                    <select data-id="${comment.id}" class="statusSelect">
                        <option value="pending" ${comment.status === 'pending' ? 'selected' : ''}>در انتظار</option>
                        <option value="approved" ${comment.status === 'approved' ? 'selected' : ''}>تأیید شده</option>
                        <option value="rejected" ${comment.status === 'rejected' ? 'selected' : ''}>رد شده</option>
                    </select>
                </p>
            `;
            commentsList.appendChild(div);
        });

        let paginationDiv = document.createElement('div');
        paginationDiv.style.textAlign = "center";
        paginationDiv.style.marginTop = "20px";

        if (data.previous) {
            let prevBtn = document.createElement('button');
            prevBtn.textContent = "صفحه قبل";
            prevBtn.onclick = () => loadComments(page - 1);
            paginationDiv.appendChild(prevBtn);
        }

        if (data.next) {
            let nextBtn = document.createElement('button');
            nextBtn.textContent = "صفحه بعد";
            nextBtn.onclick = () => loadComments(page + 1);
            paginationDiv.appendChild(nextBtn);
        }
        commentsList.appendChild(paginationDiv);

        document.querySelectorAll('.statusSelect').forEach(sel => {
            sel.addEventListener('change', async e => {
                const id = e.target.dataset.id;
                const status = e.target.value;

                try {
                    const res = await fetch(`/customers/admincommentstatus/${id}/`, {
                        method: 'PATCH',
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrftoken
                        },
                        body: JSON.stringify({ status })
                    });

                    if (res.ok) {
                        showPopup("وضعیت کامنت بروزرسانی شد.", "success");
                    } else {
                        showPopup("خطا در بروزرسانی وضعیت کامنت.", "error");
                    }
                } catch {
                    showPopup("ارتباط با سرور برقرار نشد.", "error");
                }
            });
        });

    } catch {
        showPopup("خطا در بارگذاری کامنت‌ها", "error");
    }
}

async function loadGallery() {

    try {
        const res = await fetch('/CMS/gallery/');
        const data = await res.json();

        galleryList.innerHTML = "";

        if (data.length === 0) {
            showPopup("هیچ تصویری ثبت نشده است.", "warning");
            return;
        }

        data.forEach(img => {
            const div = document.createElement('div');
            div.classList.add('gallery-card');
            div.innerHTML = `
                <img src="${img.image}" alt="${img.title}">
                <p>${img.title || "بدون عنوان"}</p>

                <div class="btn-container">
                    <label>
                        فعال:
                        <input type="checkbox" class="activeCheckbox" data-id="${img.id}" ${img.is_active ? 'checked' : ''}>
                    </label>

                    <button class="delete-btn" data-id="${img.id}">حذف</button>
                </div>
            `;
            galleryList.appendChild(div);
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', async e => {
                const id = e.target.dataset.id;

                try {
                    const res = await fetch(`/CMS/gallery/${id}/`, {
                        method: "DELETE",
                        headers: { "X-CSRFToken": csrftoken }
                    });

                    if (res.ok) {
                        showPopup("عکس با موفقیت حذف شد.", "success");
                        loadGallery();
                    } else {
                        showPopup("خطا در حذف عکس.", "error");
                    }
                } catch {
                    showPopup("خطا در ارتباط با سرور.", "error");
                }
            });
        });

        document.querySelectorAll('.activeCheckbox').forEach(cb => {
            cb.addEventListener('change', async e => {
              const id = e.target.dataset.id;
              const isActive = e.target.checked;
          
              try {
                const res = await fetch(`/CMS/gallery/${id}/`, {
                  method: "PATCH",
                  headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                  },
                  body: JSON.stringify({ is_active: isActive })
                });
                if (res.ok) {
                  showPopup("وضعیت تصویر با موفقیت بروزرسانی شد.", "success");
                } else {
                  let text;
                  try { text = await res.json(); text = JSON.stringify(text); }
                  catch { text = await res.text(); }
                  e.target.checked = !isActive;
                  showPopup("خطا در بروزرسانی وضعیت تصویر: " + (text || res.status), "error");
                }
              } catch (err) {
                e.target.checked = !isActive;
                showPopup("خطا در ارتباط با سرور. دوباره تلاش کنید.", "error");
              }
            });
          });
          

    } catch {
        showPopup("خطا در بارگذاری تصاویر.", "error");
    }
}

galleryForm.addEventListener('submit', async e => {
    e.preventDefault();
    const formData = new FormData(galleryForm);

    try {
        const res = await fetch('/CMS/gallery/', {
            method: "POST",
            headers: { "X-CSRFToken": csrftoken },
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            showPopup("تصویر با موفقیت آپلود شد.", "success");
            galleryForm.reset();
            loadGallery();
        } else {
            showPopup("خطا در آپلود تصویر.", "error");
        }
    } catch {
        showPopup("خطا در ارتباط با سرور.", "error");
    }
});


















const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
const apiBase = "/CMS/notifications/";

document.addEventListener("DOMContentLoaded", function () {
    loadNotifs();

    document.getElementById("notifForm").addEventListener("submit", saveNotif);
    document.getElementById("filter").addEventListener("change", loadNotifs);
    document.getElementById("cancelEdit").addEventListener("click", resetForm);
});


/* -------------------------
   گرفتن لیست نوتیفیکیشن‌ها
-------------------------- */
function loadNotifs() {
    fetch(apiBase)
        .then(res => res.json())
        .then(data => {
            let list = data;
            const filter = document.getElementById("filter").value;

            if (filter === "active") list = list.filter(n => n.is_active === true);
            if (filter === "inactive") list = list.filter(n => n.is_active === false);

            renderNotifs(list);
        })
        .catch(() => {
            showPopup("خطا در دریافت لیست نوتیفیکیشن‌ها.", "error");
        });
}


/* -------------------------
   نمایش نوتیف‌ها در صفحه
-------------------------- */
function renderNotifs(notifs) {
    const container = document.getElementById("notifList");
    container.innerHTML = "";

    if (notifs.length === 0) {
        container.innerHTML = "<p>نوتیفیکیشنی موجود نیست.</p>";
        return;
    }

    let row;
    notifs.forEach((n, index) => {
        // هر 3 آیتم یک ردیف جدید
        if (index % 3 === 0) {
            row = document.createElement("div");
            row.className = "row mb-3";
            container.appendChild(row);
        }

        const col = document.createElement("div");
        col.className = "col-md-4"; // هر باکس یک سوم عرض ردیف

        col.innerHTML = `
            <div class="card p-3 h-100">
                <h5>${n.title}</h5>
                <p>${n.message}</p>
                <span class="badge ${n.is_active ? 'bg-success' : 'bg-danger'}">
                    ${n.is_active ? 'فعال' : 'غیرفعال'}
                </span>
                <div class="mt-3">
                    <button class="btn btn-warning btn-sm" onclick="editNotif(${n.id})">ویرایش</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteNotif(${n.id})">حذف</button>
                </div>
            </div>
        `;

        row.appendChild(col);
    });
}



/* -------------------------
         ساخت / ویرایش با PATCH
-------------------------- */
function saveNotif(event) {
    event.preventDefault();

    const id = document.getElementById("notifId").value;

    const body = {
        title: document.getElementById("title").value,
        message: document.getElementById("message").value,
        is_active: document.getElementById("is_active").value === "true"
    };

    const url = id ? apiBase + id + "/" : apiBase;
    const method = id ? "PATCH" : "POST";

    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(body)
    })
        .then(res => {
            if (!res.ok) {
                showPopup("خطا در ذخیره نوتیفیکیشن.", "error");
            }
            return res.json();
        })
        .then(() => {
            resetForm();
            loadNotifs();
            if (id) {
                showPopup("نوتیفیکیشن با موفقیت ویرایش شد.", "success");
            } else {
                showPopup("نوتیفیکیشن جدید با موفقیت ایجاد شد.", "success");
            }
        })
        .catch(() => {
            showPopup("خطا در ارتباط با سرور.", "error");
        });
}


/* -------------------------
        حذف نوتیف
-------------------------- */
function deleteNotif(id) {
    if (!confirm("مطمئن هستی؟")) return;

    fetch(apiBase + id + "/", {
        method: "DELETE",
        headers: { "X-CSRFToken": csrfToken }
    })
    .then(res => {
        if (res.ok) {
            showPopup("نوتیفیکیشن حذف شد.", "success");
            loadNotifs();
        } else {
            showPopup("خطا در حذف نوتیفیکیشن.", "error");
        }
    })
    .catch(() => showPopup("خطا در ارتباط با سرور.", "error"));
}



/* -------------------------
       ویرایش نوتیف (فقط پر کردن فرم)
-------------------------- */
function editNotif(id) {
    fetch(apiBase + id + "/")
        .then(res => {
            if (!res.ok) showPopup("خطا در دریافت اطلاعات نوتیف.", "error");
            return res.json();
        })
        .then(n => {
            document.getElementById("notifId").value = n.id;
            document.getElementById("title").value = n.title;
            document.getElementById("message").value = n.message;
            document.getElementById("is_active").value = n.is_active ? "true" : "false";

            document.getElementById("formTitle").innerText = "ویرایش نوتیفیکیشن";
            document.getElementById("cancelEdit").style.display = "inline-block";
        })
        .catch(() => showPopup("خطا در ارتباط با سرور.", "error"));
}


/* -------------------------
         ریست کردن فرم
-------------------------- */
function resetForm() {
    document.getElementById("notifId").value = "";
    document.getElementById("title").value = "";
    document.getElementById("message").value = "";
    document.getElementById("is_active").value = "true";

    document.getElementById("formTitle").innerText = "ایجاد نوتیفیکیشن جدید";
    document.getElementById("cancelEdit").style.display = "none";
}







loadComments();
loadGallery();