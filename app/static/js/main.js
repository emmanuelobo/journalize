function getLocation() {
    if (navigator.geolocation) {
        return navigator.geolocation.getCurrentPosition(getPosition, getError);
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}
function getPosition(position) {
    coordinates = String(position.coords.latitude + ', ' + position.coords.longitude);
    $('#id_location').val(coordinates);
    console.log('coordinates: ' + coordinates);
    return coordinates;
}

function getError(error) {
    return 'ERROR'
}

getLocation();

function ajaxCall(url, method, obj, callback){
    $.ajax({
        url: window.location.origin + url,
        method: method,
        dataType: 'json',
        success: callback(obj),
        error: function(error){
            console.error(error)
        }
    })
}

function deleteEntryAnimation(obj)
{
    $(obj).closest('.col-md-3').toggle(1000) // delete entry animation
}