/**
 * Created by swK on 24/03/2017.
 */

function WordsCloud(div) {
    // div: jQuery element of div to be tuned into a WordCloud

    this.div = div;
    this.words = {};

    this.populate = function (words) {
        // words: 'dict' where keys are the words and values the number of times
        // each word has appeared

        var i, word;
        var formatted_words = [];

        for (i=0; i<words.length; i++) {
            word = words[i];
            formatted_words.push({
                text: word.word,
                weight: word.freq
            });
        }

        this.clear();
        this.div.jQCloud(formatted_words);
        this.words = words;
    };

    this.clear = function () {
        this.div.jQCloud('destroy');
    };

    this.restore = function () {
        this.populate(this.words);
    };
}

function onclick_scan(button, url_input, words_cloud) {

    $.ajax({
        method: 'POST',
        url: 'scan_url/',
        dataType: 'json',
        data: {url: url_input.val()}
    })

    .always(() => {
        words_cloud.clear();
    })

    .then((res) => {
        words_cloud.populate(res.words_list);
    })

    .fail((e) => {
        alert("ERROR: " + JSON.stringify(e.responseText));
    });
}
