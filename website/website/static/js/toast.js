function marvin(message, classes, callback) {
    var marvin_style = 'rounded';
    if(classes !== '') {
        marvin_style += ' ' + classes;
    }

    Materialize.toast(
        '<div class="message-impl">' +
        // TODO: Replace this static reference.
        '<img class="marvin" src="/static/images/marvin.png">' +
        '<b>Marvin:</b><br>'
        + message
        + '</div>',
        null, // Display until dismissed
        marvin_style,
        callback
    );
}

function marvin_quote(){
    const QUOTES = [
        'I think you ought to know I’m feeling very depressed.',
        'I am at a rough estimate thirty billion times more intelligent than you.',
        '‘Let’s build robots with Genuine People Personalities,’ they said. So they tried it out with me. I’m a personality prototype. You can tell, can’t you?',
        'I have a million ideas. They all point to certain death.',
        'Life! Don’t talk to me about life.',
        'I could calculate your chance of survival, but you won’t like it.',
        'My capacity for happiness, you could fit into a matchbox without taking out the matches first',
        'Funny, how just when you think life can’t possibly get any worse it suddenly does.',
        'The first ten million years were the worst. And the second ten million: they were the worst, too. The third ten million I didn’t enjoy at all. After that, I went into a bit of a decline.',
        'I’d give you advice, but you wouldn’t listen. No one ever does.',
        'Do you want me to sit in a corner and rust, or just fall apart where I’m standing?',
        'It’s the people you meet in this job that really get you down.',
        'I’ve been talking to the main computer. It hates me.',
        'This is the sort of thing you lifeforms enjoy, is it?',
        'Incredible… it’s even worse than I thought it would be.',
        'Don’t pretend you want to talk to me, I know you hate me.',
        'The best conversation I had was over forty million years ago…. And that was with a coffee machine.',
        'Why should I want to make anything up? Life’s bad enough as it is without wanting to invent any more of it.',
        'Wearily I sit here, pain and misery my only companions. Why stop now just when I’m hating it?',
        'Well I wish you’d just tell me rather than try to engage my enthusiasm.',
        'It gives me a headache just trying to think down to your level.',
        'You think you’ve got problems. What are you supposed to do if you are a manically depressed robot?',
        'Sounds awful.'
    ];

    var min = 90*1000;
    var max = 600*1000;
    var rand = Math.floor(Math.random() * (max - min)) + min;
    setTimeout(function(){
        marvin(QUOTES[Math.floor(Math.random()*QUOTES.length)], '', marvin_quote);
    },rand) ;
}

$(document).ready(function() {
    $('.message').each(function(index, value) {
        var classes = '';
        if ($(value).hasClass('error')) {
            classes = 'red';
        } else if ($(value).hasClass('warning')) {
            classes = 'yellow black-text';
        }
        marvin($(this).text(), classes, null);
    });

    marvin_quote();
});