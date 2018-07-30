$( document ).ready(function() {
    $( ".cross" ).hide();
    $( ".navDiv" ).hide();
    $( ".hamburger" ).click(function() {
        $( ".navDiv" ).slideToggle( "slow", function () {
            $( ".hamburger" ).hide();
            $( ".cross" ).show();
        });
    });
    $( ".cross" ).click(function() {
        $( ".navDiv" ).slideToggle( "slow", function() {
            $( ".cross" ).hide();
            $( ".hamburger" ).show();
        });
    });
});