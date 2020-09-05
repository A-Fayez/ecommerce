// var cart = {};
// cart.cartItems = [];
// localStorage.setItem("cart", JSON.stringify(cart));

document.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("cart-items-count")) {
    document.querySelector(
      "a span.items-count"
    ).innerHTML = localStorage.getItem("cart-items-count").toString();
  }

  let itemsCountElement = document.querySelector("a span.items-count")
    .innerHTML;
  let itemsCount = parseInt(itemsCountElement);
  document.querySelectorAll("button.add-to-cart").forEach(function (button) {
    button.addEventListener("click", function () {
      // update numbers of item in a cart
      itemsCount++;
      localStorage.setItem("cart-items-count", itemsCount);
      document.querySelector(
        "a span.items-count"
      ).innerHTML = localStorage.getItem("cart-items-count").toString();

      // get the selected item info
      const quantitySelection = document.querySelector(`#${this.name}-select`);
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

      // check if user clicked on an already clicked-before item
      // increment its quantity and update totals
      // const duplicate = cart.cartItems.some(
      //   (el) =>
      //     el.itemName === cartItem.itemName && el.itemID === cartItem.itemID
      // );
      // if (duplicate) {
      //   console.log("zobr");
      //   const oldItem = cart.cartItems.find(
      //     (el) =>
      //       el.itemName === cartItem.itemName && el.itemID === cartItem.itemID
      //   );
      //   cart.cartItems.push({
      //     itemID: itemID,
      //     itemName: itemName,
      //     itemPrice: itemPrice,
      //     itemQuantity: itemQuantity + oldItem.itemQuantity,
      //     totalPrice: itemPrice * itemQuantity + oldItem.totalPrice,
      //   });
      // } else {
      //   console.log("zobr");
      //   cart.cartItems.push(cartItem);
      //   console.log(cart);
      // }

      // cart.cartItems.push(cartItem);
      // localStorage.setItem("cart", JSON.stringify(cart));
      // console.log(cart);
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
  cart.cartItems.push(item);
}

function getCart() {
  if (localStorage.getItem("cart")) {
    return JSON.parse(localStorage.getItem("cart"));
  }
  let cart = {};
  cart.cartItems = [];
  localStorage.setItem("cart", JSON.stringify(cart));
  return cart;
}

function saveCart(cart) {
  localStorage.setItem("cart", JSON.stringify(cart));
}

//   let cart = {
//     "cartItems": [
//       {
//         "itemName": "",
//         "itemID": "",
//         price: "",
//         quantity: "",
//       },
//     ],
//     total: 50,
//   };
