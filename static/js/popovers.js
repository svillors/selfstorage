document.addEventListener("DOMContentLoaded", function () {
	const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
	popoverTriggerList.forEach(function (popoverTriggerEl) {
		new bootstrap.Popover(popoverTriggerEl, {
			trigger: 'focus',
			html: true,
			placement: 'bottom',
            container: 'body'
		});
	});
});
