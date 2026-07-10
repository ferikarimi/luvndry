const PAGE_SIZE = 12;

let currentPage = 1;
let totalPages = 1;

let currentSearch = "";
let currentLevel = "";

let nextUrl = null;
let prevUrl = null;


function buildUrl(page = 1) {

    const params = new URLSearchParams();

    params.append("page", page);

    if (currentSearch.trim() !== "") {
        params.append("search", currentSearch);
    }

    if (currentLevel.trim() !== "") {
        params.append("level", currentLevel);
    }

    return `/customers/allcustomers/?${params.toString()}`;

}



function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;

            }

        }

    }

    return cookieValue;

}



function goToPage(page) {

    if (page < 1) return;

    if (page > totalPages) return;

    fetchCustomers(page);

}

async function fetchCustomers(page = 1) {

    currentPage = page;

    try {

        const response = await fetch(buildUrl(page));

        if (!response.ok) {

            throw new Error("Request Failed");

        }

        const data = await response.json();

        nextUrl = data.next;
        prevUrl = data.previous;

        totalPages = Math.max(
            1,
            Math.ceil(data.count / PAGE_SIZE)
        );

        renderCustomers(data.results);

        renderPagination();

    }

    catch (error) {

        console.error(error);

        showPopup(
            "خطا در دریافت اطلاعات مشتری‌ها.",
            "error"
        );

    }

}

function renderCustomers(customers) {

    const container = document.getElementById("customersList");

    container.innerHTML = "";

    if (!customers || customers.length === 0) {

        container.innerHTML = `

            <div class="col-12">

                <div class="alert alert-warning text-center">

                    هیچ مشتری‌ای پیدا نشد.

                </div>

            </div>

        `;

        return;

    }

    customers.forEach(customer => {

        const col = document.createElement("div");

        col.className = "col-md-4 mb-3";

        col.innerHTML = `

            <div class="card shadow-sm h-100">

                <div class="card-body">

                    <h5 class="card-title">

                        ${customer.fullname || "---"}

                    </h5>

                    <p><b>کد مشتری:</b> ${customer.code}</p>

                    <p><b>شماره:</b> ${customer.phone}</p>

                    <p><b>آدرس:</b> ${customer.address || "---"}</p>

                    <div class="d-flex justify-content-between">

                        <a
                            href="/customer_edit/?code=${customer.code}"
                            class="btn btn-warning btn-sm">

                            ویرایش

                        </a>

                        <a
                            href="/customer_order/?customer_id=${customer.id}"
                            class="btn btn-primary btn-sm">

                            سفارشات

                        </a>

                        <button
                            class="btn btn-danger btn-sm delete-btn"
                            data-code="${customer.code}"
                            data-name="${customer.fullname || ""}">

                            حذف

                        </button>

                    </div>

                </div>

            </div>

        `;

        container.appendChild(col);

    });

    document.querySelectorAll(".delete-btn").forEach(button => {

        button.addEventListener("click", () => {

            deleteCustomer(

                button.dataset.code,

                button.dataset.name

            );

        });

    });

}

function renderPagination() {

    const pagination = document.getElementById("pagination");

    pagination.innerHTML = "";

    function createButton(page, text, active = false, disabled = false) {

        const li = document.createElement("li");
        li.className = "page-item";

        if (active) li.classList.add("active");
        if (disabled) li.classList.add("disabled");

        const button = document.createElement("button");
        button.className = "page-link";
        button.innerHTML = text;

        if (!disabled) {
            button.addEventListener("click", () => goToPage(page));
        }

        li.appendChild(button);
        pagination.appendChild(li);
    }

    function createDots() {

        const li = document.createElement("li");
        li.className = "page-item disabled";
        li.innerHTML = `<span class="page-link">...</span>`;

        pagination.appendChild(li);
    }

    createButton(
        Math.max(currentPage - 10, 1),
        "&laquo;&laquo;",
        false,
        currentPage === 1
    );

    createButton(
        currentPage - 1,
        "&laquo;",
        false,
        currentPage === 1
    );

    if (totalPages <= 7) {

        for (let i = 1; i <= totalPages; i++) {
            createButton(i, i, i === currentPage);
        }

    } else {

        createButton(1, 1, currentPage === 1);

        if (currentPage > 4) createDots();

        let start = Math.max(2, currentPage - 1);
        let end = Math.min(totalPages - 1, currentPage + 1);

        for (let i = start; i <= end; i++) {
            createButton(i, i, i === currentPage);
        }

        if (currentPage < totalPages - 3) createDots();

        createButton(totalPages, totalPages, currentPage === totalPages);
    }

    createButton(
        currentPage + 1,
        "&raquo;",
        false,
        currentPage === totalPages
    );

    createButton(
        Math.min(currentPage + 10, totalPages),
        "&raquo;&raquo;",
        false,
        currentPage === totalPages
    );

}


document.getElementById("levelFilter").addEventListener("change", () => {

    currentLevel = document.getElementById("levelFilter").value;

    fetchCustomers(1);

});



document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("searchBtn").addEventListener("click", () => {

        currentSearch = document.getElementById("searchInput").value.trim();

        currentLevel = document.getElementById("levelFilter").value;

        fetchCustomers(1);

    });

    document.getElementById("resetBtn").addEventListener("click", () => {

        currentSearch = "";
        currentLevel = "";

        document.getElementById("searchInput").value = "";
        document.getElementById("levelFilter").value = "";

        fetchCustomers(1);

    });

    document.getElementById("searchInput").addEventListener("keypress", (e) => {

        if (e.key === "Enter") {
            e.preventDefault();
            document.getElementById("searchBtn").click();
        }

    });

    fetchCustomers(1);

});



















async function deleteCustomer(code, name) {

    const confirmDelete = confirm(
        `آیا از حذف مشتری ${name} مطمئن هستید؟`
    );

    if (!confirmDelete) {
        return;
    }

    try {

        const response = await fetch(`customers/delete/${code}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        });


        if (!response.ok) {
            throw new Error("Delete failed");
        }


        showPopup(
            "مشتری با موفقیت حذف شد.",
            "success"
        );


        fetchCustomers(currentPage);


    } catch(error) {

        console.error(error);

        showPopup(
            "خطا در حذف مشتری.",
            "error"
        );

    }
}