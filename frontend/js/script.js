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
    `;

    const shoppingCart = header.querySelector('.shopping-cart');
    console.log(shoppingCart);

    shoppingCart.addEventListener('click', () => {
        console.log('Shopping Cart clicked');
    });
});
