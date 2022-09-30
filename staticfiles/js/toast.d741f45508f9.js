// static
$(".close").click(closeToast);

function closeToast(event) {
    let toast = $(this).closest("div.toast");
    toast.hide();
}
