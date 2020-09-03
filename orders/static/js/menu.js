document.addEventListener("DOMContentLoaded", () => {
    let itemsCountElement = document.querySelector("a span.items-count").innerHTML;
    let itemsCount = parseInt(itemsCountElement);
    document.querySelectorAll("button.add-to-cart")
        .forEach(function(button) {
            button.addEventListener("click", function()  {
                // update numbers of item in a cart
                // localStorage.setItem("itemsCount")
                itemsCount++;
                document.querySelector("a span.items-count").innerHTML = itemsCount.toString();

                // test sessions
                fetch("/session")
                    .then(response => console.log(response));


                // get cart-item node
                console.log(this.parentElement.parentElement.children[0].innerHTML); //name
                console.log(this.parentElement.parentElement.children[1].innerHTML) // small
                console.log(this.parentElement.parentElement.children[2].innerHTML) // large
                console.log(this.parentElement.parentElement.children[3].innerHTML === "-" ? "0.0" : this.parentElement.parentElement.children[3].innerHTML) // price

            })
    })
})