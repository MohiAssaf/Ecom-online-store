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
            
            <div class="cart-box">
                <img src="../images/pulover.jpg" alt="" class="cart-img">
                <div class="cart-details">
                    <div class="cart-title">Pullover</div>
                    <div class="cart-price">30$</div>
                    <input type="number" value="1" class="cart-quantity">
                </div>

                <i class="fa-solid fa-trash"></i> 
            </div>

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
    let removeItems = header.getElementsByClassName('.fa-trash')


    cartIcon.addEventListener('click', () => {
        cart.classList.add("active")
    });

    closeCart.addEventListener('click', () =>{
        cart.classList.remove("active")
    })


    for(let i=0; i < removeItems.length; i++){
        let item = removeItems[i]

        item.addEventListener('click', removeItem)
    }


});

const removeItem = (e) => {
    let productRemoved = e.target
    productRemoved.parentElement.remove()
}