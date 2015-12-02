app.service('DataService', function(jsonrpc) {
  var service = jsonrpc.newService('api');
  this.getUDC = service.createMethod('get_udc');
});