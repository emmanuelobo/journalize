function getLocation() {
    if (navigator.geolocation) {
        return navigator.geolocation.getCurrentPosition(getPosition, getError);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}
function getPosition(position) {
    coordinates = String(position.coords.latitude + ', ' + position.coords.longitude);
    $('#id_location').val(coordinates);
    console.log(coordinates);
    return coordinates;
}

function getError(error) {
    return 'ERROR'
}

getLocation();



