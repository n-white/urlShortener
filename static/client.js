var client = {
   init: function() {
      client.$newurl = $('#newurl');
      client.$send = $('#send');
      client.$send.on('submit', client.handleSubmit);
      client.$linkList = $('#linkList');
      client.fetch();
   },
   handleSubmit: function(event) {
      // Create a message variable that will be sent in POST request
      var message = {
         'actual_url': client.$newurl.val()
      }

      // Call the send method which will make a POST request
      client.send(message)

      // Stop the form from submitting
      event.preventDefault();
   },
   send: function(message) {
      // Clear the newurl input
      client.$newurl.val('');

      // Define parameters of the POST request
      var settings = {
         "async": true,
         "url": "http://localhost:5000/",
         "method": "POST",
         "contentType": "application/json",
         "data": JSON.stringify(message)
      }

      // POST the message to the server
      $.ajax(settings).done(function (response) {
         client.fetch();               
      });
   },
   fetch: function() {
      var settings = {
         "async": true,
         "url": "http://localhost:5000/links",
         "method": "GET",
      }

      $.ajax(settings).done(function (response) {
         client.populateUrls(response);
      });
   },
   populateUrls: function(list) {
      for (key in list) {
         client.addUrl(list[key]);
      }
   },
   addUrl: function(url) {
      var $link = $('<a>', {
         text: 'http://localhost:5000/' + url[1],
         title:'none',
         href: url[1],
      });
      var $elem = $('<div></div>');
      $elem.html('<a href="http://localhost:5000/'+url[1]+'">http://localhost:5000/' + url[1] + '</a>' +
         '<p>'+url[2]+'<p><p>Number of Redirects: '+url[3]+'</p>'+
         '<p>'+url[4]+'</p>');
      $elem.appendTo(client.$linkList);
   }

}