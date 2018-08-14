$(document).ready(function() {

  var data = {
    items: [],
  };

  var clndrTemplate = $('#clndr-template').html();
  var clndrDayTemplate = $('#clndr-day-template').html();
  var clndrEventTemplate = $('#clndr-event-template').html();

  var $eventInfo = $('#event-info');

  var $clndr = $('#clndr')

  var initialDate = $clndr.attr('data-date');
  initialDate = initialDate ? moment(initialDate) : null;

  var month = initialDate || moment();




  function updateInfo(events) {
    $eventInfo.empty();
    events.forEach(renderEvent);
  }

  function renderEvent(event) {

    var date = moment(event.start_date).format('DD MMMM YYYY [kl.] HH:mm');
    if (event.end_date) {
      date += ' - ' + moment(event.end_date).format('DD MMMM YYYY [kl.] HH:mm');
    }

    $eventInfo.append(
      clndrEventTemplate
        .replace('{title}', event.summary)
        .replace('{date}', date)
    );
    if (event.description) {
      $eventInfo.children().last().find('.info').html(event.description);
    }
  }

  function renderDay(day) {
    return clndrDayTemplate
            .replace('{day}', day.day)
            .replace('{class}', day.classes);
  }

  function getData(month) {
    var id = $clndr.attr('data-id');

    // Get events 12 days before and after current month to make sure
    // that we will fill out the calendar
    var query = $.param({
      time_min: month.clone().startOf('month').startOf('day').add(-12, 'days').toISOString(),
      time_max: month.clone().endOf('month').startOf('day').add(12, 'days').toISOString(),
    }).replace(/%3A/g, ':');

    $.get('/api/google/calendar/'+id+'?'+query, function(response) {
      if (!data.items.length) {
        data = response;
        calendar.addEvents(data.items);
      } else {
        // Filter events that we don't already have
        var newEvents = response.items.filter(i => !data.items.find(di => di.id === i.id));
        if (newEvents.length) {
          data.items = data.items.concat(newEvents);
          calendar.addEvents(newEvents);
        }
      }

      if (initialDate) {
        // Get all events of the intial date and show their info
        var events = data.items.filter(item => moment(item.start_date).isSame(initialDate, 'day'));
        initialDate = null;
        updateInfo(events);
      }
    });
  }

  var calendar = $('#clndr').clndr({
    startWithMonth: month,
    moment: moment,
    weekOffset: 1,
    forceSixRows: true,
    dateParameter: 'start_date',
    events: data.items || [],
    selectedDate: initialDate ? initialDate.toDate() : null,
    trackSelectedDate: true,
    ready: function() {
      getData(month);
    },
    render: function(data) {
      var days = data.days.map(renderDay);
      return clndrTemplate
              .replace('{month}', data.month)
              .replace('{year}', data.year)
              .replace('{days}', days.join(''));
    },

    clickEvents: {
      previousMonth: function(month) {
        getData(month);
      },
      nextMonth: function(month) {
        getData(month);
      },
      click: function(data) {
        updateInfo(data.events);
      }
    },
  });
});







