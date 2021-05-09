document.addEventListener("DOMContentLoaded", () => {
  // update basket UI
  if (localStorage.getItem("cart")) {
    let cart = JSON.parse(localStorage.getItem("cart"));
    document.querySelector("a span.items-count").innerHTML = cart.cartItems.length;
  }

  document.querySelectorAll("button.add-to-cart").forEach(function (button) {
    button.addEventListener("click", function () {
      // get the selected item info
      console.log(`#${this.name}-select`);

      const quantitySelection = document.querySelector(
        `select#${this.name}-select`.trim()
      );
      const itemQuantity = parseInt(
        quantitySelection.options[quantitySelection.selectedIndex].value
      );
      const itemPrice = parseFloat(
        document.querySelector(`#${this.name}-price`).innerHTML
      );
      const itemName = this.name;
      const itemID = this.id;

      const cartItem = {
        itemID: itemID,
        itemName: itemName,
        itemPrice: itemPrice,
        itemQuantity: itemQuantity,
        totalPrice: itemPrice * itemQuantity,
      };

      let cart = getCart();
      addItemToCart(cartItem, cart);
      saveCart(cart);

      console.log(getCart);
      this.disabled = true;
      alert("Check your cart for extra modification");
    });
  });
});

// adds an item to the local storage cart items array that is inside cart key in local storage
function addItemToCart(item, cart) {
  for (let i = 0; i < cart.cartItems.length; i++) {
    if (
      item.itemID === cart.cartItems[i].itemID &&
      item.itemName === cart.cartItems[i].itemName
    ) {
      cart.cartItems[i].itemQuantity =
        cart.cartItems[i].itemQuantity + parseInt(item.itemQuantity);

      cart.cartItems[i].totalPrice = cart.cartItems[i].itemQuantity * item.itemPrice;
      return;
    }
  }
  cart.cartItems.push(item);
}

// helper functions
function getCart() {
  if (localStorage.getItem("cart")) {
    return JSON.parse(localStorage.getItem("cart"));
  }
  let cart = {};
  cart.cartItems = [];
  cart.total = 0;
  localStorage.setItem("cart", JSON.stringify(cart));
  return cart;
}

function saveCart(cart) {
  // calculate total
  let total = 0;
  cart.cartItems.forEach((item) => {
    total = total + parseFloat(item.totalPrice);
  });
  cart.total = total;
  localStorage.setItem("cart", JSON.stringify(cart));
}
