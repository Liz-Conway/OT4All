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

    // closest() method searches up to the parent. And the find() method searches down.

     /*Find the closest sibling input box to this button*/
    let closestInput = $(this).siblings(".sessionsInput");

	/*If the '+' button was clicked we will need to update the totals
	So need to show the 'Update' link*/
	showUpdatedLink(closestInput);

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

	// closest() method searches up to the parent. And the find() method searches down.

     /*Find the closest sibling input box to this button*/

    let closestInput = $(this).siblings(".sessionsInput");
	/*If the '-' button was clicked we will need to update the totals
	So need to show the 'Update' link*/
	showUpdatedLink(closestInput);

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

$(".sessionsInput").on('input', function() {
	/*If the value in the number of sessions input box changes
	Need to allow the user to update the Bookings*/
	showUpdatedLink($(this));
});

// Update number of sessions on click
$(".updateLink").click(updateSessions);

function updateSessions(event) {
    /*Use the closest() method to find the parent of the updateLink button (it is a "div")*/
    /* Use the prev() method to find the previous sibling element of that div
     *  IF it has a class of ".updateForm"*/
    let form = $(this).closest("div").prev(".updateForm");
    /*Call this form's submit method*/
    form.submit();
}

// Remove item & reload on click
$(".removeLink").click(removeSessions);

/*Post some data to a URL
Once the response comes back from the server,
 reload the page to reflect the updated bag*/
function removeSessions(event) {
    /*CSRF token which we can store as a string by just rendering it here. */
    let csrfToken = getCSRF();
    /*therapyId can be obtained by splitting the ID of the update link being clicked on
    and taking the second half of it.*/
    let therapyId = $(this).attr("id").split("remove")[1];
    let url = `/bookings/remove/${therapyId}`;
    /*data = the object we'll use to send this data to the server.
    The data variable will contain a special key called "csrfmiddlewaretoken",
    which will have our csrfToken variable as its value;
    The "csrfmiddlewaretoken" key will match the field Django is expecting
    to see in request.POST when we post it to the server.*/
    let data = {"csrfmiddlewaretoken": csrfToken};

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
    return value;
}

function showUpdatedLink(input) {
	/*From the input box traverse UP to the closest parent form*/
	let form = input.closest("form");
	/*From the parent form traverse to the NEXT sibling with a class of "editLinks"*/
	let parentLink = form.next(".editLinks")
	/*The div with class of "editLinks" is the parent of the update link we need to show.
	Use find() to traverse DOWN into the children of the editLinks div.
	Find the child with a class of "updateLink"*/
	let updateLink = parentLink.find(".updateLink")

	updateLink.css("display", "block");
}
