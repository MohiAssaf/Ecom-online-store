let addProductBtns = document.querySelectorAll('.product-addtocart');


addProductBtns.forEach((productBtn) => {
    productBtn.addEventListener('click', (e) => {
        console.log(`Product Item ${e.target} was added`)
    })
})

