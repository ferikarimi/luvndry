const apiUrl = '/CMS/admin_magazines/';
let filterType = 'active';

CKEDITOR.replace('content', {
  language: 'fa',
  height: 300,
  filebrowserUploadUrl: '/CMS/upload/',
  filebrowserUploadMethod: 'form'
});

async function fetchArticles() {
  let url = apiUrl;
  if (filterType === 'active') url += '?inactive=false';
  else if (filterType === 'inactive') url += '?inactive=true';
  const res = await fetch(url);
  const data = await res.json();
  renderArticles(data);
}

function renderArticles(articles) {
  const container = document.getElementById('articlesList');
  container.innerHTML = '';
  articles.forEach(article => {
    const div = document.createElement('div');
    div.classList.add('col-lg-4', 'col-md-6', 'col-12');
    div.innerHTML = `
      <div class="article-card">
        <img src="${article.image}" alt="${article.title}">
        <h5>${article.title}</h5>
        <p>${article.summary}</p>
        <div class="btn-container">
          <button class="btn btn-sm btn-success" onclick="editArticle(${article.id})">ویرایش</button>
          <button class="btn btn-sm btn-danger" onclick="deleteArticle(${article.id})">حذف</button>
        </div>
      </div>
    `;
    container.appendChild(div);
  });
}

document.getElementById('articleForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('articleId').value;
  const formData = new FormData();
  formData.append('title', document.getElementById('title').value);
  formData.append('summary', document.getElementById('summary').value);
  formData.append('content', CKEDITOR.instances.content.getData());
  const file = document.getElementById('image').files[0];
  if (file) formData.append('image', file);
  formData.append('is_active', document.getElementById('isActive').checked);

  const method = id ? 'PATCH' : 'POST';
  if (id) formData.append('id', id);

  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  try {
    const res = await fetch(apiUrl, {
      method: method,
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    });
  
    if (res.ok) {

      if (id) {
        showPopup("مقاله با موفقیت ویرایش شد.", "success");
      } else {
        showPopup("مقاله با موفقیت اضافه شد.", "success");
      }
    
    } else {
      showPopup("خطا در ذخیره‌سازی مقاله!", "error");
    }
    
  
    resetForm();
    fetchArticles();
  
  } catch (err) {
    showPopup("خطای شبکه! عملیات انجام نشد.", "error");
  }
  
});

function editArticle(id) {
  fetch(apiUrl)
    .then(res => res.json())
    .then(data => {
      const article = data.find(a => a.id === id);
      document.getElementById('articleId').value = article.id;
      document.getElementById('title').value = article.title;
      document.getElementById('summary').value = article.summary;
      CKEDITOR.instances.content.setData(article.content);
      document.getElementById('isActive').checked = article.is_active;
    });
}

async function deleteArticle(id) {
  const formData = new FormData();
  formData.append('id', id);
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  try {
    const res = await fetch(apiUrl, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    });
  
    if (res.ok) {
      showPopup("مقاله با موفقیت حذف شد.", "success");
    } else {
      showPopup("حذف مقاله انجام نشد!", "error");
    }
  
    fetchArticles();
  
  } catch (err) {
    showPopup("خطای شبکه در حذف مقاله!", "error");
  }
  
}

function resetForm() {
  document.getElementById('articleForm').reset();
  document.getElementById('articleId').value = '';
  CKEDITOR.instances.content.setData('');
}

document.getElementById('showActive').addEventListener('click', () => {
  filterType = 'active';
  fetchArticles();
});

document.getElementById('showInactive').addEventListener('click', () => {
  filterType = 'inactive';
  fetchArticles();
});

document.getElementById('showAll').addEventListener('click', () => {
  filterType = 'all';
  fetchArticles();
});

fetchArticles();