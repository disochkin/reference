    let currentPage = 1;
  const itemsPerPage = 5;
  const table = document.getElementById("ordersTable");


  async function loadPage(page) {
    const skip = (page - 1) * itemsPerPage;
    const res = await fetch(`/api/order?skip=${skip}&limit=${itemsPerPage}`);
    const data = await res.json();
    renderTable(data);
  }

  function renderTable(_items) {
    const tbody = document.querySelector("#orderTable tbody");
    tbody.innerHTML = "";
    for (const item of _items.items) {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.id}</td>
        <td>${item.customer.name}</td>
        <td>${item.manager.name}</td>
        <td>${item.created_at}</td>
        <td>${item.total_sum}</td>
        <td>${item.status}</td>
        <td class="actions">
              <button onclick="openEditModal(${item.id})">✏️</button>
              <button onclick="deleteOrder(${item.id})">🗑</button>
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

    const modal = document.getElementById('modalCreate');
      const openBtn = document.getElementById('openModalBtn');
      const closeBtn = document.getElementById('closeModalBtn');
      const saveBtn = document.getElementById('saveBtn');
      const managerSelect = document.getElementById('managerSelect');
      const customerSelect = document.getElementById('customerSelect');


      // открыть окно
      openBtn.onclick = async () => {
        modal.style.display = 'flex';
        await loadManagers();  // загрузить список менеджеров
        await loadCustomers();  // загрузить список покупателей
      };

      // закрыть окно
      closeBtn.onclick = () => modal.style.display = 'none';

      // загрузить список менеджеров
      async function loadManagers() {
        const res = await fetch('/api/manager');
        const data = await res.json();
        managerSelect.innerHTML = '';
        data.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s.id;
          opt.textContent = s.name;
          managerSelect.appendChild(opt);
        });
      }

      async function loadCustomers() {
        const res = await fetch('/api/customer');
        const data = await res.json();
        customerSelect.innerHTML = '';
        data.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s.id;
          opt.textContent = s.name;
          customerSelect.appendChild(opt);
        });
      }

      // сохранить заказ
      saveBtn.onclick = async () => {
        const payload = {
          manager_id: parseInt(managerSelect.value),
          customer_id: parseInt(customerSelect.value)
        };

        const res = await fetch('/api/order/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          alert('Заявка добавлена!');
          modal.style.display = 'none';
          location.reload();
        } else {
          alert('Ошибка при добавлении заявки');
        }
      };


  async function deleteOrder(id) {
        if (!confirm("Вы действительно хотите удалить этот заказ?")) {
        return; // пользователь нажал «Отмена»
        }

          try {
            const response = await fetch(`/api/order/${id}`, { method: "DELETE" });

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



  async function openEditModal(id) {
      const modal = document.getElementById("modalEdit");
      const addEquipmentBtn = document.getElementById('addEquipmentBtnForm');

      // Загружаем данные с сервера
      const res = await fetch(`/api/order/${id}/items`);
      const data = await res.json();
      document.getElementById("orderIdFormModal").value = data.id;

      document.getElementById("orderCreatedFormModal").value = data.created_at;

      document.getElementById("customerFormModal").value = data.customer.name;
      document.getElementById("managerFormModal").value = data.manager.name;
      document.getElementById("orderStatusFormModal").value = data.status;
      document.getElementById("totalAmount").value = data.total_amount;

      modal.style.display = "block";
      renderOrderItemTable(data.id, data);
      loadEquipment();
    };

      function renderOrderItemTable(orderId, _items) {
        const tbody = document.querySelector("#orderItemTable tbody");
        tbody.innerHTML = "";
        for (const orderItem of _items.order_items) {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${orderItem.id}</td>
            <td>${orderItem.equipment.name}</td>
            <td>${orderItem.price_per_unit}</td>
            <td>${orderItem.quantity}</td>
            <td>${orderItem.total_price}</td>

            <td class="actions">
               <button onclick="deleteOrderItem(${orderId}, ${orderItem.id})">🗑</button>
            </td>
          `
          tbody.appendChild(row);
        }
}

     // загрузить список оборудования + цена
      async function loadEquipment() {
        const res = await fetch('/api/equipment');
        const data = await res.json();
        equipmentSelect = document.getElementById("equipmentSelectEditOrderForm");
        price = document.getElementById("price")
        equipmentSelect.innerHTML = '';
        data.items.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s.id;
          opt.textContent = s.name;
          equipmentSelect.appendChild(opt);
        });
      }

//        document.addEventListener('DOMContentLoaded', () => {
//            setupPriceUpdater(document.getElementById('equipmentSelectEditOrderForm'), document.getElementById('price-field'));
//        });

        // Передача селекторов DOM и продукта прямо в функцию
//        async function setupPriceUpdater(productSelect, priceField) {
//            const res = await fetch('/api/equipment');
//            const data = await res.json();
//            console.log(data.items);
//
//            productSelect.addEventListener('change', () => {
//                const selectedProductID = productSelect.value;
//                if (!selectedProductID) {
//                    priceField.textContent = '';
//                    return;
//                }
//              //  const selectedProduct = data[selectedProductID];
//               priceField.textContent = findPriceById(data.items, selectedProductID);
//            });
//        }
//
//
//        // Функция для поиска цены по id
//        function findPriceById(items, id) {
//            const item = items.find(item => item.id === id);
//            return item ? item.price : undefined;
//        }

      addEquipmentBtn.onclick = async () => {
                    const payload = {
          equipment_id: parseInt(equipmentSelectEditOrderForm.value),
          quantity: parseInt(orderIdFormModal.value),
          order_id: parseInt(orderIdFormModal.value)
        };

      const res = await fetch('/api/order/add_item', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (res.ok) {
          alert('Позиция добавлена!');
          location.reload();
        } else {
          alert('Ошибка при добавлении заявки');
        }
      };


  async function deleteOrderItem(orderId, itemId) {
        if (!confirm("Вы действительно хотите удалить эту позицию?")) {
        return; // пользователь нажал «Отмена»
        }
          try {
            const response = await fetch(`/api/order/${orderId}/items/${itemId}`, { method: "DELETE" });

            if (response.status === 200) {
              // например, бекенд возвращает JSON с данными удалённого объекта
              const data = await response.json();
              //alert(`Объект "${data.name}" (ID: ${data.id}) успешно удалён.`);
              alert(`Объект успешно удалён.`);
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



        function closeForm() {
            const modal = document.getElementById('modalEdit');
            modal.style.display = 'none'; // или другой способ сокрытия, если нужно
        }
  //table.addEventListener("dblclick", async (e) => {
      //const row = e.target.closest("tr");
      //if (!row) return;
      //const id = row.children[0].textContent.trim();
      //const modal = document.getElementById("editModal");

      // Загружаем данные с сервера
      //const res = await fetch(`/api/equipment/${id}`);
      //const data = await res.json();
      //document.getElementById("equipmentId").value = data.id;
      //document.getElementById("equipmentName").value = data.name;
      //document.getElementById("equipmentPrice").value = data.price;
      //modal.style.display = "block";
   // });

  //  editModal.addEventListener("submit", async (e) => {
    //    e.preventDefault();
    //    const modal = document.getElementById("editModal");
    //    const form = document.getElementById("editForm");
    //    const id = document.getElementById("equipmentId").value;
    //    const name = document.getElementById("equipmentName").value;
    //    const price = parseFloat(document.getElementById("equipmentPrice").value);
    //    await fetch(`/api/equipment/${id}`, {
    //    method: "PATCH",
    //    headers: { "Content-Type": "application/json" },
    //    body: JSON.stringify({ name, price })
    //    });
    //    closeModal(modal, form);
    //    location.reload();
    //});

  function closeModal(modal, form) {
  modal.style.display = 'none';
  form.reset();
}