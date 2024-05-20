let addProductBtns = document.querySelectorAll('.product-addtocart');


document.addEventListener('DOMContentLoaded', () => {
    let cart = document.querySelector('.cart-orders');

    addProductBtns.forEach((productBtn) => {
        productBtn.addEventListener('click', (e) => {
            let pBtnParent = e.target.parentElement.parentElement
            console.log(`Product Item ${e.target} was added`)
            console.log(pBtnParent.img)
        })
    })
})
