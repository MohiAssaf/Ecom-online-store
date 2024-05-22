let addProductBtns = document.querySelectorAll('.product-addtocart');


document.addEventListener('DOMContentLoaded', () => {
    let cart = document.querySelector('.cart-orders');

    addProductBtns.forEach((productBtn) => {
        productBtn.addEventListener('click', (e) => {
            let productCard = e.target.parentElement.parentElement
            let productImage = productCard.querySelector('.product-img').src;
            let productName = productCard.querySelector('.product-name').innerText;       
            let productPrice = productCard.querySelector('.product-price').textContent;
            var productPriceN = parseFloat(productPrice.replace('$', ''));
            let totalPrice = document.querySelector('.t-price');
            let totalpriceTXT = totalPrice.textContent;
            var currentTotal = parseFloat(totalpriceTXT.replace('$', '')); 


            cart.innerHTML += `
            <div class="cart-orders">
            
                <div class="cart-box">
                    <img src="${productImage}" alt="" class="cart-img">
                    <div class="cart-details">
                        <div class="cart-title">${productName}</div>
                        <div class="cart-price">${productPrice}</div>
                        <input type="number" value="1" class="cart-quantity">
                    </div>

                    <i id="remove-item" class="fa-solid fa-trash"></i> 
                </div>

            </div>`

            totalPrice.textContent = productPriceN + currentTotal + '$'
            
        })
    })
})
