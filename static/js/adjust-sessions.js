/*This jQuery code is only run after the HTML document has fully loaded*/
//https://api.jquery.com/ready/
$( domLoaded );

function domLoaded() {
	/*Set event handlers to handle clicking the '+' and '-' Buttons
	which are either side of the sessions inputBox*/
	$(".incrementSessions").click(addSession);
	$(".decrementSessions").click(subtractSession);

	/* If the default number of sessions in the input box was set to  1
	It allows us to click the minus button and potentially add a number of sessions of 0 to the cart.
	Also if the default number of sessions in the input box was set to  99
	It allows us to click the plus button and potentially add a number of sessions of 100 to the cart.
	The input element's Min and Max will prevent this via form validation.
	*/

	/* Get all the sessions inputs on the page & Iterating through them.
	For each one calling the enable/disable function as soon as the page loads.*/
	let allSessionInputs = $(".sessionsInput");
	/*Ensure proper enabling/disabling of all inputs on page load*/
	for(let i =0; i < allSessionInputs.length; i++) {
	    let therapyId = $(allSessionInputs[i]).data("therapyid");
	    handleEnableDisable(therapyId);
	}

}

/*Increment number of sessions*/
function addSession(event) {
    /*prevent the default button action.*/
    event.preventDefault();

	/*If the '+' button was clicked we will need to update the totals
	So need to show the 'Update' link*/
	$(".updateLink").css("display", "block");

    // closest() method searches up to the parent. And the find() method searches down.

     /*Find the closest sibling input box to this button*/
    let closestInput = $(this).siblings(".sessionsInput");
    /*Cache the value that's currently in the input box in a variable called currentValue*/
    let currentValue = parseInt(closestInput.val());
    /*Use that variable to set the input boxes new value to the current value plus one.*/
    closestInput.val(currentValue + 1);
    /* For some reason Javascript converts the "data" identifier to lower case??????????*/
    let therapyId = $(this).data("therapyid");
	/*Check if increasing the number of sessions has brought it to the Max*/
    handleEnableDisable(therapyId);
}

/*Decrement number of sessions*/
function subtractSession(event) {
	/*prevent the default button action.*/
    event.preventDefault();

	/*If the '-' button was clicked we will need to update the totals
	So need to show the 'Update' link*/
	$(".updateLink").css("display", "block");

	// closest() method searches up to the parent. And the find() method searches down.

     /*Find the closest sibling input box to this button*/
    let closestInput = $(this).siblings(".sessionsInput");
	/*Cache the value that's currently in the input box in a variable called currentValue*/
    let currentValue = parseInt(closestInput.val());
	/*Use that variable to set the input boxes new value to the current value minus one.*/
    closestInput.val(currentValue - 1);
	/* For some reason Javascript converts the "data" identifier to lower case??????????*/
    let therapyId = $(this).data("therapyid");
	/*Check if decreasing the number of sessions has brought it to the Min*/
    handleEnableDisable(therapyId);
}

/*Each input will be associated with a specific therapy id.
We can pass that therapy id into the handleEnableDisable() function.*/
/*Disable +/- buttons outside 1 - 99 range*/
function handleEnableDisable(therapyId) {
    /*Use the therapyId to get the current value of the input based on its id attribute.*/
	let currentValue = parseInt($(`#idSessions${therapyId}`).val());
    let minusDisabled = currentValue < 2;
    let plusDisabled = currentValue > 98;

    /*Disable the minus button if the current value is less than two*/
    $(`#decrementSessions${therapyId}`).prop('disabled', minusDisabled);
    /*Disable the plus button if the current value is more than 98*/
    $(`#incrementSessions${therapyId}`).prop('disabled', plusDisabled);
}

/*Call the handle enable/disable function
if the user uses the built-in up and down arrows in the number box to change the quantity.
by listening to the change event on the sessions input*/
/*Check enable/disable every time the input is changed*/
$(".sessionsInput").change(function() {
    let therapyId = $(this).data("therapyid");
    handleEnableDisable(therapyId);
});


// Update number of sessions on click
// $(".updateLink").click(updateSessions);

function updateSessions(event) {
    /*Use the closest() method to find the parent of the updateLink button (it is a "div")*/
    /* Use the prev() method to find the previous sibling element of the div
     *  IF it has a class of ".updateForm"*/
    let form = $(this).closest("div").prev(".updateForm");
    /*Call the form's submit method*/
    form.submit();
}

// Remove item & reload on click
// $(".removeLink").click(removeSessions);

/*Post some data to a URL
Once the response comes back from the server,
 reload the page to reflect the updated bag*/
function removeSessions(event) {
    /* NB this uses the actual template variable with the double curly brackets.
    As opposed to the template tag which uses the inner percent signs.
    This is because the former renders the actual token.
    While the latter renders a hidden input field in a form.*/
    // let csrfToken = "{{ csrf_token }}";

    /*CSRF token which we can store as a string by just rendering it here. */
    let csrfToken = getCSRF();
    /*prodId can be obtained by splitting the ID of the update link being clicked on
    and taking the second half of it.*/
    let prodId = $(this).attr("id").split("remove")[1];
    /*Use the data() method to pull the size from the data-productSize attribute*/
    /*For some reason JS converts the data attribute to lowercase*/
    let size = $(this).data("productSize".toLowerCase());
    let url = `/bag/remove/${prodId}`;
    /*data = the object we'll use to send this data to the server.
    The data variable will contain a special key called "csrfmiddlewaretoken",
    which will have our csrfToken variable as its value;
    and the data variable will contain the size.
    The "csrfmiddlewaretoken" key will match the field Django is expecting
    to see in request.POST when we post it to the server.*/
    let data = {"csrfmiddlewaretoken": csrfToken, "productSize": size, "whatever": 'dude'};

    /*Use the post method from jQuery.
    Giving it both the URL and the data.*/
    $.post(url, data)
        /*When done -> execute a function to reload the page.*/
        .done(function() {
            location.reload();
        });
}

/*https://www.hacksoft.io/blog/quick-and-dirty-django-passing-data-to-javascript-without-ajax*/
function getCSRF() {
    let selector = "input[name='csrfmiddlewaretoken']";
    let element = document.querySelector(selector);
    let value = element.getAttribute('value');
    //return JSON.parse(value);
    return value;
}
