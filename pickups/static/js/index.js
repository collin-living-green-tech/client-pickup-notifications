const groups = document.getElementById('groups');
   let sortable = Sortable.create(groups, {
});


const saveOrderingButton = document.getElementById('saveOrdering');
console.log(saveOrderingButton)
const orderingForm = document.getElementById('orderingForm');
console.log(orderingForm)
const formInput = orderingForm.querySelector('#orderingInput');
saveOrderingButton.addEventListener('click', saveOrdering);


function saveOrdering() {
    const rows = document.getElementById("groups").querySelectorAll('tr');
    let ids = [];
    for (let row of rows) {
        ids.push(row.dataset.lookup);
    }
    formInput.value = ids.join(',');
    orderingForm.submit();
}