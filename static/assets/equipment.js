    let currentPage = 1;
  const itemsPerPage = 5;
  const table = document.getElementById("equipmentTable");


  async function loadPage(page) {
    const skip = (page - 1) * itemsPerPage;
    const res = await fetch(`/api/equipment?skip=${skip}&limit=${itemsPerPage}`);
    const data = await res.json();
    renderTable(data);
  }

  function renderTable(_items) {
    const tbody = document.querySelector("#equipmentTable tbody");
    tbody.innerHTML = "";

    for (const item of _items.items) {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.id}</td>
        <td>${item.name}</td>
        <td>${item.price}</td>
        <td>${item.supplier.name}</td>
        <td>${item.supplier.country}</td>
         <td class="actions">
              <button onclick="openEditModal(${item.id})">✏️</button>
              <button onclick="deleteEquipment(${item.id})">🗑</button>
        </td>
      `
      tbody.appendChild(row);
    }
    totalPages = Math.ceil(_items.total / itemsPerPage);
    document.getElementById("pageInfo").textContent = `Страница ${currentPage} из ${totalPages}`;
    document.getElementById("prevPage").disabled = currentPage === 1;
    document.getElementById("nextPage").disabled = currentPage === totalPages;
  }

  document.getElementById("prevPage").addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      loadPage(currentPage);
    }
  });

  document.getElementById("nextPage").addEventListener("click", () => {
    currentPage++;
    loadPage(currentPage);
  });

  // первая загрузка
  loadPage(currentPage);

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeAll();
      }
    });

      function closeAll() {
      document.querySelectorAll('[id^="modal"]').forEach(modal => {
        modal.style.display = "none";
      });
    }
    const modal = document.getElementById('modalCreate');
      const openBtn = document.getElementById('openModalBtn');
      const closeBtn = document.getElementById('closeModalBtn');
      const saveBtn = document.getElementById('saveBtn');
      const supplierSelect = document.getElementById('supplierSelect');

      // открыть окно
      openBtn.onclick = async () => {
        modal.style.display = 'flex';
        await loadSuppliers();  // загрузить список производителей
      };

      // загрузить список производителей
      async function loadSuppliers() {
        const res = await fetch('/api/supplier');
        const data = await res.json();
        supplierSelect.innerHTML = '';
        data.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s.id;
          opt.textContent = s.name;
          supplierSelect.appendChild(opt);
        });
      }

      // сохранить оборудование
      saveBtn.onclick = async () => {
        const payload = {
          name: document.getElementById('equipName').value,
          price: parseFloat(document.getElementById('equipPrice').value),
          supplier_id: parseInt(supplierSelect.value)
        };

        const res = await fetch('/api/equipment/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          alert('Оборудование добавлено!');
          modal.style.display = 'none';
          location.reload();
        } else {
          alert('Ошибка при добавлении оборудования');
        }
      };

    // двойной клик по строке для редактирования
  table.addEventListener("dblclick", async (e) => {
      const row = e.target.closest("tr");
      if (!row) return;
      const id = row.children[0].textContent.trim();
      openEditModal(id);
      })

  async function openEditModal(id) {
      const modal = document.getElementById("modalEdit");
      // Загружаем данные с сервера
      const res = await fetch(`/api/equipment/${id}`);
      const data = await res.json();
      document.getElementById("equipmentId").value = data.id;
      document.getElementById("equipmentName").value = data.name;
      document.getElementById("equipmentPrice").value = data.price;
      modal.style.display = "block";
    };

  async function deleteEquipment(id) {
        if (!confirm("Вы действительно хотите удалить этот объект?")) {
    return; // пользователь нажал «Отмена»
  }

  try {
    const response = await fetch(`/api/equipment/${id}`, { method: "DELETE" });

    if (response.status === 200) {
      // например, бекенд возвращает JSON с данными удалённого объекта
      const data = await response.json();
      alert(`Объект "${data.name}" (ID: ${data.id}) успешно удалён.`);
      location.reload(); // можно обновить таблицу
    }
    else if (response.status === 409) {
      const error = await response.text();
      alert(`Невозможно удалить: ${error || "есть связанные записи."}`);
    }
    else {
      alert(`Ошибка: ${response.status} ${response.statusText}`);
    }
  }
  catch (err) {
    alert("Ошибка сети: " + err.message);
  }

    };

    modalEdit.addEventListener("submit", async (e) => {
        e.preventDefault();
        const modal = document.getElementById("modalEdit");
        const form = document.getElementById("editForm");
        const id = document.getElementById("equipmentId").value;
        const name = document.getElementById("equipmentName").value;
        const price = parseFloat(document.getElementById("equipmentPrice").value);
        await fetch(`/api/equipment/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price })
        });
        closeModal(modal, form);
        location.reload();
    });

  function closeModal(modal, form) {
  modal.style.display = 'none';
  form.reset();
}