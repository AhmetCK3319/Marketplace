// let autocomplete;

// function initAutoComplete() {
//     autocomplete = new google.maps.places.Autocomplete(
//         document.getElementById('id_address'), {
//             types: ['geocode', 'establishment'],
//             //default in this app is "IN" - add your country code
//             componentRestrictions: {
//                 'country': ['in']
//             },
//         })

//     // function to specify what should happen when the prediction is clicked
//     autocomplete.addListener('place_changed', onPlaceChanged);
// }

// function onPlaceChanged() {
//     var place = autocomplete.getPlace();

//     // User did not select the prediction. Reset the input field or alert()
//     if (!place.geometry) {
//         document.getElementById('id_address').placeholder = "Start typing...";
//     } else {
//         // get the address components and assign them to the fields

//         var geocoder = new google.maps.Geocoder()
//         var address = document.getElementById('id_address').value

//         geocoder.geocode({
//             'address': address
//         }, function(results, status) {
//             if (status == google.maps.GeocoderStatus.OK) {
//                 var latitude = results[0].geometry.location.lat();
//                 var longitude = results[0].geometry.location.lng();

//                 $('#id_latitude').val(latitude);
//                 $('#id_longitude').val(longitude);

//                 $('#id_address').val(address);

//                 // adres bileşenleri arasında döngü yapın ve diğer adres verilerini atayın
//                 for (var i = 0; i < place.address_components.length; i++) {
//                     for (var j = 0; j < place.address_components[i].types.length; j++) {
//                         // get country
//                         if (place.address_components[i].types[j] == 'country') {
//                             $('#id_country').val(place.address_components[i].long_name);
//                         }
//                         // get state
//                         if (place.address_components[i].types[j] == 'administrative_area_level_1') {
//                             $('#id_state').val(place.address_components[i].long_name);
//                         }
//                         // get state
//                         if (place.address_components[i].types[j] == 'locality') {
//                             $('#id_city').val(place.address_components[i].long_name);
//                         }
//                         // get pin_code
//                         if (place.address_components[i].types[j] == 'postal_code') {
//                             $('#id_pin_code').val(place.address_components[i].long_name);
//                         } else {
//                             $('id_pin_code').val();
//                         }
//                     }
//                 }
//             }
//         });
//     }
// }

// çalısırsa detay sayfasında bulunan minus and plus butonlarına işlev verecek

$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type:'GET',
            url:url,
            success:function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal({
                        title: response.message,
                        icon: 'warning',
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // sub_total, tax and grand_total 

                    applyCartAmounts(
                        response.cart_amount['sub_total'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total'],
                    )
                    console.log(response.cart_amount['tax_dict']);
                }

            }
        })
    })
    // place the cart item quantity on load
    $('.item-qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)

    })  
    // decrease to cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type:'GET',
            url:url,
            success:function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal({
                        title: response.message,
                        icon: 'warning',
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    if(window.location.pathname == '/cart/'){

                        applyCartAmounts(
                            response.cart_amount['sub_total'],
                            response.cart_amount['tax_dict'],
                            response.cart_amount['grand_total'],
                        )

                        if(window.location.pathname == '/cart/'){
                            removeCartItem(response.qty,cart_id);
                            checkEmptyCart();
                        }
                        
                    }   
                }
            }
        })
    })
    
    // DELETE CART ITEM
    $('.delete_to_cart').on('click',function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type:'GET',
            url:url,
            success:function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal({
                        title: response.message,
                        icon: 'warning',
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status,response.message,'success')

                    applyCartAmounts(
                        response.cart_amount['sub_total'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total'],
                    )

                    removeCartItem(0,food_id);
                    checkEmptyCart();
                    
                }
            }
        })
    })

    // delete cart elemnt if the qty 0
    function removeCartItem(cartItemQty,food_id){
        if(cartItemQty <= 0 ){
        // remove the cart ıtem element 

        document.getElementById('cart-item-'+food_id).remove()

        }   
    }

    // Check if the Cart is Empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0 ){
            document.getElementById('empty-cart').style.display = 'block';
        }
    }


    function applyCartAmounts( sub_total, tax_dict, grand_total ){
        if(window.location.pathname == '/cart/'){
            $('#total').html(sub_total)
            $('#grandtotal').html(grand_total)

            console.log(tax_dict)
            for(key1 in tax_dict ){
                console.log(tax_dict[key1])
                for(key2 in tax_dict[key1]){
                    $('#tax-'+key1).html(tax_dict[key2][key2])
                }
            }
        }
    }


    $('.add_hour').on('click',function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value

        console.log( day, from_hour, to_hour, is_closed ,csrf_token)

        if(is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = "day != '' && from_hour !='' && to_hour != ''"
        }

        if(eval(condition)){
            $.ajax({
                type:'POST',
                url:url,
                data:{
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },
                success:function(response){
                    if(response.status == 'success'){
                        if(response.is_closed == 'closed'){
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>closed</td><td><a href="" class="remove_hour" data-url="/accounts/vendor/opening_hours/remove/'+response.id+'/">Remove</a></td></tr>'
                        }else{
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+ response.from_hour+' - '+response.to_hour+'</td><td><a href="" class="remove_hour" data-url="/accounts/vendor/opening_hours/remove/'+response.id+'/" >Remove</a></td></tr>'
                        }


                        $('.opening_hours').append(html)
                        document.getElementById('opening_hours').reset();
                    }else{
                        console.log(response.error)
                        swal(response.message,'','error')
                    }
                }
            })  

        }else{
            swal('Lütfen bütün kutucukları seçiniz!','','error')
        }

    })
    // docement ready close
    $('.remove_hour').on('click',function(e){
        e.preventDefault();
        url = $(this).attr('data-url');

        $.ajax({
            type:'GET',
            url:url,
            success:function(response){
                if(response.status == 'success'){
                    document.getElementById('hour-'+response.id).remove()
                }
            }
        })
    })
});

