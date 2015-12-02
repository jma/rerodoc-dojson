app.controller('AutocompleteController', function($scope, DataService) {

  $scope.populateTitleMap = function (form) {
    updateUDC(form);
  };

  $scope.setValue = function (form, item) {
    form.name = item.name;
    $scope.model.udc.fr = item.fr;
    $scope.model.udc.en = item.en;
    $scope.model.udc.it = item.it;
    $scope.model.udc.de = item.de;
    $scope.model.udc.uri = item.uri;
    $scope.model.udc.code = item.code;
  };

  function updateUDC(form){
    DataService.getUDC({'lang':'en'})
    .then(function(data) {
      form.data = data;
    });
  }
});