angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $ionicModal, $timeout) {
  
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});
  
  // Form data for the login modal
  $scope.loginData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    // Simulate a login delay. Remove this and replace with your login
    // code if using a login system
    $timeout(function() {
      $scope.closeLogin();
    }, 1000);
  };
})

.controller('StocksCtrl', function($scope) {
  $scope.stocks = [
    { title: 'HPQ (NYSE)', id: 1 },
    { title: 'YHOO (NASD)', id: 2 },
    { title: 'LNKD (NYSE)', id: 3 },
    { title: 'TWTR (NYSE)', id: 4 },
    { title: 'RHT (NYSE)', id: 5 },
    { title: 'AMZN (NASD)', id: 6 },
    { title: 'FB (NASD)', id: 7 }
  ];
})

.controller('StockCtrl', function($scope, $stateParams) {
    nv.addGraph(function() {
        var chart = nv.models.lineWithFocusChart();
        var width = 550;
        var height = 300;

        chart.brushExtent([50,70]);

        chart.xAxis.tickFormat(d3.format(',f')).axisLabel("Stream - 3,128,.1");
        chart.x2Axis.tickFormat(d3.format(',f'));
        chart.yAxis.tickFormat(d3.format(',.2f'));
        chart.y2Axis.tickFormat(d3.format(',.2f'));
        chart.useInteractiveGuideline(true);

        d3.select('#chart svg')
            .datum(testData())
            .attr('width', width)
            .attr('height', height)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });

    function testData() {
        return stream_layers(3,128,.1).map(function(data, i) {
            return {
                key: 'Stream' + i,
                area: i === 1,
                values: data
            };
        });
    }
});
