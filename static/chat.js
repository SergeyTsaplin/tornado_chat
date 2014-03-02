var app = angular.module('chat', []);

app.factory('ChatService', function() {
    var service = {};
    var ws = new WebSocket("ws://" + location.host + "/chatsocket");

    ws.onopen = function() {
        service.callback("Succeeded to open a connection");
    }

    ws.onerror = function() {
        service.callback("Failed to open a connection");
    }

    ws.onmessage = function(message) {
        service.callback(message.data);
    }

    service.send = function(message) {
        ws.send(message);
    }

    service.subscribe = function(callback) {
        service.callback = callback;
    }

    return service;
})

app.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
})

function ChatCtrl($scope, ChatService, $location, $anchorScroll, $http) {
    $scope.messages = [];
    $scope.post = {};
    $scope.historyCount = 20;

    function formatMessage(message){
        var created_at = new Date(message.created_at);
        var now = new Date();

        if (now.toDateString() != created_at.toDateString()){
            message.created_at = formatDate(created_at);
        } else {
            message.created_at = formatDate(created_at, true);
        }
        return message
    }

    ChatService.subscribe(function(message) {
        var post = angular.fromJson(message);
        post = formatMessage(post);

        $scope.messages.push(post);
        $scope.$apply();
        $location.hash(post.id);
        $anchorScroll();
    })

    $scope.send = function(post) {
        var message = angular.toJson(post);
        ChatService.send(message);
        $scope.post = {};
    }

    $scope.getHistory = function(){
        var first_message_id = '';
        if ($scope.messages.length > 0)
            first_message_id = $scope.messages[0].id;
        $http.get('/history', {params:{
            first_message_id: first_message_id,
            count: $scope.count
        }}).success(function(data){
            if (data.error) {
                //TODO: show errors with bootstrap alerts
                alert(data.error);
                return;
            }
            // Remove history link if there is no messages yet
            if (data.length == 0) {
                document.getElementById('history-link').remove();
                return;
            }
            var old_messages = [];
            for (var i = 0; i<data.length; i++){
                var post = angular.fromJson(data[i])
                post = formatMessage(post);
                old_messages.push(post)
            }
            $scope.messages =  old_messages.concat($scope.messages)
            $scope.$apply();
        });
    }
}

function formatDate(date, time_only){
    console.log(date);
    var hours = leadZero(date.getHours(), 2);
    var minutes = leadZero(date.getMinutes(), 2);
    var seconds = leadZero(date.getSeconds(), 2);
    var result = '';
    if (!time_only){
        var day = leadZero(date.getDate(), 2);
        var month = leadZero(date.getMonth(), 2);
        var year = date.getFullYear();
        result = year + '-' + month + '-' + day + ' ';
    }

    result += hours + ':' + minutes + ':' + seconds;
    return result;
}

Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}

NodeList.prototype.remove = HTMLCollection.prototype.remove = function() {
    for(var i = 0, len = this.length; i < len; i++) {
        if(this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}

function leadZero(number, length) {
    while(number.toString().length < length){
        number = '0' + number;
    }
    return number;
}