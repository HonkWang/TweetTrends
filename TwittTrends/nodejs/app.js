var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);

var es = require('elasticsearch');
var endpoint = 'http://search-twitt-trends-r5ndyqwtijzgth4oymeqymz6yq.us-east-1.es.amazonaws.com';
var client = new es.Client({host: endpoint});

var bodyParser = require('body-parser');
var request = require("request");

app.use(express.static('public'));
app.use(bodyParser.json({type: 'text/plain'}));
console.log('done1')
app.get('/', function (req, res) {
    res.sendfile(__dirname + '/public/index.html');
});
console.log('done2')
app.post('/', function (req, res) {
    res.status(200).end();
    
    var type = req.get('x-amz-sns-message-type');
    if (type === 'SubscriptionConfirmation') {
        var url = req.body.SubscribeURL;
        console.log(url)
        request(url, function (error, response, body) {
            console.log(body);
        });
    }
    else if (type === 'Notification') {
        var id = req.body.MessageId;
        var message = req.body.Message;
        client.index({
            index: 'twitt-trends',
            type: 'tweets',
            id: id,
            body: message
        });
        io.emit('newcoming', {
            tweet: JSON.parse(message)
        });
    }
});
console.log('done3')
server.listen(80);

io.on('connection', function (socket) {
    socket.on('clicked', function (data) {
        var key = data.key;
        client.search({
            q: key,
            size: 1000
        }, function (error, body) {
            var result = [];
            var hits = body.hits.hits;
            for (var i = 0; i < hits.length; i++) {
                result[i] = hits[i]._source;
            }
            socket.emit('toggle', {
                tweet: result
            });
        });
    });
});
console.log('done4')