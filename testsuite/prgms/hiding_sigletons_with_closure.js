
// hiding sigletons and utilities with closures

function html_to_md() {
    var tokens = {
        "p": "\n",
        "/p": "\n",
        "h1": "#",
        "/h1": '#\n',
        "h2": "##",
        "/h2": "##\n",
        "h3": "###",
        "/h3": "###\n",
        "ul": "\n",
        "/ul": "",
        "li": "- ",
        "/li": "\n",
        "i": "_",
        "/i": "_",
        "b": "*",
        "/b": "*"
    };

    return function(html) {
        return html.replace(/<([^<>]+)>/g, function(a, b) {
            var t = tokens[b];
            print(t);
            return typeof t === 'string' ? t : a;
        });
    };
}


var parse = html_to_md();

var r = parse("<h1>My Title</h1><h2>Subtitle</h2><ul><li>First item </li><li>Second <i>item</i></li></ul>");

print(r);
