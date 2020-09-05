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
    priceColumn.innerHTML =
      parseInt(item.itemQuantity) * parseFloat(item.itemPrice);
    row.appendChild(priceColumn);

    const incDecColumn = document.createElement("td");
    row.appendChild(incDecColumn);
    const incButton = document.createElement("button");
    const decButton = document.createElement("button");
    incButton.classList.add("increase");
    incButton.innerHTML = "+";
    decButton.classList.add("decrease");
    decButton.innerHTML = "-";
    incDecColumn.appendChild(incButton);
    incDecColumn.appendChild(decButton);
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
