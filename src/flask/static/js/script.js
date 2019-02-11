

$('input').keyup(debounce(function(){
    var $this=$(this);
    //alert( $this.val() );
    var n1 = $this.val();
    var n2 = $('#n2').val();
    var n3 = $('#n3').val();
    var calc = n1 * n2 * n3;
    alert(calc);
},500));



//http://davidwalsh.name/javascript-debounce-function
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};