/**
	Core logic for this comes from:
	https://stripe.com/docs/payments/accept-a-payment

	CSS from :
	https://stripe.com/docs/stripe-js
 */

/*Those little script elements contain the values we need as their text.
So we can get them just by getting their ids and using the .text function.
Slice off the first and last character on each
since they'll have quotation marks which we don't want.*/
let stripe_public_key = $("#id_stripe_public_key").text().slice(1, -1);
let client_secret = $("#id_client_secret").text().slice(1, -1);

/*Style taken from
https://stripe.com/docs/js/appendix/style*/
let style = {
	base: {
		iconColor: '#c4f0ff',
		color: '#000',
		fontWeight: '500',
		fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
		fontSize: '16px',
		fontSmoothing: 'antialiased',
		':-webkit-autofill': {
			color: '#fce883',
		},
		'::placeholder': {
			color: '#87BBFD',
		},
	},
	invalid: {
		iconColor: '#E84610',
		color: '#E84610',
	},
}

/*Made possible by the stripe js included in the base template.
All we need to do to set up stripe is create a variable using our stripe public key*/
let stripe = Stripe(stripe_public_key);
/*Create an instance of stripe elements.*/
let elements = stripe.elements();
/*Use "elements" to create a card element.*/
/*The card element can also accept a style argument.*/
let card = elements.create('card', {style: style});


/*Mount the card element to the div we created in purchase.html*/
card.mount("#stripeCard");

// Handle realtime validation errors on the card element
card.addEventListener('change', handleCardChange);

function handleCardChange(event) {
	let errorDiv = $("#stripeError");

	if(event.error) {
		let html = `
			<span class="icon" role="alert">
				<i class="fas fa-times"></i>
			</span>
			<span>${event.error.message}</span>
		`;
		$(errorDiv).html(html);
	} else {
		errorDiv.textContext = "";
	}
}

// Handle form submit
let form = document.getElementById('paymentForm');

form.addEventListener('submit', formSubmit);

function formSubmit(event) {
	console.log("Submitting the form");
	// console.log('Client Secret', clientSecret);

	event.preventDefault();
	/*Disable both the card element and the submit button
	 to prevent multiple submissions.*/
    card.update({ 'disabled': true});
    $('#submitButton').attr('disabled', true);
	/*Trigger the overlay and fade out the form when the user clicks the submit*/
    $('#paymentForm').fadeToggle(100);
    $('#loadingOverlay').fadeToggle(100);


        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                }
        }).then(function(result) {
            if (result.error) {
                let errorDiv = document.getElementById('stripeError');
                let html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
				/*Show the form and fade out the overlay when there is an error*/
                $('#paymentForm').fadeToggle(100);
                $('#loadingOverlay').fadeToggle(100);
				/*If there's an error.
				Re-enable the card element and the submit button
				 to allow the user to fix it*/
                card.update({ 'disabled': false});
                $('#submitButton').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
					console.log("Payment intent succeeded");
					form.submit();
                }
            }
        });
}
