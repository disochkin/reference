// -------------- Утилиты --------------
function showModal() {
  document.getElementById('editModal').style.display = 'flex';
}
function hideModal() {
  document.getElementById('editModal').style.display = 'none';
  document.getElementById('editError').style.display = 'none';
}

// Заполнить строку таблицы новыми данными
function updateTableRow(data) {
  const tr = document.querySelector(`tr[data-id='${data.id}']`);
  if (!tr) return;
  tr.querySelector('.col-name').textContent = data.name;
  tr.querySelector('.col-price').textContent = data.price;
}

// -------------- Открытие модала --------------
async function openEditModal_(id) {
    console.log(id);

  try {
    // опционально показать индикатор загрузки
    const res = await fetch(`/api/equipment/${id}`, { method: 'GET' });
    console.log(res);

    if (res.status === 404) {
      alert('Запись не найдена');
      return;
    }
    if (!res.ok) {
      const err = await res.json().catch(()=>({detail: 'Ошибка'}));
      alert('Ошибка получения данных: ' + (err.detail || res.status));
      return;
    }

    const item = await res.json();
    const idInput = document.getElementById(id);
    if (!idInput) {
      console.error('Элемент #id не найден');
    } else {
      idInput.value = item.id;
    }

    // заполнить форму
    document.getElementById('id').value = item.id;
    document.getElementById('name').value = item.name ?? '';
    document.getElementById('price').value = item.price ?? 0;
    showModal();
  } catch (err) {
    alert('Сетевая ошибка: ' + err.message);
  }
}

// -------------- Отправка изменений --------------
document.getElementById('editForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const id = document.getElementById('equipmentId').value;
  const name = document.getElementById('equipmentName').value.trim();
  const price = parseFloat(document.getElementById('equipmentPrice').value);
  const errorBox = document.getElementById('editError');

  // Простая валидация на фронте
  if (!name) {
    errorBox.textContent = 'Название не может быть пустым';
    errorBox.style.display = 'block';
    return;
  }
  if (isNaN(price) || price < 0) {
    errorBox.textContent = 'Неверная цена';
    errorBox.style.display = 'block';
    return;
  }

  try {
    const res = await fetch(`/api/equipment/${id}`, {
      method: 'PATCH', // или PUT — зависит от API
      headers: {
        'Content-Type': 'application/json'
        // 'Authorization': 'Bearer ...' если нужен токен
      },
      body: JSON.stringify({ name, price })
    });

    // успешный ответ
    if (res.ok) {
      const updated = await res.json().catch(()=>({ id, name, price }));
      // обновим строку в таблице (оптимистично)
      updateTableRow(updated);
      hideModal();
      return;
    }

    // обработать ошибки
    if (res.status === 422) {
      // Pydantic validation error
      const body = await res.json();
      // body.detail - массив ошибок
      const first = body.detail && body.detail[0];
      errorBox.textContent = first ? `${first.loc.join('.')}: ${first.msg}` : 'Ошибка валидации';
      errorBox.style.display = 'block';
      return;
    }

    if (res.status === 404) {
      errorBox.textContent = 'Запись не найдена (возможно её удалили)';
      errorBox.style.display = 'block';
      return;
    }

    if (res.status === 409) {
      const body = await res.json().catch(()=>({detail: 'Конфликт'}));
      errorBox.textContent = body.detail || 'Конфликт при сохранении';
      errorBox.style.display = 'block';
      return;
    }

    // прочие ошибки
    const body = await res.json().catch(()=>({detail: 'Ошибка сервера'}));
    errorBox.textContent = body.detail || `Ошибка: ${res.status}`;
    errorBox.style.display = 'block';
  } catch (err) {
    errorBox.textContent = 'Сетевая ошибка: ' + err.message;
    errorBox.style.display = 'block';
  }
});

