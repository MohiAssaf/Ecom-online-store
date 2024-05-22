document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('header');

    header.innerHTML = `
    <nav class="navigation">
        <img src="../images/logo1.png" alt="" class="logo">
    
        <ul>
            <li><a href="/frontend/html/index.html">Home</a></li>
            <li><a href="/frontend/html/products.html">Products</a></li>
            <li><a href="/frontend/html/contact.html">Contact</a></li>
            <li class="shopping-cart"><i class="fa-solid fa-bag-shopping"></i></li>
        </ul>
    
        <a href="/frontend/html/login.html"><button type="button" class="login">Login</button></a>
    </nav>

    <div class="cart">

        <h1 class="title">Your Cart</h1>

        <div class="cart-orders">
            

        </div>
        <div class="total-order">
            <div class="total-price">
                <div class="total-title">Total</div>
                <div class="t-price">0$</div>
            </div>

            <button class="buy-btn" type="button">Buy Now</button>

            <i class="fa-solid fa-x" id="close-cart"></i>     
        </div>
    </div>
    `;

    let cartIcon = header.querySelector('.shopping-cart');
    let cart = header.querySelector('.cart');
    let closeCart = header.querySelector('#close-cart');
    let totalPrice = cart.querySelector('.t-price').textContent;
    let totalpriceTXT = totalPrice;
    var currentTotal = parseFloat(totalpriceTXT.replace('$', '')); 


    cartIcon.addEventListener('click', () => {
        cart.classList.add("active")

        let removeItems = cart.querySelectorAll('.fa-trash')

        for(let i=0; i < removeItems.length; i++){
            let product = removeItems[i]

            product.addEventListener('click', (e) => {
                let clickedProduct = e.target;
                let productToRemove = clickedProduct.parentElement
                let productPriceToRemove = productToRemove.querySelector('.cart-price').innerText;
                var productPriceToRemoveN = parseFloat(productPriceToRemove.replace('$', ''));
                totalPrice.textContent = productPriceToRemoveN + currentTotal + '$'
                productToRemove.remove()
                console.log(totalPrice)
            })
        }
    });

    closeCart.addEventListener('click', () =>{
        cart.classList.remove("active")
    })
});
    
