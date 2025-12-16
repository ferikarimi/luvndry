(function() {
  "use strict";

  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);


  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    mobileNavToggleBtn.classList.toggle('bi-list');
    mobileNavToggleBtn.classList.toggle('bi-x');
  }
  mobileNavToggleBtn.addEventListener('click', mobileNavToogle);

  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.mobile-nav-active')) {
        mobileNavToogle();
      }
    });

  });

  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false,
      offset: 80

    });
  }
  window.addEventListener('load', aosInit);

  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  new PureCounter();

  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);

})();

  document.addEventListener("DOMContentLoaded", function () {
    const phoneBtn = document.getElementById("phone-btn");
    const workingHoursBtn = document.getElementById("working-hours-btn");
    const phoneNumber = "09172442147";

    const isMobile = /Android|iPhone|iPad|iPod|Opera Mini|IEMobile|WPDesktop/i.test(navigator.userAgent);

    phoneBtn.addEventListener("click", function (e) {
      e.preventDefault();

      if (isMobile) {
        window.location.href = `tel:${phoneNumber}`;
      } else {
        alert(`شماره تماس: ${phoneNumber}`);
      }
    });

    workingHoursBtn.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector("#footer").scrollIntoView({ behavior: "smooth" });
    });
  });



  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');
  const form = document.getElementById('commentForm');
  const loading = form.querySelector('.loading');
  const errorMessage = form.querySelector('.error-message');
  const sentMessage = form.querySelector('.sent-message');
  const commentsList = document.getElementById('commentsList');

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

async function loadComments() {
    const wrapper = document.getElementById("commentsWrapper");
    wrapper.innerHTML = '<div style="padding:20px;">در حال بارگذاری نظرات...</div>';

    try {
      const response = await fetch('/customers/commentrecently/', {
        method: 'GET',
        credentials: 'same-origin',
        headers: { 'Accept': 'application/json' }
      });

      let data = await response.json();
      let comments = Array.isArray(data) ? data : (data.results || []);

      comments.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      const recent = comments.slice(0, 5);

      if (recent.length === 0) {
        wrapper.innerHTML = '<div style="color:#777; padding:20px;">هنوز نظری ثبت نشده است.</div>';
        return;
      }

      wrapper.innerHTML = '';
      recent.forEach(comment => {
        const slide = document.createElement('div');
        slide.classList.add('swiper-slide');

        slide.innerHTML = `
          <div class="testimonial-item">
            <div class="row gy-4 justify-content-center">
              <div class="col-lg-6">
                <div class="testimonial-content">

                  <h3><span style="direction:ltr; display:inline-block;">${escapeHtml(comment.hidden_phone) || 'ناشناس'}</span> گفت :</h3>

                  <h4>
                    <span>${escapeHtml(comment.text)}</span>
                  </h4>

                  <h6>${comment.created_at ? new Date(comment.created_at).toLocaleDateString('fa-IR') : ''}</h6>
                </div>
              </div>
            </div>
          </div>
        `;
        wrapper.appendChild(slide);
      });

    } catch (err) {
      console.error(err);
      wrapper.innerHTML = '<div style="color:#777; padding:20px;">خطا در بارگذاری نظرات.</div>';
    }
  }

  function escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
  }

  loadComments();

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMessage.textContent = '';
    sentMessage.style.display = 'none';
    loading.style.display = 'block';

    const phoneVal = form.phone.value.trim();
    const textVal = form.text.value.trim();
    
    if (!phoneVal || !textVal) {
      loading.style.display = 'none';
      showPopup('لطفاً همه فیلدها را پر کنید.', "warning");
      return;
    }
    
    try {
      const response = await fetch('/customers/customercommentscreate/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken || ''
        },
        body: JSON.stringify({ phone: phoneVal, text: textVal })
      });
    
      const result = await response.json();
      loading.style.display = 'none';
    
      if (response.ok) {
    
        showPopup('کامنت شما ثبت شد و بعد از تایید نمایش داده خواهد شد.', "success");
    
        form.reset();
        loadComments();
    
      } else {
    
        const msg = result.ERROR || 'برای ثبت نظر باید از خدمات ما استفاده کرده باشید.';
        showPopup(msg, "error");
      }
    
    } catch (err) {
    
      loading.style.display = 'none';
      showPopup('خطای شبکه. لطفاً دوباره تلاش کنید.', "error");
    }    
  });








