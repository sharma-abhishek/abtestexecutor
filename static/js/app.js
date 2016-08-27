var host = '127.0.0.1';
var port = 8000;

var basePath = host + ":" + port;

//object that holds all tests data.
var test = function(data) {
    if(data) {
        this.id = data.id;
        this.requester = data.requester;
        this.environment_id = data.environment_id;
        this.status = data.status;
        this.created = data.start_time;
    }
}

//array to hold all the test(s) object
var tests = [];


//call to push testObj to array
function addTest(testObj) {
    tests.push(testObj);
}

//formatDate
function formatDate(dt) {
    var dt = new Date(dt);
    var year = dt.getFullYear();
    var month = dt.getMonth();
    var date = dt.getDate();
    date = date < 10 ? ("0" + date) : date;
    var hours = dt.getHours();
    hours = hours < 10 ? ("0" + hours) : hours;
    var mins = dt.getMinutes();
    mins = mins < 10 ? ("0" + mins) : mins;
    return year + "/" + month + "/" + date + " " + hours + ":" + mins;
}


var table = $("<table border = '1' width='100%'/>");
var first_row = $("<tr class='header' />");

//getTests
function getTests() {
    $.get('http://' + basePath + '/api/test/execute/', function(data){
        var dataLength = data.length;

        for(var i = 0; i < dataLength; i++) {
            var result = data[i];
            console.log(result);
            var testObj = new test(result);
            addTest(testObj);
        }

        if(dataLength > 0) {
           render();
        }
    });
}

//submitTestRequest
function submitTestRequest() {
    var requester = $("#requester").val();
    var environment_id = $("#environment_id").val();

    var data = {
        'requester' : requester,
        'environment_id' : environment_id
    }

    $.post('http://' + basePath + '/api/test/execute/', data).done(function(data){
        var testObj = new test(data.result);
        addTest(testObj);
        if(tests.length == 1) {
            render();
        } else {
            prepareRow(testObj).insertAfter($("tr.header"));    
        }
    }).fail(function(xhr, status, error){
        if(error == 'Bad Request') {
            alert(JSON.parse(xhr.responseText).message);
        } else {
            alert(xhr.responseText);
        }
    });
}

//prepare row for table
function prepareRow(testData) {
        var row = $("<tr />");
        
        row.append($("<td />").append(testData.id));
        row.append($("<td />").text(testData.requester));
        row.append($("<td />").text(testData.environment_id));
        var status = testData.status;
        var text = "RUNNING";
        if (status == 1) {
            var hyperlink = $("<a href='test/" + testData.id + "'>PASS</a>");
            row.append($("<td id='col_" + testData.id + "'/>").append(hyperlink));
        } else if(status == 0) {
            var hyperlink = $("<a href='test/" + testData.id + "'>FAIL</a>");
            row.append($("<td id='col_" + testData.id + "'/>").append(hyperlink));
        } else {
            row.append($("<td id='col_" + testData.id + "'/>").text("RUNNING"));
        }
        
        //row.append($("<td id='col_" + testData.id + "'/>").text(testData.status));
        row.append($("<td />").text(formatDate(testData.created)));
        return row;
}

//render
function render() {
    var len = tests.length;

    first_row.append($("<th />").text("Request ID"));
    first_row.append($("<th />").text("Requester"));
    first_row.append($("<th />").text("Environment ID"));
    first_row.append($("<th />").text("Status"));
    first_row.append($("<th />").text("Created"));

    table.append(first_row);

    //add table in 'results' div
    for(var i = len - 1; i >= 0; i--) {
        var row = prepareRow(tests[i]);
        table.append(row);
    }

    if(len != 0) {
        $("#results").append(table); 
    }      
}

var connection = new WebSocket('ws://' + basePath);

// When the connection is open, send some data to the server
connection.onopen = function () {
    console.log("Connected");
};

// Log errors
connection.onerror = function (error) {
  console.log('WebSocket Error ' + error);
};

// Log messages from the server
connection.onmessage = function (e) {
  var data = JSON.parse(e.data);
  var status = data.status;

  if(status == 1) {
     var hyperlink = $("<a href='test/" + data.id + "'>PASS</a>");
     $("#col_" + data.id).html(hyperlink);
  } else if (status == 0) {
      var hyperlink = $("<a href='test/" + data.id + "'>FAIL</a>");
      $("#col_" + data.id).html(hyperlink);
  } else {
      $("#col_" + data.id).html("ERROR");
  } 
};

//handle onclose
connection.onclose = function(e) {
    console.log('Disconnected!');
};


$('document').ready(function() {
        getTests();
});