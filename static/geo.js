ymaps.ready(init);
var myMap;

function init() {
    myMap = new ymaps.Map("map", {
        center: [55.7878, 37.6076], zoom: 14, controls: []
    }, {
        balloonMaxWidth: 200, searchControlProvider: 'yandex#search'
    });

    var geolocationControl = new ymaps.control.GeolocationControl({});
    geolocationControl.events.add('locationchange', async function (event) {
        myMap.balloon.close();
        var position = event.get('position');
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: JSON.stringify({latitude: position[0], longitude: position[1], geo_location: true}),
            headers: {'Content-Type': 'application/json'}
        });
        await response.json();
    });
    myMap.controls.add(geolocationControl);
    myMap.controls.add(new ymaps.control.ZoomControl({}));
    myMap.controls.add(new ymaps.control.SearchControl({}));
    myMap.controls.add(new ymaps.control.RulerControl({}));
    myMap.controls.add(new ymaps.control.TypeSelector({}));


    myMap.events.add('click', async function (e) {
        if (!myMap.balloon.isOpen()) {
            var coords = e.get('coords');
            myMap.balloon.open(coords, {
                contentHeader: 'Вы отметили ваше место нахождения',
                contentBody: '<p>Координаты: ' + [coords[0].toPrecision(6), coords[1].toPrecision(6)].join(', ') + '</p>',
                contentFooter: '<sup>Щелкните еще раз,<br> если хотите выбрать другое место</sup>'
            });
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: JSON.stringify({latitude: coords[0], longitude: coords[1], geo_location: false}),
                headers: {'Content-Type': 'application/json'}
            });
            await response.json();
        } else {
            myMap.balloon.close();
        }
    });
}