document.addEventListener('DOMContentLoaded', () => {
  console.log('[order-tracking] script loaded');

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const form = document.getElementById('orderForm');
  const phoneInput = document.getElementById('phone');
  const btn = document.getElementById('checkOrderBtn');
  const loading = document.getElementById('loading');
  const errorMessage = document.getElementById('error-message');
  const resultMessage = document.getElementById('result-message');
  const orderStatus = document.getElementById('order-status');

  if (!form || !phoneInput || !btn) {
    console.error('[order-tracking] required elements not found', { form, phoneInput, btn });
    return;
  }
  console.log('[order-tracking] elements found');


  form.addEventListener('submit', (e) => {
    e.preventDefault();
    return false;
  });
  phoneInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      btn.click(); 
    }
  });

  function showError(text) {
    errorMessage.textContent = text || '';
    errorMessage.style.display = text ? 'block' : 'none';
  }
  function showResult(text) {
    resultMessage.textContent = text || '';
    resultMessage.style.display = text ? 'block' : 'none';
  }

  const csrftoken = getCookie('csrftoken');
  console.log('[order-tracking] csrftoken:', !!csrftoken);

  btn.addEventListener('click', async () => {
    showError('');
    showResult('');
    orderStatus.innerHTML = '';
    loading.style.display = 'block';

    const phoneVal = phoneInput.value.trim();
    console.log('[order-tracking] button clicked, phone:', phoneVal);

    if (!phoneVal) {
      loading.style.display = 'none';
      showPopup("لطفاً شماره تلفن را وارد کنید." , "error");
      return;
    }

    try {
      console.log('[order-tracking] sending POST to /ordertracking/ ...');
      const response = await fetch('/orders/ordertracking/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken || ''
        },
        body: JSON.stringify({ phone: phoneVal })
      });

      console.log('[order-tracking] response status:', response.status);
      let data = null;
      try {
        data = await response.json();
      } catch (jsonErr) {
        console.warn('[order-tracking] response JSON parse failed', jsonErr);
      }
      console.log('[order-tracking] response data:', data);

      loading.style.display = 'none';

      if (response.ok && data && data.last_order_status) {
        showLongPopup("وضعیت سفارش : " + data.last_order_status, "success");
      }
      else {
        showLongPopup(data.ERROR || "خطایی رخ داده است.", "error");
      }
    

    } catch (err) {
      console.error('[order-tracking] fetch error', err);
      loading.style.display = 'none';
      showLongPopup("ارتباط با سرور برقرار نشد.", "error");
    }
  });
});

document.addEventListener("DOMContentLoaded", function() {
    fetch("/orders/stats/")
        .then(res => res.json())
        .then(data => {
            document.getElementById("days-counter").textContent = "+" + data.days.toLocaleString();
            document.getElementById("orders-counter").textContent = "+" + data.orders.toLocaleString();
            document.getElementById("items-counter").textContent = "+" + data.items.toLocaleString();
        })
        .catch(err => console.error(err));
});

const magazineApiUrl = '/CMS/magazines/';

async function loadMagazineArticles() {
  try {
    const res = await fetch(magazineApiUrl);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const articles = await res.json();

    const container = document.getElementById('magazineList');
    container.innerHTML = ''; 

    (articles || []).forEach(article => {

      const slide = document.createElement('div');
      slide.className = 'swiper-slide';

      const card = document.createElement('div');
      card.className = 'magazine-card';
      card.onclick = () => { window.location = '/magazine/' + article.id + '/'; };

      const img = document.createElement('img');
      img.className = 'mag-card-media';
      img.src = article.image || '';
      img.onerror = () => { img.src = 'https://via.placeholder.com/600?text=No+Image'; };

      const content = document.createElement('div');
      content.className = 'magazine-content';

      const h = document.createElement('h3');
      h.textContent = article.title || '';

      const p = document.createElement('p');
      p.textContent = article.summary || '';

      const a = document.createElement('a');
      a.className = 'read-btn';
      a.href = '/magazine/' + article.id + '/';
      a.textContent = 'مطالعه بیشتر';

      content.appendChild(h);
      content.appendChild(p);
      content.appendChild(a);

      card.appendChild(img);
      card.appendChild(content);
      slide.appendChild(card);
      container.appendChild(slide);
    });

    initSwiper();

  } catch (err) {
    console.error('خطا در بارگذاری مقالات:', err);
  }
}

function initSwiper() {
  new Swiper('.magazine-swiper', {
    slidesPerView: 'auto',
    centeredSlides: true,
    loop: true,
    spaceBetween: 25,
    speed: 500,
    autoplay:{
      delay:6500,
      disableOnInteraction: false,
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  });
}

document.addEventListener('DOMContentLoaded', loadMagazineArticles);


fetch('/customers/customerlevel/')
.then(response => response.json())
.then(data => {
  document.getElementById('bronze-counter').textContent = data.bronze;
  document.getElementById('silver-counter').textContent = data.silver;
  document.getElementById('gold-counter').textContent = data.gold;
});





document.addEventListener("DOMContentLoaded", function () {
  
  fetch("/CMS/showlastnotif/")
      .then(response => response.json())
      .then(data => {

          if (!data.is_active) return;

          const container = document.getElementById("latestNotification");

          container.innerHTML = `
              <div id="notifBox" class="notif-box">
                  <button class="close-btn">&times;</button>
                  <h4>${data.title}</h4>
                  <p>${data.message}</p>
              </div>
          `;

          const notifBox = document.getElementById("notifBox");

          setTimeout(() => {
              notifBox.classList.add("show");
          }, 50);

          setTimeout(() => {
              notifBox.classList.remove("show");
              notifBox.classList.add("hide");

              setTimeout(() => {
                  notifBox.remove();
              }, 500);
          }, 60000);

          notifBox.querySelector(".close-btn").addEventListener("click", () => {
              notifBox.classList.remove("show");
              notifBox.classList.add("hide");
              setTimeout(() => notifBox.remove(), 500);
          });
      });
});