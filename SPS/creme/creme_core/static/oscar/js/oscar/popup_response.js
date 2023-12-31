(function() {
    'use strict';
    var initData = JSON.parse(document.getElementById('oscar-popup-response-constants').dataset.popupResponse);
    switch(initData.action) {
    case 'change':
        window.opener.creme.dismissChangeRelatedObjectPopup(window, initData.value, initData.obj, initData.new_value);
        break;
    case 'delete':
        window.opener.creme.dismissDeleteRelatedObjectPopup(window, initData.value);
        break;
    default:
        window.opener.creme.dismissAddRelatedObjectPopup(window, initData.value, initData.obj);
        break;
    }
})();
