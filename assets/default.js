function trim(x) { return (""+x).replace(/^\s+/,"").replace(/\s+$/,"") }
function map(a, f, undef) {
    var aa = [];
    for (var i in a) {
        var result = f(a[i]);
        if (result != undef) aa.push(result);
    }
    return aa;
}
function mapfilter(a, key, value, f) { return map(a, function(x) { if (x[key] == value) return f(x)}) }
function filter(a, key, value) { return map(a, function(x) { if (x[key] == value) return x }) }
function zip(a) { var aa = []; for (var i in a) aa = aa.concat(a[i]); return aa; }
function unique(a) { var aa = []; for (var i in a) if (aa.indexOf(a[i]) < 0) aa.push(a[i]) return aa; }
function render_text(text, undef) {
    if (!text) text="";
    return text
        .replace(/</g, '&lt;')
        .replace(/&/g, '&amp;')
        .replace(/^h[0-9]\.(.*)$/gmi, '<strong>$1</strong>')
        .replace(/(http(s?):\/\/\S*[^\s,.?\)])/g, '<a href="$1">$1</a>')
        .replace(/([^a](\s|>)[^<\s]{20,30})/g, '$1<wbr>')
        .replace(/([^a](\s|>)[^<\s]{20,30})/g, '$1<wbr>') // TODO proper rendering of texts
        .replace(/([^a](\s|>)[^<\s]{20,30})/g, '$1<wbr>')
        .replace(/([^a](\s|>)[^<\s]{20,30})/g, '$1<wbr>')
        .replace(/\n/g, '<br>\n')
}
function pad(x, char, len, undef) {
    x = "" + x;
    if (char === undef) char = "0";
    if (len  === undef) len  = 2;
    for (var i=x.length; i<len; i++)
        x=char+x;
    return x;
}
function render_date(date) {
    return [pad(date.getDate()), pad(date.getMonth()+1), date.getFullYear()].join(".");
}
