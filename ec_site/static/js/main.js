/*  ---------------------------------------------------
    Template Name: Ogani
    Description:  Ogani eCommerce  HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Gallery filter
        --------------------*/
        $('.featured__controls li').on('click', function () {
            $('.featured__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.featured__filter').length > 0) {
            var containerEl = document.querySelector('.featured__filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
        $("body").addClass("over_hid");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
        $("body").removeClass("over_hid");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*-----------------------
        Categories Slider
    ------------------------*/
    $(".categories__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 4,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            0: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 3,
            },

            992: {
                items: 4,
            }
        }
    });


    $('.hero__categories__all').on('click', function(){
        $('.hero__categories ul').slideToggle(400);
    });

    /*--------------------------
        Latest Product Slider
    ----------------------------*/
    $(".latest-product__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------------
        Product Discount Slider
    -------------------------------*/
    $(".product__discount__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            320: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 2,
            },

            992: {
                items: 3,
            }
        }
    });

    /*---------------------------------
        Product Details Pic Slider
    ----------------------------------*/
    $(".product__details__pic__slider").owlCarousel({
        loop: true,
        margin: 20,
        items: 4,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------
		Price Range Slider
	------------------------ */
    var rangeSlider = $(".price-range"),
        minamount = $("#minamount"),
        maxamount = $("#maxamount"),
        minPrice = rangeSlider.data('min'),
        maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            minamount.val('$' + ui.values[0]);
            maxamount.val('$' + ui.values[1]);
        }
    });
    minamount.val('$' + rangeSlider.slider("values", 0));
    maxamount.val('$' + rangeSlider.slider("values", 1));

    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();

    /*------------------
		Single Product
	--------------------*/
    $('.product__details__pic__slider img').on('click', function () {

        var imgurl = $(this).data('imgbigurl');
        var bigImg = $('.product__details__pic__item--large').attr('src');
        if (imgurl != bigImg) {
            $('.product__details__pic__item--large').attr({
                src: imgurl
            });
        }
    });

    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
    proQty.prepend('<span class="dec qtybtn">-</span>');
    proQty.append('<span class="inc qtybtn">+</span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }

        $button.parent().find('input').val(newVal);

        var obj_id = $(this).parent().parent().parent().attr('id');
        var id_split = obj_id.split('__');


        // by JS DOM
        // var product_price = document.getElementById('shoping__cart__price__' + id_split[id_split.length-1]);
        // var product_total_price = document.getElementById('shoping__cart__total__' + id_split[id_split.length-1]);
        // // console.log(product_price);
        // // console.log(total_price);
        // // console.log(product_price.textContent.slice(1));
        // var new_product_total = parseFloat(product_price.textContent.slice(1)) * newVal;
        // //console.log(new_total);
        // //product_total_price.textContent = '$' + new_product_total;

        // by JQuery
        var product_price = $("td.shoping__cart__price#shoping__cart__price__" + id_split[id_split.length-1]);
        var product_total_price = $("td.shoping__cart__total#shoping__cart__total__" + id_split[id_split.length-1]);
        // console.log(product_price);
        var new_product_total = parseFloat(product_price.text().slice(1)) * newVal;
        product_total_price.text('$' + new_product_total);

        // calculate and edit the total price
        var all_product_list = $("tr.product__cart");
        var t_price = 0;
        var index = 0;
        while (index < all_product_list.length){
            var price = parseFloat(all_product_list[index].childNodes[7].textContent.slice(1));
            // var q = parseFloat(all_product_list[index].childNodes[5].textContent);
            t_price += price;
            // console.log(all_product_list[index].childNodes);
            // console.log(t_price);
            index += 1;
        }
        var total_price_obj = $('.shoping__checkout');
        total_price_obj[0].childNodes[3].childNodes[1].innerHTML='Subtotal <span>$' + t_price + '</span>';
        total_price_obj[0].childNodes[3].childNodes[3].innerHTML='Total <span>$' + t_price + '</span>';

    });
    // delete item in shopping cart  (botton X)
    var icon_close = $('.shoping__cart__item__close');
    icon_close.on('click', '.icon_close', function () {
        var button = $(this);
        console.log(button);
        var obj = button.parent().parent();
        console.log(obj);
        obj.remove();

        // after delete the item, calculate all price again
        var all_product_list = $("tr.product__cart");
        var t_price = 0;
        var index = 0;
        while (index < all_product_list.length){
            var price = parseFloat(all_product_list[index].childNodes[7].textContent.slice(1));
            // var q = parseFloat(all_product_list[index].childNodes[5].textContent);
            t_price += price;
            // console.log(all_product_list[index].childNodes);
            // console.log(t_price);
            index += 1;
        }
        var total_price_obj = $('.shoping__checkout');
        total_price_obj[0].childNodes[3].childNodes[1].innerHTML='Subtotal <span>$' + t_price + '</span>';
        total_price_obj[0].childNodes[3].childNodes[3].innerHTML='Total <span>$' + t_price + '</span>';
    })

    // update shopping cart
    var update_cart_btn = $('button#btn_update_cart');
    // console.log('666');
    // console.log(update_cart_btn);
    update_cart_btn[0].addEventListener('click', async _ => {
        try {
            //{ id1: q1, id2: q2, .....}
            var all_product_obj = $("tr.product__cart");
            // console.log(all_product_obj);
            var ec_cart = {};
            var idx = 0;
            while(idx < all_product_obj.length){
                var product_id = all_product_obj[idx].id.split('__')[2];
                var q_list_obj = all_product_obj.find('input');
                ec_cart[product_id] = q_list_obj[idx].value
                idx += 1;
            }
            const response = await fetch('/shop/update_shoping-cart/', {
              method: 'POST',
              body: JSON.stringify({ec_cart: ec_cart})
            });
        console.log('Completed!', response);
        } catch(err) {
        console.error(`Error: ${err}`);
        }
    });

})(jQuery);