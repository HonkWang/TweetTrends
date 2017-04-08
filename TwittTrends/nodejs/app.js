var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);

app.use(express.static('public'));
app.get('/', function (req, res) {
    res.sendfile(__dirname + '/public/index.html');
});

server.listen(2222)
// server.listen(2222, function(){
//     console.log('listening on*:2222')
// });

var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
    host: 'https://search-mytestdomain-qnyhs32jjgymxujnd6h75uqwtq.us-east-1.es.amazonaws.com:443'
});

io.on('connection', function (socket) {
    socket.emit('news', {message: 'welcome!', id: socket.id});//Note that emit event name on the server matches the emit event name

    socket.on('my other event', function (data) {
        var key = data.key;
        client.search({
            q: key,
            size: 1000
        } ,function (error, body) {
            var result = [];
            var hits = body.hits.hits;
            for (var i = 0; i < hits.length; i++) {
                result[i] = hits[i]._source;
            }
            // console.log(result) //it's working here
            // console.log(result.geo.location)
            var myObject = {
                "tweeter": result
            };
            socket.emit('toggle', myObject);
        });
    });
});