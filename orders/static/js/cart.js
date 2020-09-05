document.addEventListener("DOMContentLoaded", () => {
  const itemsCount = parseInt(localStorage.getItem("cart-items-count"));
  let cart = JSON.parse(localStorage.getItem("cart"));
  // populate cart table
  const table = document.querySelector("tbody.cart-table");

  cart.cartItems.forEach(function (item) {
    const row = document.createElement("tr");
    table.appendChild(row);

    const nameColumn = document.createElement("th");
    nameColumn.setAttribute("scope", "row");
    nameColumn.innerHTML = item.itemName;
    row.appendChild(nameColumn);

    const quantityColumn = document.createElement("td");
    quantityColumn.innerHTML = item.itemQuantity;
    row.appendChild(quantityColumn);

    const priceColumn = document.createElement("td");
    priceColumn.innerHTML = parseInt(item.itemQuantity) * parseFloat(item.itemPrice);
    row.appendChild(priceColumn);

    const incDecColumn = document.createElement("td");
    incDecColumn.classList.add("inc-dec-column");
    row.appendChild(incDecColumn);

    const incButton = document.createElement("button");
    incButton.classList.add("increase", "btn", "btn-success");
    incButton.setAttribute("id", item.itemID);
    incButton.setAttribute("name", item.itemName);
    incButton.setAttribute("data-quantity", item.itemQuantity);
    incButton.innerHTML = "+";
    incDecColumn.appendChild(incButton);

    const decButton = document.createElement("button");
    decButton.classList.add("decrease", "btn", "btn-danger");
    decButton.setAttribute("id", item.itemID);
    decButton.setAttribute("name", item.itemName);
    decButton.setAttribute("data-quantity", item.itemQuantity);
    decButton.innerHTML = "-";
    incDecColumn.appendChild(decButton);
  });

  // control increment and decrease of quantity items
  // A bug in calculating total
  document.querySelectorAll("button.increase, button.decrease").forEach((button) => {
    // configure increase buttons
    if (button.classList.item(0) === "increase") {
      button.addEventListener("click", function () {
        console.log(`${this.getAttribute("id")} - ${this.getAttribute("name")}`);
        console.log(this.getAttribute("data-quantity"));
        // TODO: set new attribute

        let quantity = parseInt(this.getAttribute("data-quantity")) + 1;
        updateCart(this.getAttribute("id"), this.getAttribute("name"), quantity);
      });
    }
  });

  //update basket number
  document.querySelector("a span.items-count").innerHTML = localStorage
    .getItem("cart-items-count")
    .toString();

  //testing
  document
    .querySelector("button.checkout")
    .addEventListener("click", function (event) {});
});

function updateCart(id, name, newQuantity) {
  let cart = JSON.parse(localStorage.getItem("cart"));

  cart.cartItems.forEach((item) => {
    if (item.itemID === id && item.itemName === name) {
      item.itemQuantity = newQuantity;
      item.totalPrice = item.itemPrice * newQuantity;
    }
  });

  // update total and save cart state
  let total = 0;
  cart.cartItems.forEach((item) => {
    total = total + item.totalPrice;
  });
  cart.total = total;
  localStorage.setItem("cart", JSON.stringify(cart));
}
