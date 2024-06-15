const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}


document.addEventListener('DOMContentLoaded', () => {
    const header = document.querySelector('header');
    const footer = document.querySelector('footer');
    let navInnerHtml = null
    let cookieSession = getCookie('session_id')

    if ( cookieSession) {

        navInnerHtml = `    
            <nav class="navigation">
                <img src="../images/logo1.png" alt="" class="logo">
            
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/products">Products</a></li>
                    <li><a href="/contact">Contact</a></li>
                    <li class="shopping-cart"><i class="fa-solid fa-bag-shopping"></i></li>
                    <li class="shopping-cart"><i class="fa-solid fa-id-badge"></i></li>
                </ul>
            
                <a href="/logout"><button type="button" class="login">Logout</button></a>
            </nav>
        `
    }else{

        navInnerHtml = `
            <nav class="navigation">
                <img src="../images/logo1.png" alt="" class="logo">
            
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/products">Products</a></li>
                    <li><a href="/contact">Contact</a></li>
                    <li class="shopping-cart"><i class="fa-solid fa-bag-shopping"></i></li>
                </ul>
            
                <a href="/login"><button type="button" class="login">Login</button></a>
            </nav>`

    }

    header.innerHTML =  navInnerHtml + `

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

    footer.innerHTML = `
    <p class="copyright">Copyright All Rights Resereved &#169 || Created by mo's fashion store</p>`

    let cartIcon = header.querySelector('.shopping-cart');
    let cart = header.querySelector('.cart');
    let closeCart = header.querySelector('#close-cart');
    let buyCart = header.querySelector('.buy-btn')

    cartIcon.addEventListener('click', () => {
        cart.classList.add("active")

        let productItems = cart.querySelectorAll('.cart-box');
        let totalPrice = cart.querySelector('.t-price').textContent;
        var currentTotal = parseFloat(totalPrice.replace('$', '')); 


        for(let i=0; i < productItems.length; i++){
            let product = productItems[i]
            let removeItem = product.querySelector('.fa-trash');

            removeItem.addEventListener('click', (e) => {
                let clickedProduct = e.target;
                let productToRemove = clickedProduct.parentElement

                let productPriceToRemove = productToRemove.querySelector('.cart-price').innerText;
                var productPriceToRemoveN = parseFloat(productPriceToRemove.replace('$', ''));

                cart.querySelector('.t-price').textContent = currentTotal - productPriceToRemoveN + '$'
                currentTotal -= productPriceToRemoveN
                productToRemove.remove()
              
            })
        }
    });

    closeCart.addEventListener('click', () =>{
        cart.classList.remove("active")
    })

    buyCart.addEventListener('click', () => {
        let productItems = cart.querySelectorAll('.cart-box');
        let currentTotal = cart.querySelector('.t-price').textContent;

        if(currentTotal == '0$'){
            alert('You didnt add any products to buy :(\nYou have to add some products before pressing the buy button')
            closeCart.click()
        }else{
            alert(`Thank you for shopping from mo's fashion store :)\nYour order of ${currentTotal} will be deleviered in 3 days.\nHave a nice day!!`)
    
            for(let i=0; i < productItems.length; i++){
                let product = productItems[i]
                product.remove()
            }
            cart.querySelector('.t-price').textContent = 0 + '$'
            currentTotal = 0
    
            closeCart.click()
        }

})
